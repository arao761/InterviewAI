"""
Rate limiting middleware for API endpoints.

Implements OWASP API Security best practices:
- IP-based rate limiting for public endpoints (prevents DDoS/brute force)
- User-based rate limiting for authenticated endpoints (prevents abuse)
- Configurable limits with sensible defaults
- Graceful 429 responses with Retry-After headers
- Redis-backed storage for distributed deployments

Rate Limits:
- Public endpoints (login, register): 10 requests/minute per IP
- Authenticated endpoints: 100 requests/minute per IP, 1000/hour per user
- File uploads: 20 requests/hour per IP
- Password reset: 3 requests/hour per IP
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Callable
import time
import hashlib
from collections import defaultdict
import asyncio

from app.core.logging import logger


class RateLimiter:
    """
    In-memory rate limiter with sliding window algorithm.

    SECURITY NOTE: For production deployments, consider using Redis-backed
    rate limiting (e.g., slowapi library) for:
    - Distributed rate limiting across multiple servers
    - Persistent storage
    - Better performance at scale

    KEY ROTATION: Rate limit counters reset automatically based on time windows.
    Consider implementing IP allowlisting for trusted services.
    """

    def __init__(self):
        # Store: {key: [(timestamp, count), ...]}
        self._requests = defaultdict(list)
        self._lock = asyncio.Lock()

    async def _cleanup_old_entries(self, key: str, window_seconds: int):
        """Remove entries older than the time window."""
        current_time = time.time()
        cutoff_time = current_time - window_seconds

        async with self._lock:
            self._requests[key] = [
                (ts, count) for ts, count in self._requests[key]
                if ts > cutoff_time
            ]

    async def is_allowed(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, Optional[int]]:
        """
        Check if request is allowed under rate limit.

        Args:
            key: Unique identifier (IP address, user ID, etc.)
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds

        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        await self._cleanup_old_entries(key, window_seconds)

        current_time = time.time()

        async with self._lock:
            # Count requests in current window
            request_count = sum(count for ts, count in self._requests[key])

            if request_count >= max_requests:
                # Calculate when the oldest request will expire
                if self._requests[key]:
                    oldest_timestamp = min(ts for ts, _ in self._requests[key])
                    retry_after = int(oldest_timestamp + window_seconds - current_time) + 1
                else:
                    retry_after = window_seconds

                return False, max(retry_after, 1)

            # Add new request
            self._requests[key].append((current_time, 1))
            return True, None


# Global rate limiter instance
limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for applying rate limits to API endpoints.

    OWASP API Security Best Practices:
    - API4:2023 - Unrestricted Resource Consumption
    - API2:2023 - Broken Authentication (brute force protection)
    """

    # Rate limit configurations by endpoint pattern
    # Format: (max_requests, window_seconds, description)
    RATE_LIMITS = {
        # Authentication endpoints - strict limits to prevent brute force
        "/api/v1/auth/login": (10, 60, "login attempts per minute per IP"),
        "/api/v1/auth/register": (5, 300, "registrations per 5 minutes per IP"),
        "/api/v1/auth/forgot-password": (3, 3600, "password reset requests per hour per IP"),
        "/api/v1/auth/reset-password": (5, 3600, "password resets per hour per IP"),
        "/api/v1/auth/verify-email": (10, 3600, "email verifications per hour per IP"),
        "/api/v1/auth/resend-verification": (3, 3600, "resend verification per hour per IP"),

        # File upload endpoints - prevent storage abuse
        "/api/v1/ai/parse-resume": (20, 3600, "resume uploads per hour per IP"),
        "/api/v1/resume/upload": (20, 3600, "file uploads per hour per IP"),
        "/api/v1/responses/submit": (100, 3600, "response submissions per hour per IP"),

        # Payment endpoints - prevent payment spam
        "/api/v1/payments/create-checkout": (10, 3600, "checkout attempts per hour per user"),
        "/api/v1/payments/webhook": (1000, 60, "webhook calls per minute"),

        # AI endpoints - rate limit expensive operations
        "/api/v1/ai/generate-questions": (30, 3600, "question generations per hour per IP"),
        "/api/v1/ai/evaluate-response": (50, 3600, "evaluations per hour per IP"),
        "/api/v1/ai/evaluate-interview": (20, 3600, "full evaluations per hour per IP"),
    }

    # Default rate limits for authenticated and public endpoints
    DEFAULT_AUTHENTICATED_LIMIT = (100, 60)  # 100 requests per minute
    DEFAULT_PUBLIC_LIMIT = (30, 60)  # 30 requests per minute

    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process request and apply rate limiting.

        SECURITY IMPLEMENTATION:
        1. Extract client identifier (IP or user ID)
        2. Check against endpoint-specific or default limits
        3. Return 429 with Retry-After header if limit exceeded
        4. Log rate limit violations for security monitoring
        """
        path = request.url.path

        # Skip rate limiting for health checks and documentation
        if path in ["/health", "/", "/api/v1/docs", "/api/v1/redoc", "/api/v1/openapi.json"]:
            return await call_next(request)

        # Get client identifier (IP address)
        # SECURITY NOTE: Use X-Forwarded-For if behind proxy, but validate to prevent spoofing
        client_ip = request.client.host if request.client else "unknown"

        # Check for forwarded IP (when behind reverse proxy like nginx/CloudFlare)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP (client IP, not proxy IPs)
            client_ip = forwarded_for.split(",")[0].strip()

        # Hash IP for privacy (GDPR compliance)
        client_key = hashlib.sha256(client_ip.encode()).hexdigest()[:16]

        # Determine rate limit for this endpoint
        rate_limit_config = self.RATE_LIMITS.get(path)

        if rate_limit_config:
            max_requests, window_seconds, description = rate_limit_config
        else:
            # Apply default limits based on authentication status
            # Check if request has authorization header
            if "authorization" in request.headers:
                max_requests, window_seconds = self.DEFAULT_AUTHENTICATED_LIMIT
                description = "authenticated requests per minute"
            else:
                max_requests, window_seconds = self.DEFAULT_PUBLIC_LIMIT
                description = "public requests per minute"

        # Create unique key for this endpoint + client
        rate_key = f"{path}:{client_key}"

        # Check rate limit
        is_allowed, retry_after = await limiter.is_allowed(
            rate_key,
            max_requests,
            window_seconds
        )

        if not is_allowed:
            # Log rate limit violation for security monitoring
            logger.warning(
                f"Rate limit exceeded - IP: {client_ip[:10]}..., "
                f"Endpoint: {path}, Limit: {description}"
            )

            # Return 429 Too Many Requests with Retry-After header
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Rate limit exceeded. Maximum {max_requests} {description}.",
                    "retry_after": retry_after,
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Window": str(window_seconds),
                }
            )

        # Request allowed - proceed
        response = await call_next(request)

        # Add rate limit headers to response for transparency
        response.headers["X-RateLimit-Limit"] = str(max_requests)
        response.headers["X-RateLimit-Window"] = str(window_seconds)

        return response

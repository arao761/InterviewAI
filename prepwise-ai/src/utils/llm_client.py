"""
LLM Client Wrapper
Unified interface for OpenAI and Anthropic APIs with retry logic
"""

from openai import OpenAI
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
import json
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMClient:
    """Unified LLM client supporting OpenAI and Anthropic"""

    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        temperature: float = 0.0,
        api_key: Optional[str] = None,
        max_tokens: int = 4096
    ):
        """
        Initialize LLM client

        Args:
            provider: "openai" or "anthropic"
            model: Model name (defaults to env var or provider default)
            temperature: Temperature for generation (0.0 = deterministic)
            api_key: API key (defaults to env var)
            max_tokens: Maximum tokens in response
        """
        self.provider = provider.lower()
        self.temperature = temperature
        self.max_tokens = max_tokens

        if self.provider == "openai":
            self.client = OpenAI(
                api_key=api_key or os.getenv("OPENAI_API_KEY")
            )
            self.model = model or os.getenv("DEFAULT_MODEL", "gpt-4")

        elif self.provider == "anthropic":
            self.client = Anthropic(
                api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
            )
            self.model = model or "claude-3-5-sonnet-20241022"

        else:
            raise ValueError(
                f"Unsupported provider: {provider}. Choose 'openai' or 'anthropic'"
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_mode: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response from LLM

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            json_mode: Enable JSON response format
            temperature: Override default temperature
            max_tokens: Override default max tokens

        Returns:
            Generated text response

        Raises:
            Exception: If API call fails after retries
        """
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens

        if self.provider == "openai":
            return self._generate_openai(prompt, system_prompt, json_mode, temp, tokens)
        elif self.provider == "anthropic":
            return self._generate_anthropic(prompt, system_prompt, temp, tokens)

    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        json_mode: bool,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate response using OpenAI API"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Enable JSON mode if requested (only for certain models)
        if json_mode and self.model in ["gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini", "gpt-4-mini"]:
            kwargs["response_format"] = {"type": "json_object"}
            # Ensure prompt asks for JSON
            if "json" not in prompt.lower():
                messages[-1]["content"] += "\n\nReturn your response as valid JSON."

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate response using Anthropic API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[Any, Any]:
        """
        Generate and parse JSON response

        Args:
            prompt: User prompt (should request JSON output)
            system_prompt: System prompt (optional)
            temperature: Override default temperature
            max_tokens: Override default max tokens

        Returns:
            Parsed JSON dictionary

        Raises:
            json.JSONDecodeError: If response is not valid JSON
        """
        # Ensure prompt asks for JSON
        if "json" not in prompt.lower():
            prompt += "\n\nReturn ONLY valid JSON, no additional text."

        response = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            json_mode=True,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Clean response (remove markdown code blocks if present)
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            raise ValueError(f"Failed to parse JSON response: {e}\nResponse: {response[:500]}")

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text

        Args:
            text: Input text

        Returns:
            Approximate token count
        """
        try:
            import tiktoken
            if self.provider == "openai":
                encoding = tiktoken.encoding_for_model(self.model)
            else:
                # Use cl100k_base for Claude (approximation)
                encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except ImportError:
            # Rough approximation: 1 token H 4 characters
            return len(text) // 4

    def __repr__(self) -> str:
        return f"LLMClient(provider='{self.provider}', model='{self.model}')"

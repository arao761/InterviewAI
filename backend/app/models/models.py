"""
Database models for PrepWise application.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class InterviewType(str, enum.Enum):
    """Interview type enumeration."""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"


class SessionStatus(str, enum.Enum):
    """Session status enumeration."""
    CREATED = "created"
    RESUME_UPLOADED = "resume_uploaded"
    RESUME_PROCESSED = "resume_processed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class QuestionType(str, enum.Enum):
    """Question type enumeration."""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    CODING = "coding"
    SYSTEM_DESIGN = "system_design"


class DifficultyLevel(str, enum.Enum):
    """Question difficulty level enumeration."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# ====== USER MODEL ======
class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = "users"
    
    # Basic user information
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Subscription information
    subscription_plan = Column(String(50), nullable=True)  # 'starter', 'professional', 'enterprise', None
    subscription_status = Column(String(50), nullable=True)  # 'active', 'canceled', 'past_due', 'trialing', None
    stripe_customer_id = Column(String(255), nullable=True, unique=True, index=True)
    stripe_subscription_id = Column(String(255), nullable=True, unique=True, index=True)
    subscription_start_date = Column(DateTime(timezone=True), nullable=True)
    subscription_end_date = Column(DateTime(timezone=True), nullable=True)
    trial_end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sessions = relationship("Session", back_populates="user")
    payments = relationship("Payment", back_populates="user")


# ====== SESSION MODEL ======
class Session(Base):
    """Interview session model."""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for MVP
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.CREATED, nullable=False)
    interview_type = Column(SQLEnum(InterviewType), nullable=True)
    technical_domain = Column(String(255), nullable=True)  # e.g., "Python", "System Design"
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    resume = relationship("Resume", back_populates="session", uselist=False)
    questions = relationship("Question", back_populates="session", cascade="all, delete-orphan")


# ====== RESUME MODEL ======
class Resume(Base):
    """Resume upload and parsing model."""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), unique=True, nullable=False)
    file_path = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=False)
    extracted_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)  # Structured resume data (skills, experience, etc.)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("Session", back_populates="resume")


# ====== QUESTION MODEL ======
class Question(Base):
    """Interview question model."""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False)
    category = Column(String(255), nullable=True)  # e.g., "Leadership", "Algorithms"
    difficulty_level = Column(SQLEnum(DifficultyLevel), nullable=True)
    order_index = Column(Integer, nullable=False)  # Order in the interview
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("Session", back_populates="questions")
    response = relationship("Response", back_populates="question", uselist=False)


# ====== RESPONSE MODEL ======
class Response(Base):
    """User response to interview question model."""
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), unique=True, nullable=False)
    audio_file_path = Column(String(500), nullable=True)
    transcript = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    duration_seconds = Column(Float, nullable=True)
    
    # Relationships
    question = relationship("Question", back_populates="response")
    feedback = relationship("Feedback", back_populates="response", uselist=False)


# ====== FEEDBACK MODEL ======
class Feedback(Base):
    """AI-generated feedback for user responses."""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.id"), unique=True, nullable=False)
    overall_score = Column(Float, nullable=True)  # Score out of 10
    
    # Behavioral feedback
    star_analysis = Column(JSON, nullable=True)  # {situation, task, action, result}
    
    # Technical feedback
    technical_accuracy = Column(JSON, nullable=True)  # {correctness, depth, clarity}
    
    # Speech feedback
    speech_metrics = Column(JSON, nullable=True)  # {pace, filler_words, confidence, clarity}
    
    # Improvement suggestions
    improvement_suggestions = Column(JSON, nullable=True)  # List of actionable suggestions
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    response = relationship("Response", back_populates="feedback")


# ====== PAYMENT MODEL ======
class Payment(Base):
    """Payment and subscription tracking model."""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Stripe information
    stripe_payment_intent_id = Column(String(255), nullable=True, unique=True, index=True)
    stripe_charge_id = Column(String(255), nullable=True, unique=True, index=True)
    stripe_invoice_id = Column(String(255), nullable=True, unique=True, index=True)
    
    # Payment details
    amount = Column(Float, nullable=False)  # Amount in dollars
    currency = Column(String(10), default="usd", nullable=False)
    status = Column(String(50), nullable=False)  # 'succeeded', 'pending', 'failed', 'refunded'
    payment_method = Column(String(50), nullable=True)  # 'card', 'paypal', etc.
    
    # Subscription details (if applicable)
    subscription_plan = Column(String(50), nullable=True)
    billing_period_start = Column(DateTime(timezone=True), nullable=True)
    billing_period_end = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    payment_metadata = Column(JSON, nullable=True)  # Additional payment metadata
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="payments")
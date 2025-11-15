"""
Resume Parser
LLM-based resume parsing to extract structured data from resume text
"""

from pathlib import Path
from typing import Optional, Dict, Any
import logging
import json

from src.utils.llm_client import LLMClient
from src.resume_parser.extractors import TextExtractor
from src.resume_parser.schemas import ParsedResume

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeParser:
    """Parse resumes using LLM-based extraction"""

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        model: str = "gpt-4o-mini"  # Use mini for cost efficiency
    ):
        """
        Initialize resume parser

        Args:
            llm_client: Optional LLM client instance (creates default if not provided)
            model: Model to use for parsing (default: gpt-4o-mini for cost)
        """
        self.llm_client = llm_client or LLMClient(
            provider="openai",
            model=model,
            temperature=0.0  # Deterministic for consistent parsing
        )
        self.extractor = TextExtractor()

        # Load parsing prompt template
        self.prompt_template = self._load_prompt_template()

        logger.info(f"ResumeParser initialized with model: {self.llm_client.model}")

    def _load_prompt_template(self) -> str:
        """Load resume parsing prompt template from file"""
        prompt_path = Path(__file__).parent.parent.parent / "prompts" / "resume_parsing.txt"

        try:
            with open(prompt_path, 'r') as f:
                template = f.read()
            logger.debug(f"Loaded prompt template from {prompt_path}")
            return template
        except FileNotFoundError:
            logger.warning(f"Prompt template not found at {prompt_path}, using inline version")
            return self._get_inline_prompt_template()

    def _get_inline_prompt_template(self) -> str:
        """Fallback inline prompt template if file not found"""
        return """You are an expert resume parser. Extract structured information from this resume text.

Resume Text:
{resume_text}

Return a JSON object with contact, education, experience, skills, projects, certifications, leadership, awards, publications, volunteer, and total_years_experience fields.

Extract ALL available information accurately. Use null or empty arrays for missing fields.
Return ONLY valid JSON, no additional text."""

    def parse_resume(self, file_path: str) -> ParsedResume:
        """
        Parse resume from file path

        Args:
            file_path: Path to PDF or DOCX resume file

        Returns:
            ParsedResume object with structured data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If parsing fails

        Examples:
            >>> parser = ResumeParser()
            >>> resume = parser.parse_resume("resume.pdf")
            >>> print(resume.contact.name)
            >>> print(resume.experience_level)
        """
        logger.info(f"Parsing resume from file: {file_path}")

        # Step 1: Extract text from file
        try:
            resume_text = self.extractor.extract_text(file_path)
            logger.info(f"Extracted {len(resume_text)} characters from resume")
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            raise

        # Step 2: Parse text with LLM
        try:
            parsed_resume = self.parse_resume_from_text(resume_text)
            logger.info(f"Successfully parsed resume for: {parsed_resume.contact.name}")
            return parsed_resume
        except Exception as e:
            logger.error(f"Resume parsing failed: {e}")
            raise

    def parse_resume_from_text(self, resume_text: str) -> ParsedResume:
        """
        Parse resume from already-extracted text

        Args:
            resume_text: Raw text from resume

        Returns:
            ParsedResume object with structured data

        Raises:
            ValueError: If parsing fails

        Examples:
            >>> parser = ResumeParser()
            >>> text = "John Doe\\njohn@example.com\\n..."
            >>> resume = parser.parse_resume_from_text(text)
        """
        logger.info("Parsing resume text with LLM")

        # Clean text first
        cleaned_text = self.extractor.clean_text(resume_text)

        if len(cleaned_text) < 100:
            raise ValueError(
                f"Resume text too short ({len(cleaned_text)} chars). "
                "Minimum 100 characters required."
            )

        # Generate prompt
        prompt = self.prompt_template.format(resume_text=cleaned_text)

        # Count tokens for cost estimation
        token_count = self.llm_client.count_tokens(prompt)
        logger.info(f"Prompt token count: ~{token_count} tokens")

        # Call LLM to parse resume
        try:
            logger.debug("Calling LLM for resume parsing...")
            response = self.llm_client.generate_json(
                prompt=prompt,
                max_tokens=4096  # Allow for detailed resumes
            )
            logger.debug("LLM response received")
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            raise ValueError(f"Failed to call LLM for parsing: {e}")

        # Validate and convert to ParsedResume object
        try:
            parsed_resume = self._validate_and_convert(response)
            logger.info("Resume parsing successful")
            return parsed_resume
        except Exception as e:
            logger.error(f"Failed to validate parsed resume: {e}")
            logger.debug(f"LLM response: {json.dumps(response, indent=2)[:500]}...")
            raise ValueError(f"Failed to validate parsed resume: {e}")

    def _validate_and_convert(self, llm_response: Dict[Any, Any]) -> ParsedResume:
        """
        Validate LLM response and convert to ParsedResume

        Args:
            llm_response: Raw JSON response from LLM

        Returns:
            Validated ParsedResume object

        Raises:
            ValueError: If validation fails
        """
        try:
            # Pydantic will validate the data
            parsed_resume = ParsedResume(**llm_response)

            # Log parsed data summary
            logger.info(f"Parsed resume summary:")
            logger.info(f"  - Name: {parsed_resume.contact.name}")
            logger.info(f"  - Email: {parsed_resume.contact.email}")
            logger.info(f"  - Education entries: {len(parsed_resume.education)}")
            logger.info(f"  - Experience entries: {len(parsed_resume.experience)}")
            logger.info(f"  - Projects: {len(parsed_resume.projects)}")
            logger.info(f"  - Total years experience: {parsed_resume.total_years_experience}")
            logger.info(f"  - Experience level: {parsed_resume.experience_level}")

            return parsed_resume

        except Exception as e:
            raise ValueError(f"Validation failed: {e}\nResponse: {llm_response}")

    def parse_resume_to_dict(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume and return as dictionary (for API responses)

        Args:
            file_path: Path to resume file

        Returns:
            Resume data as dictionary

        Examples:
            >>> parser = ResumeParser()
            >>> resume_dict = parser.parse_resume_to_dict("resume.pdf")
            >>> print(resume_dict['contact']['name'])
        """
        parsed_resume = self.parse_resume(file_path)
        return parsed_resume.model_dump()

    def get_parsing_stats(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume and return both data and statistics

        Args:
            file_path: Path to resume file

        Returns:
            Dictionary with 'resume' and 'stats' keys

        Examples:
            >>> parser = ResumeParser()
            >>> result = parser.get_parsing_stats("resume.pdf")
            >>> print(result['stats']['tokens_used'])
        """
        # Extract text
        resume_text = self.extractor.extract_text(file_path)
        text_stats = self.extractor.get_text_stats(resume_text)

        # Parse resume
        parsed_resume = self.parse_resume_from_text(resume_text)

        # Calculate token usage
        prompt = self.prompt_template.format(resume_text=resume_text)
        input_tokens = self.llm_client.count_tokens(prompt)
        output_tokens = self.llm_client.count_tokens(json.dumps(parsed_resume.model_dump()))

        stats = {
            'text_stats': text_stats,
            'tokens_used': {
                'input': input_tokens,
                'output': output_tokens,
                'total': input_tokens + output_tokens
            },
            'estimated_cost': self._estimate_cost(input_tokens, output_tokens),
            'model_used': self.llm_client.model
        }

        return {
            'resume': parsed_resume.model_dump(),
            'stats': stats
        }

    def _estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate API cost based on token usage

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        # Pricing for GPT-4o-mini (as of 2024)
        # Input: $0.15 per 1M tokens
        # Output: $0.60 per 1M tokens
        if 'gpt-4o-mini' in self.llm_client.model or 'gpt-4-mini' in self.llm_client.model:
            input_cost = (input_tokens / 1_000_000) * 0.15
            output_cost = (output_tokens / 1_000_000) * 0.60
        # Pricing for GPT-4
        elif 'gpt-4' in self.llm_client.model:
            input_cost = (input_tokens / 1_000) * 0.03
            output_cost = (output_tokens / 1_000) * 0.06
        else:
            # Default to GPT-4 pricing
            input_cost = (input_tokens / 1_000) * 0.03
            output_cost = (output_tokens / 1_000) * 0.06

        return input_cost + output_cost


# Convenience function for quick parsing
def parse_resume(file_path: str, model: str = "gpt-4o-mini") -> ParsedResume:
    """
    Quick function to parse a resume

    Args:
        file_path: Path to PDF or DOCX resume
        model: Model to use (default: gpt-4o-mini for cost efficiency)

    Returns:
        ParsedResume object

    Examples:
        >>> from src.resume_parser.parser import parse_resume
        >>> resume = parse_resume("resume.pdf")
        >>> print(resume.contact.name)
    """
    parser = ResumeParser(model=model)
    return parser.parse_resume(file_path)

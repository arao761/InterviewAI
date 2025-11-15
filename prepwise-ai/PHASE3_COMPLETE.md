# Phase 3: Question Generator - COMPLETE ✅

## Overview
Phase 3 implements an intelligent question generation system that creates tailored interview questions based on job roles, experience levels, and candidate resumes.

## Implemented Components

### 1. Core Schemas (`src/question_generator/schemas.py`)
- **QuestionType**: Enum for question types (TECHNICAL, BEHAVIORAL, SITUATIONAL, SYSTEM_DESIGN, CODING)
- **DifficultyLevel**: Enum for difficulty levels (EASY, MEDIUM, HARD)
- **InterviewQuestion**: Pydantic model for individual questions with metadata
- **QuestionSet**: Collection of questions for an interview session
- **QuestionGenerationRequest**: Request model for question generation

### 2. Question Generator (`src/question_generator/generator.py`)
Main class that handles question generation with the following capabilities:

#### Features
- ✅ **LLM-Powered Generation**: Uses OpenAI/Anthropic for intelligent question creation
- ✅ **Multiple Question Types**: Technical, behavioral, situational, system design
- ✅ **Difficulty Levels**: Automatically adjusts based on experience level
- ✅ **Resume-Tailored**: Generates questions based on candidate's skills and experience
- ✅ **Focus Areas**: Customize questions for specific topics/technologies
- ✅ **Fallback Templates**: Built-in question banks when LLM unavailable
- ✅ **Follow-up Generation**: Dynamic follow-up questions based on answers
- ✅ **Session Management**: Unique session IDs for tracking

#### Methods
```python
# Main generation method
generate_questions(request: QuestionGenerationRequest) -> QuestionSet

# Generate follow-ups based on answers
generate_follow_up(original_question, user_answer) -> str

# Internal generation methods
_generate_technical_questions(request, count) -> List[InterviewQuestion]
_generate_behavioral_questions(request, count) -> List[InterviewQuestion]
_generate_situational_questions(request, count) -> List[InterviewQuestion]
_generate_system_design_questions(request, count) -> List[InterviewQuestion]
```

### 3. Prompt Templates
Enhanced prompt templates for better question generation:
- `prompts/technical_questions.txt`: Template for technical questions
- `prompts/behavioral_questions.txt`: Template for behavioral questions

### 4. Question Banks (Fallback)
Built-in question templates organized by:
- **Experience Level**: Junior, Mid, Senior
- **Question Type**: Technical, Behavioral, Situational, System Design
- **Category**: General, Domain-specific

## Usage Examples

### Basic Usage
```python
from src.question_generator.generator import QuestionGenerator
from src.question_generator.schemas import QuestionGenerationRequest

# Initialize generator
generator = QuestionGenerator()

# Create request
request = QuestionGenerationRequest(
    target_role="Software Engineer",
    target_level="mid",
    num_technical=5,
    num_behavioral=3
)

# Generate questions
questions = generator.generate_questions(request)

# Access questions
for q in questions.questions:
    print(f"{q.type}: {q.question}")
```

### Resume-Tailored Generation
```python
# With resume context
request = QuestionGenerationRequest(
    target_role="Senior Full Stack Engineer",
    target_level="senior",
    num_technical=4,
    num_behavioral=2,
    resume_context={
        "skills": {"technical": ["Python", "React", "AWS"]},
        "experience": [...]
    },
    tailor_to_experience=True,
    focus_areas=["system architecture", "leadership"]
)

questions = generator.generate_questions(request)
```

### Filtering and Organization
```python
# Filter by type
technical = questions.get_questions_by_type(QuestionType.TECHNICAL)
behavioral = questions.get_questions_by_type(QuestionType.BEHAVIORAL)

# Filter by difficulty
easy = questions.get_questions_by_difficulty(DifficultyLevel.EASY)
hard = questions.get_questions_by_difficulty(DifficultyLevel.HARD)

# Get total duration
total_time = questions.get_total_duration()
```

### Dynamic Follow-ups
```python
# Generate follow-up based on answer
follow_up = generator.generate_follow_up(
    original_question=question,
    user_answer="I would use a hash map and doubly linked list..."
)
```

## Testing

### Test Coverage
- ✅ Question generator initialization
- ✅ Technical question generation
- ✅ Behavioral question generation
- ✅ Mixed question types
- ✅ System design questions
- ✅ Question filtering and organization
- ✅ Session ID uniqueness
- ✅ Question structure validation
- ✅ Difficulty level appropriateness
- ✅ Focus areas customization
- ✅ Resume context integration
- ✅ Duration calculation

### Run Tests
```bash
# Run all tests
python test_setup.py

# Run Phase 3 tests specifically
pytest tests/test_question_generator.py -v

# Run examples
python examples/question_generator_example.py
```

## API Integration

The Question Generator integrates seamlessly with:
1. **Resume Parser** (Phase 2): Uses parsed resume data for tailored questions
2. **LLM Client**: Leverages AI for intelligent question generation
3. **Future Evaluator** (Phase 4): Questions will feed into answer evaluation

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: For OpenAI-powered generation
- `ANTHROPIC_API_KEY`: For Claude-powered generation (optional)
- `DEFAULT_MODEL`: Model to use (default: gpt-4o-mini)
- `TEMPERATURE`: Generation temperature (default: 0.7-0.8 for questions)

### Customization Options
```python
QuestionGenerationRequest(
    # Basic settings
    target_role="Software Engineer",
    target_level="mid",  # junior, mid, senior
    target_company="Google",  # optional
    
    # Question distribution
    num_technical=5,
    num_behavioral=3,
    num_situational=2,
    num_system_design=1,
    
    # Customization
    focus_areas=["Python", "algorithms", "AWS"],
    avoid_topics=["frontend", "mobile"],
    difficulty_distribution={"easy": 2, "medium": 4, "hard": 2},
    
    # Resume integration
    resume_context={...},
    tailor_to_experience=True,
    include_resume_specific=True,
    
    # Session constraints
    max_duration_minutes=60,
    include_follow_ups=True,
    include_hints=False
)
```

## Question Types in Detail

### 1. Technical Questions
- Programming concepts
- Data structures & algorithms
- System architecture
- Best practices
- Technology-specific questions

### 2. Behavioral Questions
- Uses STAR method
- Assesses soft skills
- Past experience evaluation
- Situational judgment

### 3. Situational Questions
- Hypothetical scenarios
- Problem-solving approach
- Decision-making skills

### 4. System Design Questions
- Architecture design
- Scalability considerations
- Trade-off analysis
- Level-appropriate complexity

## Question Metadata

Each question includes:
- **question**: The question text
- **type**: Question type enum
- **difficulty**: Difficulty level enum
- **category**: Topic/competency area
- **skills_tested**: List of skills evaluated
- **expected_duration_minutes**: Time allocation
- **follow_up_questions**: Pre-defined follow-ups
- **hints**: Optional hints for candidates
- **sample_answer_points**: Key points for evaluation
- **related_resume_section**: Links to resume data
- **company_specific**: Company-specific flag
- **role_specific**: Role-specific flag

## Performance Considerations

### Caching
- Question templates are cached on initialization
- Fallback questions provide instant generation
- LLM responses are generated fresh (not cached for variety)

### Rate Limiting
- Respects LLM API rate limits with retry logic
- Graceful degradation to template questions
- Configurable timeout and retry settings

### Token Optimization
- Prompts optimized for concise responses
- JSON mode for structured output
- Context pruning for large resume data

## Error Handling

The generator includes robust error handling:
- LLM API failures → Fallback to templates
- Parsing errors → Structured error messages
- Invalid requests → Validation errors with details
- Empty responses → Default question generation

## Next Steps (Phase 4)

With Phase 3 complete, the next phase will focus on:
1. **Answer Evaluation**: Scoring candidate responses
2. **Feedback Generation**: Providing constructive feedback
3. **Performance Analytics**: Tracking candidate performance
4. **Interview Simulation**: Real-time interview experience

## Files Created/Modified

### New Files
- `src/question_generator/schemas.py` ✅
- `src/question_generator/generator.py` ✅
- `tests/test_question_generator.py` ✅
- `examples/question_generator_example.py` ✅
- `PHASE3_COMPLETE.md` ✅

### Modified Files
- `src/question_generator/__init__.py` ✅
- `prompts/technical_questions.txt` ✅
- `prompts/behavioral_questions.txt` ✅
- `test_setup.py` ✅

### Existing Files (Intact)
- `src/question_generator/technical.py` (empty, reserved for future)
- `src/question_generator/behavioral.py` (empty, reserved for future)
- `src/question_generator/question_banks.py` (empty, reserved for future)

## Verification

Run the following to verify Phase 3:
```bash
cd prepwise-ai
source venv/bin/activate
python test_setup.py
```

Expected output:
```
✅ PASS - Environment
✅ PASS - Package Imports
✅ PASS - Pydantic Schemas
✅ PASS - Validators
✅ PASS - LLM Client
✅ PASS - Question Generator

🎉 All tests passed! Phase 3 setup is complete!
```

## Version
- **Phase**: 3
- **Status**: Complete
- **Date**: November 15, 2025
- **Tested**: ✅
- **Documented**: ✅
- **Integrated**: ✅

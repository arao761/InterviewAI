# -*- coding: utf-8 -*-
"""
Resume Parser - Usage Examples
Demonstrates how to use the resume parser
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.resume_parser.parser import ResumeParser, parse_resume
from src.resume_parser.extractors import extract_text


def example_1_basic_parsing():
    """Example 1: Basic resume parsing"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Resume Parsing")
    print("=" * 60)

    # Initialize parser
    parser = ResumeParser()

    # Parse resume (replace with your resume path)
    resume_path = "examples/sample_resumes/sample_resume.pdf"

    try:
        resume = parser.parse_resume(resume_path)

        # Access parsed data
        print(f"\nName: {resume.contact.name}")
        print(f"Email: {resume.contact.email}")
        print(f"Experience Level: {resume.experience_level}")
        print(f"Total Years Experience: {resume.total_years_experience}")

        print(f"\nEducation:")
        for edu in resume.education:
            print(f"  - {edu.degree} in {edu.field} from {edu.institution}")

        print(f"\nExperience:")
        for exp in resume.experience:
            print(f"  - {exp.title} at {exp.company} ({exp.start_date} - {exp.end_date})")

        print(f"\nTop Skills: {', '.join(resume.skills.technical[:5])}")

    except FileNotFoundError:
        print(f"L Resume file not found: {resume_path}")
        print("   Please add a sample resume to examples/sample_resumes/")
    except Exception as e:
        print(f"L Error: {e}")


def example_2_convenience_function():
    """Example 2: Using convenience function"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Using Convenience Function")
    print("=" * 60)

    resume_path = "examples/sample_resumes/sample_resume.docx"

    try:
        # Quick parsing with convenience function
        resume = parse_resume(resume_path, model="gpt-4o-mini")

        print(f"\nParsed Resume for: {resume.contact.name}")
        print(f"Summary: {resume.get_summary()}")

    except FileNotFoundError:
        print(f"L Resume file not found: {resume_path}")
    except Exception as e:
        print(f"L Error: {e}")


def example_3_text_extraction_only():
    """Example 3: Extract text without parsing"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Text Extraction Only")
    print("=" * 60)

    resume_path = "examples/sample_resumes/sample_resume.pdf"

    try:
        # Just extract text
        text = extract_text(resume_path)

        print(f"\nExtracted {len(text)} characters")
        print(f"\nFirst 200 characters:")
        print(text[:200])

    except FileNotFoundError:
        print(f"L Resume file not found: {resume_path}")
    except Exception as e:
        print(f"L Error: {e}")


def example_4_parsing_stats():
    """Example 4: Get parsing statistics"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Parsing Statistics")
    print("=" * 60)

    resume_path = "examples/sample_resumes/sample_resume.pdf"

    try:
        parser = ResumeParser()
        result = parser.get_parsing_stats(resume_path)

        resume = result['resume']
        stats = result['stats']

        print(f"\nResume: {resume['contact']['name']}")
        print(f"\nText Statistics:")
        print(f"  - Characters: {stats['text_stats']['character_count']}")
        print(f"  - Words: {stats['text_stats']['word_count']}")
        print(f"  - Lines: {stats['text_stats']['line_count']}")

        print(f"\nToken Usage:")
        print(f"  - Input tokens: {stats['tokens_used']['input']}")
        print(f"  - Output tokens: {stats['tokens_used']['output']}")
        print(f"  - Total tokens: {stats['tokens_used']['total']}")

        print(f"\nEstimated Cost: ${stats['estimated_cost']:.4f}")
        print(f"Model Used: {stats['model_used']}")

    except FileNotFoundError:
        print(f"L Resume file not found: {resume_path}")
    except Exception as e:
        print(f"L Error: {e}")


def example_5_parse_to_dict():
    """Example 5: Parse to dictionary (for API responses)"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Parse to Dictionary")
    print("=" * 60)

    resume_path = "examples/sample_resumes/sample_resume.pdf"

    try:
        parser = ResumeParser()
        resume_dict = parser.parse_resume_to_dict(resume_path)

        # Dictionary is easier to serialize to JSON for APIs
        import json
        print("\nResume as JSON (first 500 chars):")
        json_str = json.dumps(resume_dict, indent=2)
        print(json_str[:500] + "...")

    except FileNotFoundError:
        print(f"L Resume file not found: {resume_path}")
    except Exception as e:
        print(f"L Error: {e}")


def example_6_parse_from_text():
    """Example 6: Parse from already-extracted text"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Parse from Text")
    print("=" * 60)

    # Sample resume text
    resume_text = """
    JOHN DOE
    john.doe@example.com | 555-1234 | San Francisco, CA
    linkedin.com/in/johndoe | github.com/johndoe

    EDUCATION
    Stanford University, Stanford, CA
    Bachelor of Science in Computer Science, May 2020
    GPA: 3.8/4.0
    Dean's List (4 semesters)

    EXPERIENCE
    Google Inc., Mountain View, CA
    Software Engineer, June 2020 - Present
    " Developed microservices using Python and Go for YouTube infrastructure
    " Led team of 3 engineers in migration project
    " Reduced API latency by 40% through optimization
    " Technologies: Python, Go, Kubernetes, Docker, PostgreSQL

    Tech Startup, San Francisco, CA
    Software Engineering Intern, Summer 2019
    " Built full-stack web application using React and Node.js
    " Implemented authentication system with JWT
    " Technologies: React, Node.js, MongoDB, AWS

    SKILLS
    Languages: Python, Java, JavaScript, Go, C++
    Frameworks: React, Django, FastAPI, TensorFlow
    Tools: Git, Docker, Kubernetes, Jenkins
    Databases: PostgreSQL, MongoDB, Redis
    Cloud: AWS, GCP

    PROJECTS
    E-commerce Platform (github.com/johndoe/ecommerce)
    " Built full-stack e-commerce platform with React and Node.js
    " Integrated Stripe payment processing
    " Handled 10,000+ daily active users
    " Technologies: React, Node.js, MongoDB, Stripe API

    CERTIFICATIONS
    " AWS Certified Developer - Associate
    " Google Cloud Professional Developer

    AWARDS
    " First Place, Stanford Hackathon 2019
    " Best Technical Project, CS Fair 2020
    """

    try:
        parser = ResumeParser()
        resume = parser.parse_resume_from_text(resume_text)

        print(f"\nParsed Resume:")
        print(f"Name: {resume.contact.name}")
        print(f"Email: {resume.contact.email}")
        print(f"Education: {len(resume.education)} entries")
        print(f"Experience: {len(resume.experience)} entries")
        print(f"Projects: {len(resume.projects)} entries")
        print(f"Certifications: {len(resume.certifications)}")
        print(f"Experience Level: {resume.experience_level}")

    except Exception as e:
        print(f"L Error: {e}")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("PREPWISE AI - RESUME PARSER EXAMPLES")
    print("=" * 60)

    # Run examples that don't require files
    print("\n Running Example 6 (Parse from text - no file required)...")
    example_6_parse_from_text()

    # File-based examples will show error if files don't exist
    print("\n�  File-based examples (will show errors if files missing)...")
    example_1_basic_parsing()
    example_2_convenience_function()
    example_3_text_extraction_only()
    example_4_parsing_stats()
    example_5_parse_to_dict()

    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETE")
    print("=" * 60)
    print("\nTo run file-based examples, add sample resumes to:")
    print("  examples/sample_resumes/sample_resume.pdf")
    print("  examples/sample_resumes/sample_resume.docx")


if __name__ == "__main__":
    main()

"""
Question Generator
Generates tailored interview questions based on role, level, and resume
"""

from typing import List, Dict, Optional, Any
import random
from datetime import datetime
import os

from src.question_generator.schemas import (
    InterviewQuestion,
    QuestionSet,
    QuestionGenerationRequest,
    QuestionType,
    DifficultyLevel
)
from src.utils.llm_client import LLMClient


def load_prompt(prompt_name: str) -> str:
    """Load a prompt template from the prompts directory"""
    try:
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "prompts",
            f"{prompt_name}.txt"
        )
        if os.path.exists(prompt_path):
            with open(prompt_path, 'r') as f:
                content = f.read().strip()
                if content:
                    return content
        return ""
    except Exception:
        return ""


class QuestionGenerator:
    """Generates interview questions using LLM"""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize question generator
        
        Args:
            llm_client: LLM client for question generation
        """
        self.llm_client = llm_client or LLMClient()
        self._load_templates()
    
    def _load_templates(self):
        """Load question templates and prompts"""
        try:
            self.technical_prompt = load_prompt("technical_questions")
            self.behavioral_prompt = load_prompt("behavioral_questions")
        except Exception as e:
            print(f"Warning: Could not load prompts: {e}")
            self.technical_prompt = None
            self.behavioral_prompt = None
    
    def generate_questions(
        self,
        request: QuestionGenerationRequest
    ) -> QuestionSet:
        """
        Generate a complete set of interview questions
        
        Args:
            request: Question generation request with specifications
            
        Returns:
            QuestionSet with generated questions
        """
        session_id = self._generate_session_id()
        
        question_set = QuestionSet(
            session_id=session_id,
            target_role=request.target_role,
            target_level=request.target_level,
            target_company=request.target_company,
            created_at=datetime.now().isoformat()
        )
        
        # Generate technical questions
        if request.num_technical > 0:
            technical_questions = self._generate_technical_questions(
                request=request,
                count=request.num_technical
            )
            for q in technical_questions:
                question_set.add_question(q)
        
        # Generate behavioral questions
        if request.num_behavioral > 0:
            behavioral_questions = self._generate_behavioral_questions(
                request=request,
                count=request.num_behavioral
            )
            for q in behavioral_questions:
                question_set.add_question(q)
        
        # Generate situational questions
        if request.num_situational > 0:
            situational_questions = self._generate_situational_questions(
                request=request,
                count=request.num_situational
            )
            for q in situational_questions:
                question_set.add_question(q)
        
        # Generate system design questions
        if request.num_system_design > 0:
            system_design_questions = self._generate_system_design_questions(
                request=request,
                count=request.num_system_design
            )
            for q in system_design_questions:
                question_set.add_question(q)
        
        return question_set
    
    def _generate_technical_questions(
        self,
        request: QuestionGenerationRequest,
        count: int
    ) -> List[InterviewQuestion]:
        """Generate technical interview questions"""
        
        # Build context from request
        context = self._build_technical_context(request)
        
        # Use LLM to generate questions
        prompt = self._build_technical_prompt(context, count)
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=0.8,
                max_tokens=2000
            )
            
            # Parse response into questions
            questions = self._parse_llm_response(
                response,
                QuestionType.TECHNICAL,
                request
            )
            
            return questions[:count]
            
        except Exception as e:
            print(f"Error generating technical questions: {e}")
            # Fallback to template questions
            return self._get_fallback_technical_questions(request, count)
    
    def _generate_behavioral_questions(
        self,
        request: QuestionGenerationRequest,
        count: int
    ) -> List[InterviewQuestion]:
        """Generate behavioral interview questions"""
        
        context = self._build_behavioral_context(request)
        prompt = self._build_behavioral_prompt(context, count)
        
        try:
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=1500
            )
            
            questions = self._parse_llm_response(
                response,
                QuestionType.BEHAVIORAL,
                request
            )
            
            return questions[:count]
            
        except Exception as e:
            print(f"Error generating behavioral questions: {e}")
            return self._get_fallback_behavioral_questions(request, count)
    
    def _generate_situational_questions(
        self,
        request: QuestionGenerationRequest,
        count: int
    ) -> List[InterviewQuestion]:
        """Generate situational interview questions"""
        
        questions = []
        
        situational_templates = [
            "You're working on a critical project with a tight deadline when a major bug is discovered. How would you handle this?",
            "A team member consistently misses deadlines. How would you address this situation?",
            "You disagree with your manager's technical decision. What would you do?",
            "You discover a security vulnerability in production code. What are your next steps?",
            "Two stakeholders have conflicting requirements. How do you proceed?"
        ]
        
        for i, template in enumerate(situational_templates[:count]):
            questions.append(
                InterviewQuestion(
                    question=template,
                    type=QuestionType.SITUATIONAL,
                    difficulty=DifficultyLevel.MEDIUM,
                    category="problem_solving",
                    skills_tested=["critical thinking", "decision making"],
                    expected_duration_minutes=7,
                    follow_up_questions=[
                        "What factors would you consider?",
                        "What would be the potential consequences?"
                    ]
                )
            )
        
        return questions
    
    def _generate_system_design_questions(
        self,
        request: QuestionGenerationRequest,
        count: int
    ) -> List[InterviewQuestion]:
        """Generate system design questions"""
        
        level_templates = {
            "junior": [
                "Design a simple URL shortener service",
                "Design a basic chat application",
                "Design a todo list API"
            ],
            "mid": [
                "Design a scalable notification system",
                "Design a rate limiter",
                "Design a file storage service like Dropbox",
                "Design a content delivery network (CDN)"
            ],
            "senior": [
                "Design Instagram/Twitter at scale",
                "Design a distributed cache system",
                "Design a real-time analytics platform",
                "Design a global payment processing system"
            ]
        }
        
        templates = level_templates.get(request.target_level, level_templates["mid"])
        
        questions = []
        for template in templates[:count]:
            difficulty = self._get_difficulty_for_level(request.target_level)
            
            questions.append(
                InterviewQuestion(
                    question=template,
                    type=QuestionType.SYSTEM_DESIGN,
                    difficulty=difficulty,
                    category="system_design",
                    skills_tested=["architecture", "scalability", "design patterns"],
                    expected_duration_minutes=30,
                    follow_up_questions=[
                        "How would you handle failures?",
                        "How would you scale this to millions of users?",
                        "What are the bottlenecks?"
                    ],
                    hints=[
                        "Consider data consistency",
                        "Think about caching strategies",
                        "Consider load balancing"
                    ]
                )
            )
        
        return questions
    
    def _build_technical_context(self, request: QuestionGenerationRequest) -> Dict[str, Any]:
        """Build context for technical question generation"""
        context = {
            "role": request.target_role,
            "level": request.target_level,
            "focus_areas": request.focus_areas or [],
            "avoid_topics": request.avoid_topics or [],
            "company": request.target_company
        }

        # Add resume context if available
        if request.resume_context and request.tailor_to_experience:
            context["skills"] = request.resume_context.get("skills", {})
            context["experience"] = request.resume_context.get("experience", [])

        return context
    
    def _build_behavioral_context(self, request: QuestionGenerationRequest) -> Dict[str, Any]:
        """Build context for behavioral question generation"""
        context = {
            "role": request.target_role,
            "level": request.target_level,
            "company": request.target_company,
            "resume_context": request.resume_context
        }

        if request.resume_context:
            context["past_roles"] = [
                exp.get("title") for exp in request.resume_context.get("experience", [])
            ]
            context["skills"] = request.resume_context.get("skills", {})
            context["experience"] = request.resume_context.get("experience", [])
            context["education"] = request.resume_context.get("education", [])
            context["projects"] = request.resume_context.get("projects", [])

        return context
    
    def _build_technical_prompt(self, context: Dict, count: int) -> str:
        """Build prompt for technical questions"""
        company = context.get("company")
        focus_areas = ", ".join(context.get("focus_areas", [])) or "general programming"

        if company:
            # Company-specific prompt
            return f"""Generate {count} technical interview questions that are frequently asked at {company} for a {context['level']} {context['role']} position.

These should be the types of questions that {company} is known to ask in their technical interviews. Include:
- Algorithm and data structure questions typical of {company}
- System design questions if appropriate for the level
- Coding problems that match {company}'s interview style

Focus areas: {focus_areas}

For each question, provide:
1. The question text
2. Difficulty level (easy/medium/hard)
3. Category/topic
4. Skills being tested
5. Expected duration in minutes

Format as JSON array with keys: question, difficulty, category, skills_tested (array), duration"""

        # Generic prompt when no company specified
        return f"""Generate {count} technical interview questions for a {context['level']} {context['role']} position.

Focus areas: {focus_areas}

For each question, provide:
1. The question text
2. Difficulty level (easy/medium/hard)
3. Category/topic
4. Skills being tested
5. Expected duration in minutes

Format as JSON array with keys: question, difficulty, category, skills_tested (array), duration"""
    
    def _build_behavioral_prompt(self, context: Dict, count: int) -> str:
        """Build prompt for behavioral questions"""
        company = context.get("company")
        resume_context = context.get("resume_context")

        # Build resume context string if available
        resume_info = ""
        if resume_context:
            experience = resume_context.get("experience", [])
            skills = resume_context.get("skills", {})
            projects = resume_context.get("projects", [])

            if experience:
                resume_info += "\n\nCandidate's Work Experience:\n"
                for exp in experience[:3]:  # Top 3 experiences
                    title = exp.get("title") or exp.get("position", "")
                    company_name = exp.get("company", "")
                    desc = exp.get("description", "")
                    resume_info += f"- {title} at {company_name}: {desc[:200] if desc else 'N/A'}\n"

            if projects:
                resume_info += "\nCandidate's Projects:\n"
                for proj in projects[:2]:  # Top 2 projects
                    name = proj.get("name", "")
                    desc = proj.get("description", "")
                    resume_info += f"- {name}: {desc[:150] if desc else 'N/A'}\n"

            if skills:
                if isinstance(skills, dict):
                    tech_skills = skills.get("technical", [])
                    if tech_skills:
                        resume_info += f"\nTechnical Skills: {', '.join(tech_skills[:10])}\n"
                elif isinstance(skills, list):
                    resume_info += f"\nSkills: {', '.join(skills[:10])}\n"

        # Calculate split between resume-based and general behavioral questions
        resume_based_count = count // 2 if resume_context else 0
        general_count = count - resume_based_count

        if company and resume_context:
            return f"""Generate {count} behavioral interview questions for a {context['level']} {context['role']} position at {company}.

IMPORTANT: Generate a mix of questions:
- {resume_based_count} questions should be based on the candidate's resume/experience below (ask about specific projects, roles, or experiences from their background)
- {general_count} questions should be general behavioral questions that {company} typically asks

{resume_info}

For resume-based questions, reference specific experiences, projects, or skills from their background.
For general questions, focus on behavioral patterns that {company} values.

Focus on STAR method questions that evaluate:
- Leadership and teamwork
- Problem solving
- Communication
- Adaptability
- Conflict resolution

Format as JSON array with keys: question, difficulty, category, skills_tested (array), duration"""

        elif resume_context:
            return f"""Generate {count} behavioral interview questions for a {context['level']} {context['role']} position.

IMPORTANT: Generate a mix of questions:
- {resume_based_count} questions should be based on the candidate's resume/experience below (ask about specific projects, roles, or experiences from their background)
- {general_count} questions should be general behavioral questions

{resume_info}

For resume-based questions, reference specific experiences, projects, or skills from their background.

Focus on STAR method questions that evaluate:
- Leadership and teamwork
- Problem solving
- Communication
- Adaptability
- Conflict resolution

Format as JSON array with keys: question, difficulty, category, skills_tested (array), duration"""

        elif company:
            return f"""Generate {count} behavioral interview questions that are frequently asked at {company} for a {context['level']} {context['role']} position.

These should reflect {company}'s culture and values. Focus on behavioral patterns that {company} values in their candidates.

Focus on STAR method questions that evaluate:
- Leadership and teamwork
- Problem solving
- Communication
- Adaptability
- Conflict resolution

Format as JSON array with keys: question, difficulty, category, skills_tested (array), duration"""

        # Generic behavioral questions
        return f"""Generate {count} behavioral interview questions for a {context['level']} {context['role']} position.

Focus on STAR method questions that evaluate:
- Leadership and teamwork
- Problem solving
- Communication
- Adaptability
- Conflict resolution

Format as JSON array with keys: question, difficulty, category, skills_tested (array), duration"""
    
    def _parse_llm_response(
        self,
        response: str,
        question_type: QuestionType,
        request: QuestionGenerationRequest
    ) -> List[InterviewQuestion]:
        """Parse LLM response into InterviewQuestion objects"""
        questions = []
        
        try:
            import json
            data = json.loads(response)
            
            if isinstance(data, list):
                for item in data:
                    question = InterviewQuestion(
                        question=item.get("question", ""),
                        type=question_type,
                        difficulty=DifficultyLevel(item.get("difficulty", "medium")),
                        category=item.get("category", "general"),
                        skills_tested=item.get("skills_tested", []),
                        expected_duration_minutes=item.get("duration", 5),
                        follow_up_questions=item.get("follow_ups", []),
                        hints=item.get("hints", [])
                    )
                    questions.append(question)
        
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
        
        return questions
    
    def _get_fallback_technical_questions(
        self,
        request: QuestionGenerationRequest,
        count: int
    ) -> List[InterviewQuestion]:
        """Get fallback technical questions from templates"""
        templates = {
            "junior": [
                "Explain the difference between let, const, and var in JavaScript",
                "What is the difference between == and === in JavaScript?",
                "Explain what a REST API is",
                "What is the difference between SQL and NoSQL databases?",
                "Explain object-oriented programming concepts"
            ],
            "mid": [
                "How would you optimize a slow database query?",
                "Explain the concept of microservices architecture",
                "What are design patterns and give examples?",
                "How do you handle errors in asynchronous code?",
                "Explain caching strategies"
            ],
            "senior": [
                "How would you design a highly available system?",
                "Explain distributed systems challenges",
                "How do you ensure code quality across a large team?",
                "Describe your approach to technical debt",
                "How do you evaluate and adopt new technologies?"
            ]
        }
        
        level_questions = templates.get(request.target_level, templates["mid"])
        questions = []
        
        for q_text in level_questions[:count]:
            difficulty = self._get_difficulty_for_level(request.target_level)
            
            questions.append(
                InterviewQuestion(
                    question=q_text,
                    type=QuestionType.TECHNICAL,
                    difficulty=difficulty,
                    category="general",
                    skills_tested=["technical knowledge"],
                    expected_duration_minutes=5
                )
            )
        
        return questions
    
    def _get_fallback_behavioral_questions(
        self,
        request: QuestionGenerationRequest,
        count: int
    ) -> List[InterviewQuestion]:
        """Get fallback behavioral questions"""
        templates = [
            "Tell me about a time when you had to work under pressure",
            "Describe a situation where you had to work with a difficult colleague",
            "Give an example of a project that didn't go as planned",
            "Tell me about a time when you had to learn something new quickly",
            "Describe a situation where you had to make a difficult decision",
            "Tell me about your greatest professional achievement",
            "Describe a time when you received critical feedback",
            "Tell me about a time when you had to persuade someone"
        ]
        
        questions = []
        for q_text in templates[:count]:
            questions.append(
                InterviewQuestion(
                    question=q_text,
                    type=QuestionType.BEHAVIORAL,
                    difficulty=DifficultyLevel.MEDIUM,
                    category="behavioral",
                    skills_tested=["communication", "self-awareness"],
                    expected_duration_minutes=7,
                    follow_up_questions=[
                        "What was the outcome?",
                        "What did you learn from this experience?"
                    ]
                )
            )
        
        return questions
    
    def _get_difficulty_for_level(self, level: str) -> DifficultyLevel:
        """Map experience level to question difficulty"""
        mapping = {
            "junior": DifficultyLevel.EASY,
            "mid": DifficultyLevel.MEDIUM,
            "senior": DifficultyLevel.HARD
        }
        return mapping.get(level, DifficultyLevel.MEDIUM)
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        import uuid
        return f"sess_{uuid.uuid4().hex[:12]}"
    
    def generate_follow_up(
        self,
        original_question: InterviewQuestion,
        user_answer: str
    ) -> str:
        """Generate a follow-up question based on the answer"""
        prompt = f"""Based on the interview question and answer below, generate an insightful follow-up question.

Original Question: {original_question.question}
Candidate's Answer: {user_answer}

Generate a follow-up question that:
1. Probes deeper into their answer
2. Tests their knowledge further
3. Is relevant to the original question

Respond with just the follow-up question."""
        
        try:
            follow_up = self.llm_client.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=200
            )
            return follow_up.strip()
        except Exception as e:
            print(f"Error generating follow-up: {e}")
            return random.choice(original_question.follow_up_questions) if original_question.follow_up_questions else "Can you elaborate on that?"

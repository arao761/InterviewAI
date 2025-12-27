"""
DSA Question Generator Service

Generates LeetCode-style coding problems using AI based on difficulty and topic.
"""
import json
from typing import Dict, List, Optional, Any
from app.services.ai_service import AIService
from app.core.logging import logger

# Import LLM client from ai-engine
try:
    from src.utils.llm_client import LLMClient
except ImportError:
    # Fallback if import fails
    LLMClient = None


class DSAGenerator:
    """Generates DSA coding problems using AI."""
    
    # DSA Topics organized by category
    CORE_DATA_STRUCTURES = [
        "Arrays & Strings",
        "Linked Lists",
        "Hash Maps & Sets",
        "Stacks & Queues",
        "Trees",
        "Heaps (Priority Queues)",
        "Graphs",
        "Tries (Prefix Trees)",
    ]
    
    ALGORITHMS_TECHNIQUES = [
        "Sorting & Searching",
        "Recursion & Backtracking",
        "Dynamic Programming",
        "Greedy Algorithms",
        "Bit Manipulation",
    ]
    
    ALL_TOPICS = CORE_DATA_STRUCTURES + ALGORITHMS_TECHNIQUES
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        # Initialize LLM client for direct question generation
        if LLMClient:
            self.llm_client = LLMClient()
        else:
            self.llm_client = None
            logger.warning("LLMClient not available, DSA generation may be limited")
    
    async def generate_dsa_question(
        self,
        difficulty: str = "medium",
        topic: Optional[str] = None,
        num_questions: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Generate DSA coding problems using AI.
        
        Args:
            difficulty: easy, medium, or hard
            topic: Specific DSA topic (optional, will be randomly selected if not provided)
            num_questions: Number of questions to generate
            
        Returns:
            List of DSA question dictionaries with problem statement, examples, constraints, etc.
        """
        try:
            # Select topic if not provided
            if not topic:
                import random
                topic = random.choice(self.ALL_TOPICS)
            
            logger.info(f"Generating {num_questions} DSA question(s) - Difficulty: {difficulty}, Topic: {topic}")
            
            # Use AI to generate the question
            prompt = self._build_dsa_prompt(difficulty, topic, num_questions)
            
            # Call AI service to generate question
            # We'll use the PrepWise API's question generation with a specialized prompt
            response = await self._generate_with_ai(prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating DSA question: {e}")
            raise
    
    def _build_dsa_prompt(self, difficulty: str, topic: str, num_questions: int) -> str:
        """Build the prompt for AI to generate DSA questions."""
        return f"""Generate {num_questions} LeetCode-style coding problem(s) for a {difficulty} difficulty interview.

Topic: {topic}

Requirements:
1. Create a complete coding problem similar to LeetCode format
2. Include a clear problem statement
3. Provide 2-3 examples with input/output
4. List all constraints
5. Provide function signature for common languages (Python, JavaScript, Java, C++)
6. Include expected time/space complexity hints
7. Make it appropriate for {difficulty} level

For each question, provide:
- title: Short descriptive title (e.g., "Two Sum", "Reverse Linked List")
- problem_statement: Full problem description
- examples: Array of examples with input, output, and explanation
- constraints: Array of constraint strings
- function_signatures: Object with language-specific function signatures
  - python: Function signature for Python
  - javascript: Function signature for JavaScript/TypeScript
  - java: Function signature for Java
  - cpp: Function signature for C++
- hints: Array of 2-3 hints (optional)
- expected_complexity: Object with time and space complexity
- difficulty: {difficulty}
- topic: {topic}

Return ONLY a valid JSON array. No markdown, no code blocks, just pure JSON.

Example format:
[
  {{{{
    "title": "Two Sum",
    "problem_statement": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.",
    "examples": [
      {{{{
        "input": "nums = [2,7,11,15], target = 9",
        "output": "[0,1]",
        "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
      }}}},
      {{{{
        "input": "nums = [3,2,4], target = 6",
        "output": "[1,2]",
        "explanation": "The numbers at indices 1 and 2 add up to 6."
      }}}}
    ],
    "constraints": [
      "2 <= nums.length <= 10^4",
      "-10^9 <= nums[i] <= 10^9",
      "-10^9 <= target <= 10^9",
      "Only one valid answer exists."
    ],
    "function_signatures": {{{{
      "python": "def twoSum(nums: List[int], target: int) -> List[int]:",
      "javascript": "function twoSum(nums, target) {{",
      "java": "public int[] twoSum(int[] nums, int target) {{",
      "cpp": "vector<int> twoSum(vector<int>& nums, int target) {{"
    }}}},
    "hints": [
      "A really brute force way would be to search for all possible pairs of numbers",
      "Use a hash map to store the complement of each number"
    ],
    "expected_complexity": {{{{
      "time": "O(n)",
      "space": "O(n)"
    }}}},
    "difficulty": "easy",
    "topic": "Hash Maps & Sets"
  }}}}
]"""
    
    async def _generate_with_ai(self, prompt: str) -> List[Dict[str, Any]]:
        """Use AI service to generate DSA questions."""
        try:
            # Try to use LLMClient first (preferred method)
            if self.llm_client:
                system_prompt = "You are an expert at creating LeetCode-style coding problems. Always return valid JSON only, no markdown, no code blocks. Return a JSON array of question objects."
                
                # Generate using LLM client (synchronous, but we're in async context)
                import asyncio
                loop = asyncio.get_event_loop()
                response_text = await loop.run_in_executor(
                    None,
                    lambda: self.llm_client.generate(
                        prompt=prompt,
                        system_prompt=system_prompt,
                        json_mode=True,
                        temperature=0.7,
                        max_tokens=3000
                    )
                )
            else:
                # Fallback to direct OpenAI call
                logger.warning("LLMClient not available, using direct OpenAI call")
                response_text = await self._call_openai_direct(prompt)
            
            # Parse the JSON response
            try:
                # Clean response - remove markdown code blocks if present
                cleaned_response = response_text.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.startswith("```"):
                    cleaned_response = cleaned_response[3:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                cleaned_response = cleaned_response.strip()
                
                questions = json.loads(cleaned_response)
                if not isinstance(questions, list):
                    questions = [questions]
                
                logger.info(f"✅ Generated {len(questions)} DSA question(s)")
                return questions
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                logger.error(f"Response text (first 500 chars): {response_text[:500]}")
                # Return a fallback question
                return [self._get_fallback_question()]
                
        except Exception as e:
            logger.error(f"Error in AI generation: {e}")
            return [self._get_fallback_question()]
    
    async def _call_openai_direct(self, prompt: str) -> str:
        """Call OpenAI directly to generate DSA questions (fallback method)."""
        try:
            from openai import AsyncOpenAI
            import os
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            
            client = AsyncOpenAI(api_key=api_key)
            
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating LeetCode-style coding problems. Always return valid JSON only, no markdown, no code blocks."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            return response.choices[0].message.content.strip()
                
        except Exception as e:
            logger.error(f"Error calling OpenAI directly: {e}")
            raise
    
    def _get_fallback_question(self) -> Dict[str, Any]:
        """Return a fallback DSA question if AI generation fails."""
        return {
            "title": "Two Sum",
            "problem_statement": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.",
            "examples": [
                {
                    "input": "nums = [2,7,11,15], target = 9",
                    "output": "[0,1]",
                    "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
                }
            ],
            "constraints": [
                "2 <= nums.length <= 10^4",
                "-10^9 <= nums[i] <= 10^9",
                "-10^9 <= target <= 10^9",
                "Only one valid answer exists."
            ],
            "function_signatures": {
                "python": "def twoSum(nums: List[int], target: int) -> List[int]:",
                "javascript": "function twoSum(nums, target) {",
                "java": "public int[] twoSum(int[] nums, int target) {",
                "cpp": "vector<int> twoSum(vector<int>& nums, int target) {"
            },
            "hints": [
                "Use a hash map to store complements"
            ],
            "expected_complexity": {
                "time": "O(n)",
                "space": "O(n)"
            },
            "difficulty": "easy",
            "topic": "Hash Maps & Sets"
        }


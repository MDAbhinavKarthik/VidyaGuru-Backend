"""
LLM (Large Language Model) Client

Centralized wrapper for Google Generative AI (Gemini) interactions.
Handles configuration, prompt engineering, and response parsing.

Usage:
    from utils.llm_client import LLMClient
    
    client = LLMClient()
    response = await client.generate_challenge(category="system_design")
    hint = await client.get_hint(question, current_attempt)
"""

import logging
from typing import Optional, Dict, Any, List
import google.generativeai as genai
from datetime import datetime

from core.exceptions import (
    ExternalServiceError,
    ChallengeGenerationError,
    MentorResponseError,
)
from utils.constants import FEATURES

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Wrapper for Google Generative AI API.
    
    Handles:
    - Challenge generation
    - Solution evaluation
    - Hint generation
    - Mentor responses
    - Code analysis
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize LLM client with API key"""
        if api_key:
            genai.configure(api_key=api_key)
        
        self.model = "gemini-2.0-flash"  # Using latest Gemini model
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
    
    async def generate_challenge(
        self,
        category: str,
        difficulty: str,
        industry: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate an industry challenge using AI.
        
        Args:
            category: Challenge category (system_design, scalability, etc.)
            difficulty: Difficulty level (easy, intermediate, hard, expert)
            industry: Optional industry context
            description: Optional additional requirements
        
        Returns:
            Dict with challenge details
        
        Raises:
            ChallengeGenerationError: If generation fails
        """
        if not FEATURES["challenges"]:
            raise ExternalServiceError(
                "challenges",
                "Challenge generation is currently disabled"
            )
        
        prompt = self._build_challenge_prompt(
            category, difficulty, industry, description
        )
        
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config=self.generation_config,
            )
            
            challenge = self._parse_challenge_response(response.text)
            return challenge
            
        except Exception as e:
            logger.error(f"Challenge generation failed: {str(e)}")
            raise ChallengeGenerationError(
                "Failed to generate challenge",
                details={"category": category, "difficulty": difficulty}
            )
    
    async def evaluate_solution(
        self,
        challenge_description: str,
        solution: str,
        difficulty: str,
    ) -> Dict[str, Any]:
        """
        Evaluate a solution using AI.
        
        Returns scores for innovation, practicality, completeness, quality.
        """
        prompt = self._build_evaluation_prompt(
            challenge_description, solution, difficulty
        )
        
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config=self.generation_config,
            )
            
            evaluation = self._parse_evaluation_response(response.text)
            return evaluation
            
        except Exception as e:
            logger.error(f"Solution evaluation failed: {str(e)}")
            raise ExternalServiceError(
                "gemini",
                "Failed to evaluate solution"
            )
    
    async def get_hint(
        self,
        question: str,
        current_attempt: str,
        struggle_area: str,
    ) -> Dict[str, str]:
        """
        Get Socratic hint without revealing answer.
        
        Returns:
            Dict with guiding_question and encouragement
        """
        prompt = self._build_hint_prompt(question, current_attempt, struggle_area)
        
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            
            hint = self._parse_hint_response(response.text)
            return hint
            
        except Exception as e:
            logger.error(f"Hint generation failed: {str(e)}")
            raise ExternalServiceError(
                "gemini",
                "Failed to generate hint"
            )
    
    async def get_mentor_response(
        self,
        topic: str,
        user_question: str,
        conversation_history: List[Dict[str, str]] = None,
        user_level: str = "intermediate",
    ) -> str:
        """
        Get AI mentor response to user question.
        
        Args:
            topic: Topic being discussed
            user_question: User's question
            conversation_history: Previous messages (for context)
            user_level: User's proficiency level
        
        Returns:
            Mentor response text
        """
        if not FEATURES["live_mentor"]:
            raise ExternalServiceError(
                "mentor",
                "Mentor service is currently unavailable"
            )
        
        prompt = self._build_mentor_prompt(
            topic, user_question, conversation_history, user_level
        )
        
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config=self.generation_config,
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Mentor response failed: {str(e)}")
            raise MentorResponseError(
                "Failed to generate mentor response"
            )
    
    async def analyze_code(
        self,
        code: str,
        context: str = "general",
    ) -> Dict[str, Any]:
        """
        Analyze code for quality, issues, and improvements.
        
        Returns:
            Dict with analysis results
        """
        prompt = f"""
        Analyze the following code for:
        1. Code quality and style
        2. Potential bugs or issues
        3. Performance considerations
        4. Security vulnerabilities (if any)
        5. Suggested improvements
        
        Context: {context}
        
        Code:
        ```
        {code}
        ```
        
        Provide analysis in JSON format with keys: quality_score, issues, suggestions, security_notes
        """
        
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            
            analysis = self._parse_json_response(response.text)
            return analysis
            
        except Exception as e:
            logger.error(f"Code analysis failed: {str(e)}")
            raise ExternalServiceError(
                "gemini",
                "Failed to analyze code"
            )
    
    # ========================================================================
    # Prompt Building Methods
    # ========================================================================
    
    def _build_challenge_prompt(
        self,
        category: str,
        difficulty: str,
        industry: Optional[str],
        description: Optional[str],
    ) -> str:
        """Build prompt for challenge generation"""
        return f"""
        Generate a technical challenge for the following:
        
        Category: {category}
        Difficulty: {difficulty}
        Industry Context: {industry or 'General technology'}
        Additional Requirements: {description or 'None'}
        
        Please generate a challenging problem that:
        1. Is realistic and industry-relevant
        2. Requires thoughtful design decisions
        3. Has trade-offs to discuss
        4. Can be evaluated based on innovation and practicality
        
        Format your response as JSON with keys:
        - title: Challenge title
        - description: Full problem description
        - context: Business context/background
        - requirements: List of must-have requirements
        - constraints: Technical constraints
        - success_criteria: How to know the solution is good
        - example_solution_outline: High-level approach (without full code)
        - estimated_time_minutes: Expected completion time
        """
    
    def _build_evaluation_prompt(
        self,
        challenge: str,
        solution: str,
        difficulty: str,
    ) -> str:
        """Build prompt for solution evaluation"""
        return f"""
        Evaluate this solution to a technical challenge.
        
        Challenge:
        {challenge}
        
        Solution Provided:
        {solution}
        
        Difficulty Level: {difficulty}
        
        Please evaluate based on:
        1. Innovation (30%): Does it show creative thinking?
        2. Practicality (25%): Is it implementable and maintainable?
        3. Completeness (25%): Does it address all requirements?
        4. Code Quality (20%): Is the approach well-structured?
        
        Provide your response as JSON with:
        - innovation_score: 0-100
        - practicality_score: 0-100
        - completeness_score: 0-100
        - code_quality_score: 0-100
        - overall_score: 0-100 (weighted average)
        - strengths: List of strengths
        - improvements: List of areas to improve
        - is_resume_worthy: boolean
        - feedback: Detailed feedback
        """
    
    def _build_hint_prompt(
        self,
        question: str,
        current_attempt: str,
        struggle_area: str,
    ) -> str:
        """Build prompt for hint generation (Socratic method)"""
        return f"""
        The user is working on this problem: {question}
        
        Their current attempt/understanding: {current_attempt}
        
        They're struggling with: {struggle_area}
        
        Please provide a Socratic hint that:
        1. Does NOT reveal the answer
        2. Asks guiding questions
        3. Helps them think through the problem
        4. Builds on what they've already done
        
        Response format:
        Guiding Question: [Your question here]
        Think About: [One specific aspect they should focus on]
        Encouragement: [Brief encouraging message]
        """
    
    def _build_mentor_prompt(
        self,
        topic: str,
        user_question: str,
        conversation_history: Optional[List[Dict[str, str]]],
        user_level: str,
    ) -> str:
        """Build prompt for mentor response"""
        history_text = ""
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                history_text += f"\nUser: {msg.get('user', '')}\nMentor: {msg.get('mentor', '')}"
        
        return f"""
        You are an experienced software engineering mentor helping a student.
        
        Topic: {topic}
        Student Level: {user_level}
        
        Previous Conversation:
        {history_text or "This is the start of the conversation"}
        
        Student Question: {user_question}
        
        Please respond as a mentor would:
        1. Acknowledge their question/concern
        2. Provide relevant guidance or explanation
        3. Ask follow-up questions to deepen understanding
        4. Suggest resources or next steps if appropriate
        
        Keep response concise and encouraging.
        """
    
    # ========================================================================
    # Response Parsing Methods
    # ========================================================================
    
    def _parse_challenge_response(self, response_text: str) -> Dict[str, Any]:
        """Parse challenge generation response"""
        import json
        try:
            # Try to extract JSON from response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse JSON from challenge response: {e}")
        
        # Fallback: return structured response
        return {
            "title": "Generated Challenge",
            "description": response_text,
            "success_criteria": "Implement according to requirements",
        }
    
    def _parse_evaluation_response(self, response_text: str) -> Dict[str, Any]:
        """Parse evaluation response"""
        import json
        try:
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse evaluation JSON: {e}")
        
        return {
            "innovation_score": 70,
            "practicality_score": 75,
            "completeness_score": 80,
            "code_quality_score": 75,
            "overall_score": 75,
        }
    
    def _parse_hint_response(self, response_text: str) -> Dict[str, str]:
        """Parse hint response"""
        lines = response_text.strip().split("\n")
        return {
            "guiding_question": response_text,
            "encouragement": "Keep exploring different approaches!",
        }
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Generic JSON response parser"""
        import json
        try:
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse JSON response: {e}")
        
        return {"raw_response": response_text}

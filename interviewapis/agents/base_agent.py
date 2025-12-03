"""
Base Agent Module
Provides base class and utilities for all specialized agents

Usage:
    from agents.base_agent import BaseAgent
"""

from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os


class BaseAgent:
    """Base class for all specialized interview agents"""
    
    def __init__(self, agent_type: str, system_prompt: str, llm: Optional[ChatOpenAI] = None):
        """
        Initialize base agent
        
        Args:
            agent_type: Identifier for the agent (e.g., 'product_manager')
            system_prompt: System prompt defining agent's expertise
            llm: Optional LangChain LLM instance
        """
        self.agent_type = agent_type
        self.system_prompt = system_prompt
        self.llm = llm or ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            api_key=os.environ.get("OPENAI_API_KEY")
        )
    
    def process(
        self,
        question: str,
        user_context: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Process interview question and generate response
        
        Args:
            question: The interview question
            user_context: Additional context about the candidate
            conversation_history: Previous Q&A exchanges
            
        Returns:
            Dict with answer, confidence, and metadata
        """
        # Build context from conversation history
        history_context = self._build_history_context(conversation_history)
        
        # Construct user prompt
        user_prompt = self._build_user_prompt(question, user_context, history_context)
        
        # Generate response
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            return {
                "answer": answer,
                "agent_type": self.agent_type,
                "confidence": self._calculate_confidence(answer),
                "metadata": self._extract_metadata(answer)
            }
            
        except Exception as e:
            return {
                "answer": f"Error generating response: {str(e)}",
                "agent_type": self.agent_type,
                "confidence": 0.0,
                "metadata": {}
            }
    
    def _build_history_context(self, conversation_history: Optional[List[Dict]]) -> str:
        """Build context string from conversation history"""
        if not conversation_history:
            return ""
        
        history_context = "\n\nPrevious conversation:\n"
        for i, exchange in enumerate(conversation_history[-3:], 1):  # Last 3 exchanges
            history_context += f"Q{i}: {exchange.get('question', '')}\n"
            history_context += f"A{i}: {exchange.get('answer', '')[:200]}...\n\n"
        
        return history_context
    
    def _build_user_prompt(
        self,
        question: str,
        user_context: Optional[str],
        history_context: str
    ) -> str:
        """Build the user prompt"""
        prompt = f"""Interview Question: "{question}"

{f'Candidate Context: {user_context}' if user_context else ''}
{history_context if history_context else ''}

Provide a comprehensive, well-structured answer that would impress in an interview."""
        
        return prompt
    
    def _calculate_confidence(self, answer: str) -> float:
        """Calculate confidence score based on answer quality"""
        # Simple heuristic - can be enhanced
        if len(answer) < 100:
            return 0.6
        elif len(answer) < 500:
            return 0.75
        elif len(answer) < 1000:
            return 0.85
        else:
            return 0.9
    
    def _extract_metadata(self, answer: str) -> Dict:
        """Extract metadata from answer"""
        return {
            "word_count": len(answer.split()),
            "char_count": len(answer),
            "has_examples": "example" in answer.lower() or "for instance" in answer.lower(),
            "has_structure": any(marker in answer for marker in ["1.", "2.", "First", "Second", "•", "-"])
        }
    
    def get_capabilities(self) -> Dict:
        """Return agent capabilities"""
        return {
            "agent_type": self.agent_type,
            "system_prompt": self.system_prompt[:200] + "...",
            "model": "gpt-4o"
        }

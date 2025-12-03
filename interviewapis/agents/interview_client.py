"""
Multi-Agent Mock Interview Client
Interactive CLI for conducting mock interviews

Usage:
    python interview_client.py
"""

import requests
import json
from typing import List, Dict
from datetime import datetime


class InterviewClient:
    """Client for Multi-Agent Mock Interview System"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.conversation_history: List[Dict] = []
        
    def health_check(self) -> dict:
        """Check API health"""
        response = requests.get(f"{self.base_url}/api/health")
        return response.json()
    
    def list_agents(self) -> dict:
        """Get all available agents"""
        response = requests.get(f"{self.base_url}/api/agents")
        return response.json()
    
    def ask_question(
        self,
        question: str,
        interview_type: str = None,
        user_context: str = None
    ) -> dict:
        """Ask an interview question"""
        
        payload = {
            "question": question,
            "interview_type": interview_type,
            "user_context": user_context,
            "conversation_history": self.conversation_history
        }
        
        response = requests.post(
            f"{self.base_url}/api/interview",
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        
        result = response.json()
        
        # Add to conversation history
        self.conversation_history.append({
            "question": question,
            "answer": result['answer'],
            "agent": result['agent_used'],
            "timestamp": result['timestamp']
        })
        
        return result
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history


def print_banner():
    """Print application banner"""
    print("\n" + "="*70)
    print("  🎤 MULTI-AGENT MOCK INTERVIEW SYSTEM")
    print("  Practice interviews with AI-powered specialized agents")
    print("="*70 + "\n")


def print_agents_info(agents_data: dict):
    """Print available agents"""
    print("📋 Available Interview Agents:\n")
    
    for i, agent in enumerate(agents_data['agents'], 1):
        print(f"{i}. {agent['name']} ({agent['id']})")
        print(f"   Best for: {agent['best_for']}")
        print(f"   Capabilities:")
        for cap in agent['capabilities'][:3]:
            print(f"      • {cap}")
        print()


def print_interview_response(result: dict):
    """Print formatted interview response"""
    
    print("\n" + "="*70)
    print("📝 INTERVIEW RESPONSE")
    print("="*70)
    
    # Question
    print(f"\n❓ Question:")
    print(f"   {result['question']}")
    
    # Agent info
    print(f"\n🤖 Agent Used: {result['agent_used'].replace('_', ' ').title()}")
    print(f"💡 Reasoning: {result['reasoning']}")
    print(f"⭐ Confidence: {result['confidence_score']*100:.0f}%")
    
    # Answer
    print(f"\n✅ Answer:")
    print("-" * 70)
    
    # Format answer with proper line wrapping
    answer_lines = result['answer'].split('\n')
    for line in answer_lines:
        if len(line) > 70:
            # Wrap long lines
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= 70:
                    current_line += word + " "
                else:
                    print(current_line.strip())
                    current_line = word + " "
            if current_line:
                print(current_line.strip())
        else:
            print(line)
    
    print("-" * 70)
    
    # Follow-up questions
    if result.get('suggested_follow_ups'):
        print(f"\n💭 Suggested Follow-up Questions:")
        for i, follow_up in enumerate(result['suggested_follow_ups'], 1):
            print(f"   {i}. {follow_up}")
    
    print("\n" + "="*70 + "\n")


def conduct_interview_session(client: InterviewClient):
    """Run an interactive interview session"""
    
    print("\n🎯 Starting Interview Session")
    print("   Type 'quit' to exit, 'clear' to reset history, 'history' to view past Q&A\n")
    
    # Optional: Get user context
    print("📝 Optional: Provide context about yourself (or press Enter to skip):")
    print("   Example: '5 years as PM at tech startup, focusing on B2B SaaS'")
    user_context = input("➤ ").strip()
    if not user_context:
        user_context = None
    
    print("\n✅ Session started! Ask your first interview question.\n")
    
    question_count = 0
    
    while True:
        # Get question
        question = input("❓ Your Question: ").strip()
        
        # Handle special commands
        if question.lower() == 'quit':
            print("\n👋 Thanks for practicing! Good luck with your interviews!\n")
            break
        
        if question.lower() == 'clear':
            client.clear_history()
            print("✅ Conversation history cleared\n")
            continue
        
        if question.lower() == 'history':
            history = client.get_history()
            if not history:
                print("📝 No conversation history yet\n")
            else:
                print(f"\n📚 Conversation History ({len(history)} exchanges):\n")
                for i, exchange in enumerate(history, 1):
                    print(f"{i}. Q: {exchange['question'][:60]}...")
                    print(f"   Agent: {exchange['agent']}")
                    print(f"   Time: {exchange['timestamp'][:19]}")
                    print()
            continue
        
        if not question or len(question) < 5:
            print("⚠️  Please enter a valid question (at least 5 characters)\n")
            continue
        
        # Process question
        try:
            question_count += 1
            print(f"\n🔍 Processing question #{question_count}...")
            print("   (This may take 10-30 seconds...)\n")
            
            result = client.ask_question(
                question=question,
                user_context=user_context
            )
            
            print_interview_response(result)
            
            # Ask if they want to use a follow-up
            if result.get('suggested_follow_ups'):
                use_followup = input("💭 Use a follow-up question? (1-3 or press Enter to skip): ").strip()
                if use_followup.isdigit() and 1 <= int(use_followup) <= 3:
                    question = result['suggested_follow_ups'][int(use_followup) - 1]
                    print(f"\n❓ Follow-up Question: {question}\n")
                    
                    result = client.ask_question(
                        question=question,
                        user_context=user_context
                    )
                    print_interview_response(result)
        
        except KeyboardInterrupt:
            print("\n\n⏸️  Interrupted. Type 'quit' to exit or continue with another question.\n")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            print("Please try again or check if the API is running.\n")


def quick_test_mode(client: InterviewClient):
    """Quick test with example questions"""
    
    examples = [
        {
            "category": "Product Management",
            "question": "How would you prioritize features for a new product launch?",
            "context": "5 years PM experience"
        },
        {
            "category": "Technical",
            "question": "Explain the difference between a hash table and a binary search tree",
            "context": "3 years as software engineer"
        },
        {
            "category": "System Design",
            "question": "Design a URL shortener like bit.ly",
            "context": "Senior engineer with distributed systems experience"
        },
        {
            "category": "Behavioral",
            "question": "Tell me about a time you had to deal with a difficult stakeholder",
            "context": "Team lead with 4 years experience"
        },
        {
            "category": "Coding",
            "question": "Write a function to reverse a linked list",
            "context": "Preparing for FAANG interviews"
        }
    ]
    
    print("\n🧪 Quick Test Mode - Example Questions\n")
    
    for i, ex in enumerate(examples, 1):
        print(f"{i}. [{ex['category']}] {ex['question']}")
    
    choice = input("\nSelect a question (1-5) or press Enter to skip: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= 5:
        selected = examples[int(choice) - 1]
        print(f"\n✅ Selected: {selected['category']}")
        print(f"📝 Context: {selected['context']}\n")
        
        try:
            print("🔍 Processing question...\n")
            
            result = client.ask_question(
                question=selected['question'],
                user_context=selected['context']
            )
            
            print_interview_response(result)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            return False
    
    return False


def main():
    """Main function"""
    
    print_banner()
    
    # Initialize client
    client = InterviewClient()
    
    # Health check
    print("🔍 Checking API connection...")
    try:
        health = client.health_check()
        print(f"   ✅ API Status: {health['status']}")
        print(f"   ✅ Agents Available: {health['agents_available']}")
        print(f"   ✅ LLM Configured: {health['llm_configured']}\n")
    except Exception as e:
        print(f"   ❌ Error: API is not reachable")
        print(f"   Make sure the API is running: uvicorn main:app --reload")
        print(f"   Error details: {e}\n")
        return
    
    # Get agents info
    try:
        agents = client.list_agents()
        print_agents_info(agents)
    except Exception as e:
        print(f"⚠️  Could not load agents info: {e}\n")
    
    # Main menu
    print("Select mode:")
    print("  1. Interactive Interview Session (recommended)")
    print("  2. Quick Test with Examples")
    print("  3. Single Question")
    
    mode = input("\nEnter choice (1-3): ").strip()
    
    if mode == "1":
        conduct_interview_session(client)
    
    elif mode == "2":
        if quick_test_mode(client):
            # Ask if they want to continue with interactive mode
            cont = input("\n💭 Continue with interactive session? (y/n): ").strip().lower()
            if cont == 'y':
                conduct_interview_session(client)
    
    elif mode == "3":
        question = input("\n❓ Enter your question: ").strip()
        context = input("📝 Context (optional): ").strip() or None
        
        if question and len(question) >= 5:
            try:
                print("\n🔍 Processing...\n")
                result = client.ask_question(question, user_context=context)
                print_interview_response(result)
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
        else:
            print("\n⚠️  Invalid question\n")
    
    else:
        print("\n⚠️  Invalid choice\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")

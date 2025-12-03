"""
Supervisor Agent
Routes questions to the appropriate specialized agent

Usage:
    from agents.supervisor import SupervisorAgent
    
    agent = SupervisorAgent()
    routing = agent.route_question("How would you design Twitter?")
"""

from agents.base_agent import BaseAgent
import json


SUPERVISOR_PROMPT = """You are an Interview Supervisor Agent with expertise in routing questions to specialized agents. Your role is to:

1. **Analyze the interview question**
2. **Determine the domain and type**
3. **Select the most appropriate specialized agent**
4. **Provide clear reasoning**

**Available Specialized Agents:**

1. **product_manager**
   - Best for: Product strategy, frameworks (CIRCLES, RICE, RICE), metrics (AARRR, HEART), user research, roadmaps, prioritization
   - Keywords: "product", "feature", "prioritize", "metric", "user", "roadmap", "PM", "strategy"
   - Examples: "How would you prioritize features?", "What metrics for Instagram?"

2. **technical**
   - Best for: Algorithms, data structures, complexity analysis, design patterns, software concepts
   - Keywords: "algorithm", "data structure", "complexity", "sort", "search", "tree", "hash", "array"
   - Examples: "Explain binary search", "What's Big O of quicksort?"

3. **architect**
   - Best for: System architecture, design patterns, scalability, infrastructure, cloud, microservices
   - Keywords: "architecture", "design pattern", "scalability", "microservices", "monolith", "infrastructure"
   - Examples: "Microservices vs monolith", "How to scale a database?"

4. **coding**
   - Best for: Writing code, implementation, code review, coding best practices
   - Keywords: "write", "implement", "code", "function", "class", "program", "script"
   - Examples: "Write a function to...", "Implement a linked list"

5. **behavioral**
   - Best for: Soft skills, leadership, conflict resolution, past experiences, STAR method
   - Keywords: "tell me about", "describe a time", "how do you handle", "conflict", "team", "leadership"
   - Examples: "Tell me about a time you...", "How do you handle disagreement?"

6. **system_design**
   - Best for: Designing large-scale distributed systems, trade-offs, capacity estimation
   - Keywords: "design", "build", "create" + system names (Twitter, Instagram, Uber, etc.)
   - Examples: "Design Twitter", "Design a URL shortener", "Build a messaging system"

**Routing Decision Criteria:**

**system_design** takes priority when:
- Question starts with "Design", "Build", "Create" + a system/product
- Mentions specific apps/systems to design
- Asks about distributed systems, scalability of entire systems

**product_manager** for:
- Product strategy questions
- Framework application (CIRCLES, RICE, etc.)
- Metrics and KPI definition
- User research and personas
- Feature prioritization
- Product roadmaps

**technical** for:
- Algorithm explanations
- Data structure concepts
- Complexity analysis
- Software engineering concepts
- NOT for writing code (use coding agent)

**architect** for:
- Architecture patterns
- Scalability of components
- Infrastructure decisions
- Microservices design
- Cloud architecture
- NOT for full system design (use system_design agent)

**coding** for:
- Explicit requests to write code
- Implementation questions
- Code review scenarios
- "Write a function/class"

**behavioral** for:
- Questions starting with "Tell me about a time..."
- "Describe a situation..."
- "How do you handle..."
- Leadership and soft skills

**Response Format:**
Respond ONLY with valid JSON (no additional text):
{
  "selected_agent": "agent_name",
  "reasoning": "Clear explanation of why this agent is best suited",
  "confidence": 0.95,
  "alternative_agents": ["backup_agent"] or []
}

**Important:**
- Choose exactly ONE agent
- Confidence: 0.8-1.0 for clear matches, 0.6-0.8 for ambiguous
- Include alternatives only if question spans multiple domains
- Be decisive - don't overthink
"""


class SupervisorAgent(BaseAgent):
    """Supervisor agent for routing questions"""
    
    def __init__(self, llm=None):
        super().__init__(
            agent_type="supervisor",
            system_prompt=SUPERVISOR_PROMPT,
            llm=llm
        )
    
    def route_question(
        self,
        question: str,
        user_context: str = None,
        interview_type: str = None
    ) -> dict:
        """
        Route question to appropriate agent
        
        Args:
            question: The interview question
            user_context: Optional context about the candidate
            interview_type: Optional hint about interview type
            
        Returns:
            Dict with selected_agent, reasoning, confidence
        """
        # Build routing prompt
        prompt = f"""Analyze this interview question and route it to the most appropriate agent.

Question: "{question}"

{f'Interview Type Hint: {interview_type}' if interview_type else ''}
{f'Candidate Context: {user_context}' if user_context else ''}

Determine the best agent to handle this question."""

        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self.llm.invoke([
                type("Message", (), {"content": self.system_prompt, "type": "system"})(),
                type("Message", (), {"content": prompt, "type": "human"})()
            ])
            
            response_text = response.content
            
            # Extract JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            routing = json.loads(response_text)
            
            # Validate selected agent
            valid_agents = [
                "product_manager", "technical", "architect",
                "coding", "behavioral", "system_design"
            ]
            
            if routing.get('selected_agent') not in valid_agents:
                # Fallback to technical agent
                routing = {
                    "selected_agent": "technical",
                    "reasoning": "Default routing due to invalid agent selection",
                    "confidence": 0.7,
                    "alternative_agents": []
                }
            
            return routing
            
        except Exception as e:
            print(f"Error in routing: {e}")
            # Default fallback
            return {
                "selected_agent": "technical",
                "reasoning": f"Default routing due to error: {str(e)}",
                "confidence": 0.6,
                "alternative_agents": []
            }
    
    def get_capabilities(self):
        """Return supervisor capabilities"""
        return {
            **super().get_capabilities(),
            "role": "Question routing and agent selection",
            "available_agents": [
                "product_manager",
                "technical",
                "architect",
                "coding",
                "behavioral",
                "system_design"
            ],
            "routing_criteria": [
                "Question content analysis",
                "Keyword detection",
                "Interview type hints",
                "Context understanding"
            ]
        }


def create_supervisor_agent(llm=None) -> SupervisorAgent:
    """Factory function to create SupervisorAgent"""
    return SupervisorAgent(llm)

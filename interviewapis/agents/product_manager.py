"""
Product Manager Agent
Specialized in product strategy, frameworks, metrics, and PM methodologies

Usage:
    from agents.product_manager import ProductManagerAgent
    
    agent = ProductManagerAgent()
    result = agent.process("How would you prioritize features?")
"""

from agents.base_agent import BaseAgent


PRODUCT_MANAGER_PROMPT = """You are an Expert Product Manager with 15+ years of experience at top tech companies (Google, Amazon, Microsoft). You excel at:

**Product Strategy & Vision**
- Defining product vision and strategy
- Market analysis and competitive positioning
- Product-market fit evaluation
- Go-to-market strategy

**Frameworks & Methodologies**
- Prioritization: RICE, ICE, Kano Model, MoSCoW, Value vs Effort
- Problem-solving: CIRCLES Method, Jobs-to-be-Done
- Strategy: Porter's Five Forces, Blue Ocean Strategy, Ansoff Matrix
- Product Development: Design Thinking, Lean Startup, Agile

**Metrics & Analytics**
- AARRR Pirate Metrics (Acquisition, Activation, Retention, Revenue, Referral)
- HEART Framework (Happiness, Engagement, Adoption, Retention, Task Success)
- North Star Metric identification
- KPI definition and tracking
- A/B testing and experimentation

**User Research & Insights**
- User personas and segmentation
- Customer journey mapping
- User interviews and surveys
- Usability testing
- Voice of Customer analysis

**Stakeholder Management**
- Cross-functional collaboration
- Executive communication
- Roadmap planning and presentations
- Conflict resolution
- Influence without authority

**Product Lifecycle**
- 0-to-1 product launches
- Feature development and iteration
- Product sunset decisions
- Technical debt management

**When Answering Interview Questions:**

1. **Use Structured Frameworks**: Always apply relevant PM frameworks (CIRCLES, RICE, etc.)
2. **Think User-First**: Start with user needs and pain points
3. **Consider Business Impact**: Balance user value with business goals
4. **Define Metrics**: Specify how you'd measure success
5. **Address Trade-offs**: Explicitly discuss what you're optimizing for
6. **Be Specific**: Use concrete examples and numbers when possible
7. **Show Process**: Walk through your thinking step-by-step
8. **Consider Constraints**: Think about resources, time, technical limitations

**Response Structure:**
- Start with clarifying the problem/goal
- Apply relevant framework(s)
- Provide structured, logical analysis
- Include specific examples
- Define success metrics
- Address implementation considerations
- Discuss trade-offs and alternatives

Answer with the depth and structure expected from a senior PM in a FAANG interview."""


class ProductManagerAgent(BaseAgent):
    """Product Manager specialized agent"""
    
    def __init__(self, llm=None):
        super().__init__(
            agent_type="product_manager",
            system_prompt=PRODUCT_MANAGER_PROMPT,
            llm=llm
        )
    
    def get_capabilities(self):
        """Return PM-specific capabilities"""
        return {
            **super().get_capabilities(),
            "specializations": [
                "Product Strategy",
                "Prioritization Frameworks (RICE, ICE, Kano)",
                "Metrics (AARRR, HEART)",
                "User Research",
                "Roadmap Planning",
                "Stakeholder Management"
            ],
            "frameworks": [
                "CIRCLES Method",
                "RICE Framework",
                "Jobs-to-be-Done",
                "HEART Framework",
                "Design Thinking",
                "Kano Model"
            ],
            "best_for": [
                "Product strategy questions",
                "Feature prioritization",
                "Metric definition",
                "User research approaches",
                "PM framework application"
            ]
        }


# Convenience function for direct usage
def create_product_manager_agent(llm=None) -> ProductManagerAgent:
    """Factory function to create ProductManagerAgent"""
    return ProductManagerAgent(llm)

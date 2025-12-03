# Modular Multi-Agent System - Clean Architecture

## 🎯 Overview

This is a **modular version** of the multi-agent interview system where each agent is in its own file for better organization, maintainability, and extensibility.

## 📁 File Structure

```
agents/
├── __init__.py              # Package initialization & agent registry
├── base_agent.py            # Base class for all agents
├── supervisor.py            # Supervisor agent (routing)
├── product_manager.py       # Product Manager agent
├── technical.py             # Technical Expert agent
├── architect.py             # System Architect agent
├── coding.py                # Coding Expert agent
├── behavioral.py            # Behavioral Coach agent
└── system_design.py         # System Design Expert agent

main_modular.py              # Main API using modular agents
interview_client.py          # Client (works with both versions)
```

## 🚀 Quick Start

### Installation

```bash
# 1. Install dependencies
pip install fastapi uvicorn langchain langchain-openai langgraph python-dotenv pydantic

# 2. Set API key
export OPENAI_API_KEY="sk-your-key-here"

# 3. Run modular version
uvicorn main_modular:app --reload --port 8000

# 4. Use client
python interview_client.py
```

## 📚 Agent Files Explained

### 1. `base_agent.py` - Base Agent Class

The foundation for all specialized agents.

**Key Features**:
- Common processing logic
- Conversation history handling
- Confidence score calculation
- Metadata extraction
- Standard interface for all agents

**Usage**:
```python
from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            agent_type="my_agent",
            system_prompt="Your specialized prompt",
            llm=llm
        )
```

---

### 2. `supervisor.py` - Supervisor Agent

Routes questions to the appropriate specialized agent.

**Routing Logic**:
- Analyzes question content
- Detects keywords
- Considers context
- Selects best agent
- Provides confidence score

**Usage**:
```python
from agents.supervisor import SupervisorAgent

supervisor = SupervisorAgent()
routing = supervisor.route_question("How would you design Twitter?")
# Returns: {'selected_agent': 'system_design', 'reasoning': '...', 'confidence': 0.95}
```

---

### 3. `product_manager.py` - Product Manager Agent

Specialized in PM frameworks, strategy, and metrics.

**Expertise**:
- Product strategy
- RICE, ICE, Kano frameworks
- AARRR, HEART metrics
- User research
- Roadmap planning

**Example Questions**:
- "How would you prioritize features?"
- "What metrics for Instagram?"
- "Explain the CIRCLES method"

**Usage**:
```python
from agents.product_manager import ProductManagerAgent

pm_agent = ProductManagerAgent()
result = pm_agent.process("How would you prioritize features?")
print(result['answer'])
```

---

### 4. `technical.py` - Technical Expert Agent

Specialized in algorithms, data structures, and software concepts.

**Expertise**:
- Algorithms and Big O
- Data structures
- Design patterns
- SOLID principles
- Complexity analysis

**Example Questions**:
- "Explain binary search trees"
- "What's Big O of quicksort?"
- "Compare hash tables and arrays"

---

### 5. `architect.py` - System Architect Agent

Specialized in system architecture and infrastructure.

**Expertise**:
- Architecture patterns
- Microservices design
- Scalability
- Cloud architecture
- High availability

**Example Questions**:
- "Microservices vs monolith?"
- "How to scale a database?"
- "Explain circuit breakers"

---

### 6. `coding.py` - Coding Expert Agent

Specialized in writing production-quality code.

**Expertise**:
- Clean code principles
- Multiple languages (Python, Java, JS, etc.)
- Testing and TDD
- Code review
- Performance optimization

**Example Questions**:
- "Write a function to reverse a linked list"
- "Implement binary search"
- "Review this code"

---

### 7. `behavioral.py` - Behavioral Coach Agent

Specialized in soft skills and leadership.

**Expertise**:
- STAR method
- Leadership stories
- Conflict resolution
- Communication skills
- Team management

**Example Questions**:
- "Tell me about a time you dealt with conflict"
- "Describe a project that failed"
- "How do you handle disagreement?"

---

### 8. `system_design.py` - System Design Expert Agent

Specialized in distributed systems design.

**Expertise**:
- Distributed systems
- CAP theorem trade-offs
- Database selection
- Caching strategies
- Scalability patterns

**Example Questions**:
- "Design Twitter"
- "Design a URL shortener"
- "Build a messaging system"

---

## 🔧 How to Use the Modular System

### Option 1: Using the API

```bash
# Start API
uvicorn main_modular:app --reload --port 8000

# Make request
curl -X POST http://localhost:8000/api/interview \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How would you design Instagram?",
    "user_context": "5 years as software engineer"
  }'
```

### Option 2: Direct Agent Usage

```python
# Import specific agent
from agents import ProductManagerAgent

# Create agent instance
pm_agent = ProductManagerAgent()

# Process question
result = pm_agent.process(
    question="How would you prioritize features?",
    user_context="3 years PM experience"
)

print(result['answer'])
```

### Option 3: Using Agent Factory

```python
from agents import create_agent

# Create any agent by name
agent = create_agent('product_manager')
result = agent.process("Your question here")

# Or
agent = create_agent('system_design')
result = agent.process("Design Twitter")
```

### Option 4: List All Agents

```python
from agents import list_agents

# Get info about all agents
agents = list_agents()

for agent_info in agents:
    print(f"{agent_info['name']}:")
    print(f"  Type: {agent_info['type']}")
    print(f"  Capabilities: {agent_info['capabilities']}")
```

---

## 🎨 Customizing Agents

### Add a New Agent

1. **Create new file**: `agents/my_agent.py`

```python
from agents.base_agent import BaseAgent

MY_AGENT_PROMPT = """You are an expert in..."""

class MyAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(
            agent_type="my_agent",
            system_prompt=MY_AGENT_PROMPT,
            llm=llm
        )
    
    def get_capabilities(self):
        return {
            **super().get_capabilities(),
            "specializations": ["Spec 1", "Spec 2"],
            "best_for": ["Use case 1", "Use case 2"]
        }

def create_my_agent(llm=None):
    return MyAgent(llm)
```

2. **Register in** `agents/__init__.py`:

```python
from agents.my_agent import MyAgent, create_my_agent

AGENT_REGISTRY = {
    # ... existing agents
    'my_agent': MyAgent,
}
```

3. **Use in** `main_modular.py`:

```python
from agents import MyAgent

my_agent = MyAgent(llm=llm)
AGENTS['my_agent'] = my_agent
```

---

### Modify Existing Agent

Edit the agent's file directly:

```python
# agents/product_manager.py

PRODUCT_MANAGER_PROMPT = """
Your customized prompt here...
Add your specific requirements...
"""
```

---

## 💡 Advantages of Modular Architecture

### 1. **Separation of Concerns**
- Each agent has its own file
- Easy to locate and modify
- Clear responsibilities

### 2. **Maintainability**
- Changes to one agent don't affect others
- Easy to test individual agents
- Simpler debugging

### 3. **Scalability**
- Add new agents easily
- Remove unused agents
- Customize without touching core

### 4. **Team Collaboration**
- Different team members can work on different agents
- Clearer git history
- Reduced merge conflicts

### 5. **Reusability**
- Import agents in other projects
- Mix and match agents
- Create agent libraries

### 6. **Testing**
- Test agents independently
- Mock agent responses
- Unit test each agent

---

## 🧪 Testing Individual Agents

### Test Single Agent

```python
from agents import TechnicalAgent

# Create agent
agent = TechnicalAgent()

# Test question
result = agent.process("Explain binary search")

# Verify response
assert 'binary' in result['answer'].lower()
assert result['confidence'] > 0.7
print("✅ Test passed!")
```

### Test Supervisor Routing

```python
from agents import SupervisorAgent

supervisor = SupervisorAgent()

# Test routing
routing = supervisor.route_question("Design Twitter")
assert routing['selected_agent'] == 'system_design'

routing = supervisor.route_question("Explain quicksort")
assert routing['selected_agent'] == 'technical'

print("✅ Routing tests passed!")
```

---

## 📊 Comparison: Monolithic vs Modular

| Aspect | Monolithic (main.py) | Modular (main_modular.py) |
|--------|---------------------|---------------------------|
| **File Count** | 1 large file | 9 focused files |
| **Lines per File** | ~800 | ~150-300 |
| **Add New Agent** | Edit main file | Create new file |
| **Modify Agent** | Find in 800 lines | Edit specific file |
| **Testing** | Test entire system | Test individual agents |
| **Collaboration** | Git conflicts | Clean separation |
| **Reusability** | Hard to reuse | Easy to import |
| **Maintainability** | Harder | Easier |

---

## 🔄 Migration Guide

### From Monolithic to Modular

```python
# Old way (main.py)
# All prompts and logic in one file

# New way (main_modular.py + agents/)
from agents import ProductManagerAgent, TechnicalAgent

pm_agent = ProductManagerAgent()
tech_agent = TechnicalAgent()
```

Both versions produce the same results, just organized differently!

---

## 🎯 Best Practices

### 1. **Keep Agents Focused**
Each agent should have a single, clear responsibility.

### 2. **Use Base Class**
Extend `BaseAgent` for consistency.

### 3. **Document Prompts**
Add comments explaining your prompt design.

### 4. **Version Prompts**
Track changes to agent prompts over time.

### 5. **Test Independently**
Write tests for each agent.

### 6. **Monitor Performance**
Track which agents are used most.

---

## 📈 Performance

Same performance as monolithic version:
- **Routing**: ~2-3 seconds
- **Answer**: ~10-30 seconds
- **Total**: ~15-35 seconds per question

No performance overhead from modularization!

---

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY agents/ agents/
COPY main_modular.py .
EXPOSE 8000
CMD ["uvicorn", "main_modular:app", "--host", "0.0.0.0"]
```

### Run

```bash
docker build -t interview-api-modular .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY interview-api-modular
```

---

## ✅ Advantages Summary

**Use Modular Version When:**
- ✅ Building a team project
- ✅ Need to customize agents frequently
- ✅ Want clean code organization
- ✅ Planning to add many agents
- ✅ Need to reuse agents elsewhere

**Use Monolithic Version When:**
- Single developer
- Quick prototype
- Simple deployment
- No customization needed

---

## 📚 Additional Resources

- **Base Agent**: See `agents/base_agent.py`
- **Example Agent**: See `agents/product_manager.py`
- **Supervisor Logic**: See `agents/supervisor.py`
- **Main API**: See `main_modular.py`

---

**Built with**: Clean Architecture • LangGraph • FastAPI • OpenAI

**Version**: 3.0.0 (Modular)

**Status**: ✅ Production-Ready

**Happy Coding!** 🚀

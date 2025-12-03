"""
Interview Agents Package
Specialized agents for different interview domains

Usage:
    from agents import (
        ProductManagerAgent,
        TechnicalAgent,
        ArchitectAgent,
        CodingAgent,
        BehavioralAgent,
        SystemDesignAgent,
        SupervisorAgent
    )
"""

from agents.base_agent import BaseAgent
from agents.product_manager import ProductManagerAgent, create_product_manager_agent
from agents.technical import TechnicalAgent, create_technical_agent
from agents.architect import ArchitectAgent, create_architect_agent
from agents.coding import CodingAgent, create_coding_agent
from agents.behavioral import BehavioralAgent, create_behavioral_agent
from agents.system_design import SystemDesignAgent, create_system_design_agent
from agents.supervisor import SupervisorAgent, create_supervisor_agent


__all__ = [
    'BaseAgent',
    'ProductManagerAgent',
    'TechnicalAgent',
    'ArchitectAgent',
    'CodingAgent',
    'BehavioralAgent',
    'SystemDesignAgent',
    'SupervisorAgent',
    'create_product_manager_agent',
    'create_technical_agent',
    'create_architect_agent',
    'create_coding_agent',
    'create_behavioral_agent',
    'create_system_design_agent',
    'create_supervisor_agent',
]


# Agent registry for easy access
AGENT_REGISTRY = {
    'product_manager': ProductManagerAgent,
    'technical': TechnicalAgent,
    'architect': ArchitectAgent,
    'coding': CodingAgent,
    'behavioral': BehavioralAgent,
    'system_design': SystemDesignAgent,
    'supervisor': SupervisorAgent,
}


def create_agent(agent_type: str, llm=None):
    """
    Factory function to create any agent by type
    
    Args:
        agent_type: One of: product_manager, technical, architect, 
                    coding, behavioral, system_design, supervisor
        llm: Optional LangChain LLM instance
        
    Returns:
        Agent instance
        
    Example:
        >>> agent = create_agent('product_manager')
        >>> result = agent.process("How would you prioritize features?")
    """
    agent_class = AGENT_REGISTRY.get(agent_type)
    if not agent_class:
        raise ValueError(f"Unknown agent type: {agent_type}. "
                        f"Available: {list(AGENT_REGISTRY.keys())}")
    
    return agent_class(llm=llm)


def list_agents():
    """List all available agents with their capabilities"""
    agents_info = []
    
    for agent_type, agent_class in AGENT_REGISTRY.items():
        if agent_type == 'supervisor':
            continue  # Skip supervisor in listing
        
        agent = agent_class()
        capabilities = agent.get_capabilities()
        
        agents_info.append({
            'type': agent_type,
            'name': agent_class.__name__,
            'capabilities': capabilities
        })
    
    return agents_info

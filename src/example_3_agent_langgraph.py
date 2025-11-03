"""
Example 3: Simple Agent with LangGraph

This example demonstrates:
- Creating a state graph with multiple agent nodes
- Implementing conditional routing between agents
- Building a hierarchical agent system with:
  * Orchestrator: Decides which agent to use
  * Analyzer: Analyzes technical questions
  * Responder: Provides final responses

This is the foundation for building complex multi-agent systems.
"""

from typing import TypedDict, Literal
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph, END


# Define the shared state that flows through the graph
class AgentState(TypedDict):
    """
    The state object that gets passed between nodes.
    Each node can read from and write to this state.
    """
    user_query: str  # The original user question
    query_type: str  # Classification: 'technical', 'general', or 'greeting'
    analysis: str  # Analysis from the analyzer agent
    final_response: str  # The final response to return
    next_step: str  # Controls routing to the next node


# Initialize the Ollama model
# Using llama3 as it's fast and good for demos
llm = ChatOllama(model="llama3", temperature=0.7)


def orchestrator_node(state: AgentState) -> AgentState:
    """
    Agent 1: Orchestrator
    Analyzes the user query and decides which path to take.
    """
    print("=" * 60)
    print("🧠 ORCHESTRATOR: Analyzing query type...")
    print("=" * 60)

    query = state["user_query"]
    print(f"Query: {query}\n")

    # Use the LLM to classify the query type
    classification_prompt = f"""Classify this user query into one of these categories:
- 'technical' if it's about programming, code, or technical concepts
- 'greeting' if it's a greeting or casual conversation
- 'general' for everything else

Query: {query}

Respond with ONLY ONE WORD: technical, greeting, or general"""

    response = llm.invoke(classification_prompt)
    query_type = response.content.strip().lower()

    # Ensure valid classification
    if query_type not in ['technical', 'greeting', 'general']:
        query_type = 'general'

    print(f"📋 Classification: {query_type}")

    # Determine next step based on classification
    if query_type == 'technical':
        next_step = 'analyzer'
        print("➡️  Routing to: ANALYZER")
    else:
        next_step = 'responder'
        print("➡️  Routing to: RESPONDER")

    print()

    return {
        **state,
        "query_type": query_type,
        "next_step": next_step
    }


def analyzer_node(state: AgentState) -> AgentState:
    """
    Agent 2: Analyzer
    Performs deep analysis on technical queries.
    """
    print("=" * 60)
    print("🔍 ANALYZER: Analyzing technical query...")
    print("=" * 60)

    query = state["user_query"]

    # Perform technical analysis
    analysis_prompt = f"""You are a technical analyst. Analyze this query and provide:
1. Key concepts involved
2. Difficulty level (beginner/intermediate/advanced)
3. A brief technical breakdown

Query: {query}

Keep your analysis concise (2-3 sentences)."""

    response = llm.invoke(analysis_prompt)
    analysis = response.content.strip()

    print(f"Analysis:\n{analysis}\n")
    print("➡️  Routing to: RESPONDER\n")

    return {
        **state,
        "analysis": analysis,
        "next_step": "responder"
    }


def responder_node(state: AgentState) -> AgentState:
    """
    Agent 3: Responder
    Generates the final response to the user.
    """
    print("=" * 60)
    print("✍️  RESPONDER: Generating final response...")
    print("=" * 60)

    query = state["user_query"]
    query_type = state.get("query_type", "general")
    analysis = state.get("analysis", "")

    # Build the response prompt based on available context
    if analysis:
        response_prompt = f"""Based on this analysis:
{analysis}

Provide a clear, helpful response to the user's query: {query}

Keep your response concise and practical."""
    else:
        response_prompt = f"""Provide a helpful response to this query: {query}

Keep your response friendly and concise."""

    response = llm.invoke(response_prompt)
    final_response = response.content.strip()

    print(f"Response:\n{final_response}\n")
    print("✅ Complete!\n")

    return {
        **state,
        "final_response": final_response,
        "next_step": "end"
    }


def route_after_orchestrator(state: AgentState) -> Literal["analyzer", "responder"]:
    """
    Routing function that determines the next node after orchestrator.
    """
    return state["next_step"]


def create_agent_graph() -> StateGraph:
    """
    Build and compile the agent graph.
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(AgentState)

    # Add nodes (agents)
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("responder", responder_node)

    # Set entry point
    workflow.set_entry_point("orchestrator")

    # Add conditional routing from orchestrator
    workflow.add_conditional_edges(
        "orchestrator",
        route_after_orchestrator,
        {
            "analyzer": "analyzer",
            "responder": "responder"
        }
    )

    # Analyzer always goes to responder
    workflow.add_edge("analyzer", "responder")

    # Responder is the end
    workflow.add_edge("responder", END)

    # Compile the graph
    return workflow.compile()


def run_query(graph, query: str) -> dict:
    """
    Run a query through the agent graph.
    """
    print("\n" + "🚀 " * 20)
    print(f"PROCESSING QUERY: {query}")
    print("🚀 " * 20 + "\n")

    initial_state = {
        "user_query": query,
        "query_type": "",
        "analysis": "",
        "final_response": "",
        "next_step": ""
    }

    # Execute the graph
    result = graph.invoke(initial_state)

    return result


def main():
    """
    Demonstrate the agent graph with different query types.
    """
    print("\n" + "=" * 60)
    print("Example 3: Simple Agent with LangGraph")
    print("=" * 60)

    # Create the agent graph
    print("\n🏗️  Building agent graph...")
    agent_graph = create_agent_graph()
    print("✅ Graph built successfully!\n")

    # Test Query 1: Technical question (should go through analyzer)
    result1 = run_query(
        agent_graph,
        "What is a Python decorator and how does it work?"
    )
    print(f"📤 FINAL OUTPUT:\n{result1['final_response']}\n")

    # Test Query 2: Greeting (should skip analyzer)
    result2 = run_query(
        agent_graph,
        "Hello! How are you today?"
    )
    print(f"📤 FINAL OUTPUT:\n{result2['final_response']}\n")

    # Test Query 3: Another technical question
    result3 = run_query(
        agent_graph,
        "Explain async/await in Python"
    )
    print(f"📤 FINAL OUTPUT:\n{result3['final_response']}\n")

    print("=" * 60)
    print("Example 3 complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Explaining the Code: Multi-Agent System with LangGraph

This code demonstrates the creation of a **hierarchical system of 3 agents** that collaborate to answer user questions.

## 🎯 Main Concept

The system intelligently routes queries between different specialized agents based on the type of question asked.

## 📊 State Structure (`AgentState`)

```python
class AgentState(TypedDict):
```

This is the **shared object** that flows between all agents. It contains:
- `user_query`: The original question
- `query_type`: The type of question (technical, general, greeting)
- `analysis`: Technical analysis (if applicable)
- `final_response`: The final answer
- `next_step`: Determines which agent comes next

## 🤖 The Three Agents

### 1️⃣ **Orchestrator (Conductor)**
```python
def orchestrator_node(state: AgentState)
```
**Role**: Classify the question and decide routing
- Uses the LLM to classify as: `technical`, `greeting`, or `general`
- If technical → routes to the **Analyzer**
- Otherwise → routes directly to the **Responder**

### 2️⃣ **Analyzer (Technical Analyst)**
```python
def analyzer_node(state: AgentState)
```
**Role**: Deeply analyze technical questions
- Identifies key concepts
- Determines difficulty level
- Produces an analysis that will be used by the Responder

### 3️⃣ **Responder (Response Generator)**
```python
def responder_node(state: AgentState)
```
**Role**: Generate the final response
- Uses technical analysis if available
- Adapts its response based on context
- Produces the definitive answer for the user

## 🔀 Data Flow

```
User Question
      ↓
🧠 ORCHESTRATOR (Classifies)
      ↓
     / \
    /   \
Technical? No
   ↓      ↓
🔍 ANALYZER → ✍️ RESPONDER
              ↓
         Final Response
```

**Technical flow example**:
1. "What is a Python decorator?" → Orchestrator
2. Classified as "technical" → Analyzer
3. Concept analysis → Responder
4. Response enriched by the analysis

**Simple flow example**:
1. "Hello!" → Orchestrator
2. Classified as "greeting" → Responder (directly)
3. Friendly response

## 🛠️ Graph Construction

```python
def create_agent_graph()
```

This function **builds the graph**:
- Adds the 3 nodes (agents)
- Defines the Orchestrator as entry point
- Configures conditional routing
- Connects Analyzer → Responder → END

## 💡 Key Points

✅ **Modularity**: Each agent has a unique responsibility  
✅ **Intelligent routing**: Simple questions avoid unnecessary analysis  
✅ **Shared state**: All agents read/write to the same object  
✅ **Scalable**: Easy to add new agents or question types  

## 🎬 Execution

The `main()` function tests the system with 3 different types of queries to demonstrate the different possible paths through the graph.

This pattern is the **foundation for building complex multi-agent systems** with specializations and sophisticated workflows!
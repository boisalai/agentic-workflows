# Agentic Workflows

Learning project for building agent-based workflows using LangGraph and Ollama.

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [https://ollama.ai](https://ollama.ai)

### 2. Pull a Model

After installing Ollama, pull the `llama3` model:

```bash
ollama pull llama3
```

### 3. Verify Ollama is Running

Make sure Ollama is running in the background:

```bash
ollama list
```

You should see `llama3` in the list of available models.

## Setup

This project uses `uv` for dependency management.

### 1. Install Dependencies

```bash
uv sync
```

### 2. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

## Examples

The project includes 3 progressive examples to learn agent workflows:

### Example 1: Simple Chat (`src/example_1_simple_chat.py`)

**Concepts**: Basic LLM interaction, single prompt/response

The simplest example showing how to:
- Connect to Ollama
- Send a prompt
- Receive a response

**Run it:**
```bash
uv run src/example_1_simple_chat.py
```

**What you'll learn:**
- Basic Ollama API usage
- Sending prompts and receiving responses
- Different types of queries (questions, code generation, creative tasks)

---

### Example 2: Multi-turn Conversation (`src/example_2_conversation.py`)

**Concepts**: Conversation history, context management, system prompts

A more advanced example showing:
- Maintaining conversation history across multiple turns
- Using system prompts to set agent behavior
- Building context so the model remembers previous exchanges

**Run it:**
```bash
uv run src/example_2_conversation.py
```

**What you'll learn:**
- How to maintain conversation context
- The importance of message history
- Using system prompts to define agent personality
- Building natural conversational flows

---

### Example 3: Agent with LangGraph (`src/example_3_agent_langgraph.py`)

**Concepts**: State graphs, agent orchestration, conditional routing, multi-agent systems

A complete agent system with:
- **Orchestrator Agent**: Classifies queries and routes to appropriate agents
- **Analyzer Agent**: Performs deep analysis on technical queries
- **Responder Agent**: Generates final responses

**Run it:**
```bash
uv run src/example_3_agent_langgraph.py
```

**What you'll learn:**
- Building state graphs with LangGraph
- Creating multiple specialized agents
- Implementing conditional routing between agents
- Managing shared state across agents
- Designing hierarchical agent architectures

**Architecture:**
```
User Query ’ Orchestrator ’ [Technical?] ’ Analyzer ’ Responder ’ Final Response
                          ˜ [Other]    ˜ Responder ’ Final Response
```

## Learning Path

It's recommended to go through the examples in order:

1. Start with **Example 1** to understand basic LLM interaction
2. Move to **Example 2** to learn about conversation management
3. Finally, tackle **Example 3** to understand multi-agent systems with LangGraph

## Next Steps

After completing these examples, you can:

1. **Experiment with different models**: Try other Ollama models like `mistral`, `codellama`, or `phi3`
2. **Add more agents**: Extend Example 3 with specialized agents (e.g., code reviewer, data analyzer)
3. **Implement RAG**: Add a vector database (ChromaDB/Qdrant) for long-term memory
4. **Add event triggers**: Integrate webhooks, file watchers, or APIs to trigger workflows automatically
5. **Mix local and cloud models**: Use Ollama for fast/cheap operations and Claude API for complex reasoning

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Python Library](https://github.com/ollama/ollama-python)

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Language | Python 3.12+ | Primary development language |
| Package Manager | uv | Fast Python package management |
| Orchestration | LangGraph | Agent workflow orchestration |
| Local LLM | Ollama | Fast, local model execution |
| Model | Llama 3 | Lightweight, capable language model |

## Troubleshooting

### Ollama connection errors

If you get connection errors:
1. Make sure Ollama is running: `ollama list`
2. Check if the model is downloaded: `ollama pull llama3`
3. Try running a simple test: `ollama run llama3 "Hello"`

### Slow responses

If responses are slow:
1. Check your system resources (CPU/Memory)
2. Try a smaller model: `ollama pull phi3`
3. Close other resource-intensive applications

### Import errors

If you get import errors:
1. Make sure you've run `uv sync`
2. Activate the virtual environment: `source .venv/bin/activate`
3. Check Python version: `python --version` (should be 3.12+)

"""
Example 1: Simple Chat with Ollama

This is the most basic example showing how to:
- Connect to a local Ollama instance
- Send a single prompt
- Receive and display a response

Prerequisites:
- Ollama must be installed and running (https://ollama.ai)
- A model must be downloaded (e.g., 'ollama pull llama3')
"""

import ollama


def simple_chat(prompt: str, model: str = "llama3") -> str:
    """
    Send a single prompt to Ollama and get a response.

    Args:
        prompt: The question or instruction to send to the model
        model: The Ollama model to use (default: llama3)

    Returns:
        The model's response as a string
    """
    print(f"\n🤖 Using model: {model}")
    print(f"📝 Prompt: {prompt}\n")

    # Send the prompt to Ollama
    response = ollama.chat(
        model=model,
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    # Extract the response text
    answer = response['message']['content']

    print(f"💬 Response:\n{answer}\n")

    return answer


def main():
    """
    Run a few example prompts to demonstrate basic functionality.
    """
    print("=" * 60)
    print("Example 1: Simple Chat with Ollama")
    print("=" * 60)

    # Example 1: Simple question
    simple_chat(
        prompt="What is Python? Answer in one sentence.",
        model="llama3"
    )

    # Example 2: Code generation
    simple_chat(
        prompt="Write a Python function that calculates the factorial of a number.",
        model="llama3"
    )

    # Example 3: Creative task
    simple_chat(
        prompt="Give me 3 tips for learning AI programming.",
        model="llama3"
    )

    print("=" * 60)
    print("Example 1 complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

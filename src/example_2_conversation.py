"""
Example 2: Multi-turn Conversation with Memory

This example demonstrates:
- Maintaining conversation history across multiple turns
- Building context so the model remembers previous exchanges
- Creating a more natural conversational flow

This is essential for building chatbots and interactive agents.
"""

import ollama
from typing import List, Dict


class ConversationManager:
    """
    Manages a conversation with memory/history.
    """

    def __init__(self, model: str = "llama3", system_prompt: str = None):
        """
        Initialize the conversation manager.

        Args:
            model: The Ollama model to use
            system_prompt: Optional system message to set behavior/context
        """
        self.model = model
        self.messages: List[Dict[str, str]] = []

        # Add system prompt if provided
        if system_prompt:
            self.messages.append({
                'role': 'system',
                'content': system_prompt
            })

        print(f"🤖 Conversation started with model: {model}")
        if system_prompt:
            print(f"📋 System prompt: {system_prompt}\n")

    def send_message(self, user_message: str) -> str:
        """
        Send a message and get a response, maintaining history.

        Args:
            user_message: The user's message

        Returns:
            The model's response
        """
        print(f"👤 User: {user_message}")

        # Add user message to history
        self.messages.append({
            'role': 'user',
            'content': user_message
        })

        # Get response from Ollama
        response = ollama.chat(
            model=self.model,
            messages=self.messages
        )

        # Extract assistant's response
        assistant_message = response['message']['content']

        # Add assistant response to history
        self.messages.append({
            'role': 'assistant',
            'content': assistant_message
        })

        print(f"🤖 Assistant: {assistant_message}\n")

        return assistant_message

    def get_history_length(self) -> int:
        """Return the number of messages in the conversation history."""
        return len(self.messages)

    def clear_history(self):
        """Clear the conversation history (except system prompt if present)."""
        system_messages = [msg for msg in self.messages if msg['role'] == 'system']
        self.messages = system_messages
        print("🗑️  Conversation history cleared.\n")


def main():
    """
    Demonstrate a multi-turn conversation.
    """
    print("=" * 60)
    print("Example 2: Multi-turn Conversation with Memory")
    print("=" * 60)
    print()

    # Create a conversation manager with a system prompt
    conversation = ConversationManager(
        model="llama3",
        system_prompt="You are a helpful Python programming tutor. Keep your answers concise and practical."
    )

    # Turn 1: Ask about a concept
    conversation.send_message("What is a Python decorator?")

    # Turn 2: Follow-up question (requires context from previous turn)
    conversation.send_message("Can you show me a simple example of one?")

    # Turn 3: Another follow-up (builds on previous context)
    conversation.send_message("What's a practical use case for decorators?")

    # Show conversation statistics
    print("=" * 60)
    print(f"📊 Conversation statistics:")
    print(f"   Total messages in history: {conversation.get_history_length()}")
    print("=" * 60)

    print("\n" + "=" * 60)
    print("Example 2: Now demonstrating a different conversation")
    print("=" * 60)
    print()

    # Start a new conversation with a different personality
    creative_bot = ConversationManager(
        model="llama3",
        system_prompt="You are a creative storyteller. Tell engaging short stories."
    )

    creative_bot.send_message("Tell me a one-paragraph story about a robot learning to code.")
    creative_bot.send_message("What happened to the robot next?")

    print("=" * 60)
    print("Example 2 complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

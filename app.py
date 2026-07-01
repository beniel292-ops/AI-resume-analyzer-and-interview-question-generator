import sys
from src.rag.pipeline import ask_rag_assistant
from src.memory.conversation import ConversationMemory

def main():
    print("========================================")
    print("Welcome to your Personal AI Assistant!")
    print("Type 'exit' or 'quit' to end the session.")
    print("========================================\n")
    
    memory = ConversationMemory(max_turns=3)
    
    while True:
        try:
            query = input("\nYou: ")
            if query.lower().strip() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not query.strip():
                continue
                
            history_str = memory.get_history_string()
            
            # Run the pipeline
            answer = ask_rag_assistant(query, chat_history=history_str)
            
            print(f"\nAssistant: {answer}")
            
            # Save to memory
            memory.add_turn(query, answer)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()

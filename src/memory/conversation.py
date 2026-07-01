class ConversationMemory:
    """Stores the last N turns of chat history to provide conversation context to the LLM."""
    def __init__(self, max_turns: int = 5):
        self.history = []
        self.max_turns = max_turns
        
    def add_turn(self, user_msg: str, ai_msg: str):
        self.history.append({"user": user_msg, "ai": ai_msg})
        if len(self.history) > self.max_turns:
            self.history.pop(0)
            
    def get_history_string(self) -> str:
        if not self.history:
            return ""
        
        history_str = ""
        for turn in self.history:
            history_str += f"User: {turn['user']}\n"
            history_str += f"Assistant: {turn['ai']}\n\n"
        return history_str.strip()

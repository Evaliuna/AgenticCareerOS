from src.tools.memory_tool import MemoryTool

class MemoryAgent:
    """
    Agent 5: Memory Agent
    Governs state persistence, interfacing with the JSON-backed Memory MCP tool.
    Does not require expensive LLM tokens simply to save structure.
    """
    def __init__(self):
        self.tool = MemoryTool()
        self.user_id = "capstone_user_001" # Single user scope for simplicity
        
    def save_state(self, state_dict: dict):
        return self.tool.execute(user_id=self.user_id, operation="save", data=state_dict)
        
    def load_state(self):
        result = self.tool.execute(user_id=self.user_id, operation="load")
        return result.get("data", {})
        
    def clear_state(self):
        return self.tool.execute(user_id=self.user_id, operation="clear")

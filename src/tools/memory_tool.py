import json
import os
from typing import Dict, Any

from .mcp_base import MCPTool

class MemoryTool(MCPTool):
    def __init__(self):
        schema = {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Identifier for the user session"
                },
                "operation": {
                    "type": "string",
                    "enum": ["save", "load", "clear"],
                    "description": "The memory operation to perform"
                },
                "data": {
                    "type": "object",
                    "description": "Data to save (only needed for 'save' operation)"
                }
            },
            "required": ["user_id", "operation"]
        }
        super().__init__(
            name="manage_memory",
            description="Persistently stores or retrieves user state and progress.",
            schema=schema
        )
        self.storage_file = "career_memory.json"
        # Initialize storage if missing
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, "w") as f:
                json.dump({}, f)

    def execute(self, user_id: str, operation: str, data: Dict = None) -> Dict[str, Any]:
        """
        Executes real persistence ops using a local JSON JSON-RPC analog state file.
        """
        with open(self.storage_file, "r") as f:
            memory = json.load(f)
            
        if operation == "save":
            if user_id not in memory:
                memory[user_id] = {}
            if data:
                memory[user_id].update(data)
            with open(self.storage_file, "w") as f:
                json.dump(memory, f, indent=2)
            return {"status": "success", "message": "Memory correctly saved via tool."}
            
        elif operation == "load":
            return {"status": "success", "data": memory.get(user_id, {})}
            
        elif operation == "clear":
            memory.pop(user_id, None)
            with open(self.storage_file, "w") as f:
                json.dump(memory, f, indent=2)
            return {"status": "success", "message": "Memory successfully cleared."}
            
        return {"status": "error", "message": "Invalid operation invoked."}

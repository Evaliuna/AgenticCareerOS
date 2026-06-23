import json
from typing import Dict, Any

class MCPTool:
    """
    Base Model Context Protocol (MCP) tool implementation.
    Standardizes tool discovery, schema definition, and execution for the agent system.
    """
    def __init__(self, name: str, description: str, schema: dict):
        self.name = name
        self.description = description
        self.schema = schema

    def get_declaration(self) -> Dict[str, Any]:
        """Returns the MCP-compatible tool declaration format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.schema,
        }

    def execute(self, **kwargs) -> Any:
        """Executes the tool logic. Must be overridden by subclasses."""
        raise NotImplementedError("Tool execution logic must be implemented.")

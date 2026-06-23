from typing import List, Dict, Any
from .mcp_base import MCPTool

class ProjectTool(MCPTool):
    def __init__(self):
        schema = {
            "type": "object",
            "properties": {
                "project_title": {
                    "type": "string",
                    "description": "Catchy title for the portfolio project."
                },
                "tech_stack": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific technologies to be used in this project."
                },
                "description": {
                    "type": "string",
                    "description": "A 2-3 sentence overview of what the user will build."
                },
                "difficulty_level": {
                    "type": "string",
                    "enum": ["Beginner", "Intermediate", "Advanced"]
                }
            },
            "required": ["project_title", "tech_stack", "description", "difficulty_level"]
        }
        super().__init__(
            name="recommend_portfolio_project",
            description="Generates a structured portfolio project specification tailored to missing skills.",
            schema=schema
        )

    def execute(self, project_title: str, tech_stack: List[str], description: str, difficulty_level: str) -> Dict[str, Any]:
        """
        Structures the project recommendation.
        """
        return {
            "title": project_title,
            "stack": tech_stack,
            "description": description,
            "difficulty": difficulty_level,
            "status": "ready_for_portfolio"
        }

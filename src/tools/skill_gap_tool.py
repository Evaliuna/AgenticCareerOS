from typing import List, Dict, Any
from .mcp_base import MCPTool

class SkillGapTool(MCPTool):
    def __init__(self):
        schema = {
            "type": "object",
            "properties": {
                "current_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of the user's current skills"
                },
                "required_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of industry standard skills required for the target role"
                }
            },
            "required": ["current_skills", "required_skills"]
        }
        super().__init__(
            name="calculate_skill_gap",
            description="Compares current skills against required skills to definitively identify gaps.",
            schema=schema
        )

    def execute(self, current_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """
        Performs exact set logic to extract missing skills.
        """
        current_set = set([str(s).lower().strip() for s in current_skills])
        required_set = set([str(s).lower().strip() for s in required_skills])
        
        missing_skills = list(required_set - current_set)
        overlapping_skills = list(required_set & current_set)
        
        gap_ratio = len(missing_skills) / len(required_set) if required_set else 0.0
        
        return {
            "missing_skills": missing_skills,
            "existing_relevant_skills": overlapping_skills,
            "gap_percentage": round(gap_ratio * 100, 2),
            "is_ready_for_role": gap_ratio <= 0.2 # Arbitrary threshold for demonstration
        }

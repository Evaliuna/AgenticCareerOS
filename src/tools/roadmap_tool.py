from typing import List, Dict, Any
from .mcp_base import MCPTool

class RoadmapGenerationTool(MCPTool):
    def __init__(self):
        schema = {
            "type": "object",
            "properties": {
                "missing_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Skills the user needs to learn"
                },
                "time_frame_weeks": {
                    "type": "integer",
                    "description": "Number of weeks available to learn (default 4)"
                }
            },
            "required": ["missing_skills"]
        }
        super().__init__(
            name="generate_roadmap_structure",
            description="Creates a skeleton weekly roadmap structure to distribute skills over time.",
            schema=schema
        )

    def execute(self, missing_skills: List[str], time_frame_weeks: int = 4) -> Dict[str, Any]:
        """
        Distributes missing skills across the specified timeframe intelligently.
        """
        weeks = {f"Week_{i+1}": [] for i in range(max(1, time_frame_weeks))}
        
        # Simple logical distribution of skills over weeks
        for i, skill in enumerate(missing_skills):
            week_idx = i % max(1, time_frame_weeks)
            weeks[f"Week_{week_idx+1}"].append(str(skill).title())
            
        return {
            "roadmap_duration_weeks": time_frame_weeks,
            "weekly_schedule": weeks,
            "status": "baseline_schedule_created"
        }

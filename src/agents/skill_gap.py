from google import genai
from google.genai import types
from src.tools.skill_gap_tool import SkillGapTool
from src.agents.api_utils import generate_content_with_retry
import os

class SkillGapAgent:
    """
    Agent 2: Skill Gap Agent
    Compares the current skill profile to current industry requirements 
    to pinpoint exactly what the user is missing for their target role.
    """
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))
        self.tool = SkillGapTool()
        
    def identify_gaps(self, current_skills: list, target_role: str) -> dict:
        """
        Leverages Gemini's internal knowledge to determine what standard skills are needed for the 
        target_role, then calculates the gap strictly through the Gap Tool.
        """
        prompt = (
            f"You are a Senior Tech Industry Skill Assessor.\\n"
            f"User's current competencies: {current_skills}\\n"
            f"Target Role: {target_role}\\n\\n"
            f"Step 1. Identify 5-8 typical industry-standard skills absolutely required for this target role.\\n"
            f"Step 2. Use the `calculate_skill_gap` tool to compute the missing skills. "
            f"Pass the user's current skills and the required skills you just generated as arguments."
        )
        
        gemini_tool = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name=self.tool.name,
                    description=self.tool.description,
                    parameters=self.tool.schema
                )
            ]
        )
        
        try:
            response = generate_content_with_retry(
                client=self.client,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[gemini_tool],
                    tool_config=types.ToolConfig(
                        function_calling_config=types.FunctionCallingConfig(
                            mode="ANY",
                            allowed_function_names=[self.tool.name]
                        )
                    ),
                    temperature=0.3, # Slight variance to generate diverse required industry skills
                )
            )
            
            if response.function_calls:
                for fn_call in response.function_calls:
                    if fn_call.name == self.tool.name:
                        args = fn_call.args
                        c_skills = args.get("current_skills", [])
                        r_skills = args.get("required_skills", [])
                        
                        # Compute logic purely using the deterministic MCP tool block
                        gap_analysis = self.tool.execute(current_skills=c_skills, required_skills=r_skills)
                        
                        return {
                            "industry_required_skills": r_skills,
                            "gap_analysis": gap_analysis
                        }
                        
            return {
                "error": "Failed to invoke gap calculation tool.",
                "raw_text": response.text
            }
        except Exception as e:
            return {
                "error": f"Agent failed due to API error: {str(e)}",
            }

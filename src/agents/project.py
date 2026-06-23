from google import genai
from google.genai import types
from src.tools.project_tool import ProjectTool
import os

class ProjectRecommendationAgent:
    """
    Agent: Project Recommendation Agent
    Generates a tailored portfolio project based on skill gaps.
    """
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))
        self.tool = ProjectTool()
        
    def recommend(self, missing_skills: list, role: str) -> dict:
        prompt = (
            f"You are a Senior Engineering Manager.\\n"
            f"Target role: {role}\\n"
            f"Skills the user needs to learn: {missing_skills}\\n\\n"
            f"Design a practical portfolio project that uses these missing skills. "
            f"Use the `recommend_portfolio_project` tool to structure your recommendation."
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
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[gemini_tool],
                    tool_config=types.ToolConfig(
                        function_calling_config=types.FunctionCallingConfig(
                            mode="ANY",
                            allowed_function_names=[self.tool.name]
                        )
                    ),
                    temperature=0.4,
                )
            )
            
            if response.function_calls:
                for fn_call in response.function_calls:
                    if fn_call.name == self.tool.name:
                        return self.tool.execute(**fn_call.args)
                        
        except Exception as e:
            return {"error": str(e)}

        return {
            "error": "Failed to generate project specification."
        }

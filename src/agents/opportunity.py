from google import genai
from google.genai import types
from src.tools.opportunity_tool import OpportunityTool
import os

class OpportunityAgent:
    """
    Agent 4: Opportunity Discovery Agent
    Aligns gap skills with practical hackathons, competitions, or open source.
    """
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))
        self.tool = OpportunityTool()
        
    def discover(self, missing_skills: list, role: str) -> dict:
        prompt = (
            f"You are a Tech Career Scout.\\n"
            f"Target role: {role}\\n"
            f"Skills to practice: {missing_skills}\\n\\n"
            f"Construct a GitHub search query to find open issues where the user can practice these skills. "
            f"Usually formatting like 'label:\"good first issue\" language:python' works well. "
            f"Use the `discover_live_opportunities` tool to perform the search."
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
                    temperature=0.2,
                )
            )
            
            if response.function_calls:
                for fn_call in response.function_calls:
                    if fn_call.name == self.tool.name:
                        return self.tool.execute(**fn_call.args)
        except Exception as e:
            return {"error": str(e)}
                    
        return {
            "error": "Failed to discover opportunities via agent mapping.",
        }

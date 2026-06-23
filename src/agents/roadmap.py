from google import genai
from google.genai import types
from src.tools.roadmap_tool import RoadmapGenerationTool
import os

class LearningRoadmapAgent:
    """
    Agent 3: Learning Roadmap Agent
    Turns missing skills into a scheduled matrix.
    """
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))
        self.tool = RoadmapGenerationTool()
        
    def generate_roadmap(self, missing_skills: list, time_frame_weeks: int = 4) -> dict:
        prompt = (
            f"You are an Expert Technical Curriculum Designer.\\n"
            f"The user needs to learn these skills: {missing_skills}\\n"
            f"Available time: {time_frame_weeks} weeks.\\n\\n"
            f"Use the `generate_roadmap_structure` tool to organize a timeline."
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
                    temperature=0.2, # Stable generation
                )
            )
            
            if response.function_calls:
                for fn_call in response.function_calls:
                    if fn_call.name == self.tool.name:
                        args = fn_call.args
                        ms = args.get("missing_skills", missing_skills)
                        tf = int(args.get("time_frame_weeks", time_frame_weeks))
                        return self.tool.execute(missing_skills=ms, time_frame_weeks=tf)
        except Exception as e:
            return {"error": str(e)}

        return {
            "error": "Failed to map roadmap via tool extraction."
        }

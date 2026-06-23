from google import genai
from google.genai import types
from pydantic import BaseModel
import os

class OpportunityItem(BaseModel):
    name: str
    url: str
    type: str  # e.g., 'Kaggle Competition', 'Devpost Hackathon', 'Google Program', 'Open Source', 'Internship'
    labels: list[str]

class OpportunityResponse(BaseModel):
    opportunities_found: list[OpportunityItem]

class OpportunityAgent:
    """
    Agent 4: Opportunity Discovery Agent
    Aligns gap skills with practical hackathons, competitions, Google programs, or open source.
    """
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key or os.environ.get("GEMINI_API_KEY"))
        
    def discover(self, missing_skills: list, role: str) -> dict:
        prompt = (
            f"You are a Tech Career Scout.\\n"
            f"Target role: {role}\\n"
            f"Skills to practice: {missing_skills}\\n\\n"
            f"Find 5-7 HIGH-QUALITY real-world or highly realistic opportunities for someone trying to learn these exact skills.\\n"
            f"MUST include a variety from:\\n"
            f"- Kaggle competitions\\n"
            f"- Devpost hackathons\\n"
            f"- Google programs (e.g., GSoC, Google Cloud Skills Boost)\\n"
            f"- GitHub issues / Open source\\n"
            f"- Internships or Fellowships\\n"
            f"Provide a realistic URL for each, e.g., https://kaggle.com/competitions/... or https://devpost.com/...\\n"
        )
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=OpportunityResponse,
                    temperature=0.4,
                )
            )
            
            # The response is validated against the schema and returned as JSON text
            import json
            data = json.loads(response.text)
            return data
        except Exception as e:
            return {"error": str(e)}


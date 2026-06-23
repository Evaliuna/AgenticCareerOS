import requests
from typing import List, Dict, Any
from .mcp_base import MCPTool

class OpportunityTool(MCPTool):
    def __init__(self):
        schema = {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "GitHub issue search query based on missing skills (e.g., 'machine learning label:\"good first issue\"')."
                }
            },
            "required": ["search_query"]
        }
        super().__init__(
            name="discover_live_opportunities",
            description="Searches GitHub's live API for open source issues matching the user's skill gaps.",
            schema=schema
        )

    def execute(self, search_query: str) -> Dict[str, Any]:
        """
        Uses the real GitHub REST API to find live open-source opportunities.
        No auth required for simple search queries.
        """
        url = f"https://api.github.com/search/issues?q={search_query}+state:open&sort=created&order=desc"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])[:3] # Limit to top 3 for brevity
                opportunities = []
                for item in items:
                    opportunities.append({
                        "type": "Live Open Source Issue",
                        "name": item.get("title", "Unknown Request"),
                        "url": item.get("html_url", ""),
                        "difficulty": "Beginner/Intermediate"
                    })
                return {
                    "opportunities_found": opportunities,
                    "search_query_used": search_query,
                    "tool_status": "live_data_retrieved"
                }
            else:
                return {
                    "opportunities_found": [],
                    "tool_status": f"API Error: {response.status_code}"
                }
        except Exception as e:
            return {
                "opportunities_found": [],
                "tool_status": f"Network Error: {str(e)}"
            }


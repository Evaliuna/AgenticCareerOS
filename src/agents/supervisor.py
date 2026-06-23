from src.agents.profile import ProfileAnalysisAgent
from src.agents.skill_gap import SkillGapAgent
from src.agents.roadmap import LearningRoadmapAgent
from src.agents.opportunity import OpportunityAgent
from src.agents.project import ProjectRecommendationAgent
from src.agents.memory import MemoryAgent

class Orchestrator:
    """
    The Central Orchestrator
    Manages the sequential invocation of the multi-agent system and tracks state.
    """
    def __init__(self, api_key: str = None):
        if not api_key:
            raise ValueError("No API Key provided. Please verify your environment configuration.")
            
        self.profile_agent = ProfileAnalysisAgent(api_key)
        self.gap_agent = SkillGapAgent(api_key)
        self.roadmap_agent = LearningRoadmapAgent(api_key)
        self.opportunity_agent = OpportunityAgent(api_key)
        self.project_agent = ProjectRecommendationAgent(api_key)
        self.memory_agent = MemoryAgent()

    def run_career_analysis(self, raw_skills, goal, weeks_timeframe=4):
        """Executes the full agentic data workflow cleanly."""
        
        # 1. Profile Agent execution
        profile_res = self.profile_agent.analyze(raw_skills, goal)
        if "error" in profile_res:
            raise RuntimeError(f"Profile Analysis Failed: {profile_res['error']}")
            
        current_skills = profile_res.get("current_competencies", [])
        if not current_skills:
            raise ValueError("Profile Agent could not extract any current competencies.")
            
        # 2. Skill Gap Agent execution
        gap_res = self.gap_agent.identify_gaps(current_skills, goal)
        if "error" in gap_res:
            raise RuntimeError(f"Skill Gap Analysis Failed: {gap_res['error']}")
            
        missing_skills = gap_res.get("gap_analysis", {}).get("missing_skills", [])
        
        # 3. Actionable Generation (Parallel conceptual targets)
        # These are independent, we can tolerate failures individually but should pass arrays
        roadmap_res = self.roadmap_agent.generate_roadmap(missing_skills, weeks_timeframe)
        project_res = self.project_agent.recommend(missing_skills, goal)
        opp_res = self.opportunity_agent.discover(missing_skills, goal)
        
        # 4. Persist the generated knowledge graph to Long-Term Memory
        final_state = {
            "profile_context": profile_res,
            "gap_context": gap_res,
            "roadmap_context": roadmap_res,
            "project_context": project_res,
            "opportunities_context": opp_res
        }
        self.memory_agent.save_state(final_state)
        
        return final_state

    def adapt_roadmap(self, feedback_text: str, current_context: dict):
        """Feedback adaptation loop: Re-triggers roadmap generation based on user feedback."""
        gap_data = current_context.get("gap_context", {}).get("gap_analysis", {})
        if not isinstance(gap_data, dict):
            gap_data = {}
        missing_skills = gap_data.get("missing_skills", [])
        if not missing_skills:
            return current_context

        # We inject the feedback directly into the Roadmap agent call via a prompt injection or override.
        adapted_prompt_context = missing_skills + [f"(USER CONSTRAINTS: {feedback_text})"]
        
        new_roadmap_res = self.roadmap_agent.generate_roadmap(adapted_prompt_context, 4)
        if "error" not in new_roadmap_res:
            current_context["roadmap_context"] = new_roadmap_res
            self.memory_agent.save_state(current_context)
            
        return current_context

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Ensure the root project directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.supervisor import Orchestrator
from src.agents.memory import MemoryAgent

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Career Growth Navigator | AI Dashboard",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern SaaS Dashboard Look
st.markdown("""
<style>
    :root {
        --primary-accent: #6366f1;
        --bg-color: #0f172a;
        --card-bg: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }
    
    .main {
        background-color: var(--bg-color);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: var(--bg-color);
    }
    
    /* Hero Section */
    .hero-container {
        padding: 2rem 0;
        text-align: left;
        margin-bottom: 2rem;
        border-bottom: 1px solid #334155;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
    }
    
    /* Metrics / Badges */
    .metric-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        background-color: rgba(99, 102, 241, 0.1);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .metric-badge.missing {
        background-color: rgba(2ef, 68, 68, 0.1);
        color: #f87171;
        border-color: rgba(239, 68, 68, 0.2);
    }
    
    .metric-badge.existing {
        background-color: rgba(34, 197, 94, 0.1);
        color: #4ade80;
        border-color: rgba(34, 197, 94, 0.2);
    }

    /* Cards */
    div[data-testid="stExpander"] {
        background-color: var(--card-bg) !important;
        border: 1px solid #334155 !important;
        border-radius: 0.5rem !important;
    }
    div[data-testid="stExpander"] summary {
        color: #fff !important;
        font-weight: 600 !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "results" not in st.session_state:
    st.session_state["results"] = None

memory_agent = MemoryAgent()

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/shapes/svg?seed=Career&backgroundColor=0f172a", width=50)
    st.title("Settings")
    st.markdown("Configure your environment and agents below.")
    
    api_key_env = os.environ.get("GEMINI_API_KEY", "")
    st.subheader("🔑 API Configuration")
    
    # 1. Try to get API key from environment
    api_key = os.environ.get("GEMINI_API_KEY", "")
    
    # 2. Try Streamlit secrets as fallback if not in env
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
            
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("API Key loaded securely.", icon="✅")
        # Give option to change it if needed
        with st.expander("Update API Key"):
            new_key = st.text_input("New Gemini API Key", type="password")
            if new_key and st.button("Save New Key"):
                os.environ["GEMINI_API_KEY"] = new_key
                with open(".env", "w") as f:
                    f.write(f"GEMINI_API_KEY={new_key}\n")
                st.rerun()
    else:
        st.warning("No API Key found. Enter one below.", icon="⚠️")
        new_key = st.text_input(
            "Gemini API Key", 
            type="password",
            help="Your key will be securely saved to a local .env file so you only have to do this once."
        )
        if new_key:
            os.environ["GEMINI_API_KEY"] = new_key
            # Save to .env automatically
            with open(".env", "a") as f:
                f.write(f"\nGEMINI_API_KEY={new_key}\n")
            st.success("API Key saved to .env file!", icon="✅")
            st.rerun()
        
    st.divider()
    st.subheader("⚙️ Pipeline Settings")
    time_frame_weeks = st.slider("Roadmap Duration (Weeks)", min_value=1, max_value=12, value=4)
    hours_per_week = st.slider("Hours per Week", min_value=1, max_value=40, value=10)

    st.divider()
    st.subheader("💾 Global Memory State")
    if st.button("📥 Load Memory JSON"):
        state = memory_agent.load_state()
        if state:
            st.session_state["results"] = state
            st.success("State loaded from storage.")
            st.rerun()
        else:
            st.info("No saved memory found.")
            
    if st.button("🗑️ Clear Memory"):
        memory_agent.clear_state()
        st.session_state["results"] = None
        st.success("Memory purged.")
        st.rerun()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🧭 Career Growth Navigator</div>
    <div class="hero-subtitle">Multi-Agent AI system designed to analyze your skill gaps and generate a personalized roadmap.</div>
</div>
""", unsafe_allow_html=True)

# 4-COLUMN METRIC ROW (if result exist)
if st.session_state.get("results"):
    res = st.session_state["results"]
    gap_data = res.get("gap_context", {}).get("gap_analysis", {}) if isinstance(res.get("gap_context", {}), dict) else {}
    existing_len = len(gap_data.get('existing_relevant_skills', []))
    missing_len = len(gap_data.get('missing_skills', []))
    total_skills = existing_len + missing_len
    gap_prec = gap_data.get('gap_percentage', 100)
    readiness = 100 - gap_prec
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Relevant Skills", total_skills)
    c2.metric("Overlapping Skills", existing_len)
    c3.metric("Gap Percentage", f"{gap_prec}%")
    c4.metric("Readiness Score", f"{readiness}%")
    st.markdown("<br/>", unsafe_allow_html=True)

# Main Navigation
tab_profile, tab_gaps, tab_roadmap, tab_projects, tab_opps = st.tabs([
    "📊 Profile Overview",
    "📈 Skill Gaps",
    "🗺️ Learning Roadmap",
    "🛠️ Custom Projects",
    "🌐 Live Opportunities"
])

# --- TAB 1: Profile Overview ---
with tab_profile:
    with st.container(border=True):
        st.subheader("1. Define Your Profile")
        col1, col2 = st.columns(2)
        with col1:
            skills_input = st.text_area("What skills do you currently possess?", placeholder="E.g., Python, React, Basic SQL, Git...", height=120)
        with col2:
            goal_input = st.text_input("What is your target functional role?", placeholder="E.g., Senior AI Engineer")
            
        st.markdown("<br/>", unsafe_allow_html=True)
        analyze_btn = st.button("Run Multi-Agent Analysis Pipeline", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not api_key:
            st.error("Cannot proceed: Please enter your Gemini API Key in the sidebar.")
        elif not skills_input or not goal_input:
            st.warning("Please fill out both your current skills and target role.")
        else:
            with st.sidebar.status("🚀 Pipeline Execution...", expanded=True) as status:
                st.write("1️⃣ Initializing Central Orchestrator...")
                orchestrator = Orchestrator(api_key=api_key)
                
                try:
                    st.write("2️⃣ Profile Agent & Skill Gap Agent analyzing...")
                    results = orchestrator.run_career_analysis(skills_input, goal_input, weeks_timeframe=time_frame_weeks)
                    
                    st.write("3️⃣ Roadmap & Project Agents planning...")
                    st.write("4️⃣ Opportunity Agent discovering links...")
                    st.session_state["results"] = results
                    status.update(label="Analysis Complete!", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    status.update(label=f"Pipeline Error: {str(e)}", state="error", expanded=True)

    # Render Analysis Results if available
if st.session_state.get("results"):
    res = st.session_state["results"]
    
    # --- TAB 2: Skill Gaps ---
    with tab_gaps:
        st.subheader("📈 Skill Gap Analysis")
        gap_context = res.get("gap_context", {})
        gap_data = gap_context.get("gap_analysis", {}) if isinstance(gap_context, dict) else {}
        
        c_left, c_right = st.columns(2)
        with c_left:
            with st.container(border=True):
                st.markdown("#### ✅ Existing Validated Skills")
                existing = gap_data.get('existing_relevant_skills', [])
                if existing:
                    html_existing = "".join([f"<span class='metric-badge existing'>{s}</span>" for s in existing])
                    st.markdown(html_existing, unsafe_allow_html=True)
                else:
                    st.write("No matching skills found.")
                    
        with c_right:
            with st.container(border=True):
                st.markdown("#### 🎯 Missing Required Skills")
                missing = gap_data.get('missing_skills', [])
                if missing:
                    html_missing = "".join([f"<span class='metric-badge missing'>{s}</span>" for s in missing])
                    st.markdown(html_missing, unsafe_allow_html=True)
                else:
                    st.write("You meet the baseline requirements!")

    # --- TAB 3: Roadmap ---
    with tab_roadmap:
        st.subheader("📅 Structured Learning Roadmap")
        roadmap_ctx = res.get("roadmap_context", {})
        weekly = roadmap_ctx.get("weekly_schedule", {})
        
        if weekly:
            # 3 Column grid for weeks
            week_keys = list(weekly.keys())
            for i in range(0, len(week_keys), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(week_keys):
                        week_label = week_keys[i+j]
                        skills_list = weekly[week_label]
                        with cols[j]:
                            with st.container(border=True):
                                st.markdown(f"**{week_label.replace('_', ' ').capitalize()}**")
                                for s in skills_list:
                                    st.markdown(f"- 🎓 {s}")
                                st.caption(f"Focus: {hours_per_week} hrs/week")
        else:
            st.write("No structured schedule generated. Check skill gaps.")
            
        # Agent Feedback Loop System
        st.markdown("---")
        st.markdown("#### 🔄 Agent Adaptation Loop")
        feedback = st.text_input("Feedback for Roadmap Agent? (e.g., 'I only have 3 hours a week')", placeholder="Talk to the Roadmap Agent...")
        if st.button("Regenerate Roadmap via Feedback"):
            with st.sidebar.status("Advising Agent with new constraints..."):
                orchestrator = Orchestrator(api_key=api_key)
                new_res = orchestrator.adapt_roadmap(feedback, st.session_state["results"])
                st.session_state["results"] = new_res
                st.rerun()
                
    # --- TAB 4: Projects ---
    with tab_projects:
        st.subheader("🛠️ Recommended Custom Project")
        proj = res.get("project_context", {})
        if "title" in proj:
            with st.container(border=True):
                st.markdown(f"### {proj['title']}")
                st.markdown(f"**Description:** {proj.get('description', 'N/A')}")
                stack_html = "".join([f"<span class='metric-badge'>{s}</span>" for s in proj.get('stack', [])])
                st.markdown(f"**Stack:** <br/>{stack_html}", unsafe_allow_html=True)
                st.caption(f"Difficulty: {proj.get('difficulty', 'Unknown')}")
        else:
            st.warning("No project generated.")
            
    # --- TAB 5: Opportunities ---
    with tab_opps:
        st.subheader("🌐 Live Opportunities (GitHub)")
        opps = res.get("opportunities_context", {}).get("opportunities_found", [])
        
        if isinstance(opps, list) and opps:
            for o in opps:
                with st.container(border=True):
                    # Styled cards with repo name, labels, clickable links
                    tags = "".join([f"<span class='metric-badge'>{l}</span>" for l in o.get('labels', [])])
                    repo_name = o.get('name', 'Issue')
                    st.markdown(f"#### [{repo_name}]({o.get('url', '#')})")
                    st.markdown(f"**Type:** {o.get('type', 'Opportunity')}")
                    if tags:
                        st.markdown(tags, unsafe_allow_html=True)
        elif opps is None:
            st.write("Live opportunity data unavailable.")
        else:
            err = res.get("opportunities_context", {}).get("error")
            if err:
                st.error(f"Agent Error: {err}")
            else:
                st.write("No live issues found for your skill gap.")

else:
    for tab in [tab_gaps, tab_roadmap, tab_projects, tab_opps]:
        with tab:
            st.info("Run the Career Analysis pipeline to generate your roadmap and opportunities.")

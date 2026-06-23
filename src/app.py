import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Ensure the root project directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.supervisor import Orchestrator

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="AI Career Growth Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* Hero Section */
    .hero-container {
        padding: 3rem 1rem;
        text-align: center;
        background: linear-gradient(180deg, rgba(30, 41, 59, 1) 0%, rgba(15, 23, 42, 1) 100%);
        border-bottom: 1px solid #334155;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #fff;
        margin-bottom: 1rem;
        background: -webkit-linear-gradient(45deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        max-width: 600px;
        margin: 0 auto;
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
        background-color: rgba(239, 68, 68, 0.1);
        color: #f87171;
        border-color: rgba(239, 68, 68, 0.2);
    }
    
    .metric-badge.existing {
        background-color: rgba(34, 197, 94, 0.1);
        color: #4ade80;
        border-color: rgba(34, 197, 94, 0.2);
    }

    /* Cards & Containers */
    div[data-testid="stExpander"], div.st-emotion-cache-1r6slb0, div.st-emotion-cache-12w0qpk {
        background-color: var(--card-bg) !important;
        border: 1px solid #334155 !important;
        border-radius: 0.75rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    div[data-testid="stExpander"] summary {
        color: #fff !important;
        font-weight: 600 !important;
    }
    
    /* Input Fields styling */
    div.stTextArea > div > div > textarea, div.stTextInput > div > div > input {
        background-color: #0f172a !important;
        color: #fff !important;
        border: 1px solid #334155 !important;
        border-radius: 0.5rem !important;
    }
    
    div.stTextArea > div > div > textarea:focus, div.stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    
    /* Tabs */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
    }
    button[data-baseweb="tab"] > div {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] > div {
        color: #818cf8 !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #818cf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "results" not in st.session_state:
    st.session_state["results"] = None

# Retrieve API Key efficiently and securely
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

# Clean the key in case it was passed with quotes or spaces from the secrets panel
if api_key:
    api_key = api_key.strip(' "\'')

if not api_key:
    st.error("Developer Warning: GEMINI_API_KEY environment variable is missing. The application will not function correctly.", icon="🚨")

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">AI Career Growth Navigator</div>
    <div class="hero-subtitle">Your personal AI career coach. We analyze your skills against industry standards to instantly provide actionable gaps, roadmaps, and next steps.</div>
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
    with c1:
        st.metric("Total Analyzed Skills", total_skills)
    with c2:
        st.metric("Validated Skills", existing_len)
    with c3:
        st.metric("Missing Skills", missing_len)
    with c4:
        st.metric("Readiness Score", f"{readiness}%")
    st.markdown("<br/>", unsafe_allow_html=True)

# Main Navigation
tab_profile, tab_dashboard = st.tabs([
    "🎯 Assessment Setup",
    "📈 Career Dashboard"
])

# --- TAB 1: Profile Overview ---
with tab_profile:
    with st.container():
        st.subheader("Define Your Trajectory")
        st.markdown("<p style='color: #94a3b8; margin-bottom: 1rem;'>Enter your current professional capabilities and your ultimate goal. Our AI orchestration pipeline will handle the rest.</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            skills_input = st.text_area("Your Current Skills", placeholder="E.g., Python, React, Basic SQL, Git...", height=150)
        with col2:
            goal_input = st.text_input("Your Target Role", placeholder="E.g., Senior AI Engineer")
            
        st.markdown("<br/>", unsafe_allow_html=True)
        analyze_btn = st.button("Initialize Multi-Agent Analysis Pipeline", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not api_key:
            st.error("Cannot proceed: Missing Gemini API configuration.")
        elif not skills_input or not goal_input:
            st.warning("Please define your current skill set and your future goal.")
        else:
            with st.status("🚀 Orchestrating Agents...", expanded=True) as status:
                st.write("1️⃣ Initializing Supervisor Agent...")
                orchestrator = Orchestrator(api_key=api_key)
                
                try:
                    st.write("2️⃣ Profile & Skill Gap Agents analyzing baseline...")
                    results = orchestrator.run_career_analysis(skills_input, goal_input, weeks_timeframe=4)
                    
                    st.write("3️⃣ Roadmap & Project Agents generating learning pathways...")
                    st.write("4️⃣ Opportunity Agent discovering live integrations...")
                    st.session_state["results"] = results
                    status.update(label="Analysis Pipeline Complete!", state="complete", expanded=False)
                    st.rerun()
                except Exception as e:
                    status.update(label="Analysis Pipeline Interrupted", state="error", expanded=True)
                    st.warning(f"The pipeline could not complete successfully:\\n\\n{str(e)}")

# Render Analysis Results if available
if st.session_state.get("results"):
    res = st.session_state["results"]
    
    # --- TAB 2: Career Dashboard ---
    with tab_dashboard:
        # GAPS ROW
        st.subheader("Skill Gap Analysis")
        gap_context = res.get("gap_context", {})
        gap_data = gap_context.get("gap_analysis", {}) if isinstance(gap_context, dict) else {}
        
        c_left, c_right = st.columns(2)
        with c_left:
            with st.container():
                st.markdown("#### ✅ Validated Core Competencies")
                existing = gap_data.get('existing_relevant_skills', [])
                if existing:
                    html_existing = "".join([f"<span class='metric-badge existing'>{s}</span>" for s in existing])
                    st.markdown(html_existing, unsafe_allow_html=True)
                else:
                    st.write("No matching skills found against the target role.")
                    
        with c_right:
            with st.container():
                st.markdown("#### 🎯 Critical Missing Attributes")
                missing = gap_data.get('missing_skills', [])
                if missing:
                    html_missing = "".join([f"<span class='metric-badge missing'>{s}</span>" for s in missing])
                    st.markdown(html_missing, unsafe_allow_html=True)
                else:
                    st.write("You meet the baseline requirements for this role!")

        st.markdown("<hr style='border-color: #334155; margin: 2rem 0;'/>", unsafe_allow_html=True)
        
        # ROADMAP ROW
        st.subheader("Learning Timeline")
        roadmap_ctx = res.get("roadmap_context", {})
        weekly = roadmap_ctx.get("weekly_schedule", {})
        
        if weekly:
            week_keys = list(weekly.keys())
            for i in range(0, len(week_keys), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(week_keys):
                        week_label = week_keys[i+j]
                        skills_list = weekly[week_label]
                        with cols[j]:
                            with st.container():
                                st.markdown(f"**{week_label.replace('_', ' ').capitalize()}**")
                                for s in skills_list:
                                    st.markdown(f"- 🎓 {s}")
        else:
            st.write("No structured schedule generated.")
            
        st.markdown("<hr style='border-color: #334155; margin: 2rem 0;'/>", unsafe_allow_html=True)

        # PROJECTS & OPPORTUNITIES ROW
        c_proj, c_opps = st.columns(2)
        with c_proj:
            st.subheader("Suggested Project")
            proj = res.get("project_context", {})
            if "title" in proj:
                with st.container():
                    st.markdown(f"### {proj['title']}")
                    st.markdown(f"*{proj.get('description', 'N/A')}*")
                    st.markdown("**Core Tech Stack:**")
                    stack_html = "".join([f"<span class='metric-badge'>{s}</span>" for s in proj.get('stack', [])])
                    st.markdown(f"{stack_html}", unsafe_allow_html=True)
                    st.caption(f"Difficulty Level: {proj.get('difficulty', 'Unknown')}")
            else:
                st.warning("No project generated by the agent.")
                
        with c_opps:
            st.subheader("Current Market Opportunities")
            opps = res.get("opportunities_context", {}).get("opportunities_found", [])
            if isinstance(opps, list) and opps:
                for o in opps:
                    with st.container():
                        tags = "".join([f"<span class='metric-badge'>{l}</span>" for l in o.get('labels', [])])
                        repo_name = o.get('name', 'Opportunity Link')
                        st.markdown(f"#### [{repo_name}]({o.get('url', '#')})")
                        st.markdown(f"**Category:** {o.get('type', 'General')}")
                        if tags:
                            st.markdown(tags, unsafe_allow_html=True)
            elif opps is None:
                st.write("Market data unavailable.")
            else:
                err = res.get("opportunities_context", {}).get("error")
                if err:
                    st.error(f"Agent Engine Error: {err}")
                else:
                    st.write("No direct opportunities found. Focus on the core skills first.")
else:
    with tab_dashboard:
        st.info("Run the Career Assessment inside the **Assessment Setup** tab to populate your dashboard.", icon="ℹ️")


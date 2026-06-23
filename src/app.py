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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary-accent: #3B82F6;
        --bg-color: #0F172A;
        --card-bg: #1E293B;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --success: #22C55E;
        --warning: #F59E0B;
        --danger: #EF4444;
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
    
    /* Typography */
    h1, h2, h3, h4, h5 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        margin-top: 2rem;
        color: var(--text-primary);
    }
    
    /* Hero Section */
    .hero-container {
        padding: 4rem 1rem 3rem;
        text-align: center;
        background: radial-gradient(circle at top, #1E293B 0%, #0F172A 70%);
        border-bottom: 1px solid #334155;
        margin-bottom: 3rem;
        border-radius: 0 0 2rem 2rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #fff;
        margin-bottom: 1.25rem;
        background: linear-gradient(135deg, #60A5FA, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 500;
        line-height: 1.6;
        color: var(--text-secondary);
        max-width: 650px;
        margin: 0 auto;
    }
    
    /* Feature Cards Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 3rem;
    }
    .feature-item {
        background-color: rgba(30, 41, 59, 0.5);
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .feature-item:hover {
        transform: translateY(-4px);
        border-color: var(--primary-accent);
        background-color: var(--card-bg);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    .feature-label {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: var(--card-bg);
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--primary-accent);
    }
    .kpi-card.score::after { background: var(--success); }
    .kpi-card.missing::after { background: var(--warning); }
    
    .kpi-title {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        color: var(--text-primary);
        font-size: 2.25rem;
        font-weight: 700;
        line-height: 1.2;
    }
    
    /* Metrics / Badges */
    .metric-badge {
        display: inline-block;
        padding: 0.4rem 0.875rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        background-color: rgba(59, 130, 246, 0.1);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .metric-badge.missing {
        background-color: rgba(245, 158, 11, 0.1);
        color: var(--warning);
        border-color: rgba(245, 158, 11, 0.2);
    }
    
    .metric-badge.existing {
        background-color: rgba(34, 197, 94, 0.1);
        color: var(--success);
        border-color: rgba(34, 197, 94, 0.2);
    }

    /* Roadmap View */
    .roadmap-list {
        position: relative;
        padding: 1rem 0;
    }
    .roadmap-item {
        position: relative;
        padding-left: 2.5rem;
        margin-bottom: 2rem;
    }
    .roadmap-item::before {
        content: '';
        position: absolute;
        left: 5px;
        top: 2rem;
        bottom: -2rem;
        width: 2px;
        background-color: #334155;
    }
    .roadmap-item:last-child::before {
        display: none;
    }
    .roadmap-bullet {
        position: absolute;
        left: 0;
        top: 0.25rem;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: var(--primary-accent);
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
    }
    .roadmap-content {
        background-color: var(--card-bg);
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .roadmap-week {
        color: var(--primary-accent);
        font-size: 0.875rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }

    /* Premium Project Card */
    .project-card {
        background: linear-gradient(145deg, #1E293B, #0F172A);
        border: 1px solid #334155;
        border-radius: 1.25rem;
        padding: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .project-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #3B82F6, #22C55E);
    }
    
    /* Opportunity Card */
    .opp-card {
        background-color: var(--card-bg);
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s ease;
    }
    .opp-card:hover {
        border-color: #64748B;
    }
    .opp-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    .opp-title a {
        color: inherit;
        text-decoration: none;
    }
    .opp-title a:hover {
        color: var(--primary-accent);
        text-decoration: underline;
    }

    /* Inputs & Buttons */
    div.stTextArea > div > div > textarea, div.stTextInput > div > div > input {
        background-color: #0f172a !important;
        color: #fff !important;
        border: 1px solid #334155 !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem !important;
    }
    div.stTextArea > div > div > textarea:focus, div.stTextInput > div > div > input:focus {
        border-color: var(--primary-accent) !important;
        box-shadow: 0 0 0 1px var(--primary-accent) !important;
    }
    
    /* Tabs */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
    }
    button[data-baseweb="tab"] > div {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] > div {
        color: var(--primary-accent) !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: var(--primary-accent) !important;
    }
    
    /* Setup Card */
    .setup-card {
        background-color: var(--card-bg);
        border: 1px solid #334155;
        border-radius: 1.25rem;
        padding: 2.5rem;
        margin-top: 1rem;
        margin-bottom: 2rem;
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

# Main Navigation
tab_profile, tab_dashboard = st.tabs([
    "🎯 Assessment Setup",
    "📈 Career Dashboard"
])

# --- TAB 1: Profile Overview ---
with tab_profile:
    st.markdown("""
    <div class="setup-card">
        <h3 style="margin-top: 0; margin-bottom: 0.5rem;">Define Your Professional Trajectory</h3>
        <p style="color: #94A3B8; margin-bottom: 1rem; font-size: 1.1rem;">
            Enter your current professional capabilities and your ultimate goal. Our AI orchestration pipeline will handle the rest.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # We use Streamlit native inputs to keep functionality intact
    col1, col2 = st.columns(2)
    with col1:
        skills_input = st.text_area("🔧 Your Current Skills & Experience", placeholder="E.g., Python (3 yrs), React, Basic SQL, Git...", height=160)
    with col2:
        goal_input = st.text_input("🎯 Your Target Role", placeholder="E.g., Senior AI Engineer")
        st.markdown("<br/>", unsafe_allow_html=True)
        analyze_btn = st.button("Initialize Multi-Agent Analysis Pipeline", type="primary", use_container_width=True)

    # Informational Features Grid below CTA
    st.markdown("""
    <div class="features-grid">
        <div class="feature-item">
            <div class="feature-icon">🎯</div>
            <div class="feature-label">Skill Gap Analysis</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🛣️</div>
            <div class="feature-label">Personalized Roadmap</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">💼</div>
            <div class="feature-label">Market Insights</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🚀</div>
            <div class="feature-label">Project Recommendations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if analyze_btn:
        if not api_key:
            st.error("Cannot proceed: Missing Gemini API configuration.")
        elif not skills_input or not goal_input:
            st.warning("Please define your current skill set and your future goal.")
        else:
            with st.status("🚀 Orchestrating AI Agents...", expanded=True) as status:
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

# --- TAB 2: Career Dashboard ---
with tab_dashboard:
    if st.session_state.get("results"):
        res = st.session_state["results"]
        gap_context = res.get("gap_context", {})
        gap_data = gap_context.get("gap_analysis", {}) if isinstance(gap_context, dict) else {}
        
        # Calculate stats safely
        existing = gap_data.get('existing_relevant_skills', [])
        missing = gap_data.get('missing_skills', [])
        gap_prec = gap_data.get('gap_percentage', 100)
        readiness = 100 - gap_prec
        
        # SECTION 1: Career Overview KPIs
        st.markdown('<div class="section-title" style="margin-top: 1rem;">Executive Summary</div>', unsafe_allow_html=True)
        
        kpi_html = f"""
        <div class="kpi-container">
            <div class="kpi-card score">
                <div class="kpi-title">Career Match Score</div>
                <div class="kpi-value">{readiness}%</div>
            </div>
            <div class="kpi-card missing">
                <div class="kpi-title">Critical Gaps</div>
                <div class="kpi-value">{len(missing)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Roadmap Duration</div>
                <div class="kpi-value">4 Weeks</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Verified Skills</div>
                <div class="kpi-value">{len(existing)}</div>
            </div>
        </div>
        """
        st.markdown(kpi_html, unsafe_allow_html=True)
        
        # SECTION 2: Skills Analysis
        st.markdown('<div class="section-title">Core Competencies & Gaps</div>', unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown("#### ✅ Validated Proficiencies")
            if existing:
                html_existing = "".join([f"<span class='metric-badge existing'>{s}</span>" for s in existing])
                st.markdown(html_existing, unsafe_allow_html=True)
            else:
                st.info("No matching skills validated against the target role.")
                
        with c_right:
            st.markdown("#### 🎯 Priority Skill Gaps")
            if missing:
                html_missing = "".join([f"<span class='metric-badge missing'>{s}</span>" for s in missing])
                st.markdown(html_missing, unsafe_allow_html=True)
            else:
                st.success("You meet the baseline requirements for this role!")

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Bottom structured row wrapper for Roadmap / Projects
        col_main, col_side = st.columns([1.3, 1], gap="large")
        
        with col_main:
            # SECTION 3: Learning Roadmap
            st.markdown('<div class="section-title" style="margin-top: 0;">Learning Journey</div>', unsafe_allow_html=True)
            roadmap_ctx = res.get("roadmap_context", {})
            weekly = roadmap_ctx.get("weekly_schedule", {})
            
            if weekly:
                roadmap_html = '<div class="roadmap-list">'
                for week_label, skills_list in weekly.items():
                    skills_items = "".join([f"<li><span style='margin-right: 8px; color: #64748B;'>▫</span>{s}</li>" for s in skills_list])
                    roadmap_html += f"""
                    <div class="roadmap-item">
                        <div class="roadmap-bullet"></div>
                        <div class="roadmap-content">
                            <div class="roadmap-week">{week_label.replace('_', ' ')}</div>
                            <ul style="list-style-type: none; padding-left: 0; margin-bottom: 0; color: var(--text-primary); line-height: 1.8;">
                                {skills_items}
                            </ul>
                        </div>
                    </div>
                    """
                roadmap_html += '</div>'
                st.markdown(roadmap_html, unsafe_allow_html=True)
            else:
                st.info("No structured roadmap generated.")
                
        with col_side:
            # SECTION 4: Featured Project
            st.markdown('<div class="section-title" style="margin-top: 0;">Featured Objective</div>', unsafe_allow_html=True)
            proj = res.get("project_context", {})
            
            if "title" in proj:
                stack_html = "".join([f"<span class='metric-badge'>{s}</span>" for s in proj.get('stack', [])])
                project_html = f"""
                <div class="project-card">
                    <h3 style="margin-top: 0; margin-bottom: 0.5rem; color: #fff;">{proj['title']}</h3>
                    <p style="color: var(--text-secondary); margin-bottom: 1.5rem; font-size: 0.95rem; line-height: 1.5;">
                        {proj.get('description', 'N/A')}
                    </p>
                    <div style="margin-bottom: 1rem;">
                        <div style="color: var(--text-secondary); font-size: 0.75rem; text-transform: uppercase; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: 0.05em;">Tech Stack</div>
                        <div>{stack_html}</div>
                    </div>
                    <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #334155; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: var(--text-secondary); font-size: 0.875rem;">Difficulty</span>
                        <span style="background-color: rgba(245, 158, 11, 0.15); color: #FBBF24; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">{proj.get('difficulty', 'Unknown')}</span>
                    </div>
                </div>
                """
                st.markdown(project_html, unsafe_allow_html=True)
            else:
                st.info("No project specification generated.")
            
            st.markdown('<br>', unsafe_allow_html=True)
            
            # SECTION 5: Market Opportunities
            st.markdown('<div class="section-title">Market Opportunities</div>', unsafe_allow_html=True)
            opps = res.get("opportunities_context", {}).get("opportunities_found", [])
            
            if isinstance(opps, list) and opps:
                for o in opps:
                    tags = "".join([f"<span style='display:inline-block; margin-right: 0.5rem; margin-top: 0.5rem; background: #334155; color: #CBD5E1; padding: 0.15rem 0.6rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500;'>{l}</span>" for l in o.get('labels', [])])
                    repo_name = o.get('name', 'Opportunity Link')
                    url = o.get('url', '#')
                    opp_type = o.get('type', 'General')
                    
                    opp_html = f"""
                    <div class="opp-card">
                        <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--primary-accent); font-weight: 700; margin-bottom: 0.5rem;">{opp_type}</div>
                        <div class="opp-title"><a href="{url}" target="_blank">{repo_name}</a></div>
                        <div>{tags}</div>
                    </div>
                    """
                    st.markdown(opp_html, unsafe_allow_html=True)
            elif opps is None:
                st.write("Market data unavailable.")
            else:
                err = res.get("opportunities_context", {}).get("error")
                if err:
                    st.error(f"Agent Engine Error: {err}")
                else:
                    st.info("No direct opportunities found matching your profile. Focus on the core roadmap first.")

    else:
        # Empty State
        st.markdown("""
        <div style="background-color: var(--card-bg); border: 1px dashed #334155; border-radius: 1rem; padding: 5rem 2rem; text-align: center; margin-top: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧭</div>
            <h3 style="margin-top: 0; color: #fff;">Your Career Dashboard is Empty</h3>
            <p style="color: var(--text-secondary); max-width: 400px; margin: 0 auto; line-height: 1.6;">
                Head over to the Assessment Setup tab, define your skills and goals, and initialize the AI pipeline to generate your insights.
            </p>
        </div>
        """, unsafe_allow_html=True)
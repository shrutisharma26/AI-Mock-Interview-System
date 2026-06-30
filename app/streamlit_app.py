import sys
import os
import time
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from question_generator import (
    generate_questions,
    generate_skill_questions
)
from report_generator import generate_report
from pdf_extractor import extract_text_from_pdf
from skill_extractor import extract_skills
from evaluator import evaluate_answer

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Mock Interview | Practice Like LeetCode",
    page_icon="🧩",
    layout="wide"
)

# ---------------------------------------------------
# DIFFICULTY / STATUS COLOR TOKENS (LeetCode palette)
# ---------------------------------------------------

DIFFICULTY_COLORS = {
    "Easy": "#00B8A3",
    "Medium": "#FFC01E",
    "Hard": "#FF375F",
}

VERDICT = {
    "accepted": {"label": "Accepted", "color": "#2CBB5D"},
    "partial": {"label": "Partial Credit", "color": "#FFC01E"},
    "wrong": {"label": "Wrong Answer", "color": "#FF375F"},
}


def get_verdict(score):
    if score >= 70:
        return VERDICT["accepted"]
    elif score >= 40:
        return VERDICT["partial"]
    return VERDICT["wrong"]


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown(
    "<div class='lc-sidebar-title'>⚙️ Interview Settings</div>",
    unsafe_allow_html=True
)

role = st.sidebar.selectbox(
    "Role",
    ["SDE", "Machine Learning", "Data Science"],
    key="role_select"
)

company = st.sidebar.selectbox(
    "Company",
    [
        "General",
        "Google",
        "Amazon",
        "Microsoft",
        "Meta",
        "Adobe",
        "Goldman Sachs",
        "Uber"
    ],
    key="company_select"
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"],
    key="difficulty_select"
)

num_questions = st.sidebar.slider(
    "Number of Questions",
    min_value=1,
    max_value=5,
    value=3,
    key="num_questions_slider"
)

st.sidebar.markdown("<hr class='lc-sidebar-divider'>", unsafe_allow_html=True)
st.sidebar.markdown(
    f"""
    <div class="lc-sidebar-summary">
        <div class="lc-sidebar-row"><span>Role</span><b>{role}</b></div>
        <div class="lc-sidebar-row"><span>Company</span><b>{company}</b></div>
        <div class="lc-sidebar-row"><span>Difficulty</span>
            <b style="color:{DIFFICULTY_COLORS[difficulty]}">{difficulty}</b>
        </div>
        <div class="lc-sidebar-row"><span>Questions</span><b>{num_questions}</b></div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# CUSTOM CSS — LeetCode-inspired dark theme
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --lc-bg: #16161A;
    --lc-bg-soft: #1E1E23;
    --lc-card: #23242A;
    --lc-card-alt: #1A1B20;
    --lc-border: #33343C;
    --lc-text: #EEEFF1;
    --lc-text-dim: #9CA3AF;
    --lc-orange: #FFA116;
    --lc-orange-dark: #E68A00;
    --lc-green: #2CBB5D;
    --lc-easy: #00B8A3;
    --lc-medium: #FFC01E;
    --lc-hard: #FF375F;
}

html, body, .stApp {
    background-color: var(--lc-bg) !important;
    color: var(--lc-text) !important;
    font-family: 'Inter', -apple-system, sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--lc-bg-soft);
    border-right: 1px solid var(--lc-border);
}
section[data-testid="stSidebar"] * {
    color: var(--lc-text) !important;
    font-family: 'Inter', sans-serif;
}
.lc-sidebar-title {
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.02em;
    padding: 4px 0 10px 0;
}
.lc-sidebar-divider {
    border-color: var(--lc-border);
    margin: 14px 0;
}
.lc-sidebar-summary {
    background: var(--lc-card);
    border: 1px solid var(--lc-border);
    border-radius: 10px;
    padding: 12px 14px;
}
.lc-sidebar-row {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    padding: 4px 0;
    color: var(--lc-text-dim) !important;
}
.lc-sidebar-row b {
    color: var(--lc-text) !important;
    font-weight: 600;
}

/* Headers */
h1, h2, h3, h4, h5, h6 { color: var(--lc-text) !important; font-family: 'Inter', sans-serif; }
p, label, span, div { color: var(--lc-text); }

/* Buttons - default (secondary) styled like LeetCode outline/ghost */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    border: 1px solid var(--lc-border);
    font-weight: 600;
    color: var(--lc-text);
    background: var(--lc-card);
    padding: 0.6rem;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    border-color: var(--lc-orange);
    color: var(--lc-orange);
    background: var(--lc-card-alt);
}

/* Primary buttons (Start / Submit) - LeetCode action style */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, var(--lc-orange), var(--lc-orange-dark));
    border: none;
    color: #1A1A1A;
    font-weight: 700;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #FFB84D, var(--lc-orange));
    transform: translateY(-1px);
    color: #1A1A1A;
}

/* Text Areas styled like a code editor pane */
textarea {
    background-color: #1B1C22 !important;
    color: #D9E0EC !important;
    border-radius: 10px !important;
    border: 1px solid var(--lc-border) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14.5px !important;
    line-height: 1.6 !important;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background-color: var(--lc-card);
    border: 1px solid var(--lc-border);
    padding: 14px;
    border-radius: 10px;
}
div[data-testid="stMetricLabel"] { color: var(--lc-text-dim) !important; }

/* File uploader */
section[data-testid="stFileUploader"] {
    background-color: var(--lc-card);
    border: 1px dashed var(--lc-border);
    border-radius: 10px;
    padding: 14px;
}

/* Alerts */
div[data-testid="stAlert"] { border-radius: 10px; }

/* Tabs - LeetCode problem-page tab strip */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--lc-border);
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: var(--lc-text-dim);
    font-weight: 600;
    padding: 10px 16px;
}
.stTabs [aria-selected="true"] {
    color: var(--lc-orange) !important;
    border-bottom: 2px solid var(--lc-orange) !important;
}

/* Progress bar */
div[role="progressbar"] > div { background-color: var(--lc-orange) !important; }

/* ---------- Custom navbar ---------- */
.lc-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 22px;
    background: var(--lc-bg-soft);
    border: 1px solid var(--lc-border);
    border-radius: 12px;
    margin-bottom: 18px;
}
.lc-navbar-left { display: flex; align-items: center; gap: 12px; }
.lc-logo {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 20px;
    color: var(--lc-orange);
    background: rgba(255,161,22,0.12);
    padding: 6px 10px;
    border-radius: 8px;
}
.lc-brand { font-size: 20px; font-weight: 800; letter-spacing: -0.01em; }
.lc-brand-accent { color: var(--lc-orange); }
.lc-tagline { color: var(--lc-text-dim); font-size: 13px; margin-top: 2px; }
.lc-navbar-right { display: flex; gap: 10px; }
.lc-chip {
    background: var(--lc-card);
    border: 1px solid var(--lc-border);
    color: var(--lc-text);
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}
.lc-chip-accent { border-color: var(--lc-orange); color: var(--lc-orange); }

/* Feature / info cards */
.lc-card {
    background: var(--lc-card);
    border: 1px solid var(--lc-border);
    border-radius: 12px;
    padding: 18px;
    height: 100%;
}
.lc-card h4 { margin: 0 0 6px 0; font-size: 15px; }
.lc-card p { color: var(--lc-text-dim); font-size: 13px; margin: 0; }

/* Difficulty badge */
.lc-badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 14px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 8px;
    color: #14151A;
}

.lc-badge-company {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 14px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 8px;
    background: rgba(255,161,22,0.12);
    color: var(--lc-orange);
    border: 1px solid rgba(255,161,22,0.35);
}

/* Problem statement panel */
.lc-problem-panel {
    background: var(--lc-card);
    border: 1px solid var(--lc-border);
    border-radius: 14px;
    padding: 22px;
    min-height: 320px;
}
.lc-problem-panel h2 {
    font-size: 19px;
    margin-bottom: 14px;
}
.lc-problem-text {
    font-size: 16px;
    line-height: 1.75;
    color: #D9DEE6;
}

/* Editor panel header (fake editor toolbar) */
.lc-editor-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #1B1C22;
    border: 1px solid var(--lc-border);
    border-bottom: none;
    border-radius: 10px 10px 0 0;
    padding: 9px 14px;
}
.lc-editor-dots span {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    margin-right: 6px;
}
.lc-dot-red { background: #FF5F56; }
.lc-dot-yellow { background: #FFBD2E; }
.lc-dot-green { background: #27C93F; }
.lc-editor-filename {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--lc-text-dim);
}

/* Problem list (status navigator) */
.lc-problist {
    background: var(--lc-card);
    border: 1px solid var(--lc-border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 8px;
}
.lc-problist-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    font-size: 14px;
    border-bottom: 1px solid var(--lc-border);
    color: var(--lc-text-dim);
}
.lc-problist-item:last-child { border-bottom: none; }
.lc-status-icon { font-size: 14px; width: 16px; text-align: center; }
.lc-status-solved { color: var(--lc-green); }
.lc-status-solved .lc-status-icon { color: var(--lc-green); }
.lc-status-todo .lc-status-icon { color: var(--lc-text-dim); }
.lc-current { background: rgba(255,161,22,0.08); color: var(--lc-text); font-weight: 600; }

/* Verdict banner on results page */
.lc-verdict-banner {
    border-radius: 12px;
    padding: 18px 22px;
    margin: 14px 0;
    font-size: 18px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 10px;
}

.lc-section-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--lc-text-dim);
    margin: 6px 0 10px 0;
}

.lc-company-strip {
    background: var(--lc-card);
    border: 1px solid var(--lc-border);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# NAVBAR / TITLE
# ---------------------------------------------------

st.markdown(
    f"""
    <div class="lc-navbar">
        <div>
            <div class="lc-navbar-left">
                <span class="lc-logo">&lt;/&gt;</span>
                <span class="lc-brand">AI Mock<span class="lc-brand-accent">Interview</span></span>
            </div>
            <div class="lc-tagline">Practice interviews the way you practice problems — track status, get verdicts, ship a stronger resume.</div>
        </div>
        <div class="lc-navbar-right">
            <span class="lc-chip">🏢 {company}</span>
            <span class="lc-chip lc-chip-accent">⚡ {difficulty}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(
    [
        "📜 Description",
        "💡 Hints",
        "📊 Reports"
    ]
)

with tab1:
    st.info(
        """
        Welcome to the AI Mock Interview Platform.

        • Practice company-specific interviews.
        • Get resume-based questions.
        • Receive instant feedback.
        """
    )

with tab2:
    st.warning(
        """
        Interview Tips:

        • Use real project examples.
        • Explain your thought process.
        • Mention time and space complexity.
        • Structure answers clearly.
        """
    )

with tab3:
    st.success(
        """
        After completing the interview,
        your report can be downloaded here.
        """
    )

st.write("")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="lc-card">
            <h4>📄 Upload Resume</h4>
            <p>Analyze your skills automatically.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="lc-card">
            <h4>🤖 Personalized Questions</h4>
            <p>Questions tailored to your background.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="lc-card">
            <h4>📊 AI Feedback</h4>
            <p>Get a detailed interview report.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.markdown("<div class='lc-section-label'>Resume</div>", unsafe_allow_html=True)
st.header("📄 Upload Resume")

uploaded_resume = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_resume:

    resume_text = extract_text_from_pdf(
        uploaded_resume
    )

    skills = extract_skills(resume_text)

    st.session_state["skills"] = skills

    st.success("Resume uploaded successfully!")

    st.subheader("🛠 Extracted Skills")

    if skills:
        st.write(", ".join(skills))
    else:
        st.warning(
            "No skills detected."
        )

# ---------------------------------------------------
# GENERATE QUESTIONS
# ---------------------------------------------------

st.write("")
if st.button("🚀 Start Interview", type="primary"):

    questions = []

    # Resume based questions
    if "skills" in st.session_state and len(st.session_state["skills"]) > 0:

        questions = generate_skill_questions(
            st.session_state["skills"]
        )

    # Fallback to normal questions
    if len(questions) == 0:

        questions = generate_questions(
            role,
            difficulty,
            company,
            num_questions
        )

    st.session_state["questions"] = questions
    st.session_state["started"] = True
    st.session_state["current_question"] = 0
    st.session_state["submitted"] = False

    if "time_left" not in st.session_state:
        st.session_state["time_left"] = 300

# ---------------------------------------------------
# DISPLAY QUESTIONS
# ---------------------------------------------------
if st.session_state.get("started", False):

    if not st.session_state.get("submitted", False):

        st_autorefresh(
            interval=1000,
            key="interview_timer"
        )

    minutes = st.session_state["time_left"] // 60
    seconds = st.session_state["time_left"] % 60

    if (
        st.session_state["time_left"] > 0
        and not st.session_state.get("submitted", False)
    ):
        st.session_state["time_left"] -= 1

    total_questions = len(st.session_state["questions"])

    answered = sum(
        1 for idx in range(total_questions)
        if st.session_state.get(f"answer_{idx}", "").strip()
    )

    st.markdown(
        f"""
        <div class="lc-company-strip">
            <h3 style="margin:0;">
                🏢 Company Focus:
                <span style="color:var(--lc-orange);">{company}</span>
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⏱️ Time Remaining", f"{minutes:02d}:{seconds:02d}")
    with col2:
        st.metric("📝 Questions", total_questions)
    with col3:
        st.metric("✅ Answered", answered)
    with col4:
        st.metric("⚡ Difficulty", difficulty)

    if st.session_state["time_left"] <= 0:
        st.warning("⏰ Time's up! Please submit your interview.")

    progress = answered / total_questions
    st.progress(progress)
    st.write(f"### Progress: {answered}/{total_questions} questions answered")

    if "current_question" not in st.session_state:
        st.session_state["current_question"] = 0

    # -----------------------------------------------
    # PROBLEM LIST / NAVIGATOR (LeetCode style)
    # -----------------------------------------------
    st.markdown("<div class='lc-section-label'>📚 Problem List</div>", unsafe_allow_html=True)

    problist_html = "<div class='lc-problist'>"
    for idx in range(total_questions):
        is_answered = bool(st.session_state.get(f"answer_{idx}", "").strip())
        is_current = idx == st.session_state["current_question"]
        status_class = "lc-status-solved" if is_answered else "lc-status-todo"
        current_class = "lc-current" if is_current else ""
        icon = "✓" if is_answered else "○"
        status_label = "Solved" if is_answered else "Not Attempted"
        problist_html += (
            f"<div class='lc-problist-item {status_class} {current_class}'>"
            f"<span class='lc-status-icon'>{icon}</span>"
            f"<span style='flex:1;'>Question {idx + 1}</span>"
            f"<span style='font-size:12px; opacity:0.8;'>{status_label}</span>"
            f"</div>"
        )
    problist_html += "</div>"
    st.markdown(problist_html, unsafe_allow_html=True)

    nav_cols = st.columns(total_questions)
    for idx in range(total_questions):
        with nav_cols[idx]:
            button_label = f"⭐ Q{idx + 1}" if idx == st.session_state["current_question"] else f"Q{idx + 1}"
            if st.button(button_label, key=f"nav_{idx}"):
                st.session_state["current_question"] = idx
                st.rerun()

    # -----------------------------------------------
    # CURRENT QUESTION
    # -----------------------------------------------
    i = st.session_state["current_question"]
    question = st.session_state["questions"][i]

    st.markdown(
        f"""
        <h3 style='color:var(--lc-orange); margin-top:18px;'>
            Viewing Question {i + 1} of {total_questions}
        </h3>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    left_col, right_col = st.columns([1, 1])

    with left_col:
        badge_color = DIFFICULTY_COLORS[difficulty]
        st.markdown(
            f"""
            <div class="lc-problem-panel">
                <h2>Question {i + 1}</h2>
                <div style="margin-bottom:18px;">
                    <span class="lc-badge" style="background-color:{badge_color};">{difficulty}</span>
                    <span class="lc-badge-company">🏢 {company}</span>
                </div>
                <p class="lc-problem-text">{question}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right_col:
        st.markdown(
            f"""
            <div class="lc-editor-toolbar">
                <div class="lc-editor-dots">
                    <span class="lc-dot-red"></span><span class="lc-dot-yellow"></span><span class="lc-dot-green"></span>
                </div>
                <span class="lc-editor-filename">answer_{i + 1}.txt</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        answer = st.text_area(
            "",
            height=280,
            key=f"answer_{i}",
            label_visibility="collapsed",
            placeholder="Write your answer here..."
        )

    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ Previous"):
            if st.session_state["current_question"] > 0:
                st.session_state["current_question"] -= 1
                st.rerun()
    with nav2:
        if st.button("➡️ Next"):
            if st.session_state["current_question"] < total_questions - 1:
                st.session_state["current_question"] += 1
                st.rerun()

    st.write("")
    if st.button("✅ Submit Interview", type="primary"):
        st.session_state["submitted"] = True
        st.markdown("<div class='lc-section-label'>📊 Submission Results</div>", unsafe_allow_html=True)
        st.header("Interview Results")

        total_score = 0

        for idx, q in enumerate(st.session_state["questions"]):

            ans = st.session_state.get(f"answer_{idx}", "")
            score = evaluate_answer(q, ans)
            total_score += score
            verdict = get_verdict(score)

            st.markdown(
                f"""
                <div class="lc-verdict-banner" style="background:rgba(0,0,0,0.25); border:1px solid {verdict['color']};">
                    <span style="color:{verdict['color']};">●</span>
                    <span style="color:{verdict['color']};">{verdict['label']}</span>
                    <span style="margin-left:auto; color:var(--lc-text-dim); font-size:14px;">Question {idx + 1} · Score: {score}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander(f"View Question {idx + 1} details"):
                st.write("**Question:**", q)
                st.write("**Your Score:**", f"{score}%")

        average_score = round(total_score / total_questions, 2)
        overall_verdict = get_verdict(average_score)

        st.markdown(
            f"""
            <div class="lc-verdict-banner" style="background:rgba(0,0,0,0.35); border:2px solid {overall_verdict['color']}; font-size:22px;">
                <span style="color:{overall_verdict['color']};">{overall_verdict['label']}</span>
                <span style="margin-left:auto; color:var(--lc-text); font-size:18px;">Overall Score: {average_score}%</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        report = generate_report(role, difficulty, average_score)

        with open(report, "rb") as file:
            st.download_button(
                "📥 Download Report",
                file,
                file_name="Interview_Report.pdf",
                mime="application/pdf"
            )

        st.balloons()
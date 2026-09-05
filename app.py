import os
import re
import streamlit as st
from pypdf import PdfReader
from google import genai


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="CareerLens | AI Career Copilot",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.12), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(139,92,246,0.10), transparent 25%),
        #0b1020;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main content */
.block-container {
    max-width: 1200px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

/* Hero */
.hero {
    padding: 45px 30px;
    border-radius: 25px;
    text-align: center;
    margin-bottom: 35px;
    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,0.20),
            rgba(139,92,246,0.12)
        );
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

.hero-badge {
    display: inline-block;
    padding: 7px 16px;
    border-radius: 50px;
    background: rgba(99,102,241,0.20);
    border: 1px solid rgba(129,140,248,0.35);
    color: #c7d2fe;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: 55px;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(
        90deg,
        #a5b4fc,
        #c4b5fd,
        #93c5fd
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #b8c0d9;
    font-size: 18px;
    max-width: 720px;
    margin: 15px auto 0 auto;
    line-height: 1.6;
}


/* Section titles */
.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #f8fafc;
    margin-top: 30px;
    margin-bottom: 15px;
}

.section-subtitle {
    color: #94a3b8;
    margin-bottom: 25px;
}


/* Cards */
.card {
    padding: 25px;
    border-radius: 18px;
    background: rgba(20,27,48,0.80);
    border: 1px solid rgba(148,163,184,0.12);
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    height: 100%;
}

.card h3 {
    margin-top: 0;
    color: #f1f5f9;
}

.card p {
    color: #94a3b8;
}


/* Step cards */
.step-card {
    padding: 20px;
    border-radius: 16px;
    background: rgba(20,27,48,0.75);
    border: 1px solid rgba(148,163,184,0.12);
    min-height: 130px;
}

.step-number {
    font-size: 14px;
    font-weight: 700;
    color: #a5b4fc;
}

.step-title {
    font-size: 18px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 8px;
}

.step-text {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 7px;
}


/* Analyze button */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    height: 55px;
    font-size: 17px;
    font-weight: 700;
    border: none;
    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    );
    color: white;
    box-shadow: 0 10px 30px rgba(99,102,241,0.25);
}

.stButton > button:hover {
    border: none;
    transform: translateY(-1px);
    box-shadow: 0 15px 35px rgba(99,102,241,0.35);
}


/* Inputs */
.stTextArea textarea,
.stSelectbox div,
[data-testid="stFileUploader"] {
    border-radius: 14px !important;
}


/* Metrics */
[data-testid="stMetric"] {
    background: rgba(20,27,48,0.85);
    border: 1px solid rgba(148,163,184,0.12);
    padding: 20px;
    border-radius: 18px;
}


/* Success */
[data-testid="stAlert"] {
    border-radius: 14px;
}


/* Footer */
.footer {
    text-align: center;
    margin-top: 50px;
    padding: 25px;
    color: #64748b;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-badge">
🤖 AI-POWERED CAREER ANALYSIS
</div>

<h1>CareerLens</h1>

<p>
Turn your resume into a personalized career roadmap.
Discover your job match, skill gaps, projects and interview preparation —
all in one place.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# API CONNECTION
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:

    st.error(
        "Gemini API key not found. "
        "Please set your GEMINI_API_KEY in Windows and restart the app."
    )

    st.stop()

client = genai.Client(api_key=api_key)


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    '<div class="section-title">✨ How CareerLens Works</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Three simple steps to understand your career readiness.'
    '</div>',
    unsafe_allow_html=True
)

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">STEP 01</div>
        <div class="step-title">📄 Upload Resume</div>
        <div class="step-text">
            Upload your current resume in PDF format.
        </div>
    </div>
    """, unsafe_allow_html=True)

with step2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">STEP 02</div>
        <div class="step-title">🎯 Choose Your Goal</div>
        <div class="step-text">
            Select the job role you want to target.
        </div>
    </div>
    """, unsafe_allow_html=True)

with step3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">STEP 03</div>
        <div class="step-title">🚀 Get Your Roadmap</div>
        <div class="step-text">
            Get AI-powered career insights and recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📋 Build Your Career Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Provide your resume and target job details below.'
    '</div>',
    unsafe_allow_html=True
)


left, right = st.columns(2, gap="large")


with left:

    st.markdown(
        '<div class="section-title">📄 Your Resume</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Upload a text-based PDF resume."
    )

    st.markdown(
        '<div class="section-title">🎯 Target Role</div>',
        unsafe_allow_html=True
    )

    target_role = st.selectbox(
        "What job are you targeting?",
        [
            "Software Engineer",
            "Data Analyst",
            "Data Scientist",
            "Machine Learning Engineer",
            "AI Engineer",
            "Business Analyst",
            "Full Stack Developer"
        ]
    )


with right:

    st.markdown(
        '<div class="section-title">💼 Job Description</div>',
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Paste the job description",
        height=260,
        placeholder=(
            "Example:\n"
            "We are looking for a fresher AI/ML Engineer...\n\n"
            "Requirements:\n"
            "- Python\n"
            "- Machine Learning\n"
            "- SQL\n"
            "- Deep Learning"
        )
    )


st.write("")


# ============================================================
# PDF FUNCTION
# ============================================================

def extract_resume_text(pdf_file):

    reader = PdfReader(pdf_file)

    resume_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    return resume_text


# ============================================================
# GEMINI ANALYSIS
# ============================================================

def analyze_resume(resume_text, job_description, target_role):

    prompt = f"""

You are an expert technical recruiter, career coach and AI/ML hiring specialist.

You are analyzing an MCA student who wants to get a job in a good technology company.

TARGET JOB ROLE:
{target_role}

CANDIDATE RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Analyze the candidate carefully.

IMPORTANT RULES:

1. Do NOT invent any skills, experience, education, achievements or projects.
2. Only use information actually present in the resume.
3. Clearly identify missing skills.
4. Keep the advice practical for an MCA student.
5. Be honest about the candidate's current level.
6. Use simple and understandable language.
7. Give specific recommendations instead of generic advice.

Give the answer using these sections:

## 1. OVERALL MATCH

Give an estimated match percentage from 0 to 100.

Explain why the candidate matches or does not match the job.

## 2. SKILLS ALREADY PRESENT

Separate the skills into:

### Programming
### AI/ML
### Data/SQL
### Tools
### Other Technical Skills

## 3. MISSING SKILLS

Find important skills from the job description that are missing or weak.

For each skill provide:

- Skill
- Why it matters
- Priority: HIGH / MEDIUM / LOW

## 4. LEARNING ROADMAP

Create a practical roadmap.

### HIGH PRIORITY
### MEDIUM PRIORITY
### LOW PRIORITY

Give specific things to learn.

## 5. PROJECT RECOMMENDATIONS

Suggest 3 impressive but realistic projects for this candidate.

For each project provide:

Project Name
Problem Solved
Main Features
Technologies
Why it is impressive

## 6. INTERVIEW PREPARATION

Give:

### 5 Technical Questions
### 5 HR Questions
### 5 Resume-Based Questions

Give a short hint for each answer.

## 7. RESUME IMPROVEMENTS

Give 5 specific improvements.

Focus on:

- Project descriptions
- Technical skills
- Keywords
- Achievements
- Recruiter readability

## 8. FINAL VERDICT

Give:

Current Level
Biggest Strength
Biggest Weakness
Most Important Skill to Learn
Most Important Project to Build
Next Step

End with a short motivational recommendation.

"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.write("")

analyze_button = st.button(
    "🚀 Analyze My Career",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if uploaded_file is None:

        st.warning("⚠️ Please upload your resume first.")

    elif not job_description.strip():

        st.warning("⚠️ Please paste a job description.")

    else:

        try:

            # Read resume
            with st.spinner("📄 Reading your resume..."):

                resume_text = extract_resume_text(
                    uploaded_file
                )


            if not resume_text.strip():

                st.error(
                    "❌ I could not read text from this PDF. "
                    "Please upload a normal text-based PDF."
                )

            else:

                # Gemini analysis
                with st.spinner(
                    "🤖 CareerLens AI is analyzing your profile..."
                ):

                    result = analyze_resume(
                        resume_text,
                        job_description,
                        target_role
                    )


                # Success
                st.success(
                    "✅ Career analysis completed successfully!"
                )

                st.write("")


                # ====================================================
                # MATCH SCORE
                # ====================================================

                match = re.search(
                    r'(\d{1,3})\s*%',
                    result
                )

                if match:

                    score = int(match.group(1))

                    if score > 100:
                        score = 100

                else:

                    score = 0


                st.markdown(
                    '<div class="section-title">'
                    '📊 Your Career Snapshot'
                    '</div>',
                    unsafe_allow_html=True
                )


                m1, m2, m3, m4 = st.columns(4)

                with m1:
                    st.metric(
                        "🎯 Job Match",
                        f"{score}%"
                    )

                with m2:
                    st.metric(
                        "💼 Target Role",
                        target_role
                    )

                with m3:
                    st.metric(
                        "📄 Resume",
                        "Analyzed"
                    )

                with m4:
                    st.metric(
                        "🤖 AI Status",
                        "Complete"
                    )


                st.write("")


                # ====================================================
                # ANALYSIS TABS
                # ====================================================

                st.markdown(
                    '<div class="section-title">'
                    '🔍 Detailed Career Analysis'
                    '</div>',
                    unsafe_allow_html=True
                )


                tab1, tab2, tab3, tab4 = st.tabs(
                    [
                        "📊 Overview",
                        "🧠 Skills & Roadmap",
                        "🚀 Projects",
                        "🎤 Interview & Resume"
                    ]
                )


                # ----------------------------------------------------
                # TAB 1
                # ----------------------------------------------------

                with tab1:

                    st.markdown(
                        "### 📊 Overall Career Assessment"
                    )

                    st.markdown(result)


                # ----------------------------------------------------
                # TAB 2
                # ----------------------------------------------------

                with tab2:

                    st.markdown(
                        "### 🧠 Skills & Learning Roadmap"
                    )

                    # Try to extract relevant sections
                    skill_match = re.search(
                        r'## 2\..*?(?=## 3\.|$)',
                        result,
                        re.S
                    )

                    missing_match = re.search(
                        r'## 3\..*?(?=## 4\.|$)',
                        result,
                        re.S
                    )

                    roadmap_match = re.search(
                        r'## 4\..*?(?=## 5\.|$)',
                        result,
                        re.S
                    )

                    if skill_match:
                        st.markdown(skill_match.group(0))

                    if missing_match:
                        st.markdown(missing_match.group(0))

                    if roadmap_match:
                        st.markdown(roadmap_match.group(0))


                # ----------------------------------------------------
                # TAB 3
                # ----------------------------------------------------

                with tab3:

                    st.markdown(
                        "### 🚀 Recommended Projects"
                    )

                    project_match = re.search(
                        r'## 5\..*?(?=## 6\.|$)',
                        result,
                        re.S
                    )

                    if project_match:

                        st.markdown(
                            project_match.group(0)
                        )

                    else:

                        st.markdown(result)


                # ----------------------------------------------------
                # TAB 4
                # ----------------------------------------------------

                with tab4:

                    st.markdown(
                        "### 🎤 Interview Preparation"
                    )

                    interview_match = re.search(
                        r'## 6\..*?(?=## 7\.|$)',
                        result,
                        re.S
                    )

                    if interview_match:

                        st.markdown(
                            interview_match.group(0)
                        )


                    st.markdown(
                        "### 📝 Resume Improvements"
                    )

                    resume_match = re.search(
                        r'## 7\..*?(?=## 8\.|$)',
                        result,
                        re.S
                    )

                    if resume_match:

                        st.markdown(
                            resume_match.group(0)
                        )


                # ====================================================
                # FINAL VERDICT
                # ====================================================

                final_match = re.search(
                    r'## 8\..*',
                    result,
                    re.S
                )

                if final_match:

                    st.write("")

                    st.markdown(
                        '<div class="section-title">'
                        '🎯 Final Career Verdict'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        final_match.group(0)
                    )


                # ====================================================
                # FOOTER MESSAGE
                # ====================================================

                st.info(
                    "💡 CareerLens provides AI-powered career guidance "
                    "based on your resume and the selected job description. "
                    "It does not guarantee employment."
                )


        except Exception as error:

            st.error(
                "❌ Something went wrong."
            )

            st.code(str(error))


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

CareerLens © 2026 • AI Career Copilot

<br><br>

Built with Python • Streamlit • Gemini AI

</div>
""", unsafe_allow_html=True)
import io
import re
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch


# ============================================================
# ASLA AI STUDIO
# Streamlit + Python
# ============================================================

st.set_page_config(
    page_title="ASLA AI Studio",
    page_icon="👾",
    layout="wide",
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    max-width: 1250px;
}
.hero {
    padding: 28px;
    border-radius: 20px;
    background: linear-gradient(120deg, #fff0f5 0%, #eef4ff 52%, #e9fbf5 100%);
    color: #29324a;
    border: 1px solid #e5e8f5;
    box-shadow: 0 8px 24px rgba(91, 103, 145, 0.08);
    margin-bottom: 1rem;
}
.hero h1 {
    color: #3f4568;
    margin-bottom: .35rem;
}
.hero p {
    color: #626b85;
    margin-bottom: 0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff5f8 0%, #f3f5ff 55%, #effbf7 100%);
}
.stButton > button, .stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid #d9dff1;
}
[data-testid="stMetric"] {
    background: #fbfaff;
    border: 1px solid #eceafa;
    padding: 14px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "resume": {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "desired_role": "",
        "summary": "",
        "education": "",
        "experience": "",
        "projects": "",
        "technical_skills": "",
        "soft_skills": "",
        "certifications": "",
        "achievements": "",
        "languages": "",
    },
    "saved_jobs": [],
    "assessment_history": [],
    "roadmap": [],
    "image_history": [],
    "skill_report": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        if isinstance(value, dict):
            st.session_state[key] = value.copy()
        elif isinstance(value, list):
            st.session_state[key] = value.copy()
        else:
            st.session_state[key] = value


# ============================================================
# HELPERS
# ============================================================

def header(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def create_resume_pdf(resume):
    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    styles = getSampleStyleSheet()
    content = []

    name = resume["name"].strip() or "Your Name"
    content.append(Paragraph(name, styles["Title"]))

    contact = " | ".join(
        value for value in [
            resume["email"],
            resume["phone"],
            resume["location"],
        ] if value.strip()
    )

    if contact:
        content.append(Paragraph(contact, styles["Normal"]))

    content.append(Spacer(1, 12))

    sections = [
        ("Professional Summary", "summary"),
        ("Education", "education"),
        ("Experience", "experience"),
        ("Projects", "projects"),
        ("Technical Skills", "technical_skills"),
        ("Soft Skills", "soft_skills"),
        ("Certifications", "certifications"),
        ("Achievements", "achievements"),
        ("Languages", "languages"),
    ]

    for section_title, key in sections:
        text = resume.get(key, "").strip()

        if text:
            content.append(
                Paragraph(section_title, styles["Heading2"])
            )

            for line in text.splitlines():
                if line.strip():
                    safe_line = (
                        line.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    )
                    content.append(
                        Paragraph(safe_line, styles["BodyText"])
                    )
                    content.append(Spacer(1, 4))

    document.build(content)
    return buffer.getvalue()


SKILL_GROUPS = {
    "Programming": [
        "python", "javascript", "typescript", "java",
        "sql", "html", "css", "c++",
    ],
    "Web Development": [
        "streamlit", "react", "next.js", "node.js",
        "fastapi", "django", "flask",
    ],
    "Data and AI": [
        "pandas", "numpy", "machine learning",
        "data analysis", "openai", "tensorflow",
    ],
    "Tools and Cloud": [
        "git", "github", "docker", "aws",
        "azure", "linux", "excel",
    ],
    "Professional Skills": [
        "communication", "leadership", "teamwork",
        "problem solving", "project management",
    ],
}


def find_skills(text):
    text = text.lower()
    found = set()

    for skills in SKILL_GROUPS.values():
        for skill in skills:
            if re.search(
                r"(?<!\w)" + re.escape(skill) + r"(?!\w)",
                text,
            ):
                found.add(skill)

    return found


def quiz_level(score):
    if score >= 80:
        return "Advanced on this quiz"
    elif score >= 60:
        return "Intermediate on this quiz"
    elif score >= 40:
        return "Developing"
    return "Beginner"


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.title("👾 ASLA AI Studio")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Image Studio",
            "Resume Builder",
            "Job Discovery",
            "Skills Analyzer",
            "Assessments",
            "Career Fit & Roadmap",
            "Settings",
        ],
    )

    st.divider()
    st.caption("Local prototype")


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    header(
        "Welcome to ASLA AI Studio",
        "Create, learn, assess your skills, and plan your career.",
    )

    resume = st.session_state["resume"]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Resume fields completed",
        sum(bool(v.strip()) for v in resume.values()),
    )

    c2.metric(
        "Saved jobs",
        len(st.session_state["saved_jobs"]),
    )

    c3.metric(
        "Assessments completed",
        len(st.session_state["assessment_history"]),
    )

    c4.metric(
        "Roadmap items",
        len(st.session_state["roadmap"]),
    )

    st.subheader("Your workspace")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🖼️ Image Studio")
        st.write("Resize, compress, and convert images.")

        st.markdown("### 📄 Resume Builder")
        st.write("Create a resume and export it as a PDF.")

        st.markdown("### 💼 Job Discovery")
        st.write("Save opportunities and track applications.")

    with col2:
        st.markdown("### 🎯 Skills Analyzer")
        st.write("Compare your skills with a target role.")

        st.markdown("### 🧠 Assessments")
        st.write("Test your knowledge with practice quizzes.")

        st.markdown("### 🚀 Career Roadmap")
        st.write("Organize learning goals and track progress.")

    st.subheader("Recent assessments")

    if st.session_state["assessment_history"]:
        st.dataframe(
            pd.DataFrame(st.session_state["assessment_history"]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Complete an assessment to see your results here.")


# ============================================================
# IMAGE STUDIO
# ============================================================

elif page == "Image Studio":

    logo_path = Path(__file__).parent / "logo.png"

    if logo_path.exists():
        logo_col, title_col = st.columns([1, 4])

        with logo_col:
            st.image(str(logo_path), width=110)

        with title_col:
            header(
                "AI Image Studio",
                "Resize, compress, convert, and remove image backgrounds.",
            )
    else:
        header(
            "AI Image Studio",
            "Resize, compress, convert, and remove image backgrounds.",
        )

    tab1, tab2, tab3 = st.tabs([
        "Resize Image",
        "Compress / Convert",
        "Background Removal",
    ])

    # ---------------- RESIZE IMAGE ----------------

    with tab1:

        uploaded = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="resize_upload",
        )

        if uploaded:
            try:
                image = ImageOps.exif_transpose(
                    Image.open(uploaded)
                ).copy()

                st.image(
                    image,
                    caption=f"Original: {image.width} × {image.height}",
                    use_container_width=True,
                )

                col_width, col_height = st.columns(2)

                with col_width:
                    width = st.number_input(
                        "Output width (pixels)",
                        min_value=1,
                        max_value=12000,
                        value=image.width,
                        key="resize_width",
                    )

                with col_height:
                    height = st.number_input(
                        "Output height (pixels)",
                        min_value=1,
                        max_value=12000,
                        value=image.height,
                        key="resize_height",
                    )

                keep_ratio = st.checkbox(
                    "Keep original aspect ratio",
                    value=True,
                    key="resize_keep_ratio",
                )

                if st.button("Resize Image", type="primary"):

                    output_width = int(width)
                    output_height = int(height)

                    if keep_ratio:
                        ratio = image.width / image.height
                        output_height = max(
                            1, round(output_width / ratio)
                        )

                    result = image.resize(
                        (output_width, output_height),
                        Image.Resampling.LANCZOS,
                    )

                    output = io.BytesIO()

                    if "A" in result.getbands():
                        output_format = "PNG"
                    else:
                        output_format = "JPEG"
                        result = result.convert("RGB")

                    result.save(output, format=output_format)
                    result_bytes = output.getvalue()

                    before_col, after_col = st.columns(2)

                    with before_col:
                        st.image(
                            image,
                            caption="Before",
                            use_container_width=True,
                        )

                    with after_col:
                        st.image(
                            result,
                            caption=(
                                f"After: {result.width} × "
                                f"{result.height}"
                            ),
                            use_container_width=True,
                        )

                    st.download_button(
                        "Download Resized Image",
                        data=result_bytes,
                        file_name=f"resized.{output_format.lower()}",
                        mime=f"image/{output_format.lower()}",
                    )

            except Exception as error:
                st.error(f"Image processing failed: {error}")

    # ---------------- COMPRESS / CONVERT ----------------

    with tab2:

        uploaded = st.file_uploader(
            "Choose an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="compress_upload",
        )

        if uploaded:

            try:
                image = ImageOps.exif_transpose(
                    Image.open(uploaded)
                ).copy()

                original_bytes = uploaded.getvalue()

                output_format = st.selectbox(
                    "Output format",
                    ["JPEG", "PNG", "WEBP"],
                )

                quality = st.slider(
                    "Quality (JPEG / WEBP)",
                    min_value=20,
                    max_value=95,
                    value=80,
                )

                if st.button("Compress / Convert", type="primary"):

                    output = io.BytesIO()
                    result = image.copy()

                    if output_format == "JPEG":

                        if result.mode not in ("RGB", "L"):
                            if "A" in result.getbands():
                                background = Image.new(
                                    "RGB", result.size, "white"
                                )
                                background.paste(
                                    result,
                                    mask=result.getchannel("A"),
                                )
                                result = background
                            else:
                                result = result.convert("RGB")

                        result.save(
                            output,
                            format="JPEG",
                            quality=quality,
                            optimize=True,
                        )

                        extension = "jpg"
                        mime = "image/jpeg"

                    elif output_format == "WEBP":

                        result.save(
                            output,
                            format="WEBP",
                            quality=quality,
                            method=6,
                        )

                        extension = "webp"
                        mime = "image/webp"

                    else:

                        result.save(
                            output,
                            format="PNG",
                            optimize=True,
                        )

                        extension = "png"
                        mime = "image/png"

                    result_bytes = output.getvalue()

                    original_size = len(original_bytes)
                    output_size = len(result_bytes)

                    st.write(f"Original size: {original_size:,} bytes")
                    st.write(f"Output size: {output_size:,} bytes")

                    if original_size > 0:
                        change = (
                            1 - output_size / original_size
                        ) * 100

                        if change >= 0:
                            st.success(
                                f"File size reduced by {change:.1f}%."
                            )
                        else:
                            st.info(
                                f"Output is {abs(change):.1f}% larger "
                                "than the original."
                            )

                    st.image(result, use_container_width=True)

                    st.download_button(
                        "Download Processed Image",
                        data=result_bytes,
                        file_name=f"processed.{extension}",
                        mime=mime,
                    )

            except Exception as error:
                st.error(f"Conversion failed: {error}")

    # ---------------- BACKGROUND REMOVAL ----------------

    with tab3:

        st.write(
            "Remove an image background using a locally installed model."
        )

        st.caption(
            "The first run may download model files and may take longer."
        )

        uploaded = st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="background_upload",
        )

        if uploaded and st.button(
            "Remove Background",
            type="primary",
        ):

            try:
                from rembg import remove

                result_bytes = remove(uploaded.getvalue())

                result_image = Image.open(
                    io.BytesIO(result_bytes)
                ).convert("RGBA")

                st.image(
                    result_image,
                    caption="Transparent background preview",
                    use_container_width=True,
                )

                st.download_button(
                    "Download Transparent PNG",
                    data=result_bytes,
                    file_name="background-removed.png",
                    mime="image/png",
                )

            except ImportError:
                st.error(
                    'Background removal is not installed. Run: '
                    'pip install "rembg[cpu]"'
                )

            except Exception as error:
                st.error(f"Background removal failed: {error}")


# ============================================================
# RESUME BUILDER
# ============================================================

elif page == "Resume Builder":

    header(
        "Resume Builder",
        "Create and export your professional resume.",
    )

    resume = st.session_state["resume"]

    with st.form("resume_form"):

        st.subheader("Personal details")

        resume["name"] = st.text_input(
            "Full name",
            value=resume["name"],
        )

        resume["email"] = st.text_input(
            "Email",
            value=resume["email"],
        )

        resume["phone"] = st.text_input(
            "Phone",
            value=resume["phone"],
        )

        resume["location"] = st.text_input(
            "City / Location",
            value=resume["location"],
        )

        resume["desired_role"] = st.text_input(
            "Desired job role",
            value=resume["desired_role"],
        )

        st.subheader("Resume sections")

        fields = [
            ("summary", "Professional summary"),
            ("education", "Education"),
            ("experience", "Work experience / internships"),
            ("projects", "Projects"),
            ("technical_skills", "Technical skills"),
            ("soft_skills", "Soft skills"),
            ("certifications", "Certifications"),
            ("achievements", "Achievements"),
            ("languages", "Languages"),
        ]

        for key, label in fields:
            resume[key] = st.text_area(
                label,
                value=resume[key],
                key=f"resume_{key}",
            )

        submitted = st.form_submit_button(
            "Save Resume",
            type="primary",
        )

        if submitted:
            st.session_state["resume"] = resume.copy()
            st.success("Resume saved for this session.")

    st.subheader("Resume preview")

    st.title(resume["name"] or "Your Name")

    contact_details = [
        resume["desired_role"],
        resume["email"],
        resume["phone"],
        resume["location"],
    ]

    st.caption(
        " | ".join(
            value for value in contact_details if value.strip()
        )
    )

    for key, label in fields:
        if resume[key].strip():
            st.markdown(f"### {label}")
            st.write(resume[key])

    pdf = create_resume_pdf(resume)

    st.download_button(
        "Export Resume as PDF",
        data=pdf,
        file_name="asla-resume.pdf",
        mime="application/pdf",
        type="primary",
    )


# ============================================================
# JOB DISCOVERY
# ============================================================

elif page == "Job Discovery":

    header(
        "Job Discovery",
        "Save job opportunities and track applications.",
    )

    st.warning(
        "Live job listings are not connected yet. "
        "This page does not create fake job listings."
    )

    with st.form("job_form"):

        title = st.text_input("Job title")
        company = st.text_input("Company")
        location = st.text_input("Location")
        url = st.text_input("Original job URL")
        notes = st.text_area("Notes / requirements")

        submitted = st.form_submit_button("Save Job")

        if submitted:

            if not title.strip() or not company.strip():
                st.error("Job title and company are required.")

            elif url and not url.startswith(("https://", "http://")):
                st.error("Enter a valid http:// or https:// URL.")

            else:

                st.session_state["saved_jobs"].append({
                    "title": title.strip(),
                    "company": company.strip(),
                    "location": location.strip(),
                    "url": url.strip(),
                    "notes": notes.strip(),
                    "status": "Saved",
                    "date_saved": datetime.now().strftime("%Y-%m-%d"),
                })

                st.success("Job saved.")

    jobs = st.session_state["saved_jobs"]

    if jobs:

        st.subheader("Saved jobs")

        df = pd.DataFrame(jobs)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        selected = st.number_input(
            "Job row to update",
            min_value=1,
            max_value=len(jobs),
            value=1,
            step=1,
        )

        status = st.selectbox(
            "Application status",
            [
                "Saved",
                "Applied",
                "Interview",
                "Offer",
                "Rejected",
                "Archived",
            ],
        )

        if st.button("Update Job Status"):
            jobs[int(selected) - 1]["status"] = status
            st.success("Status updated.")

        st.download_button(
            "Export Jobs as CSV",
            data=pd.DataFrame(jobs).to_csv(index=False),
            file_name="saved-jobs.csv",
            mime="text/csv",
        )

    else:
        st.info("You haven't saved any jobs yet.")


# ============================================================
# SKILLS ANALYZER
# ============================================================

elif page == "Skills Analyzer":

    header(
        "Skills Analyzer",
        "Compare your skills with the requirements of a target role.",
    )

    st.caption(
        "This first version uses keyword matching. "
        "It is not an official competency assessment."
    )

    resume_text = st.text_area(
        "Paste your resume, skills, projects, or experience",
        height=200,
    )

    target_role = st.text_input(
        "Target role",
        value=st.session_state["resume"]["desired_role"],
    )

    job_description = st.text_area(
        "Paste target job description",
        height=180,
    )

    if st.button("Analyze Skills", type="primary"):

        user_skills = find_skills(resume_text)

        required_skills = find_skills(
            target_role + " " + job_description
        )

        st.session_state["skill_report"] = {
            "role": target_role,
            "detected": sorted(user_skills),
            "matched": sorted(user_skills & required_skills),
            "gaps": sorted(required_skills - user_skills),
        }

    report = st.session_state["skill_report"]

    if report:

        c1, c2, c3 = st.columns(3)

        c1.metric("Detected Skills", len(report["detected"]))
        c2.metric("Matched Keywords", len(report["matched"]))
        c3.metric("Potential Gaps", len(report["gaps"]))

        st.subheader("Detected skills")
        st.write(
            ", ".join(report["detected"])
            or "No supported keywords found."
        )

        st.subheader("Matched keywords")
        st.write(
            ", ".join(report["matched"])
            or "No keyword overlap found."
        )

        st.subheader("Potential skill gaps")
        st.write(
            ", ".join(report["gaps"])
            or "No gaps found among supported keywords."
        )

        st.caption(
            "Missing keywords do not prove that you lack a skill. "
            "Review each result manually."
        )

        if report["gaps"] and st.button("Add Gaps to Roadmap"):

            for skill in report["gaps"]:
                st.session_state["roadmap"].append({
                    "skill": skill,
                    "priority": "Medium",
                    "activity": f"Practice {skill} and build a project",
                    "done": False,
                })

            st.success("Skill gaps added to your roadmap.")


# ============================================================
# ASSESSMENTS
# ============================================================

elif page == "Assessments":

    header(
        "Skill Assessments",
        "Take a quiz and receive learning feedback.",
    )

    questions = {
        "Python": [
            {
                "q": "Which Python type is mutable?",
                "options": ["tuple", "str", "list", "int"],
                "answer": "list",
                "why": "A list can be modified after creation.",
            },
            {
                "q": "What does len([2, 4, 6]) return?",
                "options": ["2", "3", "6", "12"],
                "answer": "3",
                "why": "The list contains three elements.",
            },
            {
                "q": "Which keyword defines a function?",
                "options": ["func", "function", "def", "lambda"],
                "answer": "def",
                "why": "The def keyword defines a named function.",
            },
            {
                "q": "What does 7 // 2 return?",
                "options": ["3.5", "3", "4", "1"],
                "answer": "3",
                "why": "The // operator performs floor division.",
            },
            {
                "q": "Which structure stores key-value pairs?",
                "options": ["list", "dict", "set", "tuple"],
                "answer": "dict",
                "why": "A dictionary maps keys to values.",
            },
        ],
        "Web Development": [
            {
                "q": "What does CSS primarily control?",
                "options": ["Styling", "Database storage", "DNS", "CPU"],
                "answer": "Styling",
                "why": "CSS controls the appearance and layout of web pages.",
            },
            {
                "q": "Which HTTP method typically retrieves data?",
                "options": ["POST", "GET", "DELETE", "PATCH"],
                "answer": "GET",
                "why": "GET is typically used to retrieve a resource.",
            },
            {
                "q": "What is an API?",
                "options": [
                    "A color palette",
                    "A software communication interface",
                    "A file extension",
                    "A CPU",
                ],
                "answer": "A software communication interface",
                "why": "APIs define how software components communicate.",
            },
            {
                "q": "What is responsive design?",
                "options": [
                    "Desktop only",
                    "Layouts adapting to screen sizes",
                    "A database",
                    "A programming language",
                ],
                "answer": "Layouts adapting to different devices",
                "why": "Responsive layouts adapt to different devices.",
            },
            {
                "q": "Where should private API keys be stored?",
                "options": [
                    "Public frontend code",
                    "A public README",
                    "Server-side environment variables",
                    "Image alt text",
                ],
                "answer": "Server-side environment variables",
                "why": "Private keys should not be exposed publicly.",
            },
        ],
    }

    topic = st.selectbox("Choose a topic", list(questions.keys()))

    with st.form(f"quiz_{topic}"):

        answers = {}

        for index, question in enumerate(questions[topic]):

            st.markdown(
                f"**{index + 1}. {question['q']}**"
            )

            answers[index] = st.radio(
                "Choose an answer",
                question["options"],
                key=f"{topic}_{index}",
                index=None,
            )

        submitted = st.form_submit_button(
            "Submit Assessment",
            type="primary",
        )

    if submitted:

        quiz = questions[topic]

        correct = sum(
            answers[i] == quiz[i]["answer"]
            for i in range(len(quiz))
        )

        score = round(correct / len(quiz) * 100)

        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "topic": topic,
            "score": score,
            "correct": correct,
            "total": len(quiz),
            "level": quiz_level(score),
        }

        st.session_state["assessment_history"].append(result)

        st.subheader("Your Result")
        st.metric("Score", f"{score}%", quiz_level(score))

        for i, question in enumerate(quiz):

            st.markdown(f"**{i + 1}. {question['q']}**")

            st.write(
                f"Your answer: {answers[i] or 'Not answered'}"
            )

            st.write(
                f"Correct answer: {question['answer']}"
            )

            st.caption(question["why"])

        st.warning(
            "This quiz measures only a small sample of knowledge. "
            "It is not a certification or a complete measure of ability."
        )

    if st.session_state["assessment_history"]:

        st.subheader("Assessment History")

        history_df = pd.DataFrame(
            st.session_state["assessment_history"]
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Export Assessment History",
            data=history_df.to_csv(index=False),
            file_name="assessment-history.csv",
            mime="text/csv",
        )


# ============================================================
# CAREER FIT AND ROADMAP
# ============================================================

elif page == "Career Fit & Roadmap":

    header(
        "Career Fit & Learning Roadmap",
        "Review potential skill gaps and plan your next steps.",
    )

    report = st.session_state["skill_report"]

    if report:

        matched = report["matched"]
        gaps = report["gaps"]

        st.subheader(
            f"Target role: {report['role'] or 'Not specified'}"
        )

        if len(matched) >= 5 and len(gaps) <= 2:
            fit = "Stronger keyword alignment"
        elif len(matched) >= 2:
            fit = "Developing toward the role"
        else:
            fit = "More evidence needed"

        st.metric("Rule-based alignment", fit)

        st.write("**Matched keywords:**", ", ".join(matched) or "None")
        st.write("**Potential gaps:**", ", ".join(gaps) or "None")

        st.caption(
            "This is a simple keyword-based indicator, not a prediction "
            "of hiring success."
        )

    else:
        st.info("Use Skills Analyzer to compare yourself with a target role.")

    st.subheader("Your Learning Roadmap")

    with st.form("roadmap_form"):

        skill = st.text_input("Skill or goal")

        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"],
        )

        activity = st.text_input(
            "Practice activity or project"
        )

        submitted = st.form_submit_button("Add Roadmap Item")

        if submitted:

            if skill.strip():

                st.session_state["roadmap"].append({
                    "skill": skill.strip(),
                    "priority": priority,
                    "activity": activity.strip(),
                    "done": False,
                })

                st.success("Roadmap item added.")

            else:
                st.error("Enter a skill or goal.")

    roadmap = st.session_state["roadmap"]

    if roadmap:

        for index, item in enumerate(roadmap):

            col1, col2, col3, col4 = st.columns([1, 2, 1, 3])

            item["done"] = col1.checkbox(
                "Done",
                value=item["done"],
                key=f"roadmap_{index}",
            )

            col2.write(item["skill"])
            col3.write(item["priority"])
            col4.write(item["activity"])

        completed = sum(item["done"] for item in roadmap)

        st.progress(
            completed / len(roadmap),
            text=f"{completed} of {len(roadmap)} items completed",
        )

        st.download_button(
            "Export Roadmap as JSON",
            data=json.dumps(roadmap, indent=2),
            file_name="career-roadmap.json",
            mime="application/json",
        )

    else:
        st.info("Add your first roadmap item above.")


# ============================================================
# SETTINGS
# ============================================================

elif page == "Settings":

    header(
        "Settings and Integrations",
        "Review what is available in this starter version.",
    )

    st.subheader("Available now")

    st.markdown("""
    - Local image resizing and format conversion
    - Resume editing and PDF export
    - Keyword-based skills comparison
    - Built-in practice quizzes
    - Manual job tracking
    - Career roadmap
    """)

    st.subheader("Not connected yet")

    st.markdown("""
    - AI model API
    - Live job search API
    - User accounts and database
    - Cross-session persistence
    - Production deployment and security hardening
    """)

    st.subheader("Optional background-removal dependency")

    st.code('pip install "rembg[cpu]"')

    st.warning(
        "This is a local prototype. Data is held in Streamlit session state "
        "and may disappear when the session restarts. Add authentication, "
        "persistent storage, authorization, and security controls before "
        "deploying for multiple users."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ASLA AI Studio | Streamlit prototype | "
    "Review your resume and career decisions before relying on them."
)
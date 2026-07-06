import streamlit as st
import pandas as pd
import numpy as np
import random

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# SIDEBAR THEME
# -------------------------------------------------
st.sidebar.header("🎨 Theme")

theme = st.sidebar.selectbox(
    "Select Theme",
    ["Professional Blue", "Academic Green", "Analytics Purple", "Dark Mode"]
)

if theme == "Professional Blue":
    accent = "#2563eb"
    bg = "#f8fafc"
    card = "#ffffff"
    text = "#1e293b"
elif theme == "Academic Green":
    accent = "#059669"
    bg = "#f0fdf4"
    card = "#ffffff"
    text = "#064e3b"
elif theme == "Analytics Purple":
    accent = "#7c3aed"
    bg = "#faf5ff"
    card = "#ffffff"
    text = "#4c1d95"
else:
    accent = "#60a5fa"
    bg = "#0f172a"
    card = "#1e293b"
    text = "#f1f5f9"

# -------------------------------------------------
# CSS STYLING
# -------------------------------------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {bg} !important;
    background-image:
        radial-gradient(circle at 20% 20%, {accent}25, transparent 40%),
        radial-gradient(circle at 80% 0%, {accent}20, transparent 40%),
        radial-gradient(circle at 0% 80%, {accent}15, transparent 40%);
}}

[data-testid="stSidebar"] {{
    background-color: {card} !important;
}}

.card {{
    background: {card};
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}}

.metric {{
    background: linear-gradient(135deg, {accent}30, {card});
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
}}

h1, h2, h3, h4, p, label {{
    color: {text} !important;
}}

.stButton > button {{
    background: {accent};
    color: white;
    border-radius: 10px;
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="card">
<h1>📊 Student Performance Analysis</h1>
<p>Analyze relationship between Study Hours and Final Score</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["Name", "Roll No", "Course", "Study Hours", "Final Score"]
    )

# -------------------------------------------------
# DATA INPUT SECTION
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("## 📥 Add Student Data")

tab1, tab2, tab3 = st.tabs(["📂 Upload CSV", "✍️ Manual Entry", "🎲 Auto Generate"])

# -------- CSV UPLOAD --------
with tab1:
    file = st.file_uploader("Upload CSV File", type=["csv"])
    if file:
        df_csv = pd.read_csv(file)
        required = {"Name", "Roll No", "Course", "Study Hours", "Final Score"}
        if required.issubset(df_csv.columns):
            st.session_state.students = pd.concat(
                [st.session_state.students, df_csv], ignore_index=True
            )
            st.success("✅ CSV Data Added Successfully")
        else:
            st.error("❌ CSV columns are incorrect")

# -------- MANUAL ENTRY --------
with tab2:
    with st.form("manual_form"):
        name = st.text_input("Student Name")
        roll = st.text_input("Roll Number")
        course = st.selectbox(
            "Course", ["Maths", "Physics", "Chemistry", "CS", "English"]
        )
        hours = st.number_input("Study Hours", 0.0, 20.0)
        score = st.number_input("Final Score", 0.0, 100.0)
        submit = st.form_submit_button("➕ Add Student")

        if submit:
            if name and roll:
                new_row = pd.DataFrame(
                    [[name, roll, course, hours, score]],
                    columns=st.session_state.students.columns
                )
                st.session_state.students = pd.concat(
                    [st.session_state.students, new_row], ignore_index=True
                )
                st.success("✅ Student Added")
            else:
                st.warning("⚠️ Name and Roll Number required")

# -------- AUTO GENERATE --------
with tab3:
    if st.button("Generate 30 Students"):
        data = []
        for i in range(30):
            hrs = round(np.random.uniform(1, 10), 1)
            scr = min(100, max(35, 40 + hrs * 4 + np.random.normal(0, 8)))
            data.append([
                f"Student {i+1}",
                f"R{i+1}",
                random.choice(["Maths", "CS", "Physics"]),
                hrs,
                round(scr, 1)
            ])

        auto_df = pd.DataFrame(data, columns=st.session_state.students.columns)
        st.session_state.students = pd.concat(
            [st.session_state.students, auto_df], ignore_index=True
        )
        st.success("✅ Auto Data Generated")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# ANALYSIS SECTION
# -------------------------------------------------
if not st.session_state.students.empty:
    df = st.session_state.students

    # Quick Stats
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📊 Quick Statistics")

    corr = df["Study Hours"].corr(df["Final Score"]) if len(df) > 1 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(
        f"<div class='metric'><h2>{len(df)}</h2>Total Students</div>",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"<div class='metric'><h2>{df['Final Score'].mean():.1f}%</h2>Avg Score</div>",
        unsafe_allow_html=True
    )
    c3.markdown(
        f"<div class='metric'><h2>{df['Study Hours'].mean():.1f}</h2>Avg Hours</div>",
        unsafe_allow_html=True
    )
    c4.markdown(
        f"<div class='metric'><h2>{corr:.2f}</h2>Correlation</div>",
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Table
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📋 Student Table")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Scatter Plot
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📈 Study Hours vs Final Score")
    st.scatter_chart(df[["Study Hours", "Final Score"]])
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Add data using CSV, manual entry or auto-generate")

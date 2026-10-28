import streamlit as st
import pandas as pd
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Marks Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONSTANTS
# ============================================================

DATA_FILE = "students.csv"

SUBJECTS = [
    "Maths",
    "Science",
    "English",
    "Computer",
    "Hindi"
]


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if os.path.exists(DATA_FILE):

        df = pd.read_csv(DATA_FILE)

        if "Name" not in df.columns:
            df["Name"] = ""

        for subject in SUBJECTS:

            if subject not in df.columns:
                df[subject] = 0

            df[subject] = pd.to_numeric(
                df[subject],
                errors="coerce"
            ).fillna(0)

        return df[["Name"] + SUBJECTS]

    return pd.DataFrame(
        columns=["Name"] + SUBJECTS
    )


# ============================================================
# GRADE
# ============================================================

def get_grade(percentage):

    if percentage >= 90:
        return "A+"

    if percentage >= 80:
        return "A"

    if percentage >= 70:
        return "B"

    if percentage >= 60:
        return "C"

    if percentage >= 50:
        return "D"

    return "F"


# ============================================================
# RESULT
# ============================================================

def get_result(percentage):

    if percentage >= 40:
        return "Pass"

    return "Fail"


# ============================================================
# LOAD EXISTING STUDENTS
# ============================================================

df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📚 Add Student")

    st.write(
        "Enter student details and marks."
    )

    st.divider()

    name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

    marks = {}

    for subject in SUBJECTS:

        marks[subject] = st.number_input(
            subject,
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )

    st.divider()

    add_student = st.button(
        "➕ Add Student",
        type="primary",
        width="stretch"
    )

    if add_student:

        student_name = name.strip()

        existing_names = (
            df["Name"]
            .astype(str)
            .str.strip()
            .str.lower()
            .tolist()
        )

        if student_name == "":

            st.error(
                "Please enter student name."
            )

        elif student_name.lower() in existing_names:

            st.warning(
                "This student already exists."
            )

        else:

            new_student = {
                "Name": student_name,
                "Maths": marks["Maths"],
                "Science": marks["Science"],
                "English": marks["English"],
                "Computer": marks["Computer"],
                "Hindi": marks["Hindi"]
            }

            new_row = pd.DataFrame(
                [new_student]
            )

            df = pd.concat(
                [df, new_row],
                ignore_index=True
            )

            df.to_csv(
                DATA_FILE,
                index=False
            )

            st.success(
                f"{student_name} added successfully!"
            )

            st.rerun()

    st.divider()

    st.write(
        f"👥 Total Students: {len(df)}"
    )

    st.write(
        f"📚 Total Subjects: {len(SUBJECTS)}"
    )

    st.divider()

    clear_data = st.button(
        "🗑️ Clear All Students",
        width="stretch"
    )

    if clear_data:

        empty_df = pd.DataFrame(
            columns=["Name"] + SUBJECTS
        )

        empty_df.to_csv(
            DATA_FILE,
            index=False
        )

        st.success(
            "All student data cleared."
        )

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    "🎓 Student Marks Analyzer"
)

st.write(
    "Enter student details and analyze marks, "
    "percentage, grade and result."
)


# ============================================================
# NO STUDENT DATA
# ============================================================

if df.empty:

    st.info(
        "👈 Use the left sidebar to enter "
        "student name and marks."
    )

    st.stop()


# ============================================================
# CALCULATIONS
# ============================================================

df["Total"] = df[SUBJECTS].sum(
    axis=1
)

df["Average"] = df[SUBJECTS].mean(
    axis=1
).round(2)

df["Percentage"] = (
    df["Total"]
    / (len(SUBJECTS) * 100)
    * 100
).round(2)

df["Grade"] = df["Percentage"].apply(
    get_grade
)

df["Result"] = df["Percentage"].apply(
    get_result
)


# ============================================================
# CLASS STATISTICS
# ============================================================

topper_index = df["Percentage"].idxmax()

topper = df.loc[topper_index]

class_average = df["Percentage"].mean()

pass_count = (
    df["Result"] == "Pass"
).sum()

pass_rate = (
    pass_count / len(df)
) * 100


# ============================================================
# CLASS OVERVIEW
# ============================================================

st.divider()

st.subheader(
    "📊 Class Overview"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👥 Total Students",
        len(df)
    )


with col2:

    st.metric(
        "🏆 Topper",
        str(topper["Name"])
    )


with col3:

    st.metric(
        "📊 Class Average",
        f"{class_average:.2f}%"
    )


with col4:

    st.metric(
        "✅ Pass Rate",
        f"{pass_rate:.1f}%"
    )


# ============================================================
# PERFORMANCE TABLE
# ============================================================

st.divider()

st.subheader(
    "📋 Student Performance Report"
)

display_columns = [
    "Name",
    "Maths",
    "Science",
    "English",
    "Computer",
    "Hindi",
    "Total",
    "Average",
    "Percentage",
    "Grade",
    "Result"
]

st.dataframe(
    df[display_columns],
    width="stretch",
    hide_index=True
)


# ============================================================
# CHARTS
# ============================================================

st.divider()

chart_left, chart_right = st.columns(2)


# ============================================================
# STUDENT PERCENTAGE CHART
# ============================================================

with chart_left:

    st.subheader(
        "📈 Student Percentage"
    )

    percentage_chart = (
        df.set_index("Name")[["Percentage"]]
    )

    st.bar_chart(
        percentage_chart
    )


# ============================================================
# SUBJECT AVERAGE CHART
# ============================================================

with chart_right:

    st.subheader(
        "📚 Subject Average"
    )

    subject_average = df[
        SUBJECTS
    ].mean()

    st.bar_chart(
        subject_average
    )


# ============================================================
# TOP PERFORMER
# ============================================================

st.divider()

st.subheader(
    "🏆 Top Performer"
)

st.success(
    f'{topper["Name"]} | '
    f'{topper["Percentage"]:.2f}% | '
    f'Grade {topper["Grade"]}'
)

st.write(
    f'Total Marks: '
    f'{topper["Total"]:.0f} / 500'
)


# ============================================================
# SUBJECT-WISE AVERAGE
# ============================================================

st.divider()

st.subheader(
    "📚 Subject-wise Average Marks"
)

subject_table = pd.DataFrame({
    "Subject": SUBJECTS,
    "Average Marks": [
        round(df[subject].mean(), 2)
        for subject in SUBJECTS
    ]
})

st.dataframe(
    subject_table,
    width="stretch",
    hide_index=True
)


# ============================================================
# EXPORT REPORT
# ============================================================

st.divider()

st.subheader(
    "📥 Export Report"
)

csv_data = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Analysis CSV",
    data=csv_data,
    file_name="student_marks_analysis.csv",
    mime="text/csv",
    width="stretch"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Student Marks Analyzer • "
    "Python + Pandas + Streamlit"
)
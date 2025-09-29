# grading_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# -------------------------- PASSWORD PROTECTION -------------------------- #
def check_password():
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #AB9984;">
            <h1>🎓 Welcome to the Grading App</h1>
            <p>Powered by <strong>School of Digital Health</strong></p>
            <p>Developed by <strong>Pn Afiqah Kamaruddin</strong></p>
        </div>
        """, unsafe_allow_html=True
    )

    def password_entered():
        if st.session_state["password"] == "letmein":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter Password:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Password:", type="password", on_change=password_entered, key="password")
        st.error("Incorrect password")
        return False
    else:
        return True

# -------------------------- MOTIVATIONAL FEEDBACK -------------------------- #
feedback_dict = {
    "A": [
        "Phenomenal performance! You’ve shown mastery, clarity, and confidence — keep inspiring others.",
        "Outstanding! You didn’t just answer, you taught the topic back to us with excellence.",
        "Superb! You’ve nailed accuracy, depth, and presentation — a true role model.",
        "Brilliant effort! Every detail was sharp and thoughtful. Keep shining at this level.",
        "Exceptional work — you’ve turned learning into leadership. Stay consistent, you’re unstoppable."
    ],
    "B": [
        "Strong effort! You’re very close to excellence — just a little polish will get you there.",
        "Great work overall. You’ve built a solid foundation — now aim for sharper accuracy.",
        "Well done! Your understanding is clear, and with more detail, you’ll hit the top band.",
        "Good progress! Keep stretching your explanations to unlock your full potential.",
        "You’re on the right track! Stay focused and keep refining your answers."
    ],
    "C": [
        "You’ve made a fair attempt — now let’s aim for stronger accuracy and detail.",
        "Decent effort, but more depth is needed. Push yourself a little more each time.",
        "You’re building the basics. Stay consistent, and growth will follow.",
        "Good start! Strengthening clarity and completeness will lift your grade higher.",
        "Don’t stop here — keep improving step by step, and you’ll surprise yourself."
    ],
    "D": [
        "This round was tough, but it’s only the beginning — you can improve with steady effort.",
        "Don’t be discouraged! Focus on the core concepts, and progress will come.",
        "Challenges help us grow. Keep practicing, and your results will rise.",
        "It’s a slow start, but every step forward counts. Believe in your progress.",
        "Stay motivated — even small improvements will lead to big achievements."
    ]
}

def get_feedback(percentage):
    if percentage >= 80:
        return random.choice(feedback_dict["A"])
    elif percentage >= 65:
        return random.choice(feedback_dict["B"])
    elif percentage >= 50:
        return random.choice(feedback_dict["C"])
    else:
        return random.choice(feedback_dict["D"])

def get_letter_grade(percentage):
    if percentage >= 80:
        return "A"
    elif percentage >= 65:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "D"

# -------------------------- APP START -------------------------- #
if check_password():
    st.title("📊 Tutorial Grading App")
    st.write("Secure grading system with **numerical rubric scoring** (0–4 per criterion).")

    # -------------------------- SIDEBAR - RUBRIC -------------------------- #
    st.sidebar.header("Marking Description Criteria (Rubric)")
    st.sidebar.markdown("""
    | Score | Percentage Range | Accuracy | Clarity | Depth | Completeness | Presentation |
    |-------|-----------------|---------|--------|-------|--------------|--------------|
    | **4 (Excellent)** | 80–100% | All correct, precise terminology | Well-structured, logical | Beyond basics | Fully addresses all parts | Neat, organised |
    | **3 (Good)**     | 65–79% | Mostly correct, minor errors | Generally clear | Good understanding | Minor omissions | Mostly neat |
    | **2 (Fair)**     | 50–64% | Several errors | Sometimes confusing | Basic understanding | Partial response | Somewhat disorganised |
    | **1 (Poor)**     | <50% | Many incorrect answers | Unclear | Very limited | Incomplete | Messy |
    | **0 (No Attempt)** | - | No evidence | No clarity | No depth | No completeness | No presentation |
    """, unsafe_allow_html=True)

    # -------------------------- TABS -------------------------- #
    tab2, tab3, tab4, tab5, tab_rubric = st.tabs(
        ["Marks Entry", "Student Scores", "Dashboard", "Import Students", "Rubric Reference"]
    )

    # -------------------------- TAB 2 - MARKS ENTRY -------------------------- #
    with tab2:
        st.header("Enter Student Marks")
        criteria = ["Accuracy", "Clarity", "Depth", "Completeness", "Presentation"]

        # Load student list
        student_list = None
        id_col, name_col = None, None
        try:
            student_list = pd.read_csv("student_list.csv")
            for c in student_list.columns:
                if "id" in c.lower(): id_col = c
                if "name" in c.lower(): name_col = c
            student_list = student_list.astype(str).apply(lambda x: x.str.strip())
        except FileNotFoundError:
            pass

        # Existing assessments
        try:
            scores_df = pd.read_csv("student_scores.csv")
            existing_assessments = scores_df["Assessment"].dropna().unique().tolist()
        except FileNotFoundError:
            existing_assessments = []

        col1, col2 = st.columns([1, 2])
        with col1:
            if student_list is not None and name_col and id_col:
                student_name = st.selectbox("Select Student Name", student_list[name_col].tolist())
                match = student_list.loc[student_list[name_col] == student_name, id_col]
                student_id = match.values[0] if not match.empty else "N/A"
                st.write(f"**Student ID:** {student_id}")
            else:
                student_id = st.text_input("Student ID")
                student_name = st.text_input("Student Name")

            assessment_options = ["-- New Assessment --"] + existing_assessments
            selected_assessment = st.selectbox("Select Assessment", assessment_options)
            if selected_assessment == "-- New Assessment --":
                assessment = st.text_input("Enter New Assessment Name")
            else:
                assessment = selected_assessment

        with col2:
            scores = {}
            for crit in criteria:
                scores[crit] = st.number_input(f"{crit} (0–4)", min_value=0, max_value=4, value=0, step=1)

        total = sum(scores.values())
        max_score = len(criteria) * 4
        percentage = (total / max_score) * 100 if max_score > 0 else 0
        grade = get_letter_grade(percentage)
        st.info(f"📌 Total: **{total}/{max_score}** | Score: **{percentage:.1f}%** | Grade: **{grade}**")

        if st.button("Submit Marks"):
            feedback = get_feedback(percentage)
            df_new = pd.DataFrame(
                [[student_id, student_name, assessment, *scores.values(), total, percentage, grade, feedback]],
                columns=["Student ID", "Name", "Assessment"] + criteria + ["Total", "Percentage", "Grade", "Feedback"]
            )
            try:
                df = pd.read_csv("student_scores.csv")
                df = pd.concat([df, df_new], ignore_index=True)
            except FileNotFoundError:
                df = df_new
            df.to_csv("student_scores.csv", index=False)
            st.success(f"Marks for {student_name} ({assessment}) saved ✅")
            st.write(df_new)
            st.info(f"💡 Feedback: *{feedback}*")

    # -------------------------- TAB 3 - STUDENT SCORES -------------------------- #
    with tab3:
        st.header("📊 Student Scores Database")
        try:
            df = pd.read_csv("student_scores.csv")
            expected_columns = ["Student ID", "Name", "Assessment"] + criteria + ["Total", "Percentage", "Grade", "Feedback"]
            df = df[[col for col in expected_columns if col in df.columns]]
            st.dataframe(df)
            st.subheader("Summary Statistics")
            st.write(df.describe())

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Student Scores (CSV)", csv, "student_scores.csv", "text/csv")

            st.subheader("Danger Zone")
            student_ids = df["Student ID"].tolist()
            student_to_delete = st.selectbox("Select Student ID to Delete", student_ids)
            if st.button("Delete Selected Student"):
                df = df[df["Student ID"] != student_to_delete]
                df.to_csv("student_scores.csv", index=False)
                st.warning(f"⚠️ Student record with ID {student_to_delete} has been deleted.")
                st.rerun()
            if st.button("🚨 Delete All Records", type="primary"):
                pd.DataFrame(columns=df.columns).to_csv("student_scores.csv", index=False)
                st.error("⚠️ All student data has been permanently deleted!")
                st.rerun()
        except FileNotFoundError:
            st.info("No student data available yet. Please add marks in the 'Marks Entry' tab.")

    # -------------------------- TAB 4 - DASHBOARD -------------------------- #
    with tab4:
        st.header("📊 Dashboard - Student Performance Overview")
        try:
            df = pd.read_csv("student_scores.csv")
            assessments = df["Assessment"].dropna().unique().tolist()
            selected_assessment = st.selectbox("Select Assessment", ["All Assessments"] + assessments)

            if selected_assessment != "All Assessments":
                df_filtered = df[df["Assessment"] == selected_assessment]
            else:
                df_filtered = df.copy()

            st.subheader(f"Student Percentage Scores ({selected_assessment})")
            fig, ax = plt.subplots()
            ax.bar(df_filtered["Name"], df_filtered["Percentage"], color="skyblue")
            ax.set_ylabel("Percentage (%)")
            ax.set_xlabel("Students")
            ax.set_title("Percentage Scores by Student")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

            st.subheader(f"Grade Distribution ({selected_assessment})")
            grade_counts = df_filtered["Grade"].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(grade_counts, labels=grade_counts.index, autopct="%1.1f%%", startangle=90)
            ax2.axis("equal")
            st.pyplot(fig2)

            st.subheader(f"Top & Bottom Performers ({selected_assessment})")
            if not df_filtered.empty:
                top_student = df_filtered.loc[df_filtered["Percentage"].idxmax()]
                bottom_student = df_filtered.loc[df_filtered["Percentage"].idxmin()]
                st.success(f"🏆 Top Performer: **{top_student['Name']}** ({top_student['Percentage']:.1f}%) - {top_student['Grade']}")
                st.error(f"🔻 Lowest Performer: **{bottom_student['Name']}** ({bottom_student['Percentage']:.1f}%) - {bottom_student['Grade']}")
            else:
                st.info("No data available for this assessment.")

            st.subheader("Download Student Data")
            csv = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Filtered Student Data (CSV)", csv, "student_scores_filtered.csv", "text/csv")
        except FileNotFoundError:
            st.info("No student data available yet. Please add marks in the 'Marks Entry' tab.")

    # -------------------------- TAB 5 - IMPORT STUDENTS -------------------------- #
    with tab5:
        st.header("📂 Import Student Names from Excel")
        uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])
        if uploaded_file is not None:
            try:
                student_list = pd.read_excel(uploaded_file)
                student_list = student_list.astype(str).apply(lambda x: x.str.strip())
                st.success("✅ Student list uploaded successfully!")
                st.dataframe(student_list)
                if not any("id" in c.lower() for c in student_list.columns) or not any("name" in c.lower() for c in student_list.columns):
                    st.warning("⚠️ Excel file must contain 'Student ID' and 'Name' columns.")
                else:
                    student_list.to_csv("student_list.csv", index=False)
                    st.success("Student list saved for future use.")
            except Exception as e:
                st.error(f"Error reading Excel file: {e}")

    # -------------------------- TAB RUBRIC -------------------------- #
    with tab_rubric:
        st.header("Marking Description Criteria (Rubric)")
        st.markdown("""
        | Score | Percentage Range | Accuracy | Clarity | Depth | Completeness | Presentation |
        |-------|-----------------|---------|--------|-------|--------------|--------------|
        | **4 (Excellent)** | 80–100% | All correct, precise terminology | Well-structured, logical | Beyond basics | Fully addresses all parts | Neat, organised |
        | **3 (Good)**     | 65–79% | Mostly correct, minor errors | Generally clear | Good understanding | Minor omissions | Mostly neat |
        | **2 (Fair)**     | 50–64% | Several errors | Sometimes confusing | Basic understanding | Partial response | Somewhat disorganised |
        | **1 (Poor)**     | <50% | Many incorrect answers | Unclear | Very limited | Incomplete | Messy |
        | **0 (No Attempt)** | - | No evidence | No clarity | No depth | No completeness | No presentation |
        """, unsafe_allow_html=True)

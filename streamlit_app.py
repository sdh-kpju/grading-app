# grading_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import random
from io import BytesIO  # for Excel export

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
    elif percentage >= 60:
        return random.choice(feedback_dict["B"])
    elif percentage >= 50:
        return random.choice(feedback_dict["C"])
    else:
        return random.choice(feedback_dict["D"])

def get_letter_grade(percentage):
    if percentage >= 80:
        return "A"
    elif percentage >= 60:
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
    </div>
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

            # 🔽 Download updated scores as Excel
            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=False, engine="openpyxl")
            st.download_button(
                label="⬇️ Download Student Scores (Excel)",
                data=excel_buffer.getvalue(),
                file_name="student_scores.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_excel_tab2"
            )

    # -------------------------- TAB 3 - STUDENT SCORES -------------------------- #
    with tab3:
        st.header("📊 Student Scores Database")

        # Choose which dataset to use
        use_imported = st.checkbox("🔄 Use Imported Student List (from Tab 5)")

        try:
            if use_imported:
                # Load from student_list.csv (imported in Tab 5)
                df = pd.read_csv("student_list.csv")
                st.success("✅ Showing data from imported student list (Tab 5)")
            else:
                # Load from student_scores.csv (marks entry)
                df = pd.read_csv("student_scores.csv")
                expected_columns = ["Student ID", "Name", "Assessment"] + criteria + ["Total", "Percentage", "Grade", "Feedback"]
                df = df[[col for col in expected_columns if col in df.columns]]
                st.success("✅ Showing data from student scores")

            st.dataframe(df)

            if not df.empty:
                st.subheader("Summary Statistics")
                st.write(df.describe(include="all"))

                # Download button
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download Data (CSV)", csv, "student_data.csv", "text/csv")

            # 🔽 Danger Zone only available when using student_scores.csv
            if not use_imported:
                st.subheader("Danger Zone")

                # Option 1: Delete ALL records for a Student ID
                student_ids = df["Student ID"].dropna().unique().tolist()
                if student_ids:
                    student_to_delete = st.selectbox("Select Student ID to Delete ALL Records", student_ids)
                    if st.button("Delete ALL Records for Selected Student"):
                        df = df[df["Student ID"] != student_to_delete]
                        df.to_csv("student_scores.csv", index=False)
                        st.warning(f"⚠️ All records for student ID {student_to_delete} have been deleted.")
                        st.rerun()

                # Option 2: Delete ONE specific record
                st.markdown("---")
                st.write("🗑️ Delete a Specific Record")
                if "Assessment" in df.columns:
                    records = df[["Student ID", "Assessment", "Name"]].astype(str)
                    records["Display"] = records["Student ID"] + " - " + records["Name"] + " (" + records["Assessment"] + ")"
                    record_to_delete = st.selectbox("Select Record to Delete", records["Display"].tolist())
                    if st.button("Delete Selected Record"):
                        row_index = records[records["Display"] == record_to_delete].index[0]
                        df = df.drop(index=row_index)
                        df.to_csv("student_scores.csv", index=False)
                        st.warning(f"⚠️ Record {record_to_delete} has been deleted.")
                        st.rerun()

                # Option 3: Delete ALL data
                st.markdown("---")
                if st.button("🚨 Delete ALL Records", type="primary"):
                    pd.DataFrame(columns=df.columns).to_csv("student_scores.csv", index=False)
                    st.error("⚠️ All student data has been permanently deleted!")
                    st.rerun()

        except FileNotFoundError:
            st.info("No student data available yet. Please add marks in the 'Marks Entry' tab or import in Tab 5.")

    # -------------------------- TAB 4 - DASHBOARD -------------------------- #
    with tab4:
        st.header("📊 Dashboard - Student Performance Overview")

        # Choose dataset source
        use_imported = st.checkbox("🔄 Use Imported Student List (from Tab 5)", key="tab4_checkbox")

        try:
            if use_imported:
                df = pd.read_csv("student_list.csv")
                st.success("✅ Showing data from imported student list (Tab 5)")

                if not {"Percentage", "Grade"}.issubset(df.columns):
                    st.warning("⚠️ Imported file does not contain scores/grades. Only student info will be displayed.")
                    st.dataframe(df)
                else:
                    st.info("Imported file contains scores/grades. Proceeding with dashboard analysis.")
            else:
                df = pd.read_csv("student_scores.csv")
                st.success("✅ Showing data from student_scores.csv")

            # ================== TOP SECTION (ALL STUDENTS) ==================
            st.subheader("📊 Overall Performance Overview")

            # Assessment filter
            assessments = ["All Assessments"] + sorted(df["Assessment"].dropna().unique().tolist())
            selected_assessment_overall = st.selectbox("📑 Filter by Assessment (Overall)", assessments)

            df_overall = df.copy()
            if selected_assessment_overall != "All Assessments":
                df_overall = df_overall[df_overall["Assessment"] == selected_assessment_overall]

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Grade Distribution**")
                if not df_overall.empty:
                    grade_counts = df_overall["Grade"].value_counts().reset_index()
                    grade_counts.columns = ["Grade", "Count"]

                    # Plotly Pie Chart
                    fig = px.pie(
                        grade_counts,
                        values="Count",
                        names="Grade",
                        hole=0.3,
                    )
                    fig.update_traces(textinfo="percent+label")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for grade distribution.")

            with col2:
                st.write("**Average Percentage by Student**")
                if not df_overall.empty:
                    avg_scores = df_overall.groupby("Name")["Percentage"].mean().reset_index()
                    fig_avg = px.bar(
                        avg_scores,
                        x="Name",
                        y="Percentage",
                        color="Percentage",
                        color_continuous_scale="Blues",
                        labels={"Percentage": "Average (%)", "Name": "Student"},
                        title="Average Percentage by Student"
                    )
                    fig_avg.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig_avg, use_container_width=True)
                else:
                    st.info("No data available for student averages.")

            # ================== STUDENT FILTER SECTION ==================
            st.subheader("🎯 Individual Student Performance")

            student_options = ["All Students"] + df["Name"].dropna().unique().tolist()
            selected_student = st.selectbox("👤 Select Student", student_options)

            assessments = ["All Assessments"] + df["Assessment"].dropna().unique().tolist()
            selected_assessment = st.selectbox("📑 Select Assessment", assessments)

            df_filtered = df.copy()
            if selected_assessment != "All Assessments":
                df_filtered = df_filtered[df_filtered["Assessment"] == selected_assessment]
            if selected_student != "All Students":
                df_filtered = df_filtered[df_filtered["Name"] == selected_student]

            if {"Percentage", "Grade"}.issubset(df_filtered.columns) and not df_filtered.empty:
                if selected_student == "All Students":
                    st.subheader(f"Percentage Scores ({selected_assessment})")
                    fig = px.bar(
                        df_filtered,
                        x="Name",
                        y="Percentage",
                        color="Percentage",
                        color_continuous_scale="Blues",
                        title="Percentage Scores by Student",
                        labels={"Percentage": "Percentage (%)", "Name": "Students"}
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    # ✅ Show average instead of latest
                    avg_score = df_filtered["Percentage"].mean()
                    latest_grade = df_filtered["Grade"].iloc[-1]
                    st.metric(f"Average Score for {selected_student}", f"{avg_score:.1f}%", latest_grade)

                    # ---- Student Progress Over Time ----
                    st.subheader(f"📈 Progress Over Time - {selected_student}")
                    fig3 = px.line(
                        df_filtered,
                        x="Assessment",
                        y="Percentage",
                        markers=True,
                        title=f"Performance Trend for {selected_student}",
                        labels={"Percentage": "Percentage (%)", "Assessment": "Assessment"}
                    )
                    fig3.update_traces(line=dict(color="green"))
                    st.plotly_chart(fig3, use_container_width=True)

                    # 🔽 Student-specific table
                    st.subheader(f"📋 Detailed Scores for {selected_student}")
                    criteria = ["Accuracy", "Clarity", "Depth", "Completeness", "Presentation"]
                    available_columns = [c for c in criteria if c in df.columns]
                    base_columns = ["Assessment"] + available_columns + ["Total", "Percentage", "Grade", "Feedback"]

                    student_table = df_filtered[base_columns].reset_index(drop=True)
                    st.dataframe(student_table)

                    # Download this student’s data
                    csv = student_table.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        f"⬇️ Download {selected_student}'s Scores (CSV)",
                        csv,
                        f"{selected_student}_scores.csv",
                        "text/csv",
                        key=f"download_{selected_student}"
                    )

            # ---- Top & Bottom Performers ----
            st.subheader("🏆 Top & Bottom Performers")
            if not df_overall.empty and "Percentage" in df_overall.columns:
                top_n = 5
                bottom_n = 5

                # Top Performers
                top_performers = df_overall.nlargest(top_n, "Percentage")
                fig_top = px.bar(
                    top_performers,
                    x="Name",
                    y="Percentage",
                    color="Percentage",
                    color_continuous_scale="Greens",
                    title=f"Top {top_n} Performers",
                    labels={"Percentage": "Percentage (%)", "Name": "Student"}
                )
                fig_top.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_top, use_container_width=True)

                # Bottom Performers
                bottom_performers = df_overall.nsmallest(bottom_n, "Percentage")
                fig_bottom = px.bar(
                    bottom_performers,
                    x="Name",
                    y="Percentage",
                    color="Percentage",
                    color_continuous_scale="Reds",
                    title=f"Bottom {bottom_n} Performers",
                    labels={"Percentage": "Percentage (%)", "Name": "Student"}
                )
                fig_bottom.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_bottom, use_container_width=True)
            else:
                st.info("No data available for Top & Bottom Performers.")

            # ---- Download ----
            st.subheader("⬇️ Download Student Data")
            csv = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button("Download Filtered Student Data (CSV)", csv, "student_scores_filtered.csv", "text/csv")

        except FileNotFoundError:
            st.info("No student data available yet. Please add marks in the 'Marks Entry' tab or import a file in Tab 5.")

    # -------------------------- TAB 5 - IMPORT STUDENTS -------------------------- #
    with tab5:
        st.header("📂 Import Student Names (CSV or Excel)")

        uploaded_file = st.file_uploader("Upload Student Data File", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                # Read file depending on extension
                if uploaded_file.name.endswith(".csv"):
                    student_list = pd.read_csv(uploaded_file)
                else:
                    student_list = pd.read_excel(uploaded_file)

                # Clean data (remove spaces, force strings)
                student_list = student_list.astype(str).apply(lambda x: x.str.strip())
                st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                st.dataframe(student_list)

                # Validate required columns
                if not any("id" in c.lower() for c in student_list.columns) or not any("name" in c.lower() for c in student_list.columns):
                    st.warning("⚠️ File must contain 'Student ID' and 'Name' columns.")
                else:
                    student_list.to_csv("student_list.csv", index=False)
                    st.success("Student list saved for future use.")

            except Exception as e:
                st.error(f"Error reading uploaded file: {e}")


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

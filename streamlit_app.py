# grading_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import random
from io import BytesIO  # for Excel export
import os
import plotly

# Ensure test_results.csv exists and load it
TEST_RESULTS_FILE = "test_results.csv"

if not os.path.exists(TEST_RESULTS_FILE):
    # Create with proper columns if not found
    pd.DataFrame(columns=["Test Name", "Student ID", "Student Name", "MCQ Score", "SAQ Score",
                          "Total Raw", "Scaled (to 100)", "Final Weight (%)", "Weighted Score"]).to_csv(TEST_RESULTS_FILE, index=False)

test_results = pd.read_csv(TEST_RESULTS_FILE)


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
    st.title("📊 Grading Application")
    st.write("Secure grading system with tutorial **numerical rubric scoring** (0–4 per criterion) and for test advancement analysis .")

    # -------------------------- SIDEBAR NAVIGATION -------------------------- #
    st.sidebar.title("📚 Navigation")

    # Define sidebar radio buttons (shortcuts to tabs)
    selected_tab = st.sidebar.radio(
        "Jump to:",
        [
            "Rubric Reference",
            "Marks Entry",
            "Student Scores",
            "Dashboard",
            "Import Students",
            "Test Performance"
        ]
    )

    # Save selection to session state for persistent tracking
    st.session_state["selected_tab"] = selected_tab

    # -------------------------- TABS -------------------------- #
    tab_rubric, tab2, tab3, tab4, tab5, tab_test = st.tabs(
        ["Rubric Reference", "Marks Entry", "Student Scores", "Dashboard", "Import Students", "Test Performance"]
    )

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
                    avg_score = df_filtered["Percentage"].mean()
                    latest_grade = df_filtered["Grade"].iloc[-1]
                    st.metric(f"Average Score for {selected_student}", f"{avg_score:.1f}%", latest_grade)

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

                    st.subheader(f"📋 Detailed Scores for {selected_student}")
                    criteria = ["Accuracy", "Clarity", "Depth", "Completeness", "Presentation"]
                    available_columns = [c for c in criteria if c in df.columns]
                    base_columns = ["Assessment"] + available_columns + ["Total", "Percentage", "Grade", "Feedback"]

                    student_table = df_filtered[base_columns].reset_index(drop=True)
                    st.dataframe(student_table)

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

            st.subheader("⬇️ Download Student Data")
            csv = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button("Download Filtered Student Data (CSV)", csv, "student_scores_filtered.csv", "text/csv")

        except FileNotFoundError:
            st.info("📈 No student data available yet. Please add marks in the 'Marks Entry' tab or import a file in Tab 5.")

        # ------------------ Load and Display Test Performance Summary ------------------ #
        st.markdown("---")
        st.subheader("🧪 Test Performance Summary (from Test Performance Tab)")

        TEST_RESULTS_FILE = "test_results.csv"

        if os.path.exists(TEST_RESULTS_FILE):
            test_results = pd.read_csv(TEST_RESULTS_FILE)

            required_cols = {"Student Name", "Test Name", "MCQ", "SAQ", "Total", "Weighted"}
            if not required_cols.issubset(test_results.columns):
                st.warning("⚠️ Some columns (MCQ/SAQ/Total/Weighted) are missing in test_results.csv.")
                st.dataframe(test_results.head())
            else:
                test_list = ["All Tests"] + sorted(test_results["Test Name"].dropna().unique().tolist())
                selected_test = st.selectbox("Select Test", test_list, key="tab4_test_filter")

                df_display = test_results.copy()
                if selected_test != "All Tests":
                    df_display = df_display[df_display["Test Name"] == selected_test]

                # Calculate averages, min, and max
                avg_mcq, min_mcq, max_mcq = df_display["MCQ"].mean(), df_display["MCQ"].min(), df_display["MCQ"].max()
                avg_saq, min_saq, max_saq = df_display["SAQ"].mean(), df_display["SAQ"].min(), df_display["SAQ"].max()
                avg_total, min_total, max_total = df_display["Total"].mean(), df_display["Total"].min(), df_display["Total"].max()
                avg_weighted = df_display["Weighted"].mean()

                # Display metrics with min/max under average
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("MCQ (Avg)", f"{avg_mcq:.1f}", f"Min: {min_mcq:.0f} | Max: {max_mcq:.0f}")
                col2.metric("SAQ (Avg)", f"{avg_saq:.1f}", f"Min: {min_saq:.0f} | Max: {max_saq:.0f}")
                col3.metric("Total (Avg)", f"{avg_total:.1f}", f"Min: {min_total:.0f} | Max: {max_total:.0f}")
                col4.metric("Weighted (Avg %)", f"{avg_weighted:.1f}%", "")

                # Average, Min, Max by Test
                st.write("### 📈 Average, Min & Max Scores by Test")
                summary_stats = (
                    df_display.groupby("Test Name")[["MCQ", "SAQ", "Total", "Weighted"]]
                    .agg(["mean", "min", "max"])
                    .reset_index()
                )
                # Flatten column names
                summary_stats.columns = ["Test Name"] + [
                    f"{col}_{stat}" for col, stat in summary_stats.columns if col != "Test Name"
                ]

                # Melt data for visualization (Average only for chart)
                avg_scores_melted = (
                    df_display.groupby("Test Name")[["MCQ", "SAQ", "Total"]]
                    .mean()
                    .reset_index()
                    .melt(id_vars="Test Name", var_name="Category", value_name="Average Score")
                )

                # Plotly chart: Average scores by Test
                fig = px.bar(
                    avg_scores_melted,
                    x="Test Name",
                    y="Average Score",
                    color="Category",
                    barmode="group",
                    title="Average MCQ, SAQ, and Total Scores by Test",
                    labels={"Average Score": "Average Marks", "Test Name": "Test"},
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig, use_container_width=True)

                # Display summary table safely (format only numeric columns)
                st.write("### 📋 Detailed Test Summary (Average, Min, Max)")
                numeric_cols = summary_stats.select_dtypes(include=["float64", "int64"]).columns
                st.dataframe(summary_stats.style.format(subset=numeric_cols, formatter="{:.1f}"))

        else:
            st.info("📈 No test results yet. Please add some in the 'Test Performance' tab.")

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



    # -------------------------- TAB 6 - TEST PERFORMANCE -------------------------- #
    with tab_test:
        st.header("🧪 Test Student Performance")
        st.markdown("---")

        import os

        TEST_RESULTS_FILE = "test_results.csv"

        # Load student list if available
        try:
            student_list = pd.read_csv("student_list.csv")
            id_col, name_col = None, None
            for c in student_list.columns:
                if "id" in c.lower(): id_col = c
                if "name" in c.lower(): name_col = c
            student_list = student_list.astype(str).apply(lambda x: x.str.strip())
        except FileNotFoundError:
            student_list = None
            id_col, name_col = None, None

        col1, col2 = st.columns(2)

        with col1:
            # Select test and student
            predefined_tests = ["Test 1", "Test 2", "Midterm", "Final"]
            test_choice = st.selectbox("Select Test Name", predefined_tests + ["Other"], key="tab6_test_choice")
            if test_choice == "Other":
                test_name = st.text_input("Enter Custom Test Name", key="tab6_custom_test")
            else:
                test_name = test_choice

            if student_list is not None and name_col and id_col:
                student_name = st.selectbox("Select Student Name", student_list[name_col].tolist(), key="tab6_student_name")
                match = student_list.loc[student_list[name_col] == student_name, id_col]
                student_id = match.values[0] if not match.empty else "N/A"
                st.write(f"**Student ID:** {student_id}")
            else:
                student_id = st.text_input("Student ID", key="tab6_manual_id")
                student_name = st.text_input("Student Name", key="tab6_manual_name")

            # Test configuration
            st.markdown("### ⚙️ Test Configuration")
            mcq_total = st.number_input("Total MCQ Marks", min_value=0, value=20, step=1, key="tab6_mcq_total")
            saq_total = st.number_input("Total Short Answer Marks", min_value=0, value=30, step=1, key="tab6_saq_total")
            desired_total = st.number_input("Desired Total Marks (e.g., 100)", min_value=10, value=100, step=10, key="tab6_desired_total")
            test_weight = st.number_input("Test Weightage (%)", min_value=0.0, value=10.0, step=0.5, key="tab6_weight")

            scaling_factor = desired_total / (mcq_total + saq_total) if (mcq_total + saq_total) > 0 else 1
            st.write(f"**Scaling Factor:** {scaling_factor:.2f}x")

        with col2:
            st.markdown("### 🧮 Enter Scores")
            mcq_score = st.number_input("MCQ Score", min_value=0.0, max_value=float(mcq_total), value=0.0, key="tab6_mcq_score")
            saq_score = st.number_input("Short Answer Score", min_value=0.0, max_value=float(saq_total), value=0.0, key="tab6_saq_score")

            total_score_raw = mcq_score + saq_score
            total_score_scaled = total_score_raw * scaling_factor
            weighted_score = (total_score_scaled / desired_total) * test_weight

            st.markdown("---")
            st.write(f"**Raw Score:** {total_score_raw}/{mcq_total + saq_total}")
            st.write(f"**Scaled Score:** {total_score_scaled:.2f}/{desired_total}")
            st.write(f"**Weighted Score:** {weighted_score:.2f}%")

        st.markdown("---")

        # ------------------- SAVE TEST RESULT ------------------- #
        if st.button("💾 Save Test Record"):
            try:
                columns = ["Student ID", "Student Name", "Test Name", "MCQ", "SAQ", "Total", "Weighted"]

                # Load existing data
                if os.path.exists(TEST_RESULTS_FILE):
                    df_existing = pd.read_csv(TEST_RESULTS_FILE)
                else:
                    df_existing = pd.DataFrame(columns=columns)

                # Add new record
                new_data = pd.DataFrame([{
                    "Student ID": student_id,
                    "Student Name": student_name,
                    "Test Name": test_name,
                    "MCQ": mcq_score,
                    "SAQ": saq_score,
                    "Total": total_score_scaled,
                    "Weighted": weighted_score
                }])

                # Combine and remove duplicates
                df_combined = pd.concat([df_existing, new_data], ignore_index=True)
                df_combined.drop_duplicates(subset=["Student ID", "Test Name"], keep="last", inplace=True)

                # Save to CSV
                df_combined.to_csv(TEST_RESULTS_FILE, index=False)
                st.success(f"✅ Test result saved for {student_name} in {test_name}.")

            except Exception as e:
                st.error(f"❌ Error saving result: {e}")

        # ------------------- DISPLAY AND DELETE ------------------- #
        if os.path.exists(TEST_RESULTS_FILE):
            st.subheader("📊 Saved Test Results")
            df_display = pd.read_csv(TEST_RESULTS_FILE)

            # Filter by test
            df_filtered = df_display[df_display["Test Name"] == test_name]
            st.dataframe(df_filtered)

            # Delete record section
            st.markdown("### ❌ Delete Student Test Record")
            del_student = st.selectbox(
                "Select Student to Delete",
                df_filtered["Student Name"].unique() if not df_filtered.empty else [],
                key="tab6_delete_student"
            )

            if st.button("🗑️ Delete Selected Record"):
                try:
                    df_display = df_display[
                        ~((df_display["Student Name"] == del_student) & (df_display["Test Name"] == test_name))
                    ]
                    df_display.to_csv(TEST_RESULTS_FILE, index=False)
                    st.success(f"✅ Deleted record for **{del_student}** in **{test_name}**.")
                except Exception as e:
                    st.error(f"Error deleting record: {e}")
        else:
            st.info("No saved test results yet.")

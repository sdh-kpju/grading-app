# Tutorial Grading App

📊 A Streamlit-based grading application for tracking tutorial assessments, calculating grades, and providing motivational feedback. Supports multiple assessments per student, data import/export, and visual dashboards.

---

## Features

1. **Secure Access**
   - Password-protected interface.

2. **Student & Assessment Management**
   - Import student lists from Excel (.xlsx) files.
   - Add multiple assessments per student (e.g., Tutorial 1, Tutorial 2).
   - Auto-fill Student ID when selecting a student from the list.

3. **Grading & Feedback**
   - Score students based on 5 criteria: Accuracy, Clarity, Depth, Completeness, Presentation.
   - Scores range from 0–4 per criterion.
   - Automatic calculation of total score, percentage, and letter grade (A, B, C, D).
   - Randomized motivational feedback per grade band.

4. **Dashboard & Visualizations**
   - Filter results by assessment.
   - Bar chart: Percentage scores per student.
   - Pie chart: Grade distribution per assessment.
   - Top and bottom performers highlighted.
   - Optional download of filtered or complete student data as CSV.

5. **Data Management**
   - Save student scores locally in `student_scores.csv`.
   - Download CSV of student scores.
   - Delete individual student records or clear all data (Danger Zone).

---

## Installation & Setup

1. Clone this repository
2. Navigate to the project directory
3. Install required Python packages
4. Run the app
5. Enter the password when prompted (default: `letmein`).

---

## Usage

1. **Tab 1: Rubric Reference**
- View grading rubric for each score band.

2. **Tab 2: Marks Entry**
- Select a student (or enter manually).
- Select or enter an Assessment.
- Input scores for each criterion.
- Submit marks to save and receive motivational feedback.

3. **Tab 3: Student Scores**
- View, filter, and download all student scores.
- Delete single records or clear all data.

4. **Tab 4: Dashboard**
- Visualize student performance.
- Filter by assessment to focus on specific tutorials.
- Download filtered data for reporting.

5. **Tab 5: Import Students**
- Upload an Excel file with columns `Student ID` and `Name`.
- Cleaned data is saved for future sessions.

---

## File Structure
grading_app.py # Main Streamlit app
student_list.csv # Optional CSV of imported students
student_scores.csv # Auto-generated CSV storing student scores
README.txt # This file

## Notes

- Ensure your Excel file has **exact columns**: `Student ID` and `Name`.
- Assessment names are normalized to prevent typos.
- The app auto-strips whitespace from imported data to avoid mismatches.
- Motivational feedback is randomized and aligned to the grade band.

---

## License

 Free to use and modify.


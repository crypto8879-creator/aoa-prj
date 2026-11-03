#pip install pandas matplotlib openpyxl

import matplotlib.pyplot as plt
import pandas as pd

# Load raw dataset from Excel
raw = pd.read_excel(
    "Practical_07_Study_Habits_Analysis.xlsx",
    sheet_name="Raw Data",
    header=2,
)
raw.columns = ["id", "hours", "attendance", "assignment", "marks"]

# 1. Data quality checks
print("Missing values:\n", raw.isna().sum())
print("Duplicate rows:", raw.duplicated().sum())

invalid = (
    (~raw.hours.between(0, 24))
    | (~raw.attendance.between(0, 100))
    | (~raw.assignment.between(0, 100))
    | (~raw.marks.between(0, 100))
)
print(
    "Rows with invalid (non-missing) values:",
    (invalid & raw.notna().all(axis=1)).sum(),
)

# 2. Cleaning: drop duplicates, then missing / out-of-range rows
clean = raw.drop_duplicates().dropna()
clean = clean[
    clean.hours.between(0, 24)
    & clean.attendance.between(0, 100)
    & clean.assignment.between(0, 100)
    & clean.marks.between(0, 100)
]
clean.to_csv("cleaned_07.csv", index=False)

# 3. Summary statistics
print("\nSummary statistics:")
print(clean[["hours", "marks"]].agg(["mean", "median", "min", "max"]).round(2))

# 4. Group by daily study hours and compare average marks
clean["group"] = pd.cut(
    clean.hours,
    [-0.01, 0.9999, 3, 24],
    labels=["Below 1 hour", "1-3 hours", "Above 3 hours"],
)
gm = (
    clean.groupby("group", observed=False)
    .marks.agg(["count", "mean"])
    .round(1)
)
print("\nMarks by study-hours group:")
print(gm)

# 5. Correlation and charts
r = clean.hours.corr(clean.marks)
print("\nPearson r (hours vs marks):", round(r, 3))

# Chart 1: Bar plot
gm["mean"].plot(
    kind="bar",
    color="#2E75B6",
    rot=0,
    title="Average marks by study-hours group",
)
plt.ylabel("Average marks")
plt.tight_layout()
plt.savefig("chart1_group_bar.png", dpi=200)
plt.close()

# Chart 2: Scatter plot
plt.scatter(clean.hours, clean.marks, color="#2E75B6")
plt.xlabel("Daily study hours")
plt.ylabel("Exam marks")
plt.title(f"Study hours vs marks (r = {r:.2f})")
plt.tight_layout()
plt.savefig("chart2_scatter.png", dpi=200)
plt.show()
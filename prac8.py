#pip install pandas scipy matplotlib openpyxl


import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# Load cleaned dataset from Excel
df = pd.read_excel(
    "Practical_08_Statistical_Analysis.xlsx",
    sheet_name="Cleaned Data",
    header=2,
)
df.columns = ["id", "programme", "weekly_hours", "score"]

# 1. Cleaning checks
print(f"{df.isna().sum().sum()} missing | {df.id.duplicated().sum()} duplicate IDs\n")

# 2. Descriptive statistics
cols = ["weekly_hours", "score"]
summary = df[cols].agg(["count", "mean", "median", "std", "min", "max"]).round(2)
summary.loc["mode"] = [df[c].mode().iloc[0] for c in cols]
print("Summary Statistics:")
print(summary)

# 3. Programme-wise frequency table
freq = df.programme.value_counts().rename("count").to_frame()
freq["percent"] = (freq["count"] / len(df) * 100).round(1)
freq["mean_score"] = df.groupby("programme")["score"].mean().round(1)
print("\nProgramme Breakdown:")
print(freq)

# 4. Visualizations
# Chart 1: Histogram of scores
plt.hist(df.score, bins=range(20, 101, 10), color="#2E75B6", edgecolor="white")
plt.xlabel("Exam score")
plt.ylabel("Students")
plt.title("Histogram of exam scores")
plt.tight_layout()
plt.savefig("hist_scores.png", dpi=200)
plt.close()

# Chart 2: Bar plot by programme
freq["count"].plot(
    kind="bar",
    color="#ED7D31",
    rot=0,
    title="Students by programme",
)
plt.ylabel("Students")
plt.tight_layout()
plt.savefig("bar_programme.png", dpi=200)
plt.close()

# Chart 3: Scatter plot
plt.scatter(df.weekly_hours, df.score, color="#2E75B6")
plt.xlabel("Weekly study hours")
plt.ylabel("Exam score")
plt.title("Study hours vs score")
plt.tight_layout()
plt.savefig("scatter.png", dpi=200)
plt.close()

# 5. Pearson correlation test (H0: rho = 0)
r, p = stats.pearsonr(df.weekly_hours, df.score)
print(f"\nCorrelation Test Results:")
print(f"r = {r:.3f}, r^2 = {r**2:.3f}, p = {p:.2e}")
print("Reject H0" if p < 0.05 else "Fail to reject H0")
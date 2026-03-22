import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# style
sns.set_style("whitegrid")

# -----------------------------
# Load Data
# -----------------------------
try:
    matches = pd.read_csv("matches .csv")
    deliveries = pd.read_csv("deliveries.csv")
    print("✅ Data Loaded Successfully\n")
except Exception as e:
    print("❌ Error:", e)
    exit()

# -----------------------------
# Create folder for graphs
# -----------------------------
import os
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# -----------------------------
# 1. Top Winning Teams
# -----------------------------
team_wins = matches["winner"].value_counts().head(8)

plt.figure()
sns.barplot(x=team_wins.values, y=team_wins.index)
plt.title("Top IPL Teams by Wins")
plt.savefig("graphs/top_teams.png")

# -----------------------------
# 2. Top Batsmen (FIXED)
# -----------------------------
top_batsmen = (
    deliveries.groupby("batsman")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
sns.barplot(x=top_batsmen.values, y=top_batsmen.index)
plt.title("Top Batsmen")
plt.savefig("graphs/top_batsmen.png")

# -----------------------------
# 3. Top Bowlers
# -----------------------------
wickets = deliveries[
    (deliveries["dismissal_kind"].notna()) &
    (deliveries["dismissal_kind"] != "run out")
]

top_bowlers = wickets["bowler"].value_counts().head(10)

plt.figure()
sns.barplot(x=top_bowlers.values, y=top_bowlers.index)
plt.title("Top Bowlers")
plt.savefig("graphs/top_bowlers.png")

# -----------------------------
# 4. Toss Impact
# -----------------------------
matches["toss_win_match_win"] = matches["toss_winner"] == matches["winner"]

toss_result = matches["toss_win_match_win"].value_counts()

plt.figure()
sns.barplot(x=toss_result.index.astype(str), y=toss_result.values)
plt.title("Toss Impact")
plt.savefig("graphs/toss_impact.png")

print("Toss Impact %:",
      (toss_result[True] / toss_result.sum()) * 100)

# -----------------------------
# 5. Matches Per Season
# -----------------------------
matches_per_season = matches["season"].value_counts().sort_index()

plt.figure()
sns.lineplot(x=matches_per_season.index, y=matches_per_season.values)
plt.title("Matches Per Season")
plt.savefig("graphs/matches_per_season.png")

# -----------------------------
# 6. Runs Distribution
# -----------------------------
runs_per_match = deliveries.groupby("match_id")["total_runs"].sum()

plt.figure()
sns.histplot(runs_per_match, bins=20, kde=True)
plt.title("Runs Distribution")
plt.savefig("graphs/runs_distribution.png")

# -----------------------------
# 7. Correlation Heatmap
# -----------------------------
numeric_cols = matches.select_dtypes(include=['int64', 'float64'])

plt.figure()
sns.heatmap(numeric_cols.corr(), annot=True)
plt.title("Correlation Heatmap")
plt.savefig("graphs/heatmap.png")

# -----------------------------
# END
# -----------------------------
print("\n✅ All graphs saved in 'graphs' folder")

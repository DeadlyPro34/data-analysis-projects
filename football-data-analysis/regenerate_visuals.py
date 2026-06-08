import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')
import os

sns.set_style("whitegrid")
os.makedirs('visualizations', exist_ok=True)

# LOAD DATA
results = pd.read_csv("data/results.csv")
goals = pd.read_csv("data/goalscorers.csv")
shootouts = pd.read_csv("data/shootouts.csv")
former = pd.read_csv("data/former_names.csv")

# PREPROCESS
results['date'] = pd.to_datetime(results['date'])
goals['date'] = pd.to_datetime(goals['date'])
shootouts['date'] = pd.to_datetime(shootouts['date'])
results['year'] = results['date'].dt.year
goals['year'] = goals['date'].dt.year
shootouts['year'] = shootouts['date'].dt.year
results["total_goals"] = results["home_score"] + results["away_score"]

# 1. TOP TEAMS BY MATCHES
home_matches = results['home_team'].value_counts()
away_matches = results['away_team'].value_counts()
team_matches = home_matches.add(away_matches, fill_value=0).sort_values(ascending=False)

plt.figure(figsize=(12, 6))
team_matches.head(15).plot(kind='barh', color='steelblue')
plt.xlabel('Total Matches')
plt.title('Top 15 Teams by Matches Played', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/01_top_teams.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. MOST SUCCESSFUL TEAMS (WINS)
home_wins = results[results['home_score'] > results['away_score']]['home_team']
away_wins = results[results['away_score'] > results['home_score']]['away_team']
wins = pd.concat([home_wins, away_wins])
top_winners = wins.value_counts()

plt.figure(figsize=(12, 6))
top_winners.head(15).plot(kind='barh', color='seagreen')
plt.xlabel('Total Wins')
plt.title('Top 15 Most Successful Teams', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/02_most_successful_teams.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. HIGHEST SCORING TEAMS
home_goals = results.groupby('home_team')['home_score'].sum()
away_goals = results.groupby('away_team')['away_score'].sum()
total_goals_by_team = home_goals.add(away_goals, fill_value=0).sort_values(ascending=False)

plt.figure(figsize=(12, 6))
total_goals_by_team.head(15).plot(kind='barh', color='coral')
plt.xlabel('Total Goals')
plt.title('Top 15 Highest Scoring Teams', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/03_highest_scoring_teams.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. BEST DEFENSE
home_conceded = results.groupby('home_team')['away_score'].sum()
away_conceded = results.groupby('away_team')['home_score'].sum()
total_conceded = home_conceded.add(away_conceded, fill_value=0).sort_values()

plt.figure(figsize=(12, 6))
total_conceded.head(15).plot(kind='barh', color='darkblue')
plt.xlabel('Goals Conceded')
plt.title('Top 15 Teams with Best Defense', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/04_best_defense.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. HOME ADVANTAGE
home_wins_count = len(results[results['home_score'] > results['away_score']])
away_wins_count = len(results[results['away_score'] > results['home_score']])
draws = len(results[results['home_score'] == results['away_score']])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
colors = ['#2ecc71', '#e74c3c', '#95a5a6']
ax1.pie([home_wins_count, away_wins_count, draws], labels=['Home Wins', 'Away Wins', 'Draws'], autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Match Results Distribution', fontweight='bold')
ax2.bar(['Home Wins', 'Away Wins', 'Draws'], [home_wins_count, away_wins_count, draws], color=colors)
ax2.set_ylabel('Number of Matches')
ax2.set_title('Home Advantage - Absolute Numbers', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/05_home_advantage.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. GOALS OVER TIME
goals_per_year = results.groupby('year').agg({'total_goals': 'sum', 'date': 'count'}).rename(columns={'date': 'matches'})
goals_per_year['avg_goals'] = goals_per_year['total_goals'] / goals_per_year['matches']

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
ax1.plot(goals_per_year.index, goals_per_year['total_goals'], linewidth=2, color='darkblue')
ax1.fill_between(goals_per_year.index, goals_per_year['total_goals'], alpha=0.3, color='steelblue')
ax1.set_ylabel('Total Goals')
ax1.set_title('Total Goals Over Time', fontweight='bold')
ax1.grid(True, alpha=0.3)
ax2.plot(goals_per_year.index, goals_per_year['avg_goals'], linewidth=2, color='darkred', marker='o', markersize=3)
ax2.axhline(y=goals_per_year['avg_goals'].mean(), color='red', linestyle='--', alpha=0.5, label='Historical Average')
ax2.set_xlabel('Year')
ax2.set_ylabel('Average Goals per Match')
ax2.set_title('Average Goals per Match Over Time', fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/06_goals_over_time.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. TOURNAMENTS
tournament_counts = results['tournament'].value_counts()
plt.figure(figsize=(12, 6))
tournament_counts.head(15).plot(kind='barh', color='purple')
plt.xlabel('Number of Matches')
plt.title('Top 15 Tournaments by Match Count', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/07_tournaments.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. FORMER NAMES
plt.figure(figsize=(12, 6))
former['current'].value_counts().plot(kind='barh', color='teal')
plt.xlabel('Number of Name Changes')
plt.title('Countries by Number of Historical Name Changes', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/08_former_names.png', dpi=300, bbox_inches='tight')
plt.close()

# 9. TOP SCORERS
top_scorers = goals['scorer'].value_counts()
plt.figure(figsize=(12, 7))
top_scorers.head(20).plot(kind='barh', color='gold')
plt.xlabel('Total Goals')
plt.title('Top 20 All-Time International Goal Scorers', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/09_top_scorers.png', dpi=300, bbox_inches='tight')
plt.close()

# 10. TOP NATIONS (GOALS)
top_nations = goals['team'].value_counts()
plt.figure(figsize=(12, 6))
top_nations.head(15).plot(kind='barh', color='darkgreen')
plt.xlabel('Total Goals')
plt.title('Top 15 Nations by Total Goals', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/10_top_nations.png', dpi=300, bbox_inches='tight')
plt.close()

# 11. GOAL TYPES
penalty_goals = goals['penalty'].sum()
own_goals = goals['own_goal'].sum()
regular_goals = len(goals) - penalty_goals - own_goals
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
colors = ['#3498db', '#e74c3c', '#f39c12']
ax1.pie([regular_goals, int(penalty_goals), int(own_goals)], labels=['Regular Goals', 'Penalties', 'Own Goals'], autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Goal Type Distribution', fontweight='bold')
penalties_by_year = goals[goals['penalty']].groupby('year').size()
ax2.plot(penalties_by_year.index, penalties_by_year.values, linewidth=2, marker='o', color='red')
ax2.set_xlabel('Year')
ax2.set_ylabel('Penalty Goals')
ax2.set_title('Penalty Goals Over Time', fontweight='bold')
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/11_goal_types.png', dpi=300, bbox_inches='tight')
plt.close()

# 12. SHOOTOUT WINNERS
shootout_winners = shootouts['winner'].value_counts()
plt.figure(figsize=(12, 6))
shootout_winners.head(15).plot(kind='barh', color='darkred')
plt.xlabel('Shootout Wins')
plt.title('Teams with Most Penalty Shootout Wins', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/12_shootout_winners.png', dpi=300, bbox_inches='tight')
plt.close()

# 13. SHOOTOUTS OVER TIME
shootouts_per_year = shootouts.groupby('year').size()
plt.figure(figsize=(12, 6))
shootouts_per_year.plot(kind='bar', color='darkblue')
plt.xlabel('Year')
plt.ylabel('Number of Shootouts')
plt.title('Penalty Shootouts Over Time', fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/13_shootouts_over_time.png', dpi=300, bbox_inches='tight')
plt.close()

# 14. GOAL DISTRIBUTION
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
axes[0, 0].hist(results['home_score'].dropna(), bins=20, color='steelblue', edgecolor='black')
axes[0, 0].set_title('Distribution of Home Team Goals', fontweight='bold')
axes[0, 0].set_xlabel('Goals')
axes[0, 0].set_ylabel('Frequency')
axes[0, 1].hist(results['away_score'].dropna(), bins=20, color='coral', edgecolor='black')
axes[0, 1].set_title('Distribution of Away Team Goals', fontweight='bold')
axes[0, 1].set_xlabel('Goals')
axes[0, 1].set_ylabel('Frequency')
axes[1, 0].hist(results['total_goals'], bins=20, color='seagreen', edgecolor='black')
axes[1, 0].set_title('Distribution of Total Goals per Match', fontweight='bold')
axes[1, 0].set_xlabel('Total Goals')
axes[1, 0].set_ylabel('Frequency')
axes[1, 1].boxplot([results['home_score'].dropna(), results['away_score'].dropna()], labels=['Home', 'Away'])
axes[1, 1].set_title('Goals Distribution Comparison', fontweight='bold')
axes[1, 1].set_ylabel('Goals')
plt.tight_layout()
plt.savefig('visualizations/14_goal_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 15. CORRELATION
correlation = results[['home_score', 'away_score']].corr()
plt.figure(figsize=(6, 5))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, square=True)
plt.title('Correlation: Home Goals vs Away Goals', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/15_correlation.png', dpi=300, bbox_inches='tight')
plt.close()

print("All visualizations regenerated successfully.")



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")

print("✓ Libraries imported successfully")

results = pd.read_csv("data/results.csv")
goals = pd.read_csv("data/goalscorers.csv")
shootouts = pd.read_csv("data/shootouts.csv")
former = pd.read_csv("data/former_names.csv")

print("✓ Data loaded successfully")
print(f"\nResults: {results.shape}")
print(f"Goalscorers: {goals.shape}")
print(f"Shootouts: {shootouts.shape}")
print(f"Former Names: {former.shape}")

print("\n" + "="*50)
print("RESULTS DATASET")
print("="*50)
print(results.head())
print("\n")
results.info()
print("\n")
print(results.describe())

print("\n" + "="*50)
print("GOALSCORERS DATASET")
print("="*50)
print(goals.head())
print("\n")
goals.info()
print("\n")
print(goals.describe())

print("\n" + "="*50)
print("SHOOTOUTS DATASET")
print("="*50)
print(shootouts.head())
print("\n")
shootouts.info()
print("\n")
print(shootouts.describe())

print("\n" + "="*50)
print("FORMER NAMES DATASET")
print("="*50)
print(former.head())
print("\n")
former.info()
print("\n")
print(former.describe())

print("\n" + "="*50)
print("DATA QUALITY CHECK")
print("="*50)

print("\nResults - Nulls and Duplicates:")
print(f"Null values: {results.isnull().sum().sum()}")
print(f"Duplicate rows: {results.duplicated().sum()}")

print("\nGoalscorers - Nulls and Duplicates:")
print(f"Null values: {goals.isnull().sum().sum()}")
print(f"Duplicate rows: {goals.duplicated().sum()}")

print("\nShootouts - Nulls and Duplicates:")
print(f"Null values: {shootouts.isnull().sum().sum()}")
print(f"Duplicate rows: {shootouts.duplicated().sum()}")

print("\nFormer Names - Nulls and Duplicates:")
print(f"Null values: {former.isnull().sum().sum()}")
print(f"Duplicate rows: {former.duplicated().sum()}")

results['date'] = pd.to_datetime(results['date'])
goals['date'] = pd.to_datetime(goals['date'])
shootouts['date'] = pd.to_datetime(shootouts['date'])
former['start_date'] = pd.to_datetime(former['start_date'])
former['end_date'] = pd.to_datetime(former['end_date'])

results['year'] = results['date'].dt.year
goals['year'] = goals['date'].dt.year
shootouts['year'] = shootouts['date'].dt.year

print("\n✓ Date conversion completed")
print(f"\nResults date range: {results['date'].min()} to {results['date'].max()}")
print(f"Goals date range: {goals['date'].min()} to {goals['date'].max()}")
print(f"Shootouts date range: {shootouts['date'].min()} to {shootouts['date'].max()}")

total_matches = len(results)
teams = pd.concat([results["home_team"], results["away_team"]])
total_teams = teams.nunique()

results["total_goals"] = results["home_score"] + results["away_score"]
total_goals = results["total_goals"].sum()

avg_goals_per_match = results["total_goals"].mean()
total_tournaments = results["tournament"].nunique()
total_scorers = goals['scorer'].nunique()
total_shootouts = len(shootouts)

print("\n" + "="*50)
print("DATASET OVERVIEW")
print("="*50)
print(f"Total Matches: {total_matches:,}")
print(f"Unique Teams: {total_teams}")
print(f"Total Goals: {int(total_goals):,}")
print(f"Average Goals per Match: {avg_goals_per_match:.2f}")
print(f"Tournament Types: {total_tournaments}")
print(f"Total Scorers: {total_scorers:,}")
print(f"Penalty Shootouts: {total_shootouts}")
print(f"Year Range: {results['year'].min()}-{results['year'].max()}")
print("="*50)

home_matches = results['home_team'].value_counts()
away_matches = results['away_team'].value_counts()
team_matches = home_matches.add(away_matches, fill_value=0).sort_values(ascending=False)

print("\nTop 15 Teams by Matches Played:")
print(team_matches.head(15))

plt.figure(figsize=(12, 6))
team_matches.head(15).plot(kind='barh', color='steelblue')
plt.xlabel('Total Matches')
plt.title('Top 15 Teams by Matches Played', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/01_top_teams.png', dpi=300, bbox_inches='tight')
plt.show()

home_wins = results[results['home_score'] > results['away_score']]['home_team']
away_wins = results[results['away_score'] > results['home_score']]['away_team']
wins = pd.concat([home_wins, away_wins])
top_winners = wins.value_counts()

print("\nTop 15 Most Successful Teams (by wins):")
print(top_winners.head(15))

plt.figure(figsize=(12, 6))
top_winners.head(15).plot(kind='barh', color='seagreen')
plt.xlabel('Total Wins')
plt.title('Top 15 Most Successful Teams', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/02_most_successful_teams.png', dpi=300, bbox_inches='tight')
plt.show()

home_goals = results.groupby('home_team')['home_score'].sum()
away_goals = results.groupby('away_team')['away_score'].sum()
total_goals_by_team = home_goals.add(away_goals, fill_value=0).sort_values(ascending=False)

print("\nTop 15 Highest Scoring Teams:")
print(total_goals_by_team.head(15))

plt.figure(figsize=(12, 6))
total_goals_by_team.head(15).plot(kind='barh', color='coral')
plt.xlabel('Total Goals')
plt.title('Top 15 Highest Scoring Teams', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/03_highest_scoring_teams.png', dpi=300, bbox_inches='tight')
plt.show()

home_conceded = results.groupby('home_team')['away_score'].sum()
away_conceded = results.groupby('away_team')['home_score'].sum()
total_conceded = home_conceded.add(away_conceded, fill_value=0).sort_values()

print("\nTop 15 Teams with Best Defense (Fewest Goals Conceded):")
print(total_conceded.head(15))

plt.figure(figsize=(12, 6))
total_conceded.head(15).plot(kind='barh', color='darkblue')
plt.xlabel('Goals Conceded')
plt.title('Top 15 Teams with Best Defense', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/04_best_defense.png', dpi=300, bbox_inches='tight')
plt.show()

home_wins_count = len(results[results['home_score'] > results['away_score']])
away_wins_count = len(results[results['away_score'] > results['home_score']])
draws = len(results[results['home_score'] == results['away_score']])

total_decisive = home_wins_count + away_wins_count
home_win_pct = (home_wins_count / total_decisive) * 100
away_win_pct = (away_wins_count / total_decisive) * 100
draw_pct = (draws / len(results)) * 100

print("\n" + "="*50)
print("HOME ADVANTAGE ANALYSIS")
print("="*50)
print(f"Home Wins: {home_wins_count:,} ({home_win_pct:.1f}% of decisive matches)")
print(f"Away Wins: {away_wins_count:,} ({away_win_pct:.1f}% of decisive matches)")
print(f"Draws: {draws:,} ({draw_pct:.1f}% of all matches)")
print(f"\nHome teams win {home_win_pct - away_win_pct:.1f}% more often than away teams")
print("="*50)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

colors = ['#2ecc71', '#e74c3c', '#95a5a6']
ax1.pie([home_wins_count, away_wins_count, draws], 
        labels=['Home Wins', 'Away Wins', 'Draws'], 
        autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Match Results Distribution', fontweight='bold')

ax2.bar(['Home Wins', 'Away Wins', 'Draws'], 
        [home_wins_count, away_wins_count, draws], 
        color=colors)
ax2.set_ylabel('Number of Matches')
ax2.set_title('Home Advantage - Absolute Numbers', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/05_home_advantage.png', dpi=300, bbox_inches='tight')
plt.show()

goals_per_year = results.groupby('year').agg({
    'total_goals': 'sum',
    'date': 'count'
}).rename(columns={'date': 'matches'})

goals_per_year['avg_goals'] = goals_per_year['total_goals'] / goals_per_year['matches']

print("\nGoals Trend by Year (Last 10 Years):")
print(goals_per_year.tail(10))

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
plt.show()


tournament_counts = results['tournament'].value_counts()

print("\nTop 15 Tournaments by Match Count:")
print(tournament_counts.head(15))

plt.figure(figsize=(12, 6))
tournament_counts.head(15).plot(kind='barh', color='purple')
plt.xlabel('Number of Matches')
plt.title('Top 15 Tournaments by Match Count', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/07_tournaments.png', dpi=300, bbox_inches='tight')
plt.show()

tournament_goals = results.groupby('tournament').agg({
    'total_goals': ['sum', 'mean', 'count']
}).round(2)
tournament_goals.columns = ['Total_Goals', 'Avg_Goals_Per_Match', 'Matches']
tournament_goals = tournament_goals.sort_values('Avg_Goals_Per_Match', ascending=False)

print("\nTournaments with Highest Average Goals per Match (min 10 matches):")
print(tournament_goals[tournament_goals['Matches'] >= 10].head(10))

print("\n" + "="*50)
print("FORMER COUNTRY NAMES ANALYSIS")
print("="*50)

former_count = former.shape[0]
current_names = former['current'].nunique()

print(f"\nTotal countries with name changes: {former_count}")
print(f"Unique current names: {current_names}")

multiple_changes = former['current'].value_counts()
print("\nCountries with multiple name changes:")
print(multiple_changes[multiple_changes > 1])

print("\nFormer to Current Name Mappings:")
for idx, row in former.iterrows():
    print(f"{row['former']} → {row['current']} ({row['start_date'].date()} to {row['end_date'].date()})")

plt.figure(figsize=(12, 6))
former['current'].value_counts().plot(kind='barh', color='teal')
plt.xlabel('Number of Name Changes')
plt.title('Countries by Number of Historical Name Changes', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/08_former_names.png', dpi=300, bbox_inches='tight')
plt.show()

top_scorers = goals['scorer'].value_counts()

print("\nTop 20 All-Time Goal Scorers:")
print(top_scorers.head(20))

plt.figure(figsize=(12, 7))
top_scorers.head(20).plot(kind='barh', color='gold')
plt.xlabel('Total Goals')
plt.title('Top 20 All-Time International Goal Scorers', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/09_top_scorers.png', dpi=300, bbox_inches='tight')
plt.show()

top_nations = goals['team'].value_counts()

print("\nTop 15 Nations by Total Goals:")
print(top_nations.head(15))

plt.figure(figsize=(12, 6))
top_nations.head(15).plot(kind='barh', color='darkgreen')
plt.xlabel('Total Goals')
plt.title('Top 15 Nations by Total Goals', fontweight='bold')
plt.tight_layout()


penalty_goals = goals['penalty'].sum()
own_goals = goals['own_goal'].sum()
regular_goals = len(goals) - penalty_goals - own_goals

print("\n" + "="*50)
print("GOAL TYPE BREAKDOWN")
print("="*50)
print(f"Regular Goals: {regular_goals:,} ({regular_goals/len(goals)*100:.1f}%)")
print(f"Penalty Goals: {int(penalty_goals):,} ({penalty_goals/len(goals)*100:.1f}%)")
print(f"Own Goals: {int(own_goals):,} ({own_goals/len(goals)*100:.1f}%)")
print("="*50)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

colors = ['#3498db', '#e74c3c', '#f39c12']
ax1.pie([regular_goals, int(penalty_goals), int(own_goals)], 
        labels=['Regular Goals', 'Penalties', 'Own Goals'],
        autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Goal Type Distribution', fontweight='bold')

penalties_by_year = goals[goals['penalty']].groupby('year').size()
ax2.plot(penalties_by_year.index, penalties_by_year.values, linewidth=2, marker='o', color='red')
ax2.set_xlabel('Year')
ax2.set_ylabel('Penalty Goals')
ax2.set_title('Penalty Goals Over Time', fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('visualizations/10_top_nations.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*50)
print("PENALTY SHOOTOUT STATISTICS")
print("="*50)
print(f"Total Shootouts: {len(shootouts)}")
print(f"Year Range: {shootouts['year'].min()}-{shootouts['year'].max()}")
print(f"Winners analyzed: {shootouts['winner'].nunique()}")
print("="*50)

shootout_winners = shootouts['winner'].value_counts()

print("\nTeams with Most Shootout Wins:")
print(shootout_winners.head(10))

plt.figure(figsize=(12, 6))
shootout_winners.head(15).plot(kind='barh', color='darkred')
plt.xlabel('Shootout Wins')
plt.title('Teams with Most Penalty Shootout Wins', fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/11_goal_types.png', dpi=300, bbox_inches='tight')
plt.show()

shootouts_per_year = shootouts.groupby('year').size()

print("\nShootouts per Year (Recent 10 Years):")
print(shootouts_per_year.tail(10))

plt.figure(figsize=(12, 6))
shootouts_per_year.plot(kind='bar', color='darkblue')
plt.xlabel('Year')
plt.ylabel('Number of Shootouts')
plt.title('Penalty Shootouts Over Time', fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()


print("\n" + "="*50)
print("DESCRIPTIVE STATISTICS - GOALS")
print("="*50)
print(results[['home_score', 'away_score', 'total_goals']].describe().round(3))
print("="*50)

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

axes[1, 1].boxplot([results['home_score'].dropna(), results['away_score'].dropna()],
                     labels=['Home', 'Away'])
axes[1, 1].set_title('Goals Distribution Comparison', fontweight='bold')
axes[1, 1].set_ylabel('Goals')

plt.tight_layout()
plt.savefig('visualizations/12_shootout_winners.png', dpi=300, bbox_inches='tight')
plt.show()

correlation = results[['home_score', 'away_score']].corr()

print("\nCORRELATION MATRIX")
print(correlation)

plt.figure(figsize=(6, 5))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, square=True)
plt.title('Correlation: Home Goals vs Away Goals', fontweight='bold')
plt.tight_layout()


print("\n" + "="*60)
print("KEY INSIGHTS SUMMARY")
print("="*60)

print(f"\n1. HOME ADVANTAGE")
print(f"   • Home teams win {home_win_pct:.1f}% of decisive matches")
print(f"   • Away teams win {away_win_pct:.1f}% of decisive matches")
print(f"   • Difference: {home_win_pct - away_win_pct:.1f} percentage points")

regular = regular_goals / len(goals) * 100
pens = penalty_goals / len(goals) * 100
own = own_goals / len(goals) * 100
print(f"\n2. GOALSCORING PATTERNS")
print(f"   • Regular goals: {regular:.1f}%")
print(f"   • Penalty goals: {pens:.1f}%")
print(f"   • Own goals: {own:.1f}%")

print(f"\n3. TOP PERFORMING NATIONS")
for i, (team, w) in enumerate(top_winners.head(5).items(), 1):
    print(f"   {i}. {team}: {w:,} wins")

print(f"\n4. TOP GOAL SCORERS")
for i, (scorer, g) in enumerate(top_scorers.head(5).items(), 1):
    print(f"   {i}. {scorer}: {g} goals")

print(f"\n5. DATA COVERAGE")
print(f"   • Time period: {results['year'].min()}-{results['year'].max()}")
print(f"   • Total matches: {total_matches:,}")
print(f"   • Total teams: {total_teams}")
print(f"   • Tournament types: {total_tournaments}")
print(f"   • Unique scorers: {total_scorers:,}")
print(f"   • Penalty shootouts: {total_shootouts}")

print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)

import os

# Create folder once at start
os.makedirs('visualizations', exist_ok=True)

# Example - SECTION 7: TOP TEAMS

plt.figure(figsize=(12, 6))
team_matches.head(15).plot(kind='barh', color='steelblue')
plt.xlabel('Total Matches')
plt.title('Top 15 Teams by Matches Played', fontweight='bold')
plt.tight_layout()

# ADD THIS LINE BEFORE plt.show()
plt.savefig('visualizations/01_top_teams.png', dpi=300, bbox_inches='tight')

plt.show()

# Removed incorrect savefig block

import os
os.makedirs('visualizations', exist_ok=True)
print("✓ Folder created")


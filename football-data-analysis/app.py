"""
⚽ International Football Data Analysis Dashboard
Interactive Streamlit frontend for exploring 150+ years of international football history.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="⚽ Football Data Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Hero Title ── */
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00D4AA 0%, #00B4D8 50%, #7B68EE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        color: #8892A4;
        text-align: center;
        margin-top: 0.3rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: linear-gradient(145deg, #1A1F2E 0%, #141822 100%);
        border: 1px solid rgba(0, 212, 170, 0.15);
        border-radius: 16px;
        padding: 1.5rem 1.2rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00D4AA, #00B4D8, #7B68EE);
    }
    .metric-card:hover {
        border-color: rgba(0, 212, 170, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 212, 170, 0.1);
    }
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #00D4AA;
        margin: 0.2rem 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8892A4;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Section Headers ── */
    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #FAFAFA;
        margin-top: 2.5rem;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #00D4AA, transparent);
        border: none;
        border-radius: 2px;
        margin-bottom: 1.5rem;
    }

    /* ── Insight Cards ── */
    .insight-card {
        background: linear-gradient(145deg, #1A1F2E, #141822);
        border: 1px solid rgba(123, 104, 238, 0.2);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .insight-card:hover {
        border-color: rgba(123, 104, 238, 0.5);
        box-shadow: 0 8px 30px rgba(123, 104, 238, 0.08);
    }
    .insight-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #7B68EE;
        font-size: 1.05rem;
        margin-bottom: 0.4rem;
    }
    .insight-text {
        color: #C0C8D8;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #141822 100%);
    }
    [data-testid="stSidebar"] h1 {
        font-size: 1.4rem !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
    }

    /* ── Hide default Streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0E1117; }
    ::-webkit-scrollbar-thumb { background: #1A1F2E; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #00D4AA; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA LOADING (cached)
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    results = pd.read_csv("data/results.csv", parse_dates=["date"])
    goals = pd.read_csv("data/goalscorers.csv", parse_dates=["date"])
    shootouts = pd.read_csv("data/shootouts.csv", parse_dates=["date"])
    former = pd.read_csv("data/former_names.csv", parse_dates=["start_date", "end_date"])

    results["year"] = results["date"].dt.year
    results["total_goals"] = results["home_score"] + results["away_score"]
    goals["year"] = goals["date"].dt.year
    shootouts["year"] = shootouts["date"].dt.year

    return results, goals, shootouts, former


results, goals, shootouts, former = load_data()

# ──────────────────────────────────────────────
# PLOTLY DARK TEMPLATE
# ──────────────────────────────────────────────
COLORS = {
    "teal": "#00D4AA",
    "cyan": "#00B4D8",
    "purple": "#7B68EE",
    "coral": "#FF6B6B",
    "gold": "#FFD93D",
    "orange": "#FF8C42",
    "pink": "#FF6B9D",
    "lime": "#A3E635",
}
GRADIENT = ["#00D4AA", "#00B4D8", "#7B68EE", "#FF6B6B", "#FFD93D", "#FF8C42", "#FF6B9D", "#A3E635"]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#C0C8D8", size=13),
    title_font=dict(family="Outfit, sans-serif", size=20, color="#FAFAFA"),
    margin=dict(l=40, r=20, t=50, b=40),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
    hoverlabel=dict(bgcolor="#1A1F2E", bordercolor="#00D4AA", font_size=13),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)"),
)

def apply_layout(fig, **overrides):
    """Apply the dark theme layout to any Plotly figure."""
    layout = {**PLOTLY_LAYOUT, **overrides}
    fig.update_layout(**layout)
    return fig


# ──────────────────────────────────────────────
# SIDEBAR — Filters
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚽ Dashboard Filters")
    st.markdown("---")

    min_year = int(results["year"].min())
    max_year = int(results["year"].max())
    year_range = st.slider(
        "📅 Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(1900, max_year),
        help="Filter all charts by the selected year range.",
    )

    all_tournaments = sorted(results["tournament"].unique())
    selected_tournaments = st.multiselect(
        "🏆 Tournaments",
        options=all_tournaments,
        default=[],
        help="Leave empty to include all tournaments.",
    )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#555; font-size:0.8rem;'>"
        "Built with ❤️ by <b>Akhil Biju Varghese</b>"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Apply Filters ──
mask = (results["year"] >= year_range[0]) & (results["year"] <= year_range[1])
if selected_tournaments:
    mask &= results["tournament"].isin(selected_tournaments)
filt_results = results[mask].copy()

mask_g = (goals["year"] >= year_range[0]) & (goals["year"] <= year_range[1])
filt_goals = goals[mask_g].copy()

mask_s = (shootouts["year"] >= year_range[0]) & (shootouts["year"] <= year_range[1])
filt_shootouts = shootouts[mask_s].copy()


# ──────────────────────────────────────────────
# HERO SECTION
# ──────────────────────────────────────────────
st.markdown('<p class="hero-title">International Football Analytics</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Exploring 150+ years of international football history — '
    f'{len(filt_results):,} matches across {filt_results["home_team"].nunique() + filt_results["away_team"].nunique()} nations</p>',
    unsafe_allow_html=True,
)

# ── Key Metrics Row ──
teams_all = pd.concat([filt_results["home_team"], filt_results["away_team"]])
total_teams = teams_all.nunique()
total_goals_val = int(filt_results["total_goals"].sum())
avg_goals = filt_results["total_goals"].mean()
total_scorers = filt_goals["scorer"].nunique()

cols = st.columns(6)
metrics = [
    ("🏟️", f"{len(filt_results):,}", "Matches"),
    ("🌍", f"{total_teams}", "Nations"),
    ("⚽", f"{total_goals_val:,}", "Goals Scored"),
    ("📊", f"{avg_goals:.2f}", "Avg Goals/Match"),
    ("👟", f"{total_scorers:,}", "Unique Scorers"),
    ("🎯", f"{len(filt_shootouts):,}", "Shootouts"),
]
for col, (icon, value, label) in zip(cols, metrics):
    col.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-icon">{icon}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-label">{label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────
tab_teams, tab_goals, tab_trends, tab_shootouts, tab_insights = st.tabs(
    ["🏆 Teams", "⚽ Goals", "📈 Trends", "🎯 Shootouts", "💡 Insights"]
)


# ════════════════════════════════════════════
# TAB 1: TEAMS
# ════════════════════════════════════════════
with tab_teams:
    st.markdown('<div class="section-header">🏆 Team Performance</div><hr class="section-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ── Most Matches ──
    with col1:
        home_m = filt_results["home_team"].value_counts()
        away_m = filt_results["away_team"].value_counts()
        team_matches = home_m.add(away_m, fill_value=0).sort_values(ascending=False).head(15)

        fig = px.bar(
            x=team_matches.values,
            y=team_matches.index,
            orientation="h",
            labels={"x": "Total Matches", "y": ""},
            title="Top 15 Teams by Matches Played",
            color=team_matches.values,
            color_continuous_scale=["#1A1F2E", "#00D4AA"],
        )
        fig.update_layout(showlegend=False, coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        apply_layout(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)

    # ── Most Wins ──
    with col2:
        home_wins = filt_results[filt_results["home_score"] > filt_results["away_score"]]["home_team"]
        away_wins = filt_results[filt_results["away_score"] > filt_results["home_score"]]["away_team"]
        top_winners = pd.concat([home_wins, away_wins]).value_counts().head(15)

        fig = px.bar(
            x=top_winners.values,
            y=top_winners.index,
            orientation="h",
            labels={"x": "Total Wins", "y": ""},
            title="Top 15 Most Successful Teams",
            color=top_winners.values,
            color_continuous_scale=["#1A1F2E", "#7B68EE"],
        )
        fig.update_layout(showlegend=False, coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        apply_layout(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    # ── Highest Scoring ──
    with col3:
        home_g = filt_results.groupby("home_team")["home_score"].sum()
        away_g = filt_results.groupby("away_team")["away_score"].sum()
        total_g_team = home_g.add(away_g, fill_value=0).sort_values(ascending=False).head(15)

        fig = px.bar(
            x=total_g_team.values,
            y=total_g_team.index,
            orientation="h",
            labels={"x": "Total Goals", "y": ""},
            title="Top 15 Highest Scoring Teams",
            color=total_g_team.values,
            color_continuous_scale=["#1A1F2E", "#FF6B6B"],
        )
        fig.update_layout(showlegend=False, coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        apply_layout(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)

    # ── Best Defense ──
    with col4:
        home_c = filt_results.groupby("home_team")["away_score"].sum()
        away_c = filt_results.groupby("away_team")["home_score"].sum()
        total_conceded = home_c.add(away_c, fill_value=0).sort_values().head(15)

        fig = px.bar(
            x=total_conceded.values,
            y=total_conceded.index,
            orientation="h",
            labels={"x": "Goals Conceded", "y": ""},
            title="Top 15 Best Defensive Teams",
            color=total_conceded.values,
            color_continuous_scale=["#00B4D8", "#1A1F2E"],
        )
        fig.update_layout(showlegend=False, coloraxis_showscale=False, yaxis=dict(autorange="reversed"))
        apply_layout(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════
# TAB 2: GOALS
# ════════════════════════════════════════════
with tab_goals:
    st.markdown('<div class="section-header">⚽ Goalscoring Analysis</div><hr class="section-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ── Home Advantage ──
    with col1:
        hw = len(filt_results[filt_results["home_score"] > filt_results["away_score"]])
        aw = len(filt_results[filt_results["away_score"] > filt_results["home_score"]])
        dw = len(filt_results[filt_results["home_score"] == filt_results["away_score"]])

        fig = go.Figure(
            data=[go.Pie(
                labels=["Home Wins", "Away Wins", "Draws"],
                values=[hw, aw, dw],
                hole=0.55,
                marker=dict(colors=[COLORS["teal"], COLORS["coral"], COLORS["purple"]]),
                textinfo="label+percent",
                textfont=dict(size=13),
                hovertemplate="<b>%{label}</b><br>Matches: %{value:,}<br>Percentage: %{percent}<extra></extra>",
            )]
        )
        fig.update_layout(title="Home Advantage Analysis")
        fig.add_annotation(
            text=f"<b>{hw/(hw+aw)*100:.0f}%</b><br><span style='font-size:11px;color:#8892A4'>Home Win</span>",
            showarrow=False, font=dict(size=22, color="#00D4AA"),
        )
        apply_layout(fig, height=450)
        st.plotly_chart(fig, use_container_width=True)

    # ── Goal Type Distribution ──
    with col2:
        penalty_g = int(filt_goals["penalty"].sum())
        own_g = int(filt_goals["own_goal"].sum())
        regular_g = len(filt_goals) - penalty_g - own_g

        fig = go.Figure(
            data=[go.Pie(
                labels=["Regular Goals", "Penalties", "Own Goals"],
                values=[regular_g, penalty_g, own_g],
                hole=0.55,
                marker=dict(colors=[COLORS["cyan"], COLORS["gold"], COLORS["orange"]]),
                textinfo="label+percent",
                textfont=dict(size=13),
                hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>",
            )]
        )
        fig.update_layout(title="Goal Type Distribution")
        fig.add_annotation(
            text=f"<b>{len(filt_goals):,}</b><br><span style='font-size:11px;color:#8892A4'>Total Goals</span>",
            showarrow=False, font=dict(size=20, color="#00B4D8"),
        )
        apply_layout(fig, height=450)
        st.plotly_chart(fig, use_container_width=True)

    # ── Top Scorers ──
    st.markdown('<div class="section-header">👟 Top 20 All-Time Goal Scorers</div><hr class="section-divider">', unsafe_allow_html=True)

    top_scorers = filt_goals["scorer"].value_counts().head(20).iloc[::-1]
    fig = px.bar(
        x=top_scorers.values,
        y=top_scorers.index,
        orientation="h",
        labels={"x": "Goals", "y": ""},
        color=top_scorers.values,
        color_continuous_scale=["#1A1F2E", "#FFD93D"],
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    apply_layout(fig, height=600, title_text="Top 20 International Goal Scorers")
    st.plotly_chart(fig, use_container_width=True)

    # ── Goal Distribution ──
    st.markdown('<div class="section-header">📊 Goals Distribution</div><hr class="section-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(
            filt_results, x="home_score", nbins=15,
            labels={"home_score": "Goals", "count": "Frequency"},
            title="Home Team Goals Distribution",
            color_discrete_sequence=[COLORS["teal"]],
        )
        fig.update_traces(marker_line_color="#0E1117", marker_line_width=1)
        apply_layout(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            filt_results, x="away_score", nbins=15,
            labels={"away_score": "Goals", "count": "Frequency"},
            title="Away Team Goals Distribution",
            color_discrete_sequence=[COLORS["coral"]],
        )
        fig.update_traces(marker_line_color="#0E1117", marker_line_width=1)
        apply_layout(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════
# TAB 3: TRENDS
# ════════════════════════════════════════════
with tab_trends:
    st.markdown('<div class="section-header">📈 Historical Trends</div><hr class="section-divider">', unsafe_allow_html=True)

    # ── Goals Over Time ──
    goals_yr = filt_results.groupby("year").agg(
        total_goals=("total_goals", "sum"),
        matches=("date", "count"),
    )
    goals_yr["avg_goals"] = goals_yr["total_goals"] / goals_yr["matches"]

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                        subplot_titles=("Total Goals per Year", "Average Goals per Match"))

    fig.add_trace(
        go.Scatter(
            x=goals_yr.index, y=goals_yr["total_goals"],
            mode="lines", fill="tozeroy",
            line=dict(color=COLORS["teal"], width=2.5),
            fillcolor="rgba(0,212,170,0.12)",
            name="Total Goals",
            hovertemplate="Year: %{x}<br>Goals: %{y:,}<extra></extra>",
        ),
        row=1, col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=goals_yr.index, y=goals_yr["avg_goals"],
            mode="lines+markers",
            line=dict(color=COLORS["coral"], width=2),
            marker=dict(size=4),
            name="Avg Goals/Match",
            hovertemplate="Year: %{x}<br>Avg: %{y:.2f}<extra></extra>",
        ),
        row=2, col=1,
    )

    historical_avg = goals_yr["avg_goals"].mean()
    fig.add_hline(
        y=historical_avg, row=2, col=1,
        line_dash="dash", line_color=COLORS["gold"],
        annotation_text=f"Historical Avg: {historical_avg:.2f}",
        annotation_font_color=COLORS["gold"],
    )

    apply_layout(fig, height=600, title_text="Goals Over Time")
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")
    st.plotly_chart(fig, use_container_width=True)

    # ── Matches Over Time ──
    st.markdown('<div class="section-header">🗓️ Matches per Year</div><hr class="section-divider">', unsafe_allow_html=True)

    matches_yr = filt_results.groupby("year").size().reset_index(name="matches")
    fig = px.area(
        matches_yr, x="year", y="matches",
        labels={"year": "Year", "matches": "Matches Played"},
        color_discrete_sequence=[COLORS["purple"]],
    )
    fig.update_traces(fillcolor="rgba(123,104,238,0.15)", line_width=2.5)
    apply_layout(fig, height=350, title_text="International Matches per Year")
    st.plotly_chart(fig, use_container_width=True)

    # ── Tournament Breakdown ──
    st.markdown('<div class="section-header">🏆 Top Tournaments</div><hr class="section-divider">', unsafe_allow_html=True)

    tourn_counts = filt_results["tournament"].value_counts().head(15).iloc[::-1]
    fig = px.bar(
        x=tourn_counts.values,
        y=tourn_counts.index,
        orientation="h",
        labels={"x": "Matches", "y": ""},
        color=tourn_counts.values,
        color_continuous_scale=["#1A1F2E", "#7B68EE"],
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    apply_layout(fig, height=500, title_text="Top 15 Tournaments by Match Count")
    st.plotly_chart(fig, use_container_width=True)

    # ── Penalties Over Time ──
    st.markdown('<div class="section-header">🔴 Penalty Goals Over Time</div><hr class="section-divider">', unsafe_allow_html=True)

    pen_yr = filt_goals[filt_goals["penalty"]].groupby("year").size().reset_index(name="penalties")
    fig = px.line(
        pen_yr, x="year", y="penalties",
        labels={"year": "Year", "penalties": "Penalty Goals"},
        color_discrete_sequence=[COLORS["coral"]],
        markers=True,
    )
    fig.update_traces(marker_size=5, line_width=2.5)
    apply_layout(fig, height=350, title_text="Penalty Goals Scored per Year")
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════
# TAB 4: SHOOTOUTS
# ════════════════════════════════════════════
with tab_shootouts:
    st.markdown('<div class="section-header">🎯 Penalty Shootout Analysis</div><hr class="section-divider">', unsafe_allow_html=True)

    s_col1, s_col2, s_col3 = st.columns(3)
    s_col1.metric("Total Shootouts", f"{len(filt_shootouts):,}")
    s_col2.metric("Unique Winners", f"{filt_shootouts['winner'].nunique()}")
    s_col3.metric(
        "Year Range",
        f"{int(filt_shootouts['year'].min()) if len(filt_shootouts) else 'N/A'}–{int(filt_shootouts['year'].max()) if len(filt_shootouts) else 'N/A'}",
    )

    col1, col2 = st.columns(2)

    # ── Most Shootout Wins ──
    with col1:
        so_winners = filt_shootouts["winner"].value_counts().head(15).iloc[::-1]
        fig = px.bar(
            x=so_winners.values,
            y=so_winners.index,
            orientation="h",
            labels={"x": "Shootout Wins", "y": ""},
            color=so_winners.values,
            color_continuous_scale=["#1A1F2E", "#FF6B6B"],
        )
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        apply_layout(fig, height=500, title_text="Teams with Most Shootout Wins")
        st.plotly_chart(fig, use_container_width=True)

    # ── Shootouts Per Year ──
    with col2:
        so_yr = filt_shootouts.groupby("year").size().reset_index(name="shootouts")
        fig = px.bar(
            so_yr, x="year", y="shootouts",
            labels={"year": "Year", "shootouts": "Shootouts"},
            color_discrete_sequence=[COLORS["cyan"]],
        )
        fig.update_traces(marker_line_color="#0E1117", marker_line_width=0.5)
        apply_layout(fig, height=500, title_text="Penalty Shootouts per Year")
        st.plotly_chart(fig, use_container_width=True)

    # ── Correlation Heatmap ──
    st.markdown('<div class="section-header">🔗 Score Correlation</div><hr class="section-divider">', unsafe_allow_html=True)

    corr = filt_results[["home_score", "away_score"]].corr()
    fig = px.imshow(
        corr,
        text_auto=".3f",
        color_continuous_scale=["#7B68EE", "#0E1117", "#00D4AA"],
        labels=dict(color="Correlation"),
        x=["Home Score", "Away Score"],
        y=["Home Score", "Away Score"],
    )
    apply_layout(fig, height=400, title_text="Home vs Away Score Correlation")
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════
# TAB 5: KEY INSIGHTS
# ════════════════════════════════════════════
with tab_insights:
    st.markdown('<div class="section-header">💡 Key Insights</div><hr class="section-divider">', unsafe_allow_html=True)

    hw_count = len(filt_results[filt_results["home_score"] > filt_results["away_score"]])
    aw_count = len(filt_results[filt_results["away_score"] > filt_results["home_score"]])
    decisive = hw_count + aw_count
    home_pct = (hw_count / decisive * 100) if decisive else 0
    away_pct = (aw_count / decisive * 100) if decisive else 0

    pen_g = int(filt_goals["penalty"].sum())
    own_g = int(filt_goals["own_goal"].sum())
    reg_g = len(filt_goals) - pen_g - own_g
    total_g = len(filt_goals) if len(filt_goals) > 0 else 1

    top_5_winners = pd.concat([
        filt_results[filt_results["home_score"] > filt_results["away_score"]]["home_team"],
        filt_results[filt_results["away_score"] > filt_results["home_score"]]["away_team"],
    ]).value_counts().head(5)

    top_5_scorers = filt_goals["scorer"].value_counts().head(5)

    insights = [
        (
            "🏠 Home Advantage is Real",
            f"Home teams win <b>{home_pct:.1f}%</b> of decisive matches vs <b>{away_pct:.1f}%</b> for away teams — "
            f"a gap of <b>{home_pct - away_pct:.1f}</b> percentage points. This pattern has been consistent across all eras.",
        ),
        (
            "⚽ Goalscoring Breakdown",
            f"Of all {total_g:,} goals: <b>{reg_g/total_g*100:.1f}%</b> regular goals, "
            f"<b>{pen_g/total_g*100:.1f}%</b> penalties, and <b>{own_g/total_g*100:.1f}%</b> own goals. "
            "Penalty frequency increased significantly post-1990s.",
        ),
        (
            "🏆 Top Performing Nations",
            "<br>".join([f"&nbsp;&nbsp;{i}. <b>{t}</b> — {w:,} wins" for i, (t, w) in enumerate(top_5_winners.items(), 1)]),
        ),
        (
            "👟 All-Time Top Scorers",
            "<br>".join([f"&nbsp;&nbsp;{i}. <b>{s}</b> — {g} goals" for i, (s, g) in enumerate(top_5_scorers.items(), 1)]),
        ),
        (
            "📊 Data Coverage",
            f"This dataset spans <b>{int(filt_results['year'].min())}–{int(filt_results['year'].max())}</b>, "
            f"covering <b>{len(filt_results):,}</b> matches across <b>{total_teams}</b> nations "
            f"and <b>{filt_results['tournament'].nunique()}</b> tournament types.",
        ),
    ]

    for title, text in insights:
        st.markdown(
            f'<div class="insight-card">'
            f'<div class="insight-title">{title}</div>'
            f'<div class="insight-text">{text}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Former Names Table ──
    st.markdown('<div class="section-header">🗺️ Former Country Names</div><hr class="section-divider">', unsafe_allow_html=True)

    former_display = former.copy()
    former_display["start_date"] = former_display["start_date"].dt.strftime("%Y-%m-%d")
    former_display["end_date"] = former_display["end_date"].dt.strftime("%Y-%m-%d")
    former_display.columns = ["Current Name", "Former Name", "Start Date", "End Date"]
    st.dataframe(former_display, use_container_width=True, hide_index=True)

# -*- coding: utf-8 -*-
"""
Anime Analytics Dashboard — Streamlit App
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Anime Analytics",
    page_icon="⛩️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

/* Root background */
.stApp {
    background: #0a0a12;
    color: #e8e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f1e !important;
    border-right: 1px solid #1e1e3a;
}

[data-testid="stSidebar"] * {
    color: #c8c8e0 !important;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 1px;
}

h1 {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #e040fb, #7c4dff, #00b0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #12122a, #1a1a35);
    border: 1px solid #2a2a5a;
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 4px 24px rgba(124, 77, 255, 0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(124, 77, 255, 0.18);
}

[data-testid="stMetricLabel"] {
    color: #9090c0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

[data-testid="stMetricValue"] {
    color: #e040fb !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* Section divider */
.section-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #7c4dff;
    margin-bottom: 4px;
}

.section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #e8e8f0;
    margin-top: 0;
    margin-bottom: 16px;
}

/* Tag chips */
.tag-chip {
    display: inline-block;
    background: rgba(124, 77, 255, 0.15);
    border: 1px solid rgba(124, 77, 255, 0.35);
    color: #b39dff;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    margin: 3px;
    font-family: 'Inter', sans-serif;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 1px solid #1e1e3a;
    margin: 28px 0;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #1e1e3a;
}

/* Input widgets */
.stSelectbox > div > div,
.stSlider > div > div {
    background: #12122a !important;
    border-color: #2a2a5a !important;
    color: #e8e8f0 !important;
}

/* Scroll bar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a12; }
::-webkit-scrollbar-thumb { background: #2a2a5a; border-radius: 6px; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #12122a 0%, #1a0a35 50%, #0a1225 100%);
    border: 1px solid #2a1a5a;
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '⛩';
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.12;
}

.hero-subtitle {
    color: #9090c0;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    margin-top: 6px;
    font-weight: 300;
}

.stButton > button {
    background: linear-gradient(135deg, #7c4dff, #e040fb);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly Dark Theme ───────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(18,18,42,0.6)",
    font=dict(color="#c8c8e0", family="Inter, sans-serif"),
    xaxis=dict(gridcolor="#1e1e3a", zerolinecolor="#1e1e3a", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#1e1e3a", zerolinecolor="#1e1e3a", tickfont=dict(size=11)),
    margin=dict(l=20, r=20, t=50, b=20),
)
PURPLE_SCALE = [[0, "#2a0a5a"], [0.5, "#7c4dff"], [1.0, "#e040fb"]]

# ─── Data Loading ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Anime.csv")
    except FileNotFoundError:
        # Demo dataset if CSV not found
        np.random.seed(42)
        genres = ["Action", "Romance", "Fantasy", "Sci-Fi", "Comedy", "Horror", "Sports", "Thriller"]
        names = [
            "Fullmetal Alchemist: Brotherhood", "Steins;Gate", "Hunter x Hunter",
            "Attack on Titan", "Death Note", "Violet Evergarden", "Your Lie in April",
            "Demon Slayer", "Jujutsu Kaisen", "Mob Psycho 100",
            "Cowboy Bebop", "Neon Genesis Evangelion", "Sword Art Online",
            "Re:Zero", "Overlord", "The Rising of the Shield Hero",
            "Vinland Saga", "Made in Abyss", "Konosuba", "No Game No Life",
        ] + [f"Anime Title {i}" for i in range(1, 81)]
        n = len(names)
        df = pd.DataFrame({
            "Name": names,
            "Rating": np.clip(np.random.normal(7.8, 1.1, n), 4.0, 10.0).round(2),
            "Episodes": np.random.choice([12, 13, 24, 25, 26, 50, 100, 366], n),
            "Tags": np.random.choice(genres, n),
            "Members": np.random.randint(5_000, 1_000_000, n),
            "Year": np.random.randint(2000, 2024, n),
        })
    df.drop_duplicates(inplace=True)
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Episodes"] = pd.to_numeric(df["Episodes"], errors="coerce")
    df = df.dropna(subset=["Rating", "Episodes"])
    return df

df = load_data()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⛩ Filters")
    st.markdown("---")

    rating_range = st.slider(
        "Rating Range",
        float(df["Rating"].min()),
        float(df["Rating"].max()),
        (float(df["Rating"].min()), float(df["Rating"].max())),
        step=0.1,
    )

    ep_max = int(df["Episodes"].max())
    ep_range = st.slider("Max Episodes", 1, ep_max, ep_max)

    if "Tags" in df.columns:
        all_tags = sorted(df["Tags"].dropna().unique().tolist())
        selected_tags = st.multiselect("Genre / Tags", all_tags, default=all_tags[:5] if len(all_tags) > 5 else all_tags)
    else:
        selected_tags = None

    top_n = st.selectbox("Top N Anime", [5, 10, 15, 20], index=1)

    st.markdown("---")
    st.markdown('<p style="color:#5a5a8a;font-size:0.75rem;font-family:Inter;">Anime Analytics Dashboard · 2024</p>', unsafe_allow_html=True)

# ─── Filter Data ─────────────────────────────────────────────────────────────
filtered = df[
    (df["Rating"] >= rating_range[0]) &
    (df["Rating"] <= rating_range[1]) &
    (df["Episodes"] <= ep_range)
]
if selected_tags and "Tags" in df.columns:
    filtered = filtered[filtered["Tags"].isin(selected_tags)]

top_n_df = filtered.nlargest(top_n, "Rating")

# ─── Hero Banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>Anime Analytics</h1>
    <p class="hero-subtitle">Explore ratings, episodes, and genres across your anime dataset — filtered and visualized in real time.</p>
</div>
""", unsafe_allow_html=True)

# ─── KPI Metrics ─────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Anime", f"{len(filtered):,}")
c2.metric("Avg Rating", f"{filtered['Rating'].mean():.2f} ⭐")
c3.metric("Avg Episodes", f"{filtered['Episodes'].mean():.0f}")
c4.metric("Top Rating", f"{filtered['Rating'].max():.2f}")

st.markdown("<hr>", unsafe_allow_html=True)

# ─── Section 1: Top N Bar Chart ──────────────────────────────────────────────
st.markdown(f'<p class="section-label">Rankings</p><p class="section-title">Top {top_n} Highest Rated Anime</p>', unsafe_allow_html=True)

fig_bar = px.bar(
    top_n_df.sort_values("Rating"),
    x="Rating",
    y="Name",
    orientation="h",
    color="Rating",
    color_continuous_scale=PURPLE_SCALE,
    text="Rating",
)
fig_bar.update_traces(texttemplate="%{text:.2f}", textposition="outside", marker_line_width=0)
fig_bar.update_layout(
    **PLOTLY_LAYOUT,
    height=420,
    showlegend=False,
    coloraxis_showscale=False,
    xaxis_range=[filtered["Rating"].min() - 0.5, 10.2],
)
fig_bar.update_yaxes(title="")
fig_bar.update_xaxes(title="Rating")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─── Section 2: Distribution + Scatter ───────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<p class="section-label">Distribution</p><p class="section-title">Rating Spread</p>', unsafe_allow_html=True)
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=filtered["Rating"],
        nbinsx=20,
        marker=dict(
            color="rgba(124, 77, 255, 0.75)",
            line=dict(color="#e040fb", width=0.6),
        ),
        name="Rating",
    ))
    fig_hist.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False)
    fig_hist.update_xaxes(title="Rating")
    fig_hist.update_yaxes(title="Count")
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    st.markdown('<p class="section-label">Correlation</p><p class="section-title">Episodes vs Rating</p>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        filtered,
        x="Episodes",
        y="Rating",
        color="Rating",
        color_continuous_scale=PURPLE_SCALE,
        opacity=0.75,
        hover_name="Name" if "Name" in filtered.columns else None,
    )
    fig_scatter.update_traces(marker=dict(size=6, line=dict(width=0)))
    fig_scatter.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─── Section 3: Genre / Tag Breakdown ────────────────────────────────────────
if "Tags" in filtered.columns:
    st.markdown('<p class="section-label">Genre</p><p class="section-title">Tag Breakdown</p>', unsafe_allow_html=True)

    col_pie, col_tag_bar = st.columns([1, 1.5])

    tag_counts = filtered["Tags"].value_counts().reset_index()
    tag_counts.columns = ["Tag", "Count"]

    with col_pie:
        fig_pie = px.pie(
            tag_counts.head(8),
            names="Tag",
            values="Count",
            color_discrete_sequence=px.colors.sequential.Purples_r,
            hole=0.55,
        )
        fig_pie.update_traces(textfont_size=12, pull=[0.04]*8)
        fig_pie.update_layout(
            **PLOTLY_LAYOUT,
            height=320,
            legend=dict(font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_tag_bar:
        tag_avg = filtered.groupby("Tags")["Rating"].mean().reset_index().sort_values("Rating", ascending=False).head(10)
        fig_tag = px.bar(
            tag_avg,
            x="Tags",
            y="Rating",
            color="Rating",
            color_continuous_scale=PURPLE_SCALE,
        )
        fig_tag.update_layout(**PLOTLY_LAYOUT, height=320, coloraxis_showscale=False)
        fig_tag.update_xaxes(tickangle=-30, title="")
        fig_tag.update_yaxes(title="Avg Rating")
        st.plotly_chart(fig_tag, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# ─── Section 4: Raw Data Table ───────────────────────────────────────────────
st.markdown('<p class="section-label">Dataset</p><p class="section-title">Browse Filtered Anime</p>', unsafe_allow_html=True)

cols_to_show = [c for c in ["Name", "Rating", "Episodes", "Tags", "Members", "Year"] if c in filtered.columns]
st.dataframe(
    filtered[cols_to_show].sort_values("Rating", ascending=False).reset_index(drop=True),
    use_container_width=True,
    height=320,
)

st.download_button(
    label="⬇ Download Filtered CSV",
    data=filtered[cols_to_show].to_csv(index=False).encode("utf-8"),
    file_name="filtered_anime.csv",
    mime="text/csv",
)
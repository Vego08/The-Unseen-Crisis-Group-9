"""
Silent Crisis - Global Mental Health Intelligence Dashboard
============================================================
A cinematic, policy-grade Streamlit dashboard exploring the unequal
global mental health crisis through a four-chapter data narrative.

Stakeholder : WHO Global Mental Health Response Council
Run with    : streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import json


# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Silent Crisis · Global Mental Health Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. DESIGN SYSTEM
# ============================================================
THEME = {
    # --- Foundation ---
    "bg_app":        "#081120",
    "bg_panel":      "#101B2D",
    "bg_panel_alt":  "#162236",
    "bg_chart":      "#0C1628",

    # --- Lines & borders ---
    "border":        "#1E2E45",
    "border_strong": "#2A3F5C",
    "grid":          "#172033",

    # --- Typography ---
    "text":          "#F3F4F6",
    "text_muted":    "#AAB0BC",
    "text_dim":      "#5C6475",

    # --- Interactive accent ---
    "accent_teal":   "#4EA8DE",
    "accent_teal_d": "#2E88BE",

    # --- Crisis accent (high) ---
    "accent_coral":  "#C62828",
    "accent_coral_d":"#9B1C1C",

    # --- Warning / medium crisis ---
    "accent_amber":  "#E76F51",

    # --- Low crisis / gold ---
    "accent_gold":   "#E9C46A",

    # --- Supporting tones ---
    "accent_lavender": "#7B8FBF",
    "accent_steel":    "#4EA8DE",
    "accent_ocean":    "#2E88BE",
    "accent_sage":     "#6BAF8A",
}

# Crisis colour scale: gold (low) → orange (medium) → red (high)
CRISIS_SCALE = [
    [0.00, "#2A3F6F"],
    [0.25, "#5C3A1E"],
    [0.50, "#E9C46A"],
    [0.75, "#E76F51"],
    [1.00, "#C62828"],
]

INCOME_PALETTE = {
    "High":          "#C62828",   # Red
    "Upper-Middle":  "#E76F51",   # Orange
    "Lower-Middle":  "#D4A017",   # Mustard
    "Low":           "#E9C46A",   # Yellow
}



# ============================================================
# 3. GLOBAL CSS
# ============================================================
st.markdown(f"""
<style>
/* ---------- Page ---------- */
.stApp {{
    background:
        radial-gradient(1400px 700px at 12% -10%, rgba(78,168,222,0.04), transparent 60%),
        radial-gradient(1100px 550px at 92% 0%,  rgba(198,40,40,0.04),  transparent 60%),
        {THEME["bg_app"]};
    color: {THEME["text"]};
}}
html, body, [class*="css"] {{
    font-family: 'Inter', 'Helvetica Neue', system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
h1, h2, h3, h4, h5 {{ color: {THEME["text"]}; letter-spacing: -0.01em; }}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0D1A2E 0%, #081120 100%);
    border-right: 1px solid {THEME["border"]};
}}
[data-testid="stSidebar"] * {{ color: {THEME["text"]}; }}
.sidebar-brand {{
    font-size: 1.18rem; font-weight: 700; letter-spacing: 0.01em;
}}
.sidebar-tag {{
    color: {THEME["accent_teal"]}; font-size: 0.7rem;
    text-transform: uppercase; letter-spacing: 0.22em; font-weight: 600;
}}

/* Sidebar navigation links */
.nav-list a {{
    display: block;
    color: {THEME["text_muted"]} !important;
    text-decoration: none;
    padding: 0.45rem 0.7rem;
    border-radius: 8px;
    font-size: 0.88rem;
    line-height: 1.35;
    border-left: 2px solid transparent;
    transition: all 0.18s ease;
}}
.nav-list a:hover {{
    color: {THEME["text"]} !important;
    background: rgba(78,168,222,0.07);
    border-left-color: {THEME["accent_teal"]};
}}
.nav-list a .nav-num {{
    color: {THEME["accent_teal"]};
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.72rem;
    margin-right: 0.5rem;
    font-weight: 600;
}}

/* Compact expanders for filters */
[data-testid="stSidebar"] details {{
    background: rgba(255,255,255,0.015);
    border: 1px solid {THEME["border"]};
    border-radius: 10px;
    margin-bottom: 0.6rem;
}}
[data-testid="stSidebar"] details summary {{
    padding: 0.6rem 0.85rem;
    font-size: 0.85rem;
    color: {THEME["text"]};
}}
[data-testid="stSidebar"] details[open] summary {{
    border-bottom: 1px solid {THEME["border"]};
}}
.filter-summary {{
    color: {THEME["text_muted"]};
    font-size: 0.75rem;
    margin-top: 0.15rem;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"] {{
    margin-bottom: -0.4rem;
}}
[data-testid="stSidebar"] [data-testid="stCheckbox"] label p {{
    font-size: 0.85rem;
    color: {THEME["text"]};
}}

/* ---------- Hero ---------- */
.hero {{
    position: relative;
    padding: 2.6rem 2.4rem;
    border-radius: 22px;
    background:
        linear-gradient(135deg, rgba(198,40,40,0.07) 0%,
                                rgba(78,168,222,0.05) 50%,
                                rgba(233,196,106,0.04) 100%),
        {THEME["bg_panel"]};
    border: 1px solid {THEME["border"]};
    margin-bottom: 1.6rem;
    overflow: hidden;
}}
.hero::after {{
    content: ""; position: absolute; right: -120px; top: -120px;
    width: 360px; height: 360px; border-radius: 50%;
    background: radial-gradient(circle, rgba(198,40,40,0.10), transparent 70%);
    pointer-events: none;
}}
.hero-eyebrow {{
    color: {THEME["accent_teal"]}; font-size: 0.72rem;
    letter-spacing: 0.28em; text-transform: uppercase;
    font-weight: 600; margin-bottom: 0.6rem;
}}
.hero h1 {{
    font-size: 2.9rem; font-weight: 700; line-height: 1.05; margin: 0 0 0.6rem 0;
    background: linear-gradient(90deg, #FFFFFF 0%, #E9C46A 55%, #E76F51 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.hero-subtitle {{
    font-size: 1.12rem; color: {THEME["text"]}; opacity: 0.86;
    max-width: 800px; line-height: 1.55; margin: 0;
}}
.hero-meta {{
    margin-top: 1.4rem; display: flex; gap: 1.4rem; flex-wrap: wrap;
    color: {THEME["text_muted"]}; font-size: 0.82rem;
}}
.hero-meta strong {{ color: {THEME["text"]}; }}

/* ---------- Chapter marker ---------- */
.chapter-marker {{
    display: flex; align-items: center; gap: 0.9rem; margin: 2.6rem 0 0.4rem 0;
}}
.chapter-num {{
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.72rem; letter-spacing: 0.25em;
    color: {THEME["accent_teal"]}; font-weight: 600;
    padding: 0.3rem 0.7rem;
    border: 1px solid {THEME["border"]}; border-radius: 999px;
    background: rgba(78,168,222,0.06);
}}
.chapter-line {{
    flex: 1; height: 1px;
    background: linear-gradient(90deg, {THEME["border"]}, transparent);
}}
.chapter-title {{
    font-size: 1.85rem; font-weight: 700; color: {THEME["text"]};
    margin: 0.4rem 0; letter-spacing: -0.015em;
}}
.chapter-lede {{
    color: {THEME["text_muted"]}; font-size: 1.02rem;
    max-width: 820px; line-height: 1.55; margin-bottom: 1.4rem;
}}

/* ---------- Pull-quote ---------- */
.pull-quote {{
    margin: 0.4rem 0 1.6rem 0;
    padding: 1.1rem 1.4rem 1.1rem 1.6rem;
    border-left: 3px solid {THEME["accent_coral"]};
    background:
        linear-gradient(90deg,
            rgba(198,40,40,0.09) 0%,
            rgba(198,40,40,0.02) 60%,
            transparent 100%);
    border-radius: 10px;
    color: {THEME["text"]};
    font-size: 1.18rem;
    font-style: italic;
    line-height: 1.55;
    letter-spacing: 0.005em;
    max-width: 920px;
    box-shadow: 0 0 0 1px {THEME["border"]};
}}
.pull-quote .pq-tag {{
    display: block;
    font-style: normal;
    font-size: 0.66rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: {THEME["accent_coral"]};
    font-weight: 600;
    margin-bottom: 0.45rem;
}}
.pull-quote em {{
    color: {THEME["accent_amber"]}; font-style: italic;
}}

/* ---------- KPI cards ---------- */
.kpi {{
    background: {THEME["bg_panel"]};
    border: 1px solid {THEME["border"]};
    border-radius: 16px;
    padding: 1.15rem 1.25rem;
    height: 100%;
    min-height: 118px;
    max-height: 118px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease;
}}
.kpi:hover {{
    border-color: {THEME["border_strong"]};
    transform: translateY(-1px);
}}
.kpi-label {{
    color: {THEME["text_muted"]}; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 0.14em;
    font-weight: 600; margin-bottom: 0.55rem;
}}
.kpi-value {{
    color: {THEME["text"]}; font-size: 1.85rem; font-weight: 700;
    line-height: 1.1; margin-bottom: 0.25rem;
}}
.kpi-delta {{ font-size: 0.78rem; color: {THEME["text_dim"]}; min-height: 1.1em; }}
.kpi-accent-coral    .kpi-value {{ color: {THEME["accent_coral"]}; }}
.kpi-accent-amber    .kpi-value {{ color: {THEME["accent_amber"]}; }}
.kpi-accent-teal     .kpi-value {{ color: {THEME["accent_teal"]}; }}
.kpi-accent-lavender .kpi-value {{ color: {THEME["accent_lavender"]}; }}
.kpi-accent-sage     .kpi-value {{ color: {THEME["accent_sage"]}; }}
.kpi-accent-steel    .kpi-value {{ color: {THEME["accent_steel"]}; }}
.kpi-accent-gold     .kpi-value {{ color: {THEME["accent_gold"]}; }}

/* ---------- Insight callouts ---------- */
.callout {{
    background: linear-gradient(135deg, rgba(78,168,222,0.06), rgba(123,143,191,0.04));
    border-left: 3px solid {THEME["accent_teal"]};
    border-radius: 8px; padding: 0.9rem 1.1rem; margin: 1rem 0;
    color: {THEME["text"]}; font-size: 0.95rem; line-height: 1.55;
}}
.callout-warn   {{ border-left-color: {THEME["accent_amber"]};
                   background: linear-gradient(135deg, rgba(231,111,81,0.07), rgba(233,196,106,0.04)); }}
.callout-crisis {{ border-left-color: {THEME["accent_coral"]};
                   background: linear-gradient(135deg, rgba(198,40,40,0.09), rgba(198,40,40,0.02)); }}

/* ---------- Helper notes ---------- */
.helper-note {{
    font-size: 0.78rem;
    color: {THEME["text_muted"]};
    border-left: 2px solid {THEME["accent_teal"]};
    padding: 0.45rem 0.8rem;
    background: rgba(78,168,222,0.04);
    border-radius: 0 6px 6px 0;
    margin: 0.6rem 0 1rem 0;
    line-height: 1.5;
}}

/* ---------- Income legend ---------- */
.income-legend {{
    margin: 0.4rem 0 1.4rem 0;
    padding: 1rem 1.2rem;
    background: {THEME["bg_panel"]};
    border: 1px solid {THEME["border"]};
    border-radius: 12px;
}}
.income-legend-title {{
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {THEME["text_muted"]};
    font-weight: 600;
    margin-bottom: 0.7rem;
}}
.income-legend-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.7rem 1.2rem;
}}
.income-row {{
    display: flex;
    align-items: center;
    gap: 0.65rem;
    font-size: 0.86rem;
    color: {THEME["text"]};
}}
.income-dot {{
    width: 10px; height: 10px; border-radius: 50%;
    flex-shrink: 0;
}}
.income-row .income-range {{
    color: {THEME["text_muted"]};
    font-size: 0.78rem;
    margin-left: 0.2rem;
}}
.income-legend-foot {{
    color: {THEME["text_dim"]};
    font-size: 0.72rem;
    margin-top: 0.7rem;
    line-height: 1.4;
}}

/* ---------- Policy cards ---------- */
.policy-card {{
    background: {THEME["bg_panel"]};
    border: 1px solid {THEME["border"]};
    border-left: 3px solid {THEME["accent_teal"]};
    border-radius: 12px; padding: 1rem 1.15rem; height: 100%;
}}
.policy-card.high {{ border-left-color: {THEME["accent_coral"]}; }}
.policy-card.med  {{ border-left-color: {THEME["accent_amber"]}; }}
.policy-card.low  {{ border-left-color: {THEME["accent_sage"]}; }}
.policy-tag {{
    display: inline-block; font-size: 0.65rem;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: {THEME["text_muted"]}; font-weight: 600; margin-bottom: 0.4rem;
}}
.policy-title {{ font-size: 1.0rem; font-weight: 600; color: {THEME["text"]}; margin-bottom: 0.35rem; }}
.policy-body  {{ font-size: 0.86rem; color: {THEME["text_muted"]}; line-height: 1.5; }}

/* ---------- Disclaimer ---------- */
.disclaimer {{
    font-size: 0.78rem; color: {THEME["text_dim"]};
    border: 1px dashed {THEME["border"]};
    border-radius: 10px; padding: 0.7rem 0.9rem; margin-top: 0.6rem;
    background: rgba(255,255,255,0.015);
    line-height: 1.55;
}}

/* ---------- Spacing ---------- */
.spacer-sm  {{ height: 0.6rem; }}
.spacer-md  {{ height: 1.2rem; }}
.spacer-lg  {{ height: 2rem; }}

/* ---------- Streamlit metric tweaks ---------- */
[data-testid="stMetricValue"] {{ color: {THEME["text"]}; font-weight: 700; }}
[data-testid="stMetricLabel"] {{ color: {THEME["text_muted"]}; }}

/* ---------- Footer ---------- */
.footer {{
    margin-top: 3rem; padding: 1.4rem 0;
    border-top: 1px solid {THEME["border"]};
    color: {THEME["text_dim"]}; font-size: 0.78rem; text-align: center;
}}
html {{ scroll-behavior: smooth; }}
[id^="chapter-"] {{ scroll-margin-top: 1rem; }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 4. DATA LOADING (cached)
# ============================================================
@st.cache_data(show_spinner=False)
def load_data(path: str = "data/merged_dataset.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ["country", "iso3", "region", "income_group"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    yesno_map = {
        "yes": 1, "y": 1, "true": 1, "1": 1,
        "no": 0,  "n": 0, "false": 0, "0": 0,
    }
    for col in ["mh_policy_exists", "mh_law_exists"]:
        if col in df.columns and df[col].dtype == object:
            df[col] = (
                df[col].astype(str).str.strip().str.lower()
                      .map(yesno_map)
            )
    if "region" in df.columns:
        df["region_display"] = df["region"].astype(str).str.strip()
    return df


df = load_data()

# ============================================================
# 5. HELPERS
# ============================================================
def fmt_num(value, spec=".1f", suffix=""):
    if value is None or pd.isna(value):
        return "-"
    return f"{value:{spec}}{suffix}"


def fmt_usd(value, decimals=1):
    if value is None or pd.isna(value):
        return "-"
    return f"${value:,.{decimals}f}"


def style_fig(fig, *, height=480, title=None):
    fig.update_layout(
        paper_bgcolor=THEME["bg_panel"],
        plot_bgcolor=THEME["bg_chart"],
        font=dict(family="Inter, Helvetica Neue, system-ui, sans-serif",
                  color=THEME["text"], size=13),
        title=dict(
            text=title or (fig.layout.title.text if fig.layout.title else "") or "",
            font=dict(size=17, color=THEME["text"], family="Inter"),
            x=0.01, xanchor="left", y=0.96, pad=dict(t=4, b=4),
        ),
        margin=dict(l=10, r=10, t=60, b=10),
        height=height,
        hoverlabel=dict(
            bgcolor=THEME["bg_panel_alt"],
            bordercolor=THEME["border_strong"],
            font=dict(color=THEME["text"], family="Inter", size=12),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=THEME["border"], borderwidth=0,
            font=dict(color=THEME["text_muted"], size=12),
        ),
    )
    fig.update_xaxes(
        gridcolor=THEME["grid"], zerolinecolor=THEME["grid"],
        linecolor=THEME["border"], tickcolor=THEME["border"],
        title_font=dict(color=THEME["text_muted"], size=12),
        tickfont=dict(color=THEME["text_muted"], size=11),
    )
    fig.update_yaxes(
        gridcolor=THEME["grid"], zerolinecolor=THEME["grid"],
        linecolor=THEME["border"], tickcolor=THEME["border"],
        title_font=dict(color=THEME["text_muted"], size=12),
        tickfont=dict(color=THEME["text_muted"], size=11),
    )
    return fig


def kpi_card(label, value, sub="", accent=""):
    cls = f"kpi kpi-accent-{accent}" if accent else "kpi"
    sub_html = f'<div class="kpi-delta">{sub}</div>' if sub else '<div class="kpi-delta">&nbsp;</div>'
    return f"""
    <div class="{cls}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_html}
    </div>
    """


def chapter_header(num, anchor_id, title, lede):
    st.markdown(
        f"""
        <a id="{anchor_id}"></a>
        <div class="chapter-marker">
            <span class="chapter-num">CHAPTER {num}</span>
            <span class="chapter-line"></span>
        </div>
        <div class="chapter-title">{title}</div>
        <div class="chapter-lede">{lede}</div>
        """,
        unsafe_allow_html=True,
    )


def callout(text, kind="info"):
    cls = {"info": "callout",
           "warn": "callout callout-warn",
           "crisis": "callout callout-crisis"}.get(kind, "callout")
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)


def spacer(size="md"):
    st.markdown(f'<div class="spacer-{size}"></div>', unsafe_allow_html=True)


# ============================================================
# 6. SIDEBAR
# ============================================================
def _multiselect_via_checkboxes(label, options, state_key):
    if not options:
        st.caption(f"No options available for {label}")
        return []

    # Initialise ALL keys upfront before any widget renders
    all_key = f"{state_key}__ALL"
    for opt in options:
        if f"{state_key}__{opt}" not in st.session_state:
            st.session_state[f"{state_key}__{opt}"] = True
    if all_key not in st.session_state:
        st.session_state[all_key] = True

    selected = [opt for opt in options if st.session_state.get(f"{state_key}__{opt}", True)]
    summary = (
        "All selected" if len(selected) == len(options)
        else (f"{len(selected)} of {len(options)} selected" if selected else "None selected")
    )

    with st.expander(f"{label}  ·  {summary}", expanded=False):
        def _toggle_all():
            new_val = st.session_state[all_key]
            for opt in options:
                st.session_state[f"{state_key}__{opt}"] = new_val

        st.checkbox("Select all", key=all_key, on_change=_toggle_all)
        st.markdown(
            f"<div style='height:1px; background:{THEME['border']}; margin:0.4rem 0 0.6rem 0;'></div>",
            unsafe_allow_html=True,
        )
        for opt in options:
            st.checkbox(opt, key=f"{state_key}__{opt}")

    return [opt for opt in options if st.session_state.get(f"{state_key}__{opt}", True)]

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-tag">WHO Policy Intelligence</div>
        <div class="sidebar-brand">🌍 Silent Crisis</div>
        <div style="color:#AAB0BC; font-size:0.85rem; margin-top:0.2rem;">
            Global Mental Health Dashboard
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown("##### Chapters")
    st.markdown(
        """
        <div class="nav-list">
          <a href="#chapter-1"><span class="nav-num">01</span>A Silent Global Crisis</a>
          <a href="#chapter-2"><span class="nav-num">02</span>The Shape of the Crisis Differs by Country</a>
          <a href="#chapter-3"><span class="nav-num">03</span>Not All Countries Suffer Equally</a>
          <a href="#chapter-4"><span class="nav-num">04</span>Intervention Can Change Outcomes</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown("##### Filters")
    region_opts = sorted(df["region"].dropna().unique().tolist())
    _income_order = ["High", "Upper-Middle", "Lower-Middle", "Low"]
    income_opts = [g for g in _income_order if g in df["income_group"].dropna().unique().tolist()]
    if not income_opts:
        income_opts = sorted(df["income_group"].dropna().unique().tolist())

    selected_region = _multiselect_via_checkboxes("Region", region_opts, state_key="flt_region")
    selected_income = _multiselect_via_checkboxes("Income group", income_opts, state_key="flt_income")

    st.markdown("---")
    latest_year = (
        int(df["data_year"].dropna().max())
        if "data_year" in df.columns and df["data_year"].notna().any() else "-"
    )
    st.caption(f"Indicators · WHO + World Bank · latest year {latest_year}")

# ============================================================
# 7. FILTERING
# ============================================================
_eff_region = selected_region or region_opts
_eff_income = selected_income or income_opts

df_f = df[df["region"].isin(_eff_region) & df["income_group"].isin(_eff_income)].copy()
if df_f.empty:
    df_f = df.copy()
    st.sidebar.warning("No matches, showing global view.")

country_opts = sorted(df_f["country"].dropna().unique().tolist())


# ============================================================
# 8. HERO SECTION
# ============================================================
total_countries = df["country"].nunique()
total_filtered  = df_f["country"].nunique()
data_year = (
    int(df_f["data_year"].dropna().max())
    if "data_year" in df_f.columns and df_f["data_year"].notna().any() else "-"
)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-eyebrow">WHO Global Mental Health Response Council · Briefing</div>
        <h1>The Unequal Global<br/>Mental Health Crisis</h1>
        <p class="hero-subtitle">
            Mental health crises are rising worldwide, yet the countries and populations
            most affected are often the least equipped to respond. This dashboard traces
            that inequality, country by country and system by system, and explores how
            targeted investment can change outcomes.
        </p>
        <div class="hero-meta">
            <span><strong>{total_filtered}</strong> of {total_countries} countries in view</span>
            <span><strong>{len(_eff_region)}</strong> regions</span>
            <span><strong>{len(_eff_income)}</strong> income groups</span>
            <span>Latest year · <strong>{data_year}</strong></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 9. KPI BAR
# ============================================================
total_affected = df_f["total_affected_millions"].sum()
avg_gap        = df_f["treatment_gap_pct"].mean()
avg_crisis     = df_f["mh_crisis_index"].mean()

k1, k2, k3, k4 = st.columns(4)
k1.markdown(kpi_card("Countries in view",  f"{total_filtered}", "",
                     accent="teal"),   unsafe_allow_html=True)
k2.markdown(kpi_card("People affected",    fmt_num(total_affected, ",.0f", "M"),
                     "approximate, current scope", accent="coral"), unsafe_allow_html=True)
k3.markdown(kpi_card("Avg treatment gap",  fmt_num(avg_gap, ".1f", "%"),
                     "untreated despite need",     accent="amber"), unsafe_allow_html=True)
k4.markdown(kpi_card("Avg crisis index",   fmt_num(avg_crisis, ".1f"),
                     "0 to 100 composite score",   accent="gold"),  unsafe_allow_html=True)


# ============================================================
# 10. CHAPTER 01 — A SILENT GLOBAL CRISIS
# ============================================================
chapter_header(
    "01", "chapter-1",
    "A Silent Global Crisis",
    "Mental ill-health affects every region, every income group, and every age cohort. "
    "The map below summarises burden at country level using a composite crisis index, "
    "while the regional breakdown reveals where pressure concentrates."
)

# --- D3 choropleth map --------------------------------------------------
map_cols = [
    "iso3", "country", "region", "income_group",
    "mh_crisis_index", "population_millions",
    "total_affected_millions", "gdp_per_capita_usd",
]
map_data = (
    df_f[map_cols]
    .dropna(subset=["iso3", "mh_crisis_index", "income_group"])
    .to_dict(orient="records")
)
crisis_min = float(df["mh_crisis_index"].min())
crisis_max = float(df["mh_crisis_index"].max())
map_json   = json.dumps(map_data)

components.html(
    f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: #101B2D;
  font-family: Inter, Helvetica Neue, system-ui, sans-serif;
  color: #F3F4F6;
}}
#map-wrap {{ width: 100%; position: relative; }}
svg {{ display: block; width: 100%; height: auto; }}
.country {{
  stroke: #081120;
  stroke-width: 0.4px;
  cursor: pointer;
  transition: stroke 0.12s, stroke-width 0.12s;
}}
.country:hover {{
  stroke: #4EA8DE;
  stroke-width: 1.6px;
}}
.country-border {{
  fill: none;
  stroke: #1E2E45;
  stroke-width: 0.4px;
}}
#tooltip {{
  position: absolute;
  background: #162236;
  border: 1px solid #2A3F5C;
  border-radius: 10px;
  padding: 10px 13px;
  font-size: 12.5px;
  line-height: 1.65;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.12s;
  max-width: 240px;
  color: #F3F4F6;
  z-index: 10;
}}
.tt-name {{
  font-size: 13.5px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #F3F4F6;
}}
.tt-sub {{
  color: #AAB0BC;
  font-size: 11.5px;
  margin-bottom: 7px;
  padding-bottom: 6px;
  border-bottom: 1px solid #1E2E45;
}}
.tt-row {{
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 2px;
}}
.tt-label {{ color: #AAB0BC; }}
.tt-val {{ font-weight: 600; color: #F3F4F6; }}
.tt-val.crisis-high   {{ color: #C62828; }}
.tt-val.crisis-medium {{ color: #E76F51; }}
.tt-val.crisis-low    {{ color: #E9C46A; }}
#colorbar {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px 10px 14px;
  font-size: 11px;
  color: #AAB0BC;
}}
#cb-gradient {{
  flex: 1;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(to right,
    #C62828 0%, #C62828 25%,
    #E76F51 25%, #E76F51 50%,
    #D4A017 50%, #D4A017 75%,
    #E9C46A 75%, #E9C46A 100%);
}}
#cb-ticks {{
  display: flex;
  justify-content: space-between;
  padding: 2px 14px 0 14px;
  font-size: 10px;
  color: #5C6475;
}}
#zoom-controls {{
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}}
.zoom-btn {{
  width: 28px;
  height: 28px;
  background: #162236;
  border: 1px solid #1E2E45;
  border-radius: 6px;
  color: #F3F4F6;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  transition: background 0.12s, border-color 0.12s;
}}
.zoom-btn:hover {{
  background: #1E2E45;
  border-color: #4EA8DE;
  color: #4EA8DE;
}}
</style>
</head>
<body>
<div id="map-wrap">
  <div id="tooltip"></div>
  <div id="zoom-controls">
    <div class="zoom-btn" id="zin"  title="Zoom in">+</div>
    <div class="zoom-btn" id="zout" title="Zoom out">−</div>
    <div class="zoom-btn" id="zreset" title="Reset view" style="font-size:12px;">⊙</div>
  </div>
  <svg id="map-svg" viewBox="0 0 900 480"></svg>
  <div id="colorbar">
    <div id="cb-gradient"></div>
  </div>
  <div id="cb-ticks">
    <span style="color:#C62828;">■ High</span>
    <span style="color:#E76F51;">■ Upper-middle</span>
    <span style="color:#D4A017;">■ Lower-middle</span>
    <span style="color:#E9C46A;">■ Low</span>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js"></script>
<script>
const DATA       = {map_json};
const CRISIS_MIN = {crisis_min};
const CRISIS_MAX = {crisis_max};

const ISO3_TO_M49 = {{
  AFG:4,ALB:8,DZA:12,AND:20,AGO:24,ATG:28,ARG:32,ARM:51,AUS:36,AUT:40,
  AZE:31,BHS:44,BHR:48,BGD:50,BRB:52,BLR:112,BEL:56,BLZ:84,BEN:204,BTN:64,
  BOL:68,BIH:70,BWA:72,BRA:76,BRN:96,BGR:100,BFA:854,BDI:108,CPV:132,KHM:116,
  CMR:120,CAN:124,CAF:140,TCD:148,CHL:152,CHN:156,COL:170,COM:174,COD:180,
  COG:178,CRI:188,CIV:384,HRV:191,CUB:192,CYP:196,CZE:203,DNK:208,DJI:262,
  DOM:214,ECU:218,EGY:818,SLV:222,GNQ:226,ERI:232,EST:233,SWZ:748,ETH:231,
  FJI:242,FIN:246,FRA:250,GAB:266,GMB:270,GEO:268,DEU:276,GHA:288,GRC:300,
  GTM:320,GIN:324,GNB:624,GUY:328,HTI:332,HND:340,HUN:348,ISL:352,IND:356,
  IDN:360,IRN:364,IRQ:368,IRL:372,ISR:376,ITA:380,JAM:388,JPN:392,JOR:400,
  KAZ:398,KEN:404,KIR:296,PRK:408,KOR:410,KWT:414,KGZ:417,LAO:418,LVA:428,
  LBN:422,LSO:426,LBR:430,LBY:434,LIE:438,LTU:440,LUX:442,MDG:450,MWI:454,
  MYS:458,MDV:462,MLI:466,MLT:470,MHL:584,MRT:478,MUS:480,MEX:484,FSM:583,
  MDA:498,MCO:492,MNG:496,MNE:499,MAR:504,MOZ:508,MMR:104,NAM:516,NRU:520,
  NPL:524,NLD:528,NZL:554,NIC:558,NER:562,NGA:566,MKD:807,NOR:578,OMN:512,
  PAK:586,PLW:585,PAN:591,PNG:598,PRY:600,PER:604,PHL:608,POL:616,PRT:620,
  QAT:634,ROU:642,RUS:643,RWA:646,KNA:659,LCA:662,VCT:670,WSM:882,SMR:674,
  STP:678,SAU:682,SEN:686,SRB:688,SLE:694,SGP:702,SVK:703,SVN:705,SLB:90,
  SOM:706,ZAF:710,SSD:728,ESP:724,LKA:144,SDN:729,SUR:740,SWE:752,CHE:756,
  SYR:760,TWN:158,TJK:762,TZA:834,THA:764,TLS:626,TGO:768,TON:776,TTO:780,
  TUN:788,TUR:792,TKM:795,TUV:798,UGA:800,UKR:804,ARE:784,GBR:826,USA:840,
  URY:858,UZB:860,VUT:548,VEN:862,VNM:704,YEM:887,ZMB:894,ZWE:716,XKX:926
}};

const byId = {{}};
DATA.forEach(d => {{
  const num = ISO3_TO_M49[d.iso3];
  if (num) byId[num] = d;
}});

const INCOME_COLOR = {{
  "High":         "#C62828",
  "Upper-Middle": "#E76F51",
  "Lower-Middle": "#D4A017",
  "Low":          "#E9C46A",
}};

function crisisClass(val) {{
  const t = (val - CRISIS_MIN) / (CRISIS_MAX - CRISIS_MIN);
  if (t >= 0.66) return "crisis-high";
  if (t >= 0.33) return "crisis-medium";
  return "crisis-low";
}}

const svg  = d3.select("#map-svg");
const wrap = document.getElementById("map-wrap");
const tip  = document.getElementById("tooltip");

const projection = d3.geoNaturalEarth1().scale(140).translate([460, 260]);
const path = d3.geoPath(projection);

const zoom = d3.zoom()
  .scaleExtent([1, 12])
  .on("zoom", ev => g.attr("transform", ev.transform));
svg.call(zoom);

const g = svg.append("g");

document.getElementById("zin").onclick    = () => svg.transition().duration(300).call(zoom.scaleBy, 1.6);
document.getElementById("zout").onclick   = () => svg.transition().duration(300).call(zoom.scaleBy, 0.7);
document.getElementById("zreset").onclick = () => svg.transition().duration(400).call(zoom.transform, d3.zoomIdentity);

d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(world => {{
  const countries = topojson.feature(world, world.objects.countries);
  const borders   = topojson.mesh(world, world.objects.countries, (a,b) => a !== b);

  g.selectAll(".country")
    .data(countries.features)
    .join("path")
      .attr("class", "country")
      .attr("d", path)
      .attr("fill", d => {{
        const row = byId[+d.id];
        return row ? (INCOME_COLOR[row.income_group] || "#1A2D45") : "#0D1A2A";
      }})
      .on("mousemove", function(event, d) {{
        const row = byId[+d.id];
        if (!row) {{ tip.style.opacity = 0; return; }}
        const fmtF = (v, dp=1) => (v == null || isNaN(v)) ? "—" : Number(v).toFixed(dp);
        const fmtC = v => (v == null || isNaN(v)) ? "—"
          : "$" + Number(v).toLocaleString("en-US", {{maximumFractionDigits:0}});
        const cls  = crisisClass(row.mh_crisis_index);
        tip.innerHTML =
          `<div class="tt-name">${{row.country}}</div>` +
          `<div class="tt-sub">${{row.region}} · ${{row.income_group}}</div>` +
          `<div class="tt-row"><span class="tt-label">Crisis index</span>` +
            `<span class="tt-val ${{cls}}">${{fmtF(row.mh_crisis_index)}}</span></div>` +
          `<div class="tt-row"><span class="tt-label">Population</span>` +
            `<span class="tt-val">${{fmtF(row.population_millions,1)}}M</span></div>` +
          `<div class="tt-row"><span class="tt-label">Affected</span>` +
            `<span class="tt-val">${{fmtF(row.total_affected_millions,1)}}M</span></div>` +
          `<div class="tt-row"><span class="tt-label">GDP / capita</span>` +
            `<span class="tt-val">${{fmtC(row.gdp_per_capita_usd)}}</span></div>`;
        const bx = wrap.getBoundingClientRect();
        let tx = event.clientX - bx.left + 14;
        let ty = event.clientY - bx.top  - 10;
        if (tx + 250 > bx.width) tx = event.clientX - bx.left - 254;
        tip.style.left    = tx + "px";
        tip.style.top     = ty + "px";
        tip.style.opacity = 1;
      }})
      .on("mouseleave", () => {{ tip.style.opacity = 0; }});

  g.append("path")
    .datum(borders)
    .attr("class", "country-border")
    .attr("d", path);
}});
</script>
</body>
</html>
""",
    height=570,
    scrolling=False,
)

st.markdown(
    f"""
    <div style="color:{THEME['text_muted']}; font-size:0.83rem;
                margin-top:-0.4rem; margin-bottom:1rem; line-height:1.55;">
        Countries are coloured by income group: Red = High income · Orange = Upper-middle ·
        Mustard = Lower-middle · Yellow = Low income. Hover over any country for crisis index,
        population, and GDP details.
    </div>
    """,
    unsafe_allow_html=True,
)


# --- Regional comparison + spotlight ------------------------------------
left, right = st.columns([1.4, 1])

with left:
    region_summary = (
        df_f.groupby("region", as_index=False)
            .agg(
                avg_crisis=("mh_crisis_index", "mean"),
                affected=("total_affected_millions", "sum"),
                countries=("country", "nunique"),
            )
            .sort_values("avg_crisis", ascending=True)
    )
    fig_region = px.bar(
        region_summary,
        x="avg_crisis", y="region", orientation="h",
        color="avg_crisis", color_continuous_scale=CRISIS_SCALE,
        custom_data=["affected", "countries"],
    )
    fig_region.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Avg crisis index · <b>%{x:.1f}</b><br>"
            "Affected · <b>%{customdata[0]:,.1f}M</b><br>"
            "Countries · <b>%{customdata[1]}</b>"
            "<extra></extra>"
        ),
        marker_line_width=0,
    )
    fig_region = style_fig(fig_region, height=380, title="Average crisis index by region")
    fig_region.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Crisis index (0 to 100)", yaxis_title="",
    )
    st.plotly_chart(fig_region, use_container_width=True, key="ch1_region_bar")

with right:
    spotlight = df_f.dropna(subset=["mh_crisis_index"]).sort_values(
        "mh_crisis_index", ascending=False).head(1)
    if not spotlight.empty:
        sp = spotlight.iloc[0]
        callout(
            f"<strong>Spotlight ·</strong> {sp['country']} currently leads the filtered view "
            f"with a crisis index of <strong>{fmt_num(sp['mh_crisis_index'])}</strong> "
            f"and a treatment gap of <strong>{fmt_num(sp['treatment_gap_pct'], '.1f', '%')}</strong>. "
            f"Roughly <strong>{fmt_num(sp['total_affected_millions'], '.1f', 'M people')}</strong> "
            f"are estimated to be affected.",
            kind="crisis",
        )
    callout(
        "<strong>What the map shows ·</strong> countries are coloured by income group, "
        "not crisis severity. Red indicates high-income countries, orange upper-middle, "
        "mustard lower-middle, and yellow low-income. Hover any country to see its crisis "
        "index, treatment gap, and population data.",
        kind="info",
    )


# ============================================================
# 11. CHAPTER 02 — THE SHAPE OF THE CRISIS DIFFERS BY COUNTRY
# ============================================================
chapter_header(
    "02", "chapter-2",
    "The Shape of the Crisis Differs by Country",
    "Two countries can share a similar overall index while facing very different conditions. "
    "Use the country fingerprint below to compare prevalence, lethality and access for any "
    "nation against its regional and global peers."
)

if country_opts:
    pc1, pc2 = st.columns([1.2, 1])

    sorted_view = df_f.dropna(subset=["mh_crisis_index"]).sort_values(
        "mh_crisis_index", ascending=False)
    default_country = (
        sorted_view["country"].iloc[0] if not sorted_view.empty else country_opts[0]
    )
    default_idx = country_opts.index(default_country) if default_country in country_opts else 0

    with pc1:
        sel_country = st.selectbox(
            "Country profile", options=country_opts,
            index=default_idx, key="ch2_country_select",
        )
    with pc2:
        st.markdown(
            f"""
            <div style="padding-top:1.7rem; color:{THEME['text_muted']}; font-size:0.85rem;">
                Comparing <b style="color:{THEME['text']}">{sel_country}</b>
                against <b style="color:{THEME['accent_teal']}">regional</b>
                and <b style="color:{THEME['accent_lavender']}">global</b> averages.
            </div>
            """,
            unsafe_allow_html=True,
        )

    crow = df_f[df_f["country"] == sel_country].iloc[0]

    qc1, qc2, qc3, qc4 = st.columns(4)
    qc1.markdown(kpi_card("Crisis index",         fmt_num(crow['mh_crisis_index']),
                          f"{crow['region']}",    accent="teal"),    unsafe_allow_html=True)
    qc2.markdown(kpi_card("Treatment gap",         fmt_num(crow['treatment_gap_pct'], '.1f', '%'),
                          "untreated need",        accent="amber"),   unsafe_allow_html=True)
    qc3.markdown(kpi_card(
        "Psychiatrists / 100k",
        fmt_num(crow['psychiatrists_per100k'], '.2f'),
        "workforce density rate", accent="lavender",
    ), unsafe_allow_html=True)
    qc4.markdown(kpi_card("People affected",
                          fmt_num(crow['total_affected_millions'], '.1f', 'M'),
                          f"of {fmt_num(crow['population_millions'], '.1f', 'M')} population",
                          accent="coral"),         unsafe_allow_html=True)

    st.markdown(
        """
        <div class="helper-note">
            <strong>Note on workforce metric ·</strong> "psychiatrists per 100k" is a rate,
            not a percentage. A value of 0.3 means roughly one psychiatrist for every 333,000 people.
        </div>
        """,
        unsafe_allow_html=True,
    )

    spacer("sm")

    radar_dims = [
        ("Depression %",    "depression_pct"),
        ("Anxiety %",       "anxiety_pct"),
        ("Suicide rate",    "suicide_rate_per100k"),
        ("Treatment gap %", "treatment_gap_pct"),
        ("Crisis index",    "mh_crisis_index"),
    ]

    def _norm(series, value):
        lo, hi = series.min(), series.max()
        if pd.isna(value) or hi == lo:
            return 0.0
        return float((value - lo) / (hi - lo) * 100)

    region_peers = df[df["region"] == crow["region"]]
    cat_labels   = [d[0] for d in radar_dims]
    country_vals = [_norm(df[c], crow[c])                  for _, c in radar_dims]
    region_vals  = [_norm(df[c], region_peers[c].mean())   for _, c in radar_dims]
    global_vals  = [_norm(df[c], df[c].mean())             for _, c in radar_dims]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=global_vals + [global_vals[0]], theta=cat_labels + [cat_labels[0]],
        name="Global average",
        line=dict(color=THEME["accent_lavender"], width=1.5, dash="dot"),
        fillcolor="rgba(123,143,191,0.10)", fill="toself",
        hovertemplate="<b>Global</b><br>%{theta}: %{r:.0f}<extra></extra>",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=region_vals + [region_vals[0]], theta=cat_labels + [cat_labels[0]],
        name=f"{crow['region']} avg",
        line=dict(color=THEME["accent_teal"], width=1.8, dash="dash"),
        fillcolor="rgba(78,168,222,0.10)", fill="toself",
        hovertemplate=f"<b>{crow['region']}</b><br>%{{theta}}: %{{r:.0f}}<extra></extra>",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=country_vals + [country_vals[0]], theta=cat_labels + [cat_labels[0]],
        name=sel_country,
        line=dict(color=THEME["accent_coral"], width=2.6),
        fillcolor="rgba(198,40,40,0.20)", fill="toself",
        hovertemplate=f"<b>{sel_country}</b><br>%{{theta}}: %{{r:.0f}}<extra></extra>",
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor=THEME["bg_chart"],
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor=THEME["grid"], linecolor=THEME["grid"],
                            tickfont=dict(color=THEME["text_dim"], size=10),
                            tickvals=[20, 40, 60, 80]),
            angularaxis=dict(gridcolor=THEME["grid"], linecolor=THEME["border"],
                             tickfont=dict(color=THEME["text_muted"], size=12)),
        ),
    )
    fig_radar = style_fig(fig_radar, height=520,
                          title=f"Mental health fingerprint · {sel_country}")
    fig_radar.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.12, x=0))

    bar_df = pd.DataFrame({
        "Dimension":  ["Depression %", "Anxiety %", "Suicide / 100k", "Treatment gap %"],
        sel_country:  [crow["depression_pct"],           crow["anxiety_pct"],
                       crow["suicide_rate_per100k"],      crow["treatment_gap_pct"]],
        "Region avg": [region_peers["depression_pct"].mean(), region_peers["anxiety_pct"].mean(),
                       region_peers["suicide_rate_per100k"].mean(), region_peers["treatment_gap_pct"].mean()],
        "Global avg": [df["depression_pct"].mean(), df["anxiety_pct"].mean(),
                       df["suicide_rate_per100k"].mean(), df["treatment_gap_pct"].mean()],
    })
    bar_long = bar_df.melt(id_vars="Dimension", var_name="Series", value_name="Value")

    fig_bar = px.bar(
        bar_long, x="Value", y="Dimension", color="Series",
        barmode="group", orientation="h",
        color_discrete_map={
            sel_country:  THEME["accent_coral"],
            "Region avg": THEME["accent_teal"],
            "Global avg": THEME["accent_lavender"],
        },
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{y}</b><br>%{fullData.name}: <b>%{x:.1f}</b><extra></extra>",
        marker_line_width=0,
    )
    fig_bar = style_fig(fig_bar, height=520, title="Raw values vs peers")
    fig_bar.update_layout(
        xaxis_title="", yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=-0.18, x=0),
    )

    rc1, rc2 = st.columns(2)
    rc1.plotly_chart(fig_radar, use_container_width=True, key="ch2_radar")
    rc2.plotly_chart(fig_bar,   use_container_width=True, key="ch2_bars")

    callout(
        f"<strong>Reading the fingerprint ·</strong> the radar is normalised 0 to 100 across "
        f"all countries, so each axis answers: <em>where does {sel_country} sit in the global "
        f"distribution?</em> The grouped bars on the right show raw values for absolute scale.",
        kind="info",
    )
else:
    st.info("No countries match the current filter combination.")


# ============================================================
# 12. CHAPTER 03 — NOT ALL COUNTRIES SUFFER EQUALLY
# ============================================================
chapter_header(
    "03", "chapter-3",
    "Not All Countries Suffer Equally",
    "When economic capacity is plotted against treatment gap, an unmistakable pattern emerges: "
    "lower-income countries shoulder the largest unmet need despite carrying significant shares "
    "of the global mental-health burden."
)

st.markdown(
    """
    <div class="pull-quote">
        <span class="pq-tag">Narrative thesis</span>
        Awareness is rarely the bottleneck, <em>capacity to deliver care is.</em>
        High-need countries cluster together not because their citizens fail to recognise
        mental illness, but because their systems lack the workforce, financing and
        governance to respond.
    </div>
    """,
    unsafe_allow_html=True,
)

df_sc = df_f.dropna(subset=[
    "gdp_per_capita_usd", "treatment_gap_pct", "total_affected_millions"
]).copy()

fig_gdp = px.scatter(
    df_sc, x="gdp_per_capita_usd", y="treatment_gap_pct",
    size="total_affected_millions", color="income_group",
    hover_name="country",
    color_discrete_map=INCOME_PALETTE,
    log_x=True, size_max=46,
    custom_data=["region", "psychiatrists_per100k",
                 "mh_spend_usd_per_capita", "total_affected_millions"],
)
fig_gdp.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "<span style='color:#AAB0BC'>%{customdata[0]}</span><br><br>"
        "GDP per capita · <b>$%{x:,.0f}</b><br>"
        "Treatment gap · <b>%{y:.1f}%</b><br>"
        "Psychiatrists · <b>%{customdata[1]:.1f} per 100k</b><br>"
        "MH spend · <b>$%{customdata[2]:,.2f} per capita</b><br>"
        "Affected · <b>%{customdata[3]:,.1f}M</b>"
        "<extra></extra>"
    ),
    marker=dict(line=dict(width=0.5, color=THEME["bg_app"]), opacity=0.85),
)
fig_gdp = style_fig(fig_gdp, height=540,
                    title="GDP per capita vs treatment gap · bubble size = people affected")
fig_gdp.update_xaxes(
    type="log",
    tickmode="array",
    tickvals=[500, 1000, 2000, 5000, 10000, 20000, 50000, 100000],
    ticktext=["$500", "$1K", "$2K", "$5K", "$10K", "$20K", "$50K", "$100K"],
    minor=dict(showgrid=True, gridcolor=THEME["grid"]),
)
fig_gdp.update_layout(
    xaxis_title="GDP per capita (USD, log scale)",
    yaxis_title="Treatment gap (%)",
    legend_title_text="Income group",
)
st.plotly_chart(fig_gdp, use_container_width=True, key="ch3_gdp_gap")

st.markdown(
    f"""
    <div class="income-legend">
        <div class="income-legend-title">Income Group · World Bank Thresholds</div>
        <div class="income-legend-grid">
            <div class="income-row">
                <span class="income-dot" style="background:{INCOME_PALETTE['High']};"></span>
                <span><b>High</b><span class="income-range"> · above $14,005</span></span>
            </div>
            <div class="income-row">
                <span class="income-dot" style="background:{INCOME_PALETTE['Upper-Middle']};"></span>
                <span><b>Upper-Middle</b><span class="income-range"> · $4,516 to $14,005</span></span>
            </div>
            <div class="income-row">
                <span class="income-dot" style="background:{INCOME_PALETTE['Lower-Middle']};"></span>
                <span><b>Lower-Middle</b><span class="income-range"> · $1,146 to $4,515</span></span>
            </div>
            <div class="income-row">
                <span class="income-dot" style="background:{INCOME_PALETTE['Low']};"></span>
                <span><b>Low</b><span class="income-range"> · GNI per capita ≤ $1,145</span></span>
            </div>
        </div>
        <div class="income-legend-foot">
            Bands follow approximate World Bank classifications (FY2024 GNI per capita,
            Atlas method). Used here to indicate relative economic capacity, not exact GDP.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

callout(
    "<strong>The inequality signal ·</strong> as GDP per capita rises, the treatment gap "
    "tends to fall. The largest bubbles — those countries with the most people affected — "
    "frequently sit in the upper-left quadrant: high need, low capacity to respond.",
    kind="warn",
)

c3a, c3b = st.columns([1.3, 1])

with c3a:
    df_w = df_f.dropna(subset=[
        "psychiatrists_per100k", "mh_system_score", "mh_spend_usd_per_capita"
    ])
    fig_work = px.scatter(
        df_w, x="psychiatrists_per100k", y="mh_system_score",
        size="mh_spend_usd_per_capita", color="income_group",
        hover_name="country",
        color_discrete_map=INCOME_PALETTE, size_max=38,
        custom_data=["region", "treatment_gap_pct", "mh_spend_usd_per_capita"],
    )
    fig_work.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "<span style='color:#AAB0BC'>%{customdata[0]}</span><br><br>"
            "Psychiatrists · <b>%{x:.1f} per 100k</b><br>"
            "System score · <b>%{y:.1f}</b><br>"
            "Treatment gap · <b>%{customdata[1]:.1f}%</b><br>"
            "MH spend · <b>$%{customdata[2]:,.2f} per capita</b>"
            "<extra></extra>"
        ),
        marker=dict(line=dict(width=0.5, color=THEME["bg_app"]), opacity=0.85),
    )
    fig_work = style_fig(fig_work, height=520, title="Workforce density vs system readiness")
    fig_work.update_layout(
        xaxis_title="Psychiatrists per 100,000 people",
        yaxis_title="Mental health system score",
        legend_title_text="Income group",
    )
    st.plotly_chart(fig_work, use_container_width=True, key="ch3_workforce")

with c3b:
    top_gap = (df_f.dropna(subset=["treatment_gap_pct"])
                   .sort_values("treatment_gap_pct", ascending=False)
                   .head(10))
    fig_lead = px.bar(
        top_gap, x="treatment_gap_pct", y="country", orientation="h",
        color="treatment_gap_pct", color_continuous_scale=CRISIS_SCALE,
        custom_data=["region", "income_group",
                     "psychiatrists_per100k", "mh_spend_usd_per_capita"],
    )
    fig_lead.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "<span style='color:#AAB0BC'>%{customdata[0]} · %{customdata[1]}</span><br><br>"
            "Treatment gap · <b>%{x:.1f}%</b><br>"
            "Psychiatrists · <b>%{customdata[2]:.1f} per 100k</b><br>"
            "MH spend · <b>$%{customdata[3]:,.2f} per capita</b>"
            "<extra></extra>"
        ),
        marker_line_width=0,
    )
    fig_lead = style_fig(fig_lead, height=520, title="Top 10 · highest treatment gap")
    fig_lead.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Treatment gap (%)", yaxis_title="",
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_lead, use_container_width=True, key="ch3_leaderboard")

callout(
    "<strong>System failure pattern ·</strong> high-need countries cluster in the lower-left "
    "of the workforce chart, with too few psychiatrists and weaker system scores. The bubble "
    "size — mental health spend per capita — reinforces the same financial gradient.",
    kind="crisis",
)


# ============================================================
# 13. CHAPTER 04 — INTERVENTION CAN CHANGE OUTCOMES
# ============================================================
chapter_header(
    "04", "chapter-4",
    "Intervention Can Change Outcomes",
    "Adjust the simulated investment lever to see how additional spending could improve "
    "average system readiness and reduce treatment gaps across the countries currently in "
    "view. Use this as a directional planning tool, not a clinical forecast."
)

sim_left, sim_right = st.columns([1.6, 1])

with sim_left:
    investment_increase = st.slider(
        "Simulated increase in mental health spending",
        min_value=0, max_value=100, value=25, step=5,
        format="+%d%%",
        help="Applies a uniform percentage uplift to current per-capita spending across the filtered countries.",
        key="ch4_invest_slider",
    )

with sim_right:
    st.markdown(
        f"""
        <div style="padding-top:1.7rem; color:{THEME['text_muted']}; font-size:0.85rem;">
            Modelling a <b style="color:{THEME['accent_sage']}">+{investment_increase}%</b>
            uplift across <b style="color:{THEME['text']}">{total_filtered}</b> countries.
        </div>
        """,
        unsafe_allow_html=True,
    )

spacer("md")

df_sim = df_f.copy()
df_sim["sim_system_score"]  = (df_sim["mh_system_score"]   + investment_increase * 0.25).clip(upper=100)
df_sim["sim_treatment_gap"] = (df_sim["treatment_gap_pct"] - investment_increase * 0.30).clip(lower=0)
df_sim["sim_spend"]         = df_sim["mh_spend_usd_per_capita"] * (1 + investment_increase / 100)

current_score   = df_f["mh_system_score"].mean()
projected_score = df_sim["sim_system_score"].mean()
current_gap     = df_f["treatment_gap_pct"].mean()
projected_gap   = df_sim["sim_treatment_gap"].mean()

s1, s2, s3, s4 = st.columns(4, gap="medium")
s1.markdown(kpi_card("Current system score",    fmt_num(current_score),
                     "filtered average",         accent="steel"), unsafe_allow_html=True)
s2.markdown(kpi_card("Projected system score",  fmt_num(projected_score),
                     f"+{fmt_num(projected_score - current_score)} pts vs current",
                     accent="sage"),             unsafe_allow_html=True)
s3.markdown(kpi_card("Current treatment gap",   fmt_num(current_gap, '.1f', '%'),
                     "filtered average",         accent="amber"), unsafe_allow_html=True)
s4.markdown(kpi_card("Projected treatment gap", fmt_num(projected_gap, '.1f', '%'),
                     f"-{fmt_num(current_gap - projected_gap)} pts vs current",
                     accent="sage"),             unsafe_allow_html=True)

spacer("lg")

fig_sim = px.scatter(
    df_sim, x="sim_spend", y="sim_system_score",
    size="population_millions", color="income_group",
    hover_name="country",
    color_discrete_map=INCOME_PALETTE, size_max=44,
    custom_data=["region", "mh_system_score",
                 "sim_treatment_gap", "treatment_gap_pct",
                 "mh_spend_usd_per_capita"],
)
fig_sim.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "<span style='color:#AAB0BC'>%{customdata[0]}</span><br><br>"
        "Spend · <b>$%{customdata[4]:,.2f}</b> &rarr; <b>$%{x:,.2f} per capita</b><br>"
        "System score · <b>%{customdata[1]:.1f}</b> &rarr; <b>%{y:.1f}</b><br>"
        "Treatment gap · <b>%{customdata[3]:.1f}%</b> &rarr; <b>%{customdata[2]:.1f}%</b>"
        "<extra></extra>"
    ),
    marker=dict(line=dict(width=0.5, color=THEME["bg_app"]), opacity=0.85),
)
fig_sim = style_fig(fig_sim, height=540,
                    title=f"Projected system readiness at +{investment_increase}% investment")
fig_sim.update_layout(
    xaxis_title="Projected mental health spend (USD per capita)",
    yaxis_title="Projected system readiness score",
    legend_title_text="Income group",
)
st.plotly_chart(fig_sim, use_container_width=True, key="ch4_sim_chart")

st.markdown(
    """
    <div class="disclaimer">
        <b>Simulation note ·</b> projections apply uniform linear elasticities to current
        values (+0.25 points of system score and -0.30 points of treatment gap per 1%
        spending uplift). This is an <b>illustrative scenario for policy framing</b>, not a
        clinical or economic forecast. Real-world outcomes depend on workforce pipelines,
        governance and implementation quality.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h4 style='margin-top:1.8rem; margin-bottom:0.6rem;'>"
    "Policy levers · tailored to current scope</h4>",
    unsafe_allow_html=True,
)

flags = []
if pd.notna(avg_gap) and avg_gap > 50:
    flags.append((
        "HIGH PRIORITY", "Expand frontline treatment access",
        f"Average treatment gap is {avg_gap:.0f}% across this scope. Scaling community-based "
        f"and primary-care mental health services would reach untreated populations fastest.",
        "high",
    ))
if df_f["psychiatrists_per100k"].mean() < 5:
    flags.append((
        "WORKFORCE", "Build mental health workforce pipelines",
        f"Only {df_f['psychiatrists_per100k'].mean():.1f} psychiatrists per 100,000 people on average. "
        f"Investing in training, retention and task-shifting to non-specialists is essential.",
        "high",
    ))
if df_f["mh_spend_usd_per_capita"].mean() < 5:
    flags.append((
        "INVESTMENT", "Raise mental health budget allocations",
        f"Average spend is just ${df_f['mh_spend_usd_per_capita'].mean():.2f} per capita. "
        f"Even modest absolute increases produce outsized improvements in low-income contexts.",
        "med",
    ))
law_series = pd.to_numeric(df_f.get("mh_law_exists"), errors="coerce")
if law_series.notna().any() and law_series.mean() < 0.7:
    flags.append((
        "GOVERNANCE", "Strengthen mental health legislation",
        "A meaningful share of countries in this view lack a dedicated mental health law. "
        "Statutory frameworks anchor rights protections and budget continuity.",
        "med",
    ))
if (pd.notna(df_f["mh_system_score"].mean()) and df_f["mh_system_score"].mean() >= 60
        and pd.notna(avg_gap) and avg_gap < 30):
    flags.append((
        "MAINTAIN", "Sustain and refine existing systems",
        "This scope shows comparatively strong readiness. Focus shifts to quality, equity "
        "within the population, and digital and youth-specific service modernisation.",
        "low",
    ))
if not flags:
    flags.append((
        "REVIEW", "Maintain monitoring and evaluation",
        "No critical thresholds breached in this scope. Continue tracking indicators and "
        "investing in data infrastructure.",
        "low",
    ))

cols = st.columns(min(3, len(flags)))
for i, (tag, title, body, level) in enumerate(flags):
    with cols[i % len(cols)]:
        st.markdown(
            f"""
            <div class="policy-card {level}">
                <div class="policy-tag">{tag}</div>
                <div class="policy-title">{title}</div>
                <div class="policy-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# 14. FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        Silent Crisis · Global Mental Health Intelligence Dashboard ·
        Prepared for the WHO Global Mental Health Response Council<br>
        Indicators merged from WHO and World Bank public datasets ·
        Built with Streamlit and Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
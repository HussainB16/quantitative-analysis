import streamlit as st
from utils.common import PALETTE
from experiments import data, sampling, visualization, correlation, regression, hypothesis_testing

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="EduMetrics · Student Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# GLOBAL STYLES
# ──────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Outfit:wght@300;400;600;800;900&display=swap');

  html, body, [class*="css"] {{
      font-family: 'Space Grotesk', sans-serif;
      background-color: {PALETTE['bg']};
      color: {PALETTE['text']};
  }}

  /* ── Scrollbar ── */
  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-track {{ background: {PALETTE['surface']}; }}
  ::-webkit-scrollbar-thumb {{ background: {PALETTE['border2']}; border-radius: 3px; }}

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {{
      background: {PALETTE['surface']};
      border-right: 1px solid {PALETTE['border']};
      width: 260px !important;
  }}
  section[data-testid="stSidebar"] * {{ color: {PALETTE['text']} !important; }}
  section[data-testid="stSidebar"] .stRadio > div {{
      gap: 4px;
  }}
  section[data-testid="stSidebar"] .stRadio label {{
      background: transparent;
      border-radius: 8px;
      padding: 8px 12px;
      transition: all 0.2s;
      border: 1px solid transparent;
      display: block;
      cursor: pointer;
      font-size: 0.875rem;
  }}
  section[data-testid="stSidebar"] .stRadio label:hover {{
      background: {PALETTE['card']} !important;
      border-color: {PALETTE['border2']} !important;
  }}

  /* ── Main area ── */
  .main .block-container {{
      padding: 1.5rem 2.5rem 3rem;
      max-width: 1400px;
  }}

  /* ── Hero ── */
  .hero {{
      background: linear-gradient(135deg, #0a1628 0%, {PALETTE['bg']} 50%, #100d20 100%);
      border: 1px solid {PALETTE['border']};
      border-radius: 20px;
      padding: 2.5rem 3rem;
      margin-bottom: 2rem;
      position: relative;
      overflow: hidden;
  }}
  .hero::before {{
      content: "";
      position: absolute;
      top: -80px; right: -80px;
      width: 300px; height: 300px;
      border-radius: 50%;
      background: radial-gradient(circle, {PALETTE['accent']}22 0%, transparent 70%);
      pointer-events: none;
  }}
  .hero::after {{
      content: "";
      position: absolute;
      bottom: -60px; left: 30%;
      width: 200px; height: 200px;
      border-radius: 50%;
      background: radial-gradient(circle, {PALETTE['accent5']}18 0%, transparent 70%);
      pointer-events: none;
  }}
  .hero-eyebrow {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: {PALETTE['accent3']};
      letter-spacing: 0.15em;
      text-transform: uppercase;
      margin-bottom: 0.5rem;
  }}
  .hero-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 2.6rem;
      font-weight: 900;
      line-height: 1.1;
      margin: 0 0 0.6rem 0;
      background: linear-gradient(100deg, {PALETTE['text']} 20%, {PALETTE['accent']} 60%, {PALETTE['accent5']} 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
  }}
  .hero-sub {{
      color: {PALETTE['muted']};
      font-size: 0.95rem;
      margin: 0;
      font-weight: 400;
      max-width: 520px;
      line-height: 1.6;
  }}
  .hero-badges {{
      display: flex;
      gap: 0.5rem;
      margin-top: 1.2rem;
      flex-wrap: wrap;
  }}
  .badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      padding: 3px 10px;
      border-radius: 20px;
      letter-spacing: 0.05em;
      font-weight: 600;
  }}
  .badge-blue {{ background: {PALETTE['accent']}22; color: {PALETTE['accent']}; border: 1px solid {PALETTE['accent']}44; }}
  .badge-pink {{ background: {PALETTE['accent2']}22; color: {PALETTE['accent2']}; border: 1px solid {PALETTE['accent2']}44; }}
  .badge-green {{ background: {PALETTE['accent3']}22; color: {PALETTE['accent3']}; border: 1px solid {PALETTE['accent3']}44; }}
  .badge-yellow {{ background: {PALETTE['accent4']}22; color: {PALETTE['accent4']}; border: 1px solid {PALETTE['accent4']}44; }}

  /* ── Section label ── */
  .section-label {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.2rem;
      font-weight: 700;
      color: {PALETTE['text']};
      margin: 1.5rem 0 1rem 0;
      display: flex;
      align-items: center;
      gap: 0.6rem;
  }}
  .section-label::after {{
      content: "";
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, {PALETTE['border2']}, transparent);
  }}
  .section-pill {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.6rem;
      background: {PALETTE['accent']}20;
      color: {PALETTE['accent']};
      border: 1px solid {PALETTE['accent']}40;
      border-radius: 20px;
      padding: 2px 8px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
  }}

  /* ── KPI Cards ── */
  .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }}
  .kpi-card {{
      background: {PALETTE['card']};
      border: 1px solid {PALETTE['border']};
      border-radius: 14px;
      padding: 1.2rem 1.4rem;
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s;
  }}
  .kpi-card:hover {{ border-color: {PALETTE['border2']}; }}
  .kpi-card::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 2px;
      border-radius: 14px 14px 0 0;
  }}
  .kpi-card.blue::before {{ background: linear-gradient(90deg, {PALETTE['accent']}, transparent); }}
  .kpi-card.pink::before {{ background: linear-gradient(90deg, {PALETTE['accent2']}, transparent); }}
  .kpi-card.green::before {{ background: linear-gradient(90deg, {PALETTE['accent3']}, transparent); }}
  .kpi-card.yellow::before {{ background: linear-gradient(90deg, {PALETTE['accent4']}, transparent); }}
  .kpi-card.purple::before {{ background: linear-gradient(90deg, {PALETTE['accent5']}, transparent); }}
  .kpi-icon {{ font-size: 1.2rem; margin-bottom: 0.4rem; opacity: 0.8; }}
  .kpi-value {{
      font-family: 'Outfit', sans-serif;
      font-size: 2rem;
      font-weight: 800;
      line-height: 1;
      color: {PALETTE['text']};
  }}
  .kpi-label {{
      font-size: 0.7rem;
      color: {PALETTE['muted']};
      margin-top: 0.3rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 500;
  }}
  .kpi-sub {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      color: {PALETTE['accent3']};
      margin-top: 0.2rem;
  }}

  /* ── Info/Result cards ── */
  .result-box {{
      background: {PALETTE['card']};
      border: 1px solid {PALETTE['border']};
      border-radius: 14px;
      padding: 1.3rem 1.6rem;
      margin-top: 0.8rem;
  }}
  .result-grid {{ display: flex; gap: 2.5rem; flex-wrap: wrap; }}
  .result-item {{ min-width: 100px; }}
  .result-key {{
      color: {PALETTE['muted']};
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      font-weight: 600;
      margin-bottom: 0.2rem;
  }}
  .result-val {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.3rem;
      font-weight: 700;
      color: {PALETTE['accent2']};
  }}
  .result-val.green {{ color: {PALETTE['accent3']}; }}
  .result-val.blue {{ color: {PALETTE['accent']}; }}
  .result-val.yellow {{ color: {PALETTE['accent4']}; }}

  /* ── Info banner ── */
  .info-banner {{
      background: {PALETTE['accent']}12;
      border: 1px solid {PALETTE['accent']}30;
      border-radius: 10px;
      padding: 0.8rem 1.2rem;
      font-size: 0.83rem;
      color: {PALETTE['text2']};
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
  }}
  .warn-banner {{
      background: {PALETTE['accent4']}12;
      border: 1px solid {PALETTE['accent4']}30;
      border-radius: 10px;
      padding: 0.8rem 1.2rem;
      font-size: 0.83rem;
      color: {PALETTE['text2']};
      margin-bottom: 1rem;
  }}

  /* ── Insight box ── */
  .insight-box {{
      background: linear-gradient(135deg, {PALETTE['accent3']}12, {PALETTE['accent']}08);
      border: 1px solid {PALETTE['accent3']}30;
      border-radius: 12px;
      padding: 1rem 1.3rem;
      margin-top: 1rem;
      font-size: 0.85rem;
      color: {PALETTE['text2']};
      line-height: 1.6;
  }}
  .insight-title {{
      font-weight: 600;
      color: {PALETTE['accent3']};
      margin-bottom: 0.3rem;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
  }}

  /* ── Streamlit overrides ── */
  div[data-baseweb="select"] > div {{
      background: {PALETTE['card']} !important;
      border-color: {PALETTE['border2']} !important;
      color: {PALETTE['text']} !important;
      border-radius: 10px !important;
  }}
  div[data-baseweb="input"] > div {{
      background: {PALETTE['card']} !important;
      border-color: {PALETTE['border2']} !important;
      border-radius: 10px !important;
  }}
  .stSlider > div {{ background: transparent !important; }}
  .stSlider [data-testid="stTickBarMin"],
  .stSlider [data-testid="stTickBarMax"] {{
      color: {PALETTE['muted']} !important;
      font-size: 0.7rem !important;
  }}
  .stButton > button {{
      background: linear-gradient(135deg, {PALETTE['accent']}, {PALETTE['accent5']});
      color: white;
      border: none;
      border-radius: 10px;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 600;
      padding: 0.5rem 1.5rem;
      letter-spacing: 0.02em;
      transition: opacity 0.2s, transform 0.1s;
  }}
  .stButton > button:hover {{ opacity: 0.9; transform: translateY(-1px); }}
  .stButton > button:active {{ transform: translateY(0); }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{
      gap: 0.3rem;
      background: {PALETTE['surface']};
      border-radius: 12px;
      padding: 4px;
      border: 1px solid {PALETTE['border']};
  }}
  .stTabs [data-baseweb="tab"] {{
      border-radius: 9px;
      color: {PALETTE['muted']} !important;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 0.85rem;
      font-weight: 500;
      padding: 0.4rem 1rem;
      transition: all 0.2s;
  }}
  .stTabs [aria-selected="true"] {{
      background: {PALETTE['card']} !important;
      color: {PALETTE['text']} !important;
      box-shadow: 0 1px 4px rgba(0,0,0,0.3);
  }}

  /* ── Metrics ── */
  [data-testid="stMetric"] {{
      background: {PALETTE['card']};
      border: 1px solid {PALETTE['border']};
      border-radius: 12px;
      padding: 0.9rem 1.1rem;
  }}
  [data-testid="stMetricLabel"] {{ color: {PALETTE['muted']} !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.06em; }}
  [data-testid="stMetricValue"] {{ color: {PALETTE['text']} !important; font-family: 'Outfit', sans-serif !important; font-weight: 700 !important; }}
  [data-testid="stMetricDelta"] {{ font-size: 0.75rem !important; }}

  /* ── Dataframe ── */
  [data-testid="stDataFrame"] {{
      border: 1px solid {PALETTE['border']} !important;
      border-radius: 12px !important;
      overflow: hidden;
  }}

  /* ── File uploader ── */
  [data-testid="stFileUploader"] {{
      background: {PALETTE['card']};
      border: 2px dashed {PALETTE['border2']};
      border-radius: 14px;
      padding: 1rem;
  }}

  /* ── Number input ── */
  input[type="number"] {{
      background: {PALETTE['card']} !important;
      color: {PALETTE['text']} !important;
      border-color: {PALETTE['border2']} !important;
  }}

  /* ── Sidebar nav label ── */
  .nav-section {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.6rem;
      color: {PALETTE['muted']};
      text-transform: uppercase;
      letter-spacing: 0.12em;
      padding: 0.8rem 0.5rem 0.3rem;
  }}

  /* ── Divider ── */
  hr {{ border-color: {PALETTE['border']} !important; margin: 1rem 0 !important; }}

  /* ── Success/Warning overrides ── */
  .stSuccess > div {{ background: {PALETTE['accent3']}18 !important; border-left: 3px solid {PALETTE['accent3']} !important; border-radius: 8px !important; }}
  .stWarning > div {{ background: {PALETTE['accent4']}18 !important; border-left: 3px solid {PALETTE['accent4']} !important; border-radius: 8px !important; }}
  .stInfo > div {{ background: {PALETTE['accent']}18 !important; border-left: 3px solid {PALETTE['accent']} !important; border-radius: 8px !important; }}

  /* ── Multiselect tags ── */
  [data-baseweb="tag"] {{
      background: {PALETTE['accent']}30 !important;
      border: 1px solid {PALETTE['accent']}50 !important;
      border-radius: 6px !important;
  }}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1.2rem 0.5rem 0.5rem;">
      <div style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:900;
                  background:linear-gradient(120deg,{PALETTE['accent']},{PALETTE['accent5']});
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  letter-spacing:-0.02em;">
        EduMetrics
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                  color:{PALETTE['muted']};margin-top:2px;letter-spacing:0.05em;">
        v2.0 · STUDENT ANALYTICS
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="nav-section">Navigation</div>', unsafe_allow_html=True)

    section = st.radio(
        "Navigate",
        ["📥  Data", "🎯  Sampling", "📊  Visualize", "🔗  Correlation",
         "📈  Regression", "🧪  Hypothesis & MLE"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Data status indicator
    if "numeric_df" in st.session_state:
        df_shape = st.session_state["numeric_df"].shape
        st.markdown(f"""
        <div style="background:{PALETTE['accent3']}15;border:1px solid {PALETTE['accent3']}30;
                    border-radius:10px;padding:0.7rem 0.9rem;font-size:0.75rem;">
          <div style="color:{PALETTE['accent3']};font-weight:600;margin-bottom:2px;">✓ Data Loaded</div>
          <div style="color:{PALETTE['muted']};font-family:'JetBrains Mono',monospace;font-size:0.65rem;">
            {df_shape[0]} rows · {df_shape[1]} cols
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:{PALETTE['accent4']}12;border:1px solid {PALETTE['accent4']}25;
                    border-radius:10px;padding:0.7rem 0.9rem;font-size:0.75rem;">
          <div style="color:{PALETTE['accent4']};font-weight:600;margin-bottom:2px;">⚠ No Data</div>
          <div style="color:{PALETTE['muted']};font-size:0.7rem;">Go to Data tab first</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:1rem;font-size:0.68rem;color:{PALETTE['muted']};line-height:1.6;padding:0 0.2rem;">
      Upload a CSV or use the built-in synthetic dataset with 80 student records.
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">▸ Quantitative Analysis Dashboard</div>
  <p class="hero-title">Student Performance<br>Analytics</p>
  <p class="hero-sub">Explore, sample, visualize, and model your academic data with professional statistical tools — all in one place.</p>
  <div class="hero-badges">
    <span class="badge badge-blue">Sampling Methods</span>
    <span class="badge badge-pink">Regression</span>
    <span class="badge badge-green">Hypothesis Testing</span>
    <span class="badge badge-yellow">MLE Estimation</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# EXPERIMENT ROUTER
# Each experiment's existing UI and logic lives in its own module.
# ──────────────────────────────────────────────
if section == "📥  Data":
    data.render()
elif section == "🎯  Sampling":
    sampling.render()
elif section == "📊  Visualize":
    visualization.render()
elif section == "🔗  Correlation":
    correlation.render()
elif section == "📈  Regression":
    regression.render()
elif section == "🧪  Hypothesis & MLE":
    hypothesis_testing.render()

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;margin-top:3rem;padding:1.2rem;
            border-top:1px solid {PALETTE['border']};
            display:flex;justify-content:center;align-items:center;gap:2rem;flex-wrap:wrap;">
  <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:{PALETTE['muted']};">
    EduMetrics v2.0
  </span>
  <span style="color:{PALETTE['border2']};">·</span>
  <span style="font-size:0.7rem;color:{PALETTE['muted']};">Student Performance Analytics</span>
  <span style="color:{PALETTE['border2']};">·</span>
  <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:{PALETTE['muted']};">
    Built with Streamlit
  </span>
</div>
""", unsafe_allow_html=True)
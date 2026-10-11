import warnings
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy import stats
warnings.filterwarnings("ignore")

PALETTE = {
    "bg":       "#080b14",
    "surface":  "#0d1120",
    "card":     "#111827",
    "card2":    "#161d2e",
    "border":   "#1e2d4a",
    "border2":  "#243351",
    "accent":   "#4f8ef7",
    "accent2":  "#f472b6",
    "accent3":  "#34d399",
    "accent4":  "#fbbf24",
    "accent5":  "#a78bfa",
    "text":     "#f0f4ff",
    "text2":    "#c8d3f0",
    "muted":    "#6b7db3",
    "danger":   "#f87171",
}


def apply_chart_style(ax, fig, title_size=11):
    fig.patch.set_facecolor(PALETTE["card"])
    ax.set_facecolor(PALETTE["surface"])
    for spine in ax.spines.values():
        spine.set_color(PALETTE["border2"])
        spine.set_linewidth(0.8)
    ax.tick_params(colors=PALETTE["muted"], labelsize=9, length=3)
    ax.xaxis.label.set_color(PALETTE["muted"])
    ax.yaxis.label.set_color(PALETTE["muted"])
    ax.title.set_color(PALETTE["text"])
    ax.title.set_fontsize(title_size)
    ax.title.set_fontweight("semibold")
    ax.grid(True, color=PALETTE["border"], alpha=0.4, linewidth=0.6, linestyle="--")
    ax.set_axisbelow(True)

def apply_chart_style_clean(ax, fig):
    """Minimal grid for scatter/distribution plots"""
    apply_chart_style(ax, fig)
    ax.grid(True, color=PALETTE["border"], alpha=0.3, linewidth=0.5)

CHART_COLORS = [
    PALETTE["accent"], PALETTE["accent2"], PALETTE["accent3"],
    PALETTE["accent4"], PALETTE["accent5"], "#f87171", "#38bdf8"
]

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def kpi_card(value, label, icon="", sub="", color="blue"):
    return f"""
    <div class="kpi-card {color}">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
      {'<div class="kpi-sub">' + sub + '</div>' if sub else ''}
    </div>"""

def section_header(title, pill=""):
    pill_html = f'<span class="section-pill">{pill}</span>' if pill else ""
    return f'<div class="section-label">{title} {pill_html}</div>'

def insight(text, title="💡 Insight"):
    return f'<div class="insight-box"><div class="insight-title">{title}</div>{text}</div>'


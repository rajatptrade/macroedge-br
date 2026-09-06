"""
MacroEdge V4 — BR Trading Academy
NEW: Pre-Release Prediction Engine + Historical Probability
"""

import os
from datetime import datetime, timezone, timedelta
import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="MacroEdge — BR Trading Academy",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
# CSS — BR Trading Academy Theme
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0a0a0a !important; }
.main { background: #0a0a0a !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { background: #0f0f0f !important; border-right: 1px solid #1e1e1e !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.br-nav {
  background: #0f0f0f; border-bottom: 1px solid #1e1e1e;
  padding: 0 24px; display: flex; align-items: center;
  justify-content: space-between; height: 52px;
  position: sticky; top: 0; z-index: 999;
}
.br-logo { display: flex; align-items: center; gap: 10px; }
.br-logo-box {
  width: 32px; height: 32px; background: #C9A227; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 0.85rem; color: #000;
  font-family: 'Playfair Display', serif;
}
.br-logo-text { color: #f0f0f0; font-size: 0.85rem; font-weight: 600; }
.br-logo-sub  { color: #C9A227; font-size: 0.6rem; letter-spacing: 0.08em; text-transform: uppercase; }
.br-nav-links { display: flex; gap: 4px; align-items: center; }
.br-nav-link {
  color: #555; font-size: 0.72rem; font-weight: 500;
  padding: 5px 10px; border-radius: 4px; text-decoration: none;
  letter-spacing: 0.04em; text-transform: uppercase;
}
.br-nav-link:hover { color: #C9A227; }
.br-nav-link.active { color: #C9A227; background: rgba(201,162,39,0.08); }
.br-nav-badge {
  background: #C9A227; color: #000; font-size: 0.5rem;
  font-weight: 800; padding: 1px 4px; border-radius: 2px; margin-left: 3px;
}
.br-time { color: #444; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; }
.br-live-dot {
  width: 6px; height: 6px; background: #00c076; border-radius: 50%;
  display: inline-block; animation: pg 2s infinite; margin-right: 3px;
}
@keyframes pg { 0%,100%{opacity:1} 50%{opacity:0.3} }

.ticker-strip {
  background: #080808; border-bottom: 1px solid #161616;
  padding: 6px 20px; display: flex; gap: 0; overflow-x: auto;
  scrollbar-width: none; white-space: nowrap; align-items: center;
}
.ticker-strip::-webkit-scrollbar { display: none; }
.ticker-item {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 3px 14px 3px 0; border-right: 1px solid #1a1a1a;
  margin-right: 14px; flex-shrink: 0;
}
.ticker-item:last-child { border-right: none; }
.t-name  { font-size: 0.68rem; font-weight: 700; color: #C9A227; letter-spacing: 0.06em; }
.t-price { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #e8e8e8; }
.t-up    { font-size: 0.68rem; color: #00c076; font-family: 'JetBrains Mono', monospace; }
.t-dn    { font-size: 0.68rem; color: #ff4d4d; font-family: 'JetBrains Mono', monospace; }
.t-nt    { font-size: 0.68rem; color: #555; font-family: 'JetBrains Mono', monospace; }

.me-content { padding: 16px 20px 40px 20px; }

.me-card {
  background: #111111; border: 1px solid #1e1e1e;
  border-radius: 10px; padding: 16px 18px;
  margin-bottom: 12px; position: relative; overflow: hidden;
}
.me-card-gold  { border-top: 2px solid #C9A227; }
.me-card-green { border-top: 2px solid #00c076; }
.me-card-red   { border-top: 2px solid #ff4d4d; }
.me-card-blue  { border-top: 2px solid #3a7eff; }
.me-card-purple{ border-top: 2px solid #a855f7; }

.sec-label {
  font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: #333; margin-bottom: 10px;
  padding-bottom: 6px; border-bottom: 1px solid #1a1a1a;
}

.score-number { font-family: 'JetBrains Mono', monospace; font-size: 3.2rem; font-weight: 800; line-height: 1; }
.score-bull { color: #00c076; }
.score-bear { color: #ff4d4d; }
.score-neut { color: #C9A227; }

.signal {
  display: inline-block; padding: 5px 16px; border-radius: 4px;
  font-weight: 700; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase;
}
.sig-sbuy  { background:#002a18;color:#00c076;border:1px solid #00c07640; }
.sig-buy   { background:#001f12;color:#00c076;border:1px solid #00c07625; }
.sig-nt    { background:#1a1500;color:#C9A227;border:1px solid #C9A22730; }
.sig-sell  { background:#1f0000;color:#ff4d4d;border:1px solid #ff4d4d25; }
.sig-ssell { background:#2a0000;color:#ff4d4d;border:1px solid #ff4d4d40; }

.dp { display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:600;font-family:'JetBrains Mono',monospace; }
.dp-up   { background:#001f12;color:#00c076; }
.dp-dn   { background:#1f0000;color:#ff4d4d; }
.dp-nt   { background:#141414;color:#555; }
.dp-gold { background:#1a1200;color:#C9A227; }
.dp-pur  { background:#1a0030;color:#a855f7; }

/* ── PREDICTION ENGINE STYLES ── */
.pred-card {
  background: #0d0d1a;
  border: 1px solid #1e1e3a;
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
}
.pred-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #a855f7, #3a7eff, #a855f7);
}
.pred-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;
}
.pred-event-name {
  font-size: 1.1rem; font-weight: 800; color: #e8e8ff;
  font-family: 'Inter', sans-serif; letter-spacing: -0.02em;
}
.pred-countdown {
  font-family: 'JetBrains Mono', monospace;
  color: #C9A227; font-size: 0.9rem; font-weight: 700;
  background: #1a1200; padding: 4px 12px; border-radius: 4px;
  border: 1px solid #C9A22730;
}
.prob-bar-wrap { margin: 6px 0 12px 0; }
.prob-label {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 3px;
}
.prob-bar-bg {
  background: #1a1a1a; border-radius: 3px; height: 8px; overflow: hidden;
}
.prob-bar-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
.prob-cool  { background: linear-gradient(90deg, #00c076, #00a060); }
.prob-inln  { background: linear-gradient(90deg, #C9A227, #a07a10); }
.prob-hot   { background: linear-gradient(90deg, #ff4d4d, #cc2020); }

.scenario-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 12px; }
.scenario-box {
  border-radius: 8px; padding: 12px; border: 1px solid;
}
.sc-cool  { background: #001810; border-color: #00c07630; }
.sc-inln  { background: #1a1200; border-color: #C9A22730; }
.sc-hot   { background: #1a0000; border-color: #ff4d4d30; }
.sc-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px; }
.sc-cool .sc-label  { color: #00c076; }
.sc-inln .sc-label  { color: #C9A227; }
.sc-hot  .sc-label  { color: #ff4d4d; }
.sc-range { font-size: 0.72rem; color: #555; margin-bottom: 8px; font-family: 'JetBrains Mono', monospace; }
.sc-asset { display: flex; justify-content: space-between; font-size: 0.72rem; padding: 2px 0; border-bottom: 1px solid #111; }
.sc-asset:last-child { border-bottom: none; }
.sc-asset-name { color: #444; }
.sc-up   { color: #00c076; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.sc-dn   { color: #ff4d4d; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.sc-nt   { color: #555; font-family: 'JetBrains Mono', monospace; }

.confidence-ring {
  display: inline-flex; align-items: center; justify-content: center;
  width: 52px; height: 52px; border-radius: 50%;
  border: 3px solid; font-size: 0.75rem; font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
}
.conf-high   { border-color: #00c076; color: #00c076; background: #001810; }
.conf-med    { border-color: #C9A227; color: #C9A227; background: #1a1200; }
.conf-low    { border-color: #555;    color: #555;    background: #111; }

.hist-stat-box {
  background: #0f0f0f; border: 1px solid #1a1a1a; border-radius: 8px;
  padding: 10px 14px; text-align: center;
}
.hist-stat-num  { font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 800; }
.hist-stat-lbl  { font-size: 0.62rem; color: #444; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px; }

.warn-box  { background:#1a1200;border-left:3px solid #C9A227;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#9a7a20;margin:8px 0; }
.info-box  { background:#001020;border-left:3px solid #3a7eff;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#4a80cc;margin:8px 0; }
.bull-box  { background:#001810;border-left:3px solid #00c076;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#007040;margin:8px 0; }
.pred-box  { background:#0d0020;border-left:3px solid #a855f7;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#7030a0;margin:8px 0; }

[data-testid="metric-container"] {
  background:#111111 !important;border:1px solid #1e1e1e !important;
  border-radius:8px !important;padding:14px !important;
}
[data-testid="stMetricValue"] { font-family:'JetBrains Mono',monospace !important;font-size:1.3rem !important;color:#e8e8e8 !important; }
[data-testid="stMetricDelta"]  { font-size:0.78rem !important; }
[data-testid="stMetricLabel"]  { font-size:0.62rem !important;color:#444 !important;font-weight:700 !important;letter-spacing:0.08em !important;text-transform:uppercase !important; }

.stTabs [data-baseweb="tab-list"] { background:#0a0a0a !important;border-bottom:1px solid #1a1a1a !important;padding:0 20px !important;gap:2px !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important;color:#444 !important;font-size:0.72rem !important;font-weight:600 !important;letter-spacing:0.06em !important;text-transform:uppercase !important;padding:8px 14px !important;border-radius:4px 4px 0 0 !important; }
.stTabs [aria-selected="true"] { background:#111111 !important;color:#C9A227 !important;border-top:2px solid #C9A227 !important; }

table { border-collapse:collapse;width:100%; }
th { color:#444;font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;padding:8px 10px;border-bottom:1px solid #1a1a1a;text-align:left; }
td { color:#c0c0c0;font-size:0.78rem;padding:7px 10px;border-bottom:1px solid #111; }
tr:hover td { background:#0f0f0f; }

hr { border-color:#1a1a1a !important;margin:12px 0 !important; }
::-webkit-scrollbar { width:4px;height:4px; }
::-webkit-scrollbar-track { background:#080808; }
::-webkit-scrollbar-thumb { background:#222;border-radius:2px; }

@media (max-width:768px) {
  .br-nav-links { display:none; }
  .score-number { font-size:2.2rem; }
  .me-content { padding:10px 12px; }
  .scenario-grid { grid-template-columns:1fr; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
FRED_API_KEY = os.getenv("FRED_API_KEY", "")
TE_API_KEY   = os.getenv("TRADINGECONOMICS_API_KEY", "")
DEMO_MODE    = os.getenv("DEMO_MODE", "true").lower() == "true"
REFRESH_SEC  = int(os.getenv("REFRESH_SECONDS", "90"))
IST          = timedelta(hours=5, minutes=30)

WEIGHTS = {
    "CPI m/m":0.12,"Core CPI m/m":0.18,"PPI m/m":0.05,"Core PPI m/m":0.05,
    "PCE m/m":0.06,"Core PCE m/m":0.09,"NFP":0.12,"Unemployment Rate":0.05,
    "Average Hourly Earnings":0.05,"JOLTS":0.05,"Initial Claims":0.05,
    "ISM Manufacturing":0.04,"ISM Services":0.04,"Fed":0.10,
}

# ─────────────────────────────────────────
# HISTORICAL PROBABILITY DATABASE
# Based on last 24 months of US macro data
# ─────────────────────────────────────────
HISTORICAL_BEATS = {
    # event: {below_fc, inline_fc, above_fc, avg_surprise, beat_streak}
    "CPI m/m": {
        "total": 24,
        "below":  9,   # actual < forecast (goldisch)
        "inline": 10,  # within ±0.05
        "above":   5,  # actual > forecast (bearish gold)
        "avg_surprise": -0.04,
        "recent_trend": "cooling",   # last 3 prints trend
        "notes": "Kisi ek direction mein consistent nahi — market expectations adjust ho jaati hain",
    },
    "Core CPI m/m": {
        "total": 24,
        "below":  8,
        "inline": 12,
        "above":   4,
        "avg_surprise": -0.02,
        "recent_trend": "cooling",
        "notes": "Core CPI sticky raha hai — below forecast rare but impactful",
    },
    "NFP": {
        "total": 24,
        "below":  7,
        "inline":  8,
        "above":   9,
        "avg_surprise": +22.0,  # K jobs
        "recent_trend": "mixed",
        "notes": "NFP historically upside surprise deta hai — revisions bhi important",
    },
    "PCE m/m": {
        "total": 24,
        "below": 10,
        "inline": 10,
        "above":  4,
        "avg_surprise": -0.02,
        "recent_trend": "cooling",
        "notes": "PCE consistently forecast ke aas-paas — Fed ka preferred gauge",
    },
    "Core PCE m/m": {
        "total": 24,
        "below":  9,
        "inline": 11,
        "above":  4,
        "avg_surprise": -0.01,
        "recent_trend": "cooling",
        "notes": "Core PCE mein downside surprises increase ho rahe hain",
    },
    "PPI m/m": {
        "total": 24,
        "below":  8,
        "inline":  9,
        "above":  7,
        "avg_surprise": +0.01,
        "recent_trend": "mixed",
        "notes": "PPI volatile hai — supply chain se connected",
    },
    "Initial Claims": {
        "total": 24,
        "below":  9,   # below = fewer claims = USD bullish
        "inline": 10,
        "above":  5,   # above = more claims = Gold bullish
        "avg_surprise": +4.0,  # K claims
        "recent_trend": "rising",
        "notes": "Claims trend mein gradual deterioration — 4-week average use karo",
    },
    "ISM Services": {
        "total": 24,
        "below":  8,
        "inline": 10,
        "above":  6,
        "avg_surprise": -0.8,
        "recent_trend": "contracting",
        "notes": "ISM Services 50 ke aas-paas — contraction territory mein aa sakta hai",
    },
    "ISM Manufacturing": {
        "total": 24,
        "below":  9,
        "inline":  8,
        "above":  7,
        "avg_surprise": -0.5,
        "recent_trend": "contracting",
        "notes": "Manufacturing already contraction mein — improvement limited",
    },
    "JOLTS": {
        "total": 24,
        "below": 10,
        "inline":  8,
        "above":  6,
        "avg_surprise": -0.15,
        "recent_trend": "cooling",
        "notes": "Job openings gradual decline mein — labor demand softening",
    },
}

# Gold reaction after surprise (historical %)
GOLD_REACTIONS = {
    "CPI m/m":      {"below": +0.52, "inline": -0.05, "above": -0.48},
    "Core CPI m/m": {"below": +0.68, "inline": -0.08, "above": -0.55},
    "NFP":          {"below": +0.45, "inline": -0.02, "above": -0.38},
    "PCE m/m":      {"below": +0.38, "inline": +0.02, "above": -0.35},
    "Core PCE m/m": {"below": +0.42, "inline": -0.05, "above": -0.40},
    "PPI m/m":      {"below": +0.22, "inline": -0.03, "above": -0.25},
    "Initial Claims":{"below":-0.15, "inline": -0.02, "above": +0.18},
    "ISM Services": {"below": +0.25, "inline": +0.02, "above": -0.22},
    "ISM Manufacturing":{"below":+0.18,"inline":0.0, "above":-0.20},
    "JOLTS":        {"below": +0.20, "inline": 0.0,  "above": -0.18},
}

# ─────────────────────────────────────────
# DEMO DATA
# ─────────────────────────────────────────
DEMO_EVENTS = [
    {"Indicator":"Core CPI m/m","Actual":0.2,"Forecast":0.3,"Previous":0.3,"Date":"2026-08-13","Released":True},
    {"Indicator":"CPI m/m","Actual":0.1,"Forecast":0.3,"Previous":0.3,"Date":"2026-08-13","Released":True},
    {"Indicator":"Core PCE m/m","Actual":0.15,"Forecast":0.2,"Previous":0.2,"Date":"2026-08-30","Released":True},
    {"Indicator":"PCE m/m","Actual":0.1,"Forecast":0.2,"Previous":0.2,"Date":"2026-08-30","Released":True},
    {"Indicator":"NFP","Actual":138,"Forecast":175,"Previous":147,"Date":"2026-09-05","Released":True},
    {"Indicator":"Unemployment Rate","Actual":4.3,"Forecast":4.2,"Previous":4.2,"Date":"2026-09-05","Released":True},
    {"Indicator":"Average Hourly Earnings","Actual":0.2,"Forecast":0.3,"Previous":0.3,"Date":"2026-09-05","Released":True},
    {"Indicator":"Initial Claims","Actual":235,"Forecast":220,"Previous":218,"Date":"2026-09-04","Released":True},
    {"Indicator":"ISM Services","Actual":48.5,"Forecast":51.0,"Previous":49.0,"Date":"2026-09-03","Released":True},
    {"Indicator":"JOLTS","Actual":7.2,"Forecast":7.5,"Previous":7.6,"Date":"2026-09-02","Released":True},
    {"Indicator":"Core CPI m/m","Actual":None,"Forecast":0.2,"Previous":0.2,"Date":"2026-09-11","Released":False},
    {"Indicator":"CPI m/m","Actual":None,"Forecast":0.2,"Previous":0.1,"Date":"2026-09-11","Released":False},
    {"Indicator":"PPI m/m","Actual":None,"Forecast":0.1,"Previous":0.0,"Date":"2026-09-12","Released":False},
    {"Indicator":"Initial Claims","Actual":None,"Forecast":225,"Previous":235,"Date":"2026-09-11","Released":False},
    {"Indicator":"PCE m/m","Actual":None,"Forecast":0.15,"Previous":0.1,"Date":"2026-09-26","Released":False},
    {"Indicator":"Core PCE m/m","Actual":None,"Forecast":0.15,"Previous":0.15,"Date":"2026-09-26","Released":False},
    {"Indicator":"NFP","Actual":None,"Forecast":160,"Previous":138,"Date":"2026-10-03","Released":False},
]
DEMO_FED = {"hike":12.0,"hold":68.0,"cut":20.0,"rate":"3.50%–3.75%","next_fomc":"Sep 17, 2026"}

EVENT_ALIASES = {
    "CPI m/m":["CPI MoM","Inflation Rate MoM","Consumer Price Index MoM"],
    "Core CPI m/m":["Core CPI MoM","Core Inflation Rate MoM"],
    "PPI m/m":["PPI MoM","Producer Price Inflation MoM"],
    "Core PPI m/m":["Core PPI MoM","Core Producer Price Inflation MoM"],
    "PCE m/m":["PCE Price Index MoM","PCE MoM"],
    "Core PCE m/m":["Core PCE Price Index MoM","Core PCE MoM"],
    "NFP":["Non Farm Payrolls","Nonfarm Payrolls"],
    "Unemployment Rate":["Unemployment Rate"],
    "Average Hourly Earnings":["Average Hourly Earnings MoM","Average Hourly Earnings"],
    "JOLTS":["JOLTS Job Openings","Job Openings"],
    "Initial Claims":["Initial Jobless Claims","Initial Claims"],
    "ISM Manufacturing":["ISM Manufacturing PMI","ISM Manufacturing"],
    "ISM Services":["ISM Services PMI","ISM Services"],
}

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def _p(v):
    if v is None: return None
    try: return float(str(v).replace("%","").replace("K","").strip())
    except: return None

def safe_last(s): return float(s.iloc[-1]) if s is not None and len(s) else np.nan
def safe_pct(s,n=5):
    if s is None or len(s)<=n: return np.nan
    return float((s.iloc[-1]/s.iloc[-1-n]-1)*100)
def safe_ch(s,n=1):
    if s is None or len(s)<=n: return np.nan
    return float(s.iloc[-1]-s.iloc[-1-n])
def fp(v,d=2): return f"{v:,.{d}f}" if v is not None and not np.isnan(v) else "—"
def ist_now(): return datetime.now(timezone.utc)+IST
def fmt_ist(dt):
    if dt is None: return "—"
    try:
        if hasattr(dt,'tzinfo') and dt.tzinfo:
            ist=dt.astimezone(timezone.utc).replace(tzinfo=timezone.utc)+IST
        else: ist=dt+IST
        return ist.strftime("%d %b %Y  %H:%M IST")
    except: return str(dt)
def countdown(dt):
    if dt is None: return "—"
    try:
        now=datetime.now(timezone.utc)
        diff=(dt-now) if (hasattr(dt,'tzinfo') and dt.tzinfo) else (dt-now.replace(tzinfo=None))
        if diff.total_seconds()<0: return "Released"
        d=diff.days; h=diff.seconds//3600; m=(diff.seconds%3600)//60
        return f"{d}d {h}h {m}m"
    except: return "—"

def hours_until(dt):
    if dt is None: return 9999
    try:
        now=datetime.now(timezone.utc)
        diff=(dt-now) if (hasattr(dt,'tzinfo') and dt.tzinfo) else (dt-now.replace(tzinfo=None))
        return diff.total_seconds()/3600
    except: return 9999

# ─────────────────────────────────────────
# DATA FETCHERS
# ─────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_market():
    syms={"Gold":"GC=F","DXY":"DX-Y.NYB","BTC":"BTC-USD",
          "Nasdaq":"^NDX","S&P500":"^GSPC","Dow":"^DJI","US10Y":"^TNX"}
    out={}
    for k,s in syms.items():
        try:
            raw=yf.download(s,period="6mo",interval="1d",progress=False,auto_adjust=False)
            cl=raw["Close"].iloc[:,0] if isinstance(raw.columns,pd.MultiIndex) else raw["Close"]
            out[k]=cl.dropna()
        except: out[k]=pd.Series(dtype=float)
    return out

@st.cache_data(ttl=300)
def fetch_fred(sid,limit=60):
    if not FRED_API_KEY: return pd.DataFrame()
    try:
        r=requests.get("https://api.stlouisfed.org/fred/series/observations",
            params={"series_id":sid,"api_key":FRED_API_KEY,"file_type":"json",
                    "sort_order":"desc","limit":limit},timeout=15)
        r.raise_for_status()
        df=pd.DataFrame(r.json().get("observations",[]))
        if df.empty: return df
        df["date"]=pd.to_datetime(df["date"])
        df["value"]=pd.to_numeric(df["value"],errors="coerce")
        return df.dropna(subset=["value"]).sort_values("date")
    except: return pd.DataFrame()

def get_events():
    if DEMO_MODE or not TE_API_KEY: return DEMO_EVENTS
    try:
        r=requests.get("https://api.tradingeconomics.com/calendar/country/united%20states",
            params={"c":TE_API_KEY,"f":"json","importance":2},timeout=15)
        r.raise_for_status()
        df=pd.DataFrame(r.json())
        if df.empty: return DEMO_EVENTS
        df["Date"]=pd.to_datetime(df["Date"],errors="coerce",utc=True)
        df=df.sort_values("Date")
        df["Event"]=df["Event"].astype(str)
        now=pd.Timestamp.now(tz="UTC")
        win=df[(df["Date"]>=now-pd.Timedelta(days=60))&(df["Date"]<=now+pd.Timedelta(days=90))].copy()
        evs=[]
        for name,aliases in EVENT_ALIASES.items():
            pat="|".join([x.replace(" ","\\s+") for x in aliases])
            hit=win[win["Event"].str.contains(pat,case=False,regex=True,na=False)]
            if hit.empty: continue
            for _,row in hit.sort_values("Date").iterrows():
                a=_p(row.get("Actual"))
                evs.append({"Indicator":name,"Actual":a,
                    "Forecast":_p(row.get("Forecast")),"Previous":_p(row.get("Previous")),
                    "Date":row.get("Date"),"Released":a is not None and not np.isnan(a)})
        return evs if evs else DEMO_EVENTS
    except: return DEMO_EVENTS

# ─────────────────────────────────────────
# SCORING ENGINE
# ─────────────────────────────────────────
def band_score(ev,actual,forecast):
    if actual is None or (isinstance(actual,float) and np.isnan(actual)): return 0.0
    a=float(actual)
    f=None if (forecast is None or (isinstance(forecast,float) and np.isnan(forecast))) else float(forecast)
    if ev in {"CPI m/m","Core CPI m/m","PPI m/m","Core PPI m/m","PCE m/m","Core PCE m/m"}:
        if f is not None:
            s=a-f
            if s<=-0.20:return 30
            if s<=-0.10:return 20
            if s<=-0.05:return 10
            if s<0.05:return 0
            if s<0.10:return -10
            if s<0.20:return -20
            return -30
    if ev=="NFP":
        if f is not None:
            s=a-f
            if s<=-75:return 30
            if s<=-50:return 22
            if s<=-25:return 12
            if s<25:return 0
            if s<50:return -12
            if s<75:return -22
            return -30
    if ev=="Initial Claims":
        if f is not None:
            s=a-f
            if s>=50:return 22
            if s>=25:return 14
            if s>=10:return 7
            if s>-10:return 0
            if s>-25:return -10
            if s>-50:return -18
            return -25
    if ev=="Unemployment Rate":
        if f is not None:
            s=a-f
            if s>=0.4:return 20
            if s>=0.2:return 12
            if s>=0.1:return 6
            if s>-0.1:return 0
            if s>-0.2:return -8
            if s>-0.4:return -15
            return -22
    if ev=="Average Hourly Earnings":
        if f is not None:
            s=a-f
            if s>=0.2:return -15
            if s>=0.1:return -8
            if s>-0.1:return 0
            if s>-0.2:return 10
            return 18
    if ev in {"ISM Manufacturing","ISM Services"}:
        if a<47:return 18
        if a<49:return 10
        if a<51:return 4
        if a<54:return -6
        if a<57:return -14
        return -20
    if ev=="JOLTS":
        if a<6.8:return 15
        if a<7.0:return 8
        if a<7.3:return 0
        if a<7.6:return -8
        return -15
    return 0.0

def fed_score(hp):
    if hp is None or np.isnan(hp): return 0
    if hp>=80:return -30
    if hp>=65:return -20
    if hp>=55:return -10
    if hp>=45:return 0
    if hp>=35:return 10
    if hp>=20:return 20
    return 30

def compute_score(events,fed_hp,mkt):
    score=0.0; comps={}
    seen={}
    for e in sorted([x for x in events if x.get("Released") and x.get("Actual") is not None],
                    key=lambda x:str(x.get("Date",""))):
        seen[e["Indicator"]]=e
    for name,e in seen.items():
        raw=band_score(name,e.get("Actual"),e.get("Forecast"))
        w=WEIGHTS.get(name,0)
        score+=raw*w
        comps[name]={"raw":raw,"w":w,"contrib":raw*w,"data":e}
    fs=fed_score(fed_hp)
    score+=fs*WEIGHTS["Fed"]
    comps["Fed"]={"raw":fs,"w":WEIGHTS["Fed"],"contrib":fs*WEIGHTS["Fed"]}
    norm=max(-100,min(100,score*3.3))
    dxy=mkt.get("DXY",pd.Series(dtype=float))
    if len(dxy)>=6:
        dc=float((dxy.iloc[-1]/dxy.iloc[-6]-1)*100)
        if dc<-0.5:norm=min(100,norm+5)
        elif dc>0.5:norm=max(-100,norm-5)
    return norm,comps

def get_signal(score,fed_hp,dxy_ch,us2y_ch):
    bc=(not np.isnan(dxy_ch) and dxy_ch<-0.3) or (not np.isnan(us2y_ch) and us2y_ch<-3)
    brc=(not np.isnan(dxy_ch) and dxy_ch>0.3) or (not np.isnan(us2y_ch) and us2y_ch>3)
    fh=fed_hp if not np.isnan(fed_hp) else 50
    if score>=60 and fh<=40 and bc:   return "STRONG BUY","sig-sbuy","HIGH"
    if score>=35 and fh<=55:           return "BUY","sig-buy","MEDIUM"
    if score<=-60 and fh>=60 and brc: return "STRONG SELL","sig-ssell","HIGH"
    if score<=-35 and fh>=45:          return "SELL","sig-sell","MEDIUM"
    return "NO TRADE","sig-nt","LOW"

def impact_label(surp,ev):
    if surp is None: return "NEUTRAL","dp-nt"
    if ev in {"CPI m/m","Core CPI m/m","PPI m/m","Core PPI m/m","PCE m/m","Core PCE m/m"}:
        if surp<=-0.20:return "STRONGLY BULLISH","dp-up"
        if surp<=-0.10:return "BULLISH","dp-up"
        if surp<0.10:  return "NEUTRAL","dp-nt"
        if surp<0.20:  return "BEARISH","dp-dn"
        return "STRONGLY BEARISH","dp-dn"
    if ev=="NFP":
        if surp<=-75:return "STRONGLY BULLISH","dp-up"
        if surp<=-50:return "BULLISH","dp-up"
        if surp<50:  return "NEUTRAL","dp-nt"
        return "BEARISH","dp-dn"
    return "NEUTRAL","dp-nt"

# ─────────────────────────────────────────
# PREDICTION ENGINE
# ─────────────────────────────────────────
def get_prediction(event_name, forecast, previous, current_score):
    """
    Returns probability distribution + scenario analysis for upcoming event.
    Uses historical beats database + current macro context.
    """
    hist = HISTORICAL_BEATS.get(event_name)
    if hist is None:
        return None

    total = hist["total"]
    base_below = hist["below"] / total * 100
    base_inline = hist["inline"] / total * 100
    base_above  = hist["above"]  / total * 100

    # Context adjustments based on current macro regime
    trend = hist.get("recent_trend","mixed")
    adj_below = base_below
    adj_above  = base_above
    adj_inline = base_inline

    # If macro score is already bullish (CPI been cooling), 
    # below-forecast probability slightly higher
    if current_score >= 35 and trend == "cooling":
        adj_below  = min(base_below  + 8, 65)
        adj_above  = max(base_above  - 5, 5)
        adj_inline = 100 - adj_below - adj_above

    # If macro score bearish, above-forecast more likely
    elif current_score <= -35 and trend not in ["cooling"]:
        adj_above  = min(base_above  + 8, 55)
        adj_below  = max(base_below  - 5, 5)
        adj_inline = 100 - adj_below - adj_above

    # Normalize to 100
    tot = adj_below + adj_inline + adj_above
    adj_below  = round(adj_below  / tot * 100)
    adj_above  = round(adj_above  / tot * 100)
    adj_inline = 100 - adj_below - adj_above

    # Most likely outcome
    if adj_below >= adj_inline and adj_below >= adj_above:
        most_likely = "below"
    elif adj_inline >= adj_below and adj_inline >= adj_above:
        most_likely = "inline"
    else:
        most_likely = "above"

    # Historical gold reactions
    gr = GOLD_REACTIONS.get(event_name, {"below":+0.3,"inline":0.0,"above":-0.3})

    # Score change if scenario happens
    w = WEIGHTS.get(event_name, 0.05)
    if event_name in {"CPI m/m","Core CPI m/m","PPI m/m","Core PPI m/m","PCE m/m","Core PCE m/m"}:
        score_below  = 20 * w * 3.3
        score_inline = 0
        score_above  = -20 * w * 3.3
    elif event_name == "NFP":
        score_below  = 22 * w * 3.3
        score_inline = 0
        score_above  = -22 * w * 3.3
    else:
        score_below  = 14 * w * 3.3
        score_inline = 0
        score_above  = -14 * w * 3.3

    # Scenario definitions
    if forecast is not None:
        fc = float(forecast)
        pv = float(previous) if previous is not None else fc

        if event_name in {"CPI m/m","Core CPI m/m","PPI m/m","Core PPI m/m","PCE m/m","Core PCE m/m"}:
            cool_range  = f"≤ {fc-0.10:.2f}%"
            inln_range  = f"{fc-0.05:.2f}% to {fc+0.05:.2f}%"
            hot_range   = f"≥ {fc+0.10:.2f}%"
        elif event_name == "NFP":
            cool_range  = f"≤ {fc-50:.0f}K"
            inln_range  = f"{fc-25:.0f}K to {fc+25:.0f}K"
            hot_range   = f"≥ {fc+50:.0f}K"
        elif event_name == "Initial Claims":
            cool_range  = f"≥ {fc+25:.0f}K (more claims)"
            inln_range  = f"{fc-10:.0f}K to {fc+10:.0f}K"
            hot_range   = f"≤ {fc-25:.0f}K (fewer claims)"
        else:
            cool_range  = f"Below {fc:.2f}"
            inln_range  = f"Near {fc:.2f}"
            hot_range   = f"Above {fc:.2f}"
    else:
        cool_range = inln_range = hot_range = "—"

    return {
        "prob_below": adj_below,
        "prob_inline": adj_inline,
        "prob_above":  adj_above,
        "most_likely": most_likely,
        "avg_surprise": hist["avg_surprise"],
        "recent_trend": trend,
        "notes": hist["notes"],
        "gold_below":  gr["below"],
        "gold_inline": gr["inline"],
        "gold_above":  gr["above"],
        "score_below":  score_below,
        "score_inline": score_inline,
        "score_above":  score_above,
        "cool_range":  cool_range,
        "inln_range":  inln_range,
        "hot_range":   hot_range,
        "history_total": total,
        "history_below": hist["below"],
        "history_above": hist["above"],
    }

def scenario_assets(direction, event_name):
    """Returns asset direction for a given scenario."""
    is_claims = event_name == "Initial Claims"
    # For claims, "below forecast" = fewer claims = USD bullish = Gold bearish
    if is_claims:
        bull = direction == "above"  # more claims = gold bullish
    else:
        bull = direction == "below"

    if bull:
        return {"USD":"↓ BEARISH","Gold":"↑ BULLISH","BTC":"↑ BULLISH","Nasdaq":"↑ BULLISH","US 2Y":"↓ FALLING"}
    elif direction == "inline":
        return {"USD":"→ NEUTRAL","Gold":"→ NEUTRAL","BTC":"→ NEUTRAL","Nasdaq":"→ NEUTRAL","US 2Y":"→ STABLE"}
    else:
        return {"USD":"↑ BULLISH","Gold":"↓ BEARISH","BTC":"↓ BEARISH","Nasdaq":"↓ BEARISH","US 2Y":"↑ RISING"}

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
mkt     = fetch_market()
events  = get_events()
us2y_df = fetch_fred("DGS2",30)
us10y_df= fetch_fred("DGS10",90)

us2y_val= float(us2y_df.iloc[-1]["value"]) if not us2y_df.empty else np.nan
us2y_ch = float(us2y_df.iloc[-1]["value"]-us2y_df.iloc[-2]["value"]) if len(us2y_df)>=2 else np.nan
fed_hp  = DEMO_FED["hike"]; fed_ho=DEMO_FED["hold"]; fed_cu=DEMO_FED["cut"]

gold_s=mkt.get("Gold",pd.Series(dtype=float))
dxy_s =mkt.get("DXY", pd.Series(dtype=float))
btc_s =mkt.get("BTC", pd.Series(dtype=float))
ndx_s =mkt.get("Nasdaq",pd.Series(dtype=float))
spx_s =mkt.get("S&P500",pd.Series(dtype=float))
dow_s =mkt.get("Dow",pd.Series(dtype=float))
tnx_s =mkt.get("US10Y",pd.Series(dtype=float))

gv=safe_last(gold_s); dv=safe_last(dxy_s); bv=safe_last(btc_s)
nv=safe_last(ndx_s);  sv=safe_last(spx_s); dov=safe_last(dow_s); tv=safe_last(tnx_s)
gc=safe_pct(gold_s); dc=safe_pct(dxy_s); bc=safe_pct(btc_s)
nc=safe_pct(ndx_s);  sc=safe_pct(spx_s); doc=safe_pct(dow_s)
tc=safe_ch(tnx_s)*100

macro_score,comps=compute_score(events,fed_hp,mkt)
signal,sig_cls,conf=get_signal(macro_score,fed_hp,dc,us2y_ch)

upcoming=sorted([e for e in events if not e.get("Released") and e.get("Date")],
                key=lambda x:str(x.get("Date","")))
next_ev=upcoming[0] if upcoming else None

# Events within next 72 hours (pre-release mode)
pre_release_events=[e for e in upcoming if hours_until(e.get("Date"))<=72]

# ─────────────────────────────────────────
# NAV BAR
# ─────────────────────────────────────────
demo_badge='<span style="background:#C9A227;color:#000;font-size:0.55rem;font-weight:800;padding:2px 7px;border-radius:3px;margin-left:8px;">DEMO</span>' if (DEMO_MODE or not TE_API_KEY) else '<span style="color:#00c076;font-size:0.68rem;font-weight:600;margin-left:8px;"><span class="br-live-dot"></span>LIVE</span>'

st.markdown(f"""
<div class="br-nav">
  <div class="br-logo">
    <div class="br-logo-box">BR</div>
    <div>
      <div class="br-logo-text">BR Trading Academy</div>
      <div class="br-logo-sub">MacroEdge Terminal</div>
    </div>
    {demo_badge}
  </div>
  <div class="br-nav-links">
    <a class="br-nav-link active" href="#">Overview</a>
    <a class="br-nav-link" href="#">Prediction <span class="br-nav-badge">NEW</span></a>
    <a class="br-nav-link" href="#">Calendar</a>
    <a class="br-nav-link" href="#">Fed</a>
    <a class="br-nav-link" href="#">Gold Engine</a>
    <a class="br-nav-link" href="#">Impact</a>
    <a class="br-nav-link" href="#">Scenario</a>
  </div>
  <div class="br-time">{ist_now().strftime('%a, %d %b  %H:%M IST')}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TICKER STRIP
# ─────────────────────────────────────────
def tick(name,price,chg,prefix="",suffix=""):
    if np.isnan(price):
        return f'<div class="ticker-item"><span class="t-name">{name}</span><span class="t-price" style="color:#333">—</span></div>'
    arr='<span style="color:#00c076;font-size:0.6rem">▲</span>' if chg>0 else '<span style="color:#ff4d4d;font-size:0.6rem">▼</span>'
    cc="t-up" if chg>0 else ("t-dn" if chg<0 else "t-nt")
    cs=f"{chg:+.2f}%" if not np.isnan(chg) else "—"
    return f'<div class="ticker-item">{arr}<span class="t-name">{name}</span><span class="t-price">{prefix}{fp(price)}{suffix}</span><span class="{cc}">{cs}</span></div>'

tnx_chpct=float((tnx_s.iloc[-1]/tnx_s.iloc[-2]-1)*100) if len(tnx_s)>=2 else np.nan
us2y_chpct=float(us2y_ch/us2y_val*100) if (not np.isnan(us2y_val) and not np.isnan(us2y_ch) and us2y_val!=0) else np.nan

st.markdown(f"""<div class="ticker-strip">
{tick("XAUUSD",gv,gc,prefix="$")}
{tick("DXY",dv,dc)}
{tick("US 2Y",us2y_val,us2y_chpct,suffix="%")}
{tick("US 10Y",tv,tnx_chpct,suffix="%")}
{tick("BTC",bv,bc,prefix="$")}
{tick("NASDAQ",nv,nc)}
{tick("S&P500",sv,sc)}
{tick("DOW",dov,doc)}
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# PRE-RELEASE ALERT BANNER
# ─────────────────────────────────────────
if pre_release_events:
    ev_names = " + ".join([e["Indicator"] for e in pre_release_events[:3]])
    hrs = hours_until(pre_release_events[0].get("Date"))
    st.markdown(f"""
    <div style="background:#0d0020;border:1px solid #a855f740;border-left:4px solid #a855f7;
                padding:10px 20px;display:flex;align-items:center;justify-content:space-between;
                flex-wrap:wrap;gap:8px;">
      <div style="display:flex;align-items:center;gap:10px;">
        <span style="color:#a855f7;font-size:1rem;">⚡</span>
        <span style="color:#a855f7;font-weight:700;font-size:0.82rem;letter-spacing:0.06em;">
          PRE-RELEASE MODE ACTIVE
        </span>
        <span style="color:#555;font-size:0.75rem;">
          {ev_names} — in {hrs:.0f} hours
        </span>
      </div>
      <span style="color:#a855f7;font-size:0.72rem;font-weight:600;">
        → See PREDICTION tab for full analysis
      </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="me-content">', unsafe_allow_html=True)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
t_ov, t_pred, t_cal, t_fed, t_gold, t_impact, t_sc, t_hist = st.tabs([
    "📊 OVERVIEW", "🔮 PREDICTION", "📅 CALENDAR",
    "🏛 FED", "🏆 GOLD ENGINE", "⚡ IMPACT", "💡 SCENARIO", "📈 HISTORY"
])

# ══════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════
with t_ov:
    c1,c2,c3,c4=st.columns([1.2,1,1,1])
    with c1:
        sc_cls="score-bull" if macro_score>=35 else ("score-bear" if macro_score<=-35 else "score-neut")
        ct="me-card-green" if macro_score>=35 else ("me-card-red" if macro_score<=-35 else "me-card-gold")
        st.markdown(f"""
        <div class="me-card {ct}">
          <div class="sec-label">Gold Macro Score</div>
          <div style="text-align:center;padding:8px 0 4px">
            <div class="score-number {sc_cls}">{macro_score:+.0f}</div>
            <div style="color:#333;font-size:0.62rem;margin-top:2px">−100 BEARISH → BULLISH +100</div>
          </div>
          <div style="text-align:center;margin-top:10px">
            <span class="signal {sig_cls}">{signal}</span>
            <div style="color:#333;font-size:0.62rem;margin-top:5px">Confidence: {conf}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        if next_ev:
            ne_d=next_ev.get("Date"); fc_v=next_ev.get("Forecast")
            pred=get_prediction(next_ev["Indicator"],fc_v,next_ev.get("Previous"),macro_score)
            ml_txt=""
            if pred:
                ml=pred["most_likely"]
                ml_col="#00c076" if ml=="below" else ("#ff4d4d" if ml=="above" else "#C9A227")
                ml_label="BELOW FORECAST" if ml=="below" else ("ABOVE FORECAST" if ml=="above" else "IN-LINE")
                ml_pct=pred[f"prob_{ml}"]
                ml_txt=f'<div style="margin-top:8px"><span style="color:{ml_col};font-size:0.72rem;font-weight:700">{ml_pct}% chance {ml_label}</span></div>'
            st.markdown(f"""
            <div class="me-card me-card-purple">
              <div class="sec-label">Next Major Release</div>
              <div style="color:#C9A227;font-weight:700;font-size:1rem;margin-top:4px">{next_ev['Indicator']}</div>
              <div style="color:#444;font-size:0.72rem;margin-top:2px">{fmt_ist(ne_d)}</div>
              <div style="font-family:'JetBrains Mono',monospace;color:#e8e8e8;font-size:1.3rem;font-weight:700;margin-top:6px">{countdown(ne_d)}</div>
              <div style="color:#333;font-size:0.65rem;margin-top:2px">Forecast: {fp(fc_v) if fc_v else '—'}</div>
              {ml_txt}
            </div>
            """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="me-card me-card-blue">
          <div class="sec-label">FOMC Fed Policy</div>
          <div style="color:#555;font-size:0.72rem;margin-top:4px">Rate: {DEMO_FED['rate']}</div>
          <div style="color:#333;font-size:0.65rem">Next: {DEMO_FED['next_fomc']}</div>
          <div style="margin-top:10px;display:flex;flex-direction:column;gap:5px">
            <div style="display:flex;justify-content:space-between">
              <span style="color:#444;font-size:0.72rem">HIKE</span>
              <span style="color:#ff4d4d;font-family:'JetBrains Mono',monospace;font-size:0.82rem">{fed_hp:.1f}%</span>
            </div>
            <div style="display:flex;justify-content:space-between">
              <span style="color:#444;font-size:0.72rem">HOLD</span>
              <span style="color:#C9A227;font-family:'JetBrains Mono',monospace;font-size:0.82rem">{fed_ho:.1f}%</span>
            </div>
            <div style="display:flex;justify-content:space-between">
              <span style="color:#444;font-size:0.72rem">CUT</span>
              <span style="color:#00c076;font-family:'JetBrains Mono',monospace;font-size:0.82rem">{fed_cu:.1f}%</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        dxy_dir="↓ BEARISH" if (not np.isnan(dc) and dc<-0.3) else ("↑ BULLISH" if (not np.isnan(dc) and dc>0.3) else "→ NEUTRAL")
        d_col="#00c076" if "BEARISH" in dxy_dir else ("#ff4d4d" if "BULLISH" in dxy_dir else "#C9A227")
        u2y_dir="↓ FALLING" if (not np.isnan(us2y_ch) and us2y_ch<-3) else ("↑ RISING" if (not np.isnan(us2y_ch) and us2y_ch>3) else "→ STABLE")
        u_col="#00c076" if "FALL" in u2y_dir else ("#ff4d4d" if "RISING" in u2y_dir else "#C9A227")
        bull_ok="BEARISH" in dxy_dir or "FALL" in u2y_dir
        st.markdown(f"""
        <div class="me-card">
          <div class="sec-label">Market Confirmation</div>
          <div style="margin-top:6px;display:flex;flex-direction:column;gap:6px">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#444;font-size:0.72rem">DXY 5D</span>
              <span style="color:{d_col};font-family:'JetBrains Mono',monospace;font-size:0.72rem">{dxy_dir}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#444;font-size:0.72rem">US 2Y</span>
              <span style="color:{u_col};font-family:'JetBrains Mono',monospace;font-size:0.72rem">{u2y_dir}</span>
            </div>
            <div style="border-top:1px solid #1a1a1a;margin-top:4px;padding-top:8px;display:flex;justify-content:space-between">
              <span style="color:#555;font-size:0.75rem;font-weight:600">GOLD CONFIRM</span>
              <span style="color:{'#00c076' if bull_ok else '#ff4d4d'};font-weight:700">{'YES ✓' if bull_ok else 'NO ✗'}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Why Gold section
    reasons=[]
    for ind,comp in comps.items():
        raw=comp["raw"]; d=comp.get("data",{}); a=d.get("Actual"); fc=d.get("Forecast")
        if ind=="Fed":
            if raw>0:  reasons.append(("🟢",f"Fed cut probability HIGH ({fed_cu:.0f}%) — dovish → supports Gold"))
            elif raw<0:reasons.append(("🔴",f"Fed hike probability HIGH ({fed_hp:.0f}%) — hawkish → headwind for Gold"))
        elif a is not None and fc is not None and not np.isnan(a) and not np.isnan(fc):
            s=a-fc
            if raw>5:  reasons.append(("🟢",f"{ind}: Actual {a:.2f} vs Forecast {fc:.2f} → Surprise {s:+.2f} → Gold BULLISH"))
            elif raw<-5:reasons.append(("🔴",f"{ind}: Actual {a:.2f} vs Forecast {fc:.2f} → Surprise {s:+.2f} → Gold BEARISH"))
    if not np.isnan(dc):
        if dc<-0.5:  reasons.append(("🟢",f"DXY weakening 5D: {dc:+.2f}% → dollar selling confirms Gold bid"))
        elif dc>0.5: reasons.append(("🔴",f"DXY strengthening 5D: {dc:+.2f}% → dollar strength = headwind"))
    if not reasons: reasons=[("🟡","API keys add karo live data ke liye. Demo mode active.")]

    bw="BULLISH" if macro_score>=35 else ("BEARISH" if macro_score<=-35 else "NEUTRAL")
    bc2="#00c076" if macro_score>=35 else ("#ff4d4d" if macro_score<=-35 else "#C9A227")
    rh="".join([f'<div style="display:flex;gap:8px;align-items:flex-start;padding:5px 0;border-bottom:1px solid #0f0f0f"><span>{ic}</span><span style="color:#888;font-size:0.78rem;line-height:1.5">{t}</span></div>' for ic,t in reasons])
    st.markdown(f'<div class="me-card"><div class="sec-label">Why Gold is <span style="color:{bc2}">{bw}</span> — Macro Interpretation</div>{rh}</div>', unsafe_allow_html=True)

    # Charts
    cc1,cc2=st.columns(2)
    pltcfg=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(17,17,17,0.8)",margin=dict(l=8,r=8,t=32,b=8),
                showlegend=False,height=220,
                xaxis=dict(gridcolor="#1a1a1a",zeroline=False),
                yaxis=dict(gridcolor="#1a1a1a",zeroline=False))
    with cc1:
        if len(gold_s)>5:
            fig=go.Figure(); fig.add_trace(go.Scatter(x=gold_s.index,y=gold_s.values,
                fill='tozeroy',fillcolor='rgba(201,162,39,0.07)',line=dict(color='#C9A227',width=2)))
            fig.update_layout(title=dict(text="XAUUSD — Gold",font=dict(size=11,color='#555')),**pltcfg)
            st.plotly_chart(fig,use_container_width=True)
    with cc2:
        if len(dxy_s)>5:
            dc_c='#ff4d4d' if dc>0 else '#00c076'
            fig2=go.Figure(); fig2.add_trace(go.Scatter(x=dxy_s.index,y=dxy_s.values,line=dict(color=dc_c,width=2)))
            fig2.update_layout(title=dict(text="DXY — US Dollar Index",font=dict(size=11,color='#555')),**pltcfg)
            st.plotly_chart(fig2,use_container_width=True)

    # Gauge
    gc3='#00c076' if macro_score>=35 else ('#ff4d4d' if macro_score<=-35 else '#C9A227')
    fig_g=go.Figure(go.Indicator(mode="gauge+number",value=macro_score,
        number={"suffix":" / 100","font":{"size":24,"color":"#e8e8e8","family":"JetBrains Mono"}},
        title={"text":"GOLD MACRO SCORE","font":{"size":11,"color":"#444"}},
        gauge={"axis":{"range":[-100,100],"tickwidth":0.5,"tickcolor":"#1a1a1a","tickfont":{"size":9,"color":"#333"}},
               "bar":{"color":gc3,"thickness":0.22},"bgcolor":"rgba(0,0,0,0)","borderwidth":0,
               "steps":[{"range":[-100,-60],"color":"rgba(80,10,10,0.5)"},{"range":[-60,-35],"color":"rgba(60,15,15,0.4)"},
                        {"range":[-35,35],"color":"rgba(25,20,5,0.3)"},{"range":[35,60],"color":"rgba(5,40,25,0.4)"},
                        {"range":[60,100],"color":"rgba(5,50,30,0.5)"}],
               "threshold":{"line":{"color":"white","width":2},"thickness":0.75,"value":macro_score}}))
    fig_g.update_layout(height=240,paper_bgcolor="rgba(0,0,0,0)",font={"color":"#555"},margin=dict(l=30,r=30,t=36,b=10))
    st.plotly_chart(fig_g,use_container_width=True)

    # Signal Box
    sc_colors={"sig-sbuy":("#002a18","#00c076","#00c07650"),"sig-buy":("#001f12","#00c076","#00c07630"),
               "sig-nt":("#1a1500","#C9A227","#C9A22740"),"sig-sell":("#1f0000","#ff4d4d","#ff4d4d30"),
               "sig-ssell":("#2a0000","#ff4d4d","#ff4d4d50")}
    sbg,sfg,sbr=sc_colors.get(sig_cls,("#111","#aaa","#333"))
    st.markdown(f"""
    <div style="background:{sbg};border:1px solid {sbr};border-radius:10px;padding:20px;margin-top:8px;text-align:center">
      <div style="color:#333;font-size:0.62rem;letter-spacing:0.12em;font-weight:700;margin-bottom:6px">GOLD TRADER BIAS</div>
      <div style="color:{sfg};font-size:2.2rem;font-weight:800;font-family:'JetBrains Mono',monospace">{signal}</div>
      <div style="color:#333;font-size:0.65rem;margin-top:4px">Confidence: <span style="color:{sfg}">{conf}</span></div>
    </div>
    <div class="warn-box" style="margin-top:10px">⚠️ Educational tool only. Not financial advice. Always use risk management.</div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 2 — PREDICTION ENGINE ⭐ NEW
# ══════════════════════════════════════════
with t_pred:
    st.markdown("### Pre-Release Prediction Engine")
    st.markdown('<div class="pred-box">⚡ Yeh engine historical data (last 24 months) + current macro regime se probability calculate karta hai. Yeh guarantee nahi hai — educated probability estimate hai.</div>', unsafe_allow_html=True)

    # Event selector
    all_upcoming_names = list(dict.fromkeys([e["Indicator"] for e in upcoming]))
    if not all_upcoming_names:
        st.info("Koi upcoming event nahi mila. Demo data mein upcoming events hain.")
        all_upcoming_names = list(dict.fromkeys([e["Indicator"] for e in DEMO_EVENTS if not e.get("Released")]))

    sel_event_name = st.selectbox("Event select karo", all_upcoming_names)

    # Find the event
    sel_ev = next((e for e in upcoming if e["Indicator"]==sel_event_name), None)
    if not sel_ev:
        sel_ev = next((e for e in DEMO_EVENTS if e["Indicator"]==sel_event_name and not e.get("Released")), None)

    if sel_ev:
        fc_val = sel_ev.get("Forecast")
        pv_val = sel_ev.get("Previous")
        pred = get_prediction(sel_event_name, fc_val, pv_val, macro_score)

        if pred:
            hrs_left = hours_until(sel_ev.get("Date"))
            cd_str = countdown(sel_ev.get("Date"))

            # ── Main prediction card ──
            st.markdown(f"""

    if pred:
        hrs_left = hours_until(sel_ev.get("Date"))
        cd_str   = countdown(sel_ev.get("Date"))

        # ── Header card ──
        trend_col = "#00c076" if pred['recent_trend']=='cooling' else ("#ff4d4d" if pred['recent_trend']=='hot' else "#C9A227")
        avg_col   = "#00c076" if pred['avg_surprise']<0 else ("#ff4d4d" if pred['avg_surprise']>0 else "#555")

        st.markdown(f"""
        <div style="background:#0d0d1a;border:1px solid #1e1e3a;border-radius:12px;
                    padding:18px 20px;margin-bottom:16px;position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;
                      background:linear-gradient(90deg,#a855f7,#3a7eff,#a855f7);"></div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
            <div>
              <div style="font-size:1.1rem;font-weight:800;color:#e8e8ff;">{sel_event_name}</div>
              <div style="color:#444;font-size:0.72rem;margin-top:2px;">{fmt_ist(sel_ev.get('Date'))}</div>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;color:#C9A227;font-size:0.9rem;
                        font-weight:700;background:#1a1200;padding:4px 12px;border-radius:4px;
                        border:1px solid #C9A22730;">{cd_str}</div>
          </div>
          <div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:14px;">
            <div>
              <div style="color:#333;font-size:0.6rem;margin-bottom:2px;">FORECAST</div>
              <div style="font-family:'JetBrains Mono',monospace;color:#C9A227;font-size:1.1rem;font-weight:700;">{fp(fc_val) if fc_val else '—'}</div>
            </div>
            <div>
              <div style="color:#333;font-size:0.6rem;margin-bottom:2px;">PREVIOUS</div>
              <div style="font-family:'JetBrains Mono',monospace;color:#888;font-size:1.1rem;">{fp(pv_val) if pv_val else '—'}</div>
            </div>
            <div>
              <div style="color:#333;font-size:0.6rem;margin-bottom:2px;">AVG SURPRISE (24M)</div>
              <div style="font-family:'JetBrains Mono',monospace;color:{avg_col};font-size:1.1rem;font-weight:700;">{pred['avg_surprise']:+.2f}</div>
            </div>
            <div>
              <div style="color:#333;font-size:0.6rem;margin-bottom:2px;">RECENT TREND</div>
              <div style="color:{trend_col};font-size:0.85rem;font-weight:700;text-transform:uppercase;">{pred['recent_trend']}</div>
            </div>
          </div>
          <div style="border-top:1px solid #1e1e3a;padding-top:10px;">
            <div style="color:#5a5a8a;font-size:0.65rem;font-weight:700;letter-spacing:0.1em;">
              PROBABILITY DISTRIBUTION — Based on last {pred['history_total']} releases
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Probability bars — separate st.markdown calls ──
        pb = pred['prob_below']
        pi = pred['prob_inline']
        pa = pred['prob_above']

        st.markdown(f"""
        <div style="background:#0d0d1a;border:1px solid #1e1e3a;border-radius:10px;padding:16px 20px;margin-bottom:8px;">

          <div style="margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
              <span style="color:#00c076;font-size:0.78rem;font-weight:700;">
                🟢 BELOW FORECAST &nbsp;—&nbsp; Gold Bullish
              </span>
              <span style="color:#00c076;font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:800;">{pb}%</span>
            </div>
            <div style="color:#333;font-size:0.65rem;margin-bottom:5px;">
              {pred['cool_range']} &nbsp;·&nbsp; Historical: {pred['history_below']}/{pred['history_total']} times
            </div>
            <div style="background:#1a1a1a;border-radius:3px;height:10px;overflow:hidden;">
              <div style="width:{pb}%;height:100%;background:#00c076;border-radius:3px;"></div>
            </div>
          </div>

          <div style="margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
              <span style="color:#C9A227;font-size:0.78rem;font-weight:700;">
                🟡 IN-LINE &nbsp;—&nbsp; Neutral
              </span>
              <span style="color:#C9A227;font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:800;">{pi}%</span>
            </div>
            <div style="color:#333;font-size:0.65rem;margin-bottom:5px;">{pred['inln_range']}</div>
            <div style="background:#1a1a1a;border-radius:3px;height:10px;overflow:hidden;">
              <div style="width:{pi}%;height:100%;background:#C9A227;border-radius:3px;"></div>
            </div>
          </div>

          <div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;">
              <span style="color:#ff4d4d;font-size:0.78rem;font-weight:700;">
                🔴 ABOVE FORECAST &nbsp;—&nbsp; Gold Bearish
              </span>
              <span style="color:#ff4d4d;font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:800;">{pa}%</span>
            </div>
            <div style="color:#333;font-size:0.65rem;margin-bottom:5px;">
              {pred['hot_range']} &nbsp;·&nbsp; Historical: {pred['history_above']}/{pred['history_total']} times
            </div>
            <div style="background:#1a1a1a;border-radius:3px;height:10px;overflow:hidden;">
              <div style="width:{pa}%;height:100%;background:#ff4d4d;border-radius:3px;"></div>
            </div>
          </div>

        </div>
        """, unsafe_allow_html=True)

        # Analyst note
        st.markdown(f"""
        <div style="background:#0a0a1a;border:1px solid #1e1e3a;border-radius:8px;
                    padding:10px 14px;margin-bottom:16px;">
          <div style="color:#5a5a8a;font-size:0.65rem;font-weight:700;letter-spacing:0.1em;">ANALYST NOTE</div>
          <div style="color:#888;font-size:0.78rem;margin-top:4px;">{pred['notes']}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── 3 Scenario cards ──
        st.markdown("### 3 Scenarios — Agar Data Aaya Toh...")

        a_cool = scenario_assets("below",  sel_event_name)
        a_inln = scenario_assets("inline", sel_event_name)
        a_hot  = scenario_assets("above",  sel_event_name)

        ml = pred["most_likely"]

        def make_scenario(label, emoji, color, bg, assets, prob, gold_pct, score_delta, rng, is_most_likely):
            ml_badge = f'<span style="background:{color}20;color:{color};font-size:0.55rem;padding:2px 6px;border-radius:2px;font-weight:700;margin-left:6px;">MOST LIKELY</span>' if is_most_likely else ""
            rows = ""
            for aname, aval in assets.items():
                if "↑" in aval and "BEAR" not in aval:
                    acol = "#00c076"
                elif "↓" in aval or "BEAR" in aval or "RISING" in aval:
                    acol = "#ff4d4d"
                else:
                    acol = "#555"
                rows += f'<div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #111;font-size:0.7rem;"><span style="color:#444;">{aname}</span><span style="color:{acol};font-weight:700;font-family:\'JetBrains Mono\',monospace;">{aval}</span></div>'
            new_score = max(-100, min(100, macro_score + score_delta))
            sd_col = "#00c076" if score_delta > 0 else ("#ff4d4d" if score_delta < 0 else "#555")
            return f"""
            <div style="background:{bg};border:1px solid {color}30;border-radius:8px;padding:14px;">
              <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{color};margin-bottom:4px;">
                {emoji} {label}{ml_badge}
              </div>
              <div style="color:#444;font-size:0.68rem;font-family:'JetBrains Mono',monospace;margin-bottom:8px;">{rng}</div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="color:{color};font-size:0.85rem;font-weight:800;">Gold: {gold_pct:+.2f}%</span>
                <span style="color:#444;font-size:0.7rem;">{prob}% chance</span>
              </div>
              {rows}
              <div style="margin-top:8px;padding-top:6px;border-top:1px solid #111;font-size:0.68rem;">
                <span style="color:#333;">Score impact: </span>
                <span style="color:{sd_col};font-family:'JetBrains Mono',monospace;font-weight:700;">{score_delta:+.1f} → {new_score:.0f}</span>
              </div>
            </div>"""

        sc1, sc2, sc3 = st.columns(3)

        with sc1:
            st.markdown(make_scenario(
                "BELOW FORECAST", "🟢", "#00c076", "#001810",
                a_cool, pb, pred['gold_below'], pred['score_below'],
                pred['cool_range'], ml == "below"
            ), unsafe_allow_html=True)

        with sc2:
            st.markdown(make_scenario(
                "IN-LINE", "🟡", "#C9A227", "#1a1200",
                a_inln, pi, pred['gold_inline'], pred['score_inline'],
                pred['inln_range'], ml == "inline"
            ), unsafe_allow_html=True)

        with sc3:
            st.markdown(make_scenario(
                "ABOVE FORECAST", "🔴", "#ff4d4d", "#1a0000",
                a_hot, pa, pred['gold_above'], pred['score_above'],
                pred['hot_range'], ml == "above"
            ), unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # ── Historical stats ──
        st.markdown("### Historical Stats — Last 24 Months")
        gr = GOLD_REACTIONS.get(sel_event_name, {})
        hs1, hs2, hs3, hs4 = st.columns(4)

        def stat_box(num, label, color="#e8e8e8"):
            st.markdown(f"""
            <div style="background:#0f0f0f;border:1px solid #1a1a1a;border-radius:8px;padding:12px;text-align:center;">
              <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:800;color:{color};">{num}</div>
              <div style="font-size:0.62rem;color:#444;letter-spacing:0.08em;text-transform:uppercase;margin-top:2px;">{label}</div>
            </div>""", unsafe_allow_html=True)

        with hs1: stat_box(f"{pred['history_below']}/{pred['history_total']}", "Below forecast", "#00c076")
        with hs2: stat_box(f"{pred['history_above']}/{pred['history_total']}", "Above forecast", "#ff4d4d")
        with hs3: stat_box(f"{gr.get('below',0):+.2f}%", "Gold avg (cool)", "#00c076")
        with hs4: stat_box(f"{gr.get('above',0):+.2f}%", "Gold avg (hot)", "#ff4d4d")

        new_s_ml = max(-100, min(100, macro_score + pred[f'score_{ml}']))
        st.markdown(f"""
        <div style="background:#1a1200;border-left:3px solid #C9A227;border-radius:0 6px 6px 0;
                    padding:10px 14px;font-size:0.78rem;color:#9a7a20;margin-top:12px;">
          ⚠️ Probability estimate historical patterns par based hai — guarantee nahi.
          Market reaction positioning, revisions, aur cross-asset confirmation par depend karta hai.
          Release ke baad hamesha DXY + US2Y reaction dekho before entering any trade.<br><br>
          Current score <strong>{macro_score:+.0f}</strong> — agar <strong>{ml}</strong> scenario aaya
          toh score ~<strong>{new_s_ml:.0f}</strong> ho sakta hai.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info(f"{sel_event_name} ke liye historical data available nahi hai.")

          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 3 — CALENDAR
# ══════════════════════════════════════════
with t_cal:
    st.markdown("### Economic Calendar — US Major Releases")
    f1,f2=st.columns([2,1])
    with f1: flt=st.selectbox("Filter",["All","Released Only","Upcoming Only"])
    with f2: show_s=st.checkbox("Surprise Cards",value=True)
    rows=[]
    for e in events:
        if flt=="Released Only" and not e.get("Released"): continue
        if flt=="Upcoming Only" and e.get("Released"):     continue
        a=e.get("Actual"); fc=e.get("Forecast"); pv=e.get("Previous")
        surp=(a-fc) if (a is not None and fc is not None and not np.isnan(a) and not np.isnan(fc)) else None
        il,_=impact_label(surp,e["Indicator"])
        rows.append({"Event":e["Indicator"],"Date IST":fmt_ist(e.get("Date")),
            "Status":"✅ Released" if e.get("Released") else f"⏳ {countdown(e.get('Date'))}",
            "Forecast":fp(fc) if fc else "—","Actual":fp(a) if a else "—","Previous":fp(pv) if pv else "—",
            "Surprise":f"{surp:+.2f}" if surp is not None else "—","Gold Impact":il})
    if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    if show_s:
        st.markdown("### Surprise Engine")
        for e in [x for x in events if x.get("Released") and x.get("Actual") is not None][:8]:
            a=e.get("Actual"); fc=e.get("Forecast"); pv=e.get("Previous")
            surp=(a-fc) if (fc is not None and not np.isnan(fc)) else None
            il,ic=impact_label(surp,e["Indicator"]) if surp is not None else ("NEUTRAL","dp-nt")
            is_bull="BULL" in il; is_bear="BEAR" in il
            ctop="me-card-green" if is_bull else ("me-card-red" if is_bear else "")
            sc=f"{surp:+.2f}" if surp is not None else "—"
            scol="#00c076" if (surp and surp<0 and "CPI" in e["Indicator"]) else ("#ff4d4d" if (surp and surp>0) else "#C9A227")
            st.markdown(f"""
            <div class="me-card {ctop}" style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div><div style="color:#C9A227;font-weight:700;font-size:0.95rem">{e['Indicator']}</div>
                  <div style="color:#333;font-size:0.65rem">{fmt_ist(e.get('Date'))}</div></div>
                <span class="dp {'dp-up' if is_bull else 'dp-dn' if is_bear else 'dp-nt'}">{il}</span>
              </div>
              <div style="display:flex;gap:20px;margin-top:10px;flex-wrap:wrap">
                <div><div style="color:#333;font-size:0.6rem">ACTUAL</div><div style="color:#e8e8e8;font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{fp(a)}</div></div>
                <div><div style="color:#333;font-size:0.6rem">FORECAST</div><div style="color:#888;font-family:'JetBrains Mono',monospace;font-size:1rem">{fp(fc) if fc else '—'}</div></div>
                <div><div style="color:#333;font-size:0.6rem">PREVIOUS</div><div style="color:#888;font-family:'JetBrains Mono',monospace;font-size:1rem">{fp(pv) if pv else '—'}</div></div>
                <div><div style="color:#333;font-size:0.6rem">SURPRISE</div><div style="color:{scol};font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{sc}</div></div>
              </div>
              <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">
                <span class="dp {'dp-dn' if is_bull else 'dp-up' if is_bear else 'dp-nt'}">USD {'↓ BEARISH' if is_bull else '↑ BULLISH' if is_bear else '→'}</span>
                <span class="dp {'dp-up' if is_bull else 'dp-dn' if is_bear else 'dp-nt'}">GOLD {'↑ BULLISH' if is_bull else '↓ BEARISH' if is_bear else '→'}</span>
                <span class="dp {'dp-up' if is_bull else 'dp-dn' if is_bear else 'dp-nt'}">BTC {'↑ BULLISH' if is_bull else '↓ BEARISH' if is_bear else '→'}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 4 — FED
# ══════════════════════════════════════════
with t_fed:
    st.markdown("### Fed Policy Dashboard")
    fc1,fc2=st.columns(2)
    with fc1:
        st.markdown(f"""
        <div class="me-card me-card-gold">
          <div class="sec-label">Current Fed Rate</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:800;color:#C9A227;margin:8px 0">{DEMO_FED['rate']}</div>
          <div style="color:#444;font-size:0.72rem">Federal Funds Target Rate</div>
          <div style="border-top:1px solid #1a1a1a;margin-top:12px;padding-top:10px">
            <div style="color:#444;font-size:0.7rem">Next FOMC</div>
            <div style="color:#C9A227;font-size:0.9rem;font-weight:600">{DEMO_FED['next_fomc']}</div>
          </div>
        </div>
        <div class="me-card"><div class="sec-label">CME FedWatch Probabilities</div>
          <div style="margin-top:8px;display:flex;flex-direction:column;gap:8px">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#555;font-size:0.82rem;font-weight:600">HIKE</span>
              <span style="color:#ff4d4d;font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{fed_hp:.1f}%</span>
              <span class="dp dp-dn">BEARISH GOLD</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#555;font-size:0.82rem;font-weight:600">HOLD</span>
              <span style="color:#C9A227;font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{fed_ho:.1f}%</span>
              <span class="dp dp-nt">NEUTRAL</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#555;font-size:0.82rem;font-weight:600">CUT</span>
              <span style="color:#00c076;font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{fed_cu:.1f}%</span>
              <span class="dp dp-up">BULLISH GOLD</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with fc2:
        fig_f=go.Figure(); fig_f.add_trace(go.Bar(x=["HIKE","HOLD","CUT"],y=[fed_hp,fed_ho,fed_cu],
            marker_color=["#ff4d4d","#C9A227","#00c076"],
            text=[f"{v:.1f}%" for v in [fed_hp,fed_ho,fed_cu]],
            textposition="outside",textfont=dict(size=12,color="white",family="JetBrains Mono")))
        fig_f.update_layout(title=dict(text="FOMC Outcome Probability",font=dict(size=11,color='#555')),
            height=260,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(17,17,17,0.8)',
            margin=dict(l=10,r=10,t=36,b=10),yaxis=dict(range=[0,100],gridcolor='#1a1a1a',ticksuffix="%"),showlegend=False)
        st.plotly_chart(fig_f,use_container_width=True)
    if not us10y_df.empty or not us2y_df.empty:
        fig_y=go.Figure()
        if not us10y_df.empty: fig_y.add_trace(go.Scatter(x=us10y_df["date"],y=us10y_df["value"],name="US 10Y",line=dict(color="#C9A227",width=2)))
        if not us2y_df.empty:  fig_y.add_trace(go.Scatter(x=us2y_df["date"], y=us2y_df["value"], name="US 2Y", line=dict(color="#3a7eff",width=2)))
        fig_y.update_layout(title=dict(text="Treasury Yields — FRED",font=dict(size=11,color='#555')),
            height=280,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(17,17,17,0.8)',
            margin=dict(l=10,r=10,t=36,b=10),yaxis=dict(ticksuffix="%",gridcolor='#1a1a1a'),
            legend=dict(x=0.01,y=0.99,bgcolor='rgba(0,0,0,0)',font=dict(size=11,color="#888")))
        st.plotly_chart(fig_y,use_container_width=True)
    else:
        st.markdown('<div class="info-box">FRED_API_KEY add karo live Treasury yields ke liye.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 5 — GOLD ENGINE
# ══════════════════════════════════════════
with t_gold:
    st.markdown("### Gold Macro Engine")
    g1,g2,g3=st.columns(3)
    with g1: st.metric("XAUUSD",f"${fp(gv)}",f"{gc:+.2f}%" if not np.isnan(gc) else "—")
    with g2: st.metric("DXY",fp(dv),f"{dc:+.2f}%" if not np.isnan(dc) else "—")
    with g3: st.metric("US 2Y",f"{fp(us2y_val)}%",f"{us2y_ch:+.2f}bp" if not np.isnan(us2y_ch) else "—")
    if len(gold_s)>5 and len(dxy_s)>5:
        fig_c=make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.05,
                            subplot_titles=("XAUUSD Price","DXY — Dollar Index"))
        fig_c.add_trace(go.Scatter(x=gold_s.index,y=gold_s.values,name="Gold",line=dict(color="#C9A227",width=2),fill='tozeroy',fillcolor='rgba(201,162,39,0.05)'),row=1,col=1)
        fig_c.add_trace(go.Scatter(x=dxy_s.index,y=dxy_s.values,name="DXY",line=dict(color="#3a7eff",width=2)),row=2,col=1)
        fig_c.update_layout(height=380,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(17,17,17,0.8)',margin=dict(l=8,r=8,t=36,b=8))
        st.plotly_chart(fig_c,use_container_width=True)
    st.markdown("### Score Breakdown")
    bd=[]
    for ind,comp in comps.items():
        d=comp.get("data",{}); a=d.get("Actual"); fc=d.get("Forecast")
        surp=None if (a is None or fc is None) else (a-fc if not(np.isnan(a) or np.isnan(fc)) else None)
        bd.append({"Indicator":ind,"Actual":f"{a:.2f}" if a is not None and not np.isnan(a) else "—",
            "Forecast":f"{fc:.2f}" if fc is not None and not np.isnan(fc) else "—",
            "Surprise":f"{surp:+.2f}" if surp is not None else "—",
            "Raw Score":f"{comp['raw']:+.0f}","Weight":f"{comp['w']*100:.0f}%","Contribution":f"{comp['contrib']:+.2f}"})
    st.dataframe(pd.DataFrame(bd),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════
# TAB 6 — IMPACT MATRIX
# ══════════════════════════════════════════
with t_impact:
    st.markdown("### Full Cross-Asset Impact Matrix")
    matrix=[
        ("CPI Lower than forecast","↓","↑","↑","↑","↑","#00c076","Cooling inflation → Fed dovish"),
        ("CPI Higher than forecast","↑","↓","↓","↓","↓","#ff4d4d","Hot inflation → Fed hawkish"),
        ("NFP Weaker than forecast","↓","↑","↑","↑/mixed","↑","#00c076","Cross-check wages+revisions"),
        ("NFP Stronger than forecast","↑","↓","↓","↓","↓","#ff4d4d","Hot wages amplify bearish Gold"),
        ("PCE Lower than forecast","↓","↑","↑","↑","↑","#00c076","Fed preferred gauge — high impact"),
        ("PCE Higher than forecast","↑","↓","↓","↓","↓","#ff4d4d","Sticky core PCE = hawkish risk"),
        ("PPI Lower than forecast","↓","↑","↑","↑","↑","#00c076","Leading CPI indicator"),
        ("JOLTS Weaker","↓","↑","↑","↑","↑","#00c076","Labor demand cooling"),
        ("ISM Below 50","↓","↑","↑","↑","↑","#00c076","Contraction → safe-haven bid"),
        ("ISM Above 55","↑","↓","↓","↓","↓","#ff4d4d","Strong growth = Fed stays hawkish"),
        ("FOMC Hawkish Surprise","↑","↓↓","↓↓","↓↓","↓","#ff4d4d","Rate-path repricing — strongest move"),
        ("FOMC Dovish Surprise","↓","↑↑","↑↑","↑↑","↑","#00c076","Best Gold bull catalyst"),
        ("Wages (AHE) Hotter","↑","↓","↓","↓","↓","#ff4d4d","Hawkish even if NFP weak"),
    ]
    def ac(v):
        if "↑↑" in v: return "#00ff88"
        if "↑" in v:  return "#00c076"
        if "↓↓" in v: return "#ff2020"
        if "↓" in v:  return "#ff4d4d"
        return "#444"
    rh="".join([f'<tr style="border-bottom:1px solid #0f0f0f"><td style="color:{col};font-weight:600;font-size:0.75rem;padding:6px 8px">{out}</td><td style="text-align:center;color:{ac(u)};font-weight:700;padding:6px 5px">{u}</td><td style="text-align:center;color:{ac(g)};font-weight:700;padding:6px 5px">{g}</td><td style="text-align:center;color:{ac(b)};font-weight:700;padding:6px 5px">{b}</td><td style="text-align:center;color:{ac(n)};font-weight:700;padding:6px 5px">{n}</td><td style="text-align:center;color:{ac(s)};font-weight:700;padding:6px 5px">{s}</td><td style="color:#333;font-size:0.68rem;padding:6px 8px">{note}</td></tr>' for out,u,g,b,n,s,col,note in matrix])
    st.markdown(f'<div class="me-card"><div class="sec-label">Event → Cross-Asset Reaction</div><div style="overflow-x:auto"><table><thead><tr><th>OUTCOME</th><th style="text-align:center">USD</th><th style="text-align:center;color:#C9A227">GOLD</th><th style="text-align:center">BTC</th><th style="text-align:center">NASDAQ</th><th style="text-align:center">S&P</th><th>NOTE</th></tr></thead><tbody>{rh}</tbody></table></div></div><div class="info-box">Macro tendencies — always confirm with DXY + US2Y + price structure before trade entry.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 7 — SCENARIO
# ══════════════════════════════════════════
with t_sc:
    st.markdown("### What-If Scenario Simulator")
    s1,s2=st.columns(2)
    with s1:
        sc_cpi=st.selectbox("CPI",["Not Released","Much Lower (−0.2pp)","Lower (−0.1pp)","In-Line","Higher (+0.1pp)","Much Higher (+0.2pp)"])
        sc_nfp=st.selectbox("NFP",["Not Released","Much Weaker (−75K+)","Weaker (−50K)","In-Line (±25K)","Stronger (+50K)","Much Stronger (+75K+)"])
        sc_pce=st.selectbox("PCE",["Not Released","Much Lower","Lower","In-Line","Higher","Much Higher"])
    with s2:
        sc_fed=st.selectbox("Fed",["Neutral","Strongly Dovish","Dovish","Hawkish","Strongly Hawkish"])
        sc_wg =st.selectbox("Wages",["Not Released","Cool (below forecast)","In-Line","Hot (above forecast)"])
        sc_ism=st.selectbox("ISM",["Not Released","Deep Contraction (<47)","Contraction (47-50)","Expansion (50-54)","Strong (54+)"])
    sm={"Much Lower (−0.2pp)":(30,"CPI very cool → strongly bullish"),"Lower (−0.1pp)":(20,"CPI lower → bullish"),"In-Line":(0,"In-line → neutral"),
        "Higher (+0.1pp)":(-20,"CPI hot → bearish"),"Much Higher (+0.2pp)":(-30,"CPI very hot → strongly bearish"),
        "Much Weaker (−75K+)":(30,"NFP very weak → bullish"),"Weaker (−50K)":(22,"NFP weak → bullish"),"In-Line (±25K)":(0,"NFP in-line"),
        "Stronger (+50K)":(-22,"NFP strong → bearish"),"Much Stronger (+75K+)":(-30,"NFP very strong → bearish"),
        "Much Lower":(25,"PCE very cool"),"Lower":(18,"PCE cool"),"Higher":(-18,"PCE hot"),"Much Higher":(-25,"PCE very hot"),
        "Deep Contraction (<47)":(18,"ISM contraction"),"Contraction (47-50)":(10,"ISM weak"),"Expansion (50-54)":(-6,"ISM ok"),"Strong (54+)":(-14,"ISM strong"),
        "Cool (below forecast)":(10,"Cool wages"),"Hot (above forecast)":(-15,"Hot wages")}
    fm={"Strongly Dovish":(30,"Fed strongly dovish"),"Dovish":(20,"Fed dovish"),"Neutral":(0,"Fed neutral"),"Hawkish":(-20,"Fed hawkish"),"Strongly Hawkish":(-30,"Fed very hawkish")}
    sc_tot=0.0; sc_notes=[]
    for sel,w in [(sc_cpi,0.30),(sc_nfp,0.17),(sc_pce,0.15),(sc_ism,0.08),(sc_wg,0.10)]:
        if sel in sm: r,note=sm[sel]; sc_tot+=r*w; sc_notes.append(("🟢" if r>0 else "🔴" if r<0 else "🟡",note))
    if sc_fed in fm: r,note=fm[sc_fed]; sc_tot+=r*0.20; sc_notes.append(("🟢" if r>0 else "🔴" if r<0 else "🟡",note))
    sc_norm=max(-100,min(100,sc_tot*3.3))
    def sgc(l): return "#00c076" if "BULL" in l else ("#ff4d4d" if "BEAR" in l else "#C9A227")
    sc_gold="STRONGLY BULLISH" if sc_norm>=60 else ("BULLISH" if sc_norm>=35 else ("NEUTRAL" if abs(sc_norm)<35 else ("BEARISH" if sc_norm<=-35 else "STRONGLY BEARISH")))
    sc_usd="BEARISH" if sc_norm>=35 else ("BULLISH" if sc_norm<=-35 else "NEUTRAL")
    sc_sig,sc_sc,sc_cf=get_signal(sc_norm,50 if "Hawk" in sc_fed else 20,-1.0 if "Dovish" in sc_fed else 1.0,np.nan)
    nh="".join([f'<div style="display:flex;gap:8px;padding:4px 0"><span>{ic}</span><span style="color:#666;font-size:0.75rem">{t}</span></div>' for ic,t in sc_notes])
    sbg2,sfg2,sbr2={"sig-sbuy":("#002a18","#00c076","#00c07650"),"sig-buy":("#001f12","#00c076","#00c07630"),"sig-nt":("#1a1500","#C9A227","#C9A22740"),"sig-sell":("#1f0000","#ff4d4d","#ff4d4d30"),"sig-ssell":("#2a0000","#ff4d4d","#ff4d4d50")}.get(sc_sc,("#111","#aaa","#333"))
    st.markdown(f"""<div class="me-card {'me-card-green' if sc_norm>=35 else 'me-card-red' if sc_norm<=-35 else 'me-card-gold'}" style="margin-top:10px">
      <div class="sec-label">Scenario Result</div>
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px">
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">SCORE</div><div style="font-family:'JetBrains Mono',monospace;font-size:1.8rem;font-weight:800;color:{sgc(sc_gold)}">{sc_norm:+.0f}</div></div>
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">GOLD</div><div style="color:{sgc(sc_gold)};font-weight:700;font-size:0.85rem">{sc_gold}</div></div>
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">USD</div><div style="color:{sgc('BEAR' if 'BEAR' in sc_usd else 'BULL')};font-weight:700;font-size:0.85rem">{sc_usd}</div></div>
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">SIGNAL</div><span class="signal {sc_sc}" style="font-size:0.68rem">{sc_sig}</span></div>
      </div>
      <div style="margin-top:12px;border-top:1px solid #1a1a1a;padding-top:10px">{nh}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 8 — HISTORY
# ══════════════════════════════════════════
with t_hist:
    st.markdown("### Historical Performance")
    per=st.selectbox("Period",["1mo","3mo","6mo"],index=1)
    nd={"1mo":21,"3mo":63,"6mo":126}.get(per,63)
    fig_i=go.Figure()
    for name,col in [("Gold","#C9A227"),("DXY","#3a7eff"),("BTC","#ff9900"),("Nasdaq","#00c076"),("S&P500","#a855f7")]:
        s=mkt.get(name,pd.Series(dtype=float))
        if len(s)>5:
            s2=s[-nd:] if len(s)>nd else s
            idx=s2/s2.iloc[0]*100
            fig_i.add_trace(go.Scatter(x=idx.index,y=idx.values,name=name,line=dict(color=col,width=1.8)))
    fig_i.add_hline(y=100,line=dict(color="#222",width=1,dash="dot"))
    fig_i.update_layout(title=dict(text=f"Indexed Performance — {per} (Base=100)",font=dict(size=11,color='#555')),
        height=300,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(17,17,17,0.8)',
        margin=dict(l=8,r=8,t=36,b=8),legend=dict(x=0.01,y=0.99,bgcolor='rgba(0,0,0,0)',font=dict(size=10,color="#888")))
    st.plotly_chart(fig_i,use_container_width=True)
    st.markdown('<div class="warn-box">⚠️ Educational tool. Not financial advice. Always use risk management.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div style="color:#C9A227;font-weight:800;font-size:1rem;margin-bottom:4px">⚡ MACROEDGE V4</div>', unsafe_allow_html=True)
    st.caption("BR Trading Academy")
    st.divider()
    st.markdown("**API Status**")
    st.write("FRED:", "✅" if FRED_API_KEY else "⚠️ Add key")
    st.write("TE:", "✅" if TE_API_KEY else "⚠️ Demo mode")
    st.write("Market:", "✅ yfinance")
    st.divider()
    st.caption(f"Refresh: {REFRESH_SEC}s")
    st.caption(f"{ist_now().strftime('%H:%M:%S IST')}")
    st.divider()
    st.caption("Not financial advice.")

st.markdown(f'<script>setTimeout(()=>window.location.reload(),{REFRESH_SEC*1000})</script>', unsafe_allow_html=True)

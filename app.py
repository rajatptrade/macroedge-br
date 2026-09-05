"""
MacroEdge — US Macro Trading Terminal
BR Trading Academy Edition — V3
Theme: brtradingacademy.com style
"""

import os, math, time, json
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

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MacroEdge — BR Trading Academy",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
# BR TRADING ACADEMY THEME CSS
# Gold: #C9A227  |  Black: #0a0a0a  |  Dark card: #111111
# Green signal: #00c076  |  Red signal: #ff4d4d
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  background-color: #0a0a0a !important;
}
.main { background: #0a0a0a !important; }
.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}
section[data-testid="stSidebar"] {
  background: #0f0f0f !important;
  border-right: 1px solid #1a1a1a !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Top Nav Bar — BR Style ── */
.br-nav {
  background: #0f0f0f;
  border-bottom: 1px solid #1e1e1e;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
  position: sticky;
  top: 0;
  z-index: 999;
}
.br-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}
.br-logo-box {
  width: 32px; height: 32px;
  background: #C9A227;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 0.85rem; color: #000;
  font-family: 'Playfair Display', serif;
}
.br-logo-text {
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: #f0f0f0;
  letter-spacing: 0.01em;
}
.br-logo-sub {
  font-size: 0.65rem;
  color: #C9A227;
  letter-spacing: 0.08em;
  font-weight: 500;
  text-transform: uppercase;
}
.br-nav-links {
  display: flex;
  gap: 4px;
  align-items: center;
}
.br-nav-link {
  color: #888;
  font-size: 0.72rem;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  transition: color 0.15s;
}
.br-nav-link:hover { color: #C9A227; }
.br-nav-link.active {
  color: #C9A227;
  background: rgba(201,162,39,0.08);
}
.br-nav-badge {
  background: #C9A227;
  color: #000;
  font-size: 0.55rem;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 3px;
  margin-left: 3px;
  letter-spacing: 0.05em;
}
.br-nav-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.br-live-dot {
  width: 6px; height: 6px;
  background: #00c076;
  border-radius: 50%;
  animation: pulse-green 2s infinite;
  display: inline-block;
}
@keyframes pulse-green { 0%,100%{opacity:1} 50%{opacity:0.3} }
.br-time { color: #555; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; }

/* ── Live Ticker Strip ── */
.ticker-strip {
  background: #080808;
  border-bottom: 1px solid #161616;
  padding: 6px 20px;
  display: flex;
  gap: 0;
  overflow-x: auto;
  scrollbar-width: none;
  white-space: nowrap;
  align-items: center;
}
.ticker-strip::-webkit-scrollbar { display: none; }
.ticker-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 14px 3px 0;
  border-right: 1px solid #1a1a1a;
  margin-right: 14px;
  flex-shrink: 0;
}
.ticker-item:last-child { border-right: none; }
.t-name {
  font-size: 0.68rem;
  font-weight: 700;
  color: #C9A227;
  letter-spacing: 0.06em;
  font-family: 'Inter', sans-serif;
}
.t-price {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 500;
  color: #e8e8e8;
}
.t-up   { font-size: 0.68rem; color: #00c076; font-family: 'JetBrains Mono', monospace; }
.t-down { font-size: 0.68rem; color: #ff4d4d; font-family: 'JetBrains Mono', monospace; }
.t-neut { font-size: 0.68rem; color: #555; font-family: 'JetBrains Mono', monospace; }
.t-arrow-up   { color: #00c076; font-size: 0.6rem; }
.t-arrow-down { color: #ff4d4d; font-size: 0.6rem; }

/* ── Main Content Wrapper ── */
.me-content { padding: 16px 20px 40px 20px; }

/* ── Cards ── */
.me-card {
  background: #111111;
  border: 1px solid #1e1e1e;
  border-radius: 10px;
  padding: 16px 18px;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}
.me-card-gold { border-top: 2px solid #C9A227; }
.me-card-green { border-top: 2px solid #00c076; }
.me-card-red   { border-top: 2px solid #ff4d4d; }
.me-card-blue  { border-top: 2px solid #3a7eff; }

/* ── Section label ── */
.sec-label {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #333;
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid #1a1a1a;
}

/* ── Score display ── */
.score-number {
  font-family: 'JetBrains Mono', monospace;
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1;
}
.score-bull { color: #00c076; }
.score-bear { color: #ff4d4d; }
.score-neut { color: #C9A227; }

/* ── Signal pills ── */
.signal {
  display: inline-block;
  padding: 5px 16px;
  border-radius: 4px;
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-family: 'Inter', sans-serif;
}
.sig-sbuy  { background: #002a18; color: #00c076; border: 1px solid #00c07640; }
.sig-buy   { background: #001f12; color: #00c076; border: 1px solid #00c07625; }
.sig-nt    { background: #1a1500; color: #C9A227; border: 1px solid #C9A22730; }
.sig-sell  { background: #1f0000; color: #ff4d4d; border: 1px solid #ff4d4d25; }
.sig-ssell { background: #2a0000; color: #ff4d4d; border: 1px solid #ff4d4d40; }

/* ── Data pills ── */
.dp { display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:600;font-family:'JetBrains Mono',monospace; }
.dp-up   { background:#001f12;color:#00c076; }
.dp-dn   { background:#1f0000;color:#ff4d4d; }
.dp-nt   { background:#141414;color:#555; }
.dp-gold { background:#1a1200;color:#C9A227; }

/* ── Info boxes ── */
.warn-box  { background:#1a1200;border-left:3px solid #C9A227;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#9a7a20;margin:8px 0; }
.info-box  { background:#001020;border-left:3px solid #3a7eff;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#4a80cc;margin:8px 0; }
.bull-box  { background:#001810;border-left:3px solid #00c076;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#007040;margin:8px 0; }
.bear-box  { background:#180000;border-left:3px solid #ff4d4d;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#882020;margin:8px 0; }

/* ── Metrics override ── */
[data-testid="metric-container"] {
  background: #111111 !important;
  border: 1px solid #1e1e1e !important;
  border-radius: 8px !important;
  padding: 14px !important;
}
[data-testid="stMetricValue"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.3rem !important;
  color: #e8e8e8 !important;
}
[data-testid="stMetricDelta"] { font-size: 0.78rem !important; }
[data-testid="stMetricLabel"] {
  font-size: 0.62rem !important;
  color: #444 !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: #0a0a0a !important;
  border-bottom: 1px solid #1a1a1a !important;
  padding: 0 20px !important;
  gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: #444 !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  padding: 8px 14px !important;
  border-radius: 4px 4px 0 0 !important;
}
.stTabs [aria-selected="true"] {
  background: #111111 !important;
  color: #C9A227 !important;
  border-top: 2px solid #C9A227 !important;
}

/* ── Dataframe ── */
.stDataFrame { background: #0f0f0f !important; border: 1px solid #1a1a1a !important; border-radius: 8px !important; }
thead th { background: #111111 !important; color: #444 !important; font-size: 0.68rem !important; letter-spacing: 0.08em !important; }
tbody td { color: #c0c0c0 !important; font-size: 0.8rem !important; }

/* ── Select / inputs ── */
.stSelectbox div[data-baseweb="select"] { background: #111111 !important; border-color: #1e1e1e !important; }
.stSelectbox [data-baseweb="select"] * { color: #c0c0c0 !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] { background: #C9A227 !important; }

/* ── Table ── */
table { border-collapse: collapse; width: 100%; }
th { color: #444; font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 8px 10px; border-bottom: 1px solid #1a1a1a; text-align: left; }
td { color: #c0c0c0; font-size: 0.78rem; padding: 7px 10px; border-bottom: 1px solid #111; }
tr:hover td { background: #0f0f0f; }

/* ── Divider ── */
hr { border-color: #1a1a1a !important; margin: 12px 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080808; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 2px; }

/* ── Mobile ── */
@media (max-width: 768px) {
  .br-nav-links { display: none; }
  .score-number { font-size: 2.2rem; }
  .me-content { padding: 10px 12px; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
TE_API_KEY   = os.getenv("TRADINGECONOMICS_API_KEY", "")
FRED_API_KEY = os.getenv("FRED_API_KEY", "")
BLS_API_KEY  = os.getenv("BLS_API_KEY", "")
DEMO_MODE    = os.getenv("DEMO_MODE", "true").lower() == "true"
REFRESH_SEC  = int(os.getenv("REFRESH_SECONDS", "90"))
IST          = timedelta(hours=5, minutes=30)

WEIGHTS = {
    "CPI m/m": 0.12, "Core CPI m/m": 0.18,
    "PPI m/m": 0.05, "Core PPI m/m": 0.05,
    "PCE m/m": 0.06, "Core PCE m/m": 0.09,
    "NFP": 0.12, "Unemployment Rate": 0.05,
    "Average Hourly Earnings": 0.05,
    "JOLTS": 0.05, "Initial Claims": 0.05,
    "ISM Manufacturing": 0.04, "ISM Services": 0.04,
    "Fed": 0.10,
}

EVENT_ALIASES = {
    "CPI m/m":               ["CPI MoM","Inflation Rate MoM","Consumer Price Index MoM"],
    "Core CPI m/m":          ["Core CPI MoM","Core Inflation Rate MoM"],
    "PPI m/m":               ["PPI MoM","Producer Price Inflation MoM"],
    "Core PPI m/m":          ["Core PPI MoM","Core Producer Price Inflation MoM"],
    "PCE m/m":               ["PCE Price Index MoM","PCE MoM"],
    "Core PCE m/m":          ["Core PCE Price Index MoM","Core PCE MoM"],
    "NFP":                   ["Non Farm Payrolls","Nonfarm Payrolls"],
    "Unemployment Rate":     ["Unemployment Rate"],
    "Average Hourly Earnings": ["Average Hourly Earnings MoM","Average Hourly Earnings"],
    "JOLTS":                 ["JOLTS Job Openings","Job Openings"],
    "Initial Claims":        ["Initial Jobless Claims","Initial Claims"],
    "ISM Manufacturing":     ["ISM Manufacturing PMI","ISM Manufacturing"],
    "ISM Services":          ["ISM Services PMI","ISM Services"],
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
    {"Indicator":"NFP","Actual":None,"Forecast":160,"Previous":138,"Date":"2026-10-03","Released":False},
]
DEMO_FED = {"hike": 12.0, "hold": 68.0, "cut": 20.0, "rate": "3.50%–3.75%", "next_fomc": "Sep 17, 2026"}

# ─────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────
def _parse(v):
    if v is None: return None
    try: return float(str(v).replace("%","").replace("K","").strip())
    except: return None

@st.cache_data(ttl=60)
def fetch_market():
    syms = {"Gold":"GC=F","DXY":"DX-Y.NYB","BTC":"BTC-USD",
            "Nasdaq":"^NDX","S&P500":"^GSPC","Dow":"^DJI","US10Y":"^TNX"}
    out = {}
    for k, s in syms.items():
        try:
            raw = yf.download(s, period="6mo", interval="1d", progress=False, auto_adjust=False)
            cl = raw["Close"].iloc[:,0] if isinstance(raw.columns, pd.MultiIndex) else raw["Close"]
            out[k] = cl.dropna()
        except: out[k] = pd.Series(dtype=float)
    return out

@st.cache_data(ttl=300)
def fetch_fred(sid, limit=60):
    if not FRED_API_KEY: return pd.DataFrame()
    try:
        r = requests.get("https://api.stlouisfed.org/fred/series/observations",
            params={"series_id":sid,"api_key":FRED_API_KEY,"file_type":"json",
                    "sort_order":"desc","limit":limit}, timeout=15)
        r.raise_for_status()
        df = pd.DataFrame(r.json().get("observations",[]))
        if df.empty: return df
        df["date"]  = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        return df.dropna(subset=["value"]).sort_values("date")
    except: return pd.DataFrame()

@st.cache_data(ttl=120)
def fetch_te():
    if not TE_API_KEY: return pd.DataFrame()
    try:
        r = requests.get("https://api.tradingeconomics.com/calendar/country/united%20states",
            params={"c":TE_API_KEY,"f":"json","importance":2}, timeout=15)
        r.raise_for_status()
        df = pd.DataFrame(r.json())
        if df.empty: return df
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
        return df.sort_values("Date")
    except: return pd.DataFrame()

def get_events():
    if DEMO_MODE or not TE_API_KEY:
        return DEMO_EVENTS
    te = fetch_te()
    if te.empty: return DEMO_EVENTS
    te["Event"] = te["Event"].astype(str)
    now = pd.Timestamp.now(tz="UTC")
    win = te[(te["Date"] >= now - pd.Timedelta(days=60)) & (te["Date"] <= now + pd.Timedelta(days=90))].copy()
    evs = []
    for name, aliases in EVENT_ALIASES.items():
        pat = "|".join([x.replace(" ","\\s+") for x in aliases])
        hit = win[win["Event"].str.contains(pat, case=False, regex=True, na=False)]
        if hit.empty: continue
        for _, row in hit.sort_values("Date").iterrows():
            a = _parse(row.get("Actual"))
            evs.append({"Indicator":name,"Actual":a,"Forecast":_parse(row.get("Forecast")),
                        "Previous":_parse(row.get("Previous")),"Date":row.get("Date"),
                        "Released": a is not None and not np.isnan(a)})
    return evs if evs else DEMO_EVENTS

def safe_last(s): return float(s.iloc[-1]) if s is not None and len(s) else np.nan
def safe_pct(s, n=5):
    if s is None or len(s)<=n: return np.nan
    return float((s.iloc[-1]/s.iloc[-1-n]-1)*100)
def safe_ch(s, n=1):
    if s is None or len(s)<=n: return np.nan
    return float(s.iloc[-1]-s.iloc[-1-n])
def fp(v,d=2): return f"{v:,.{d}f}" if v is not None and not np.isnan(v) else "—"
def ist_now(): return datetime.now(timezone.utc) + IST
def fmt_ist(dt):
    if dt is None: return "—"
    try:
        if hasattr(dt,'tzinfo') and dt.tzinfo:
            ist = dt.astimezone(timezone.utc).replace(tzinfo=timezone.utc) + IST
        else: ist = dt + IST
        return ist.strftime("%d %b %Y  %H:%M IST")
    except: return str(dt)
def countdown(dt):
    if dt is None: return "—"
    try:
        now = datetime.now(timezone.utc)
        diff = (dt - now) if (hasattr(dt,'tzinfo') and dt.tzinfo) else (dt - now.replace(tzinfo=None))
        if diff.total_seconds() < 0: return "Released"
        d=diff.days; h=diff.seconds//3600; m=(diff.seconds%3600)//60
        return f"{d}d {h}h {m}m"
    except: return "—"

# ─────────────────────────────────────────
# SCORING ENGINE
# ─────────────────────────────────────────
def band_score(ev, actual, forecast):
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

def compute_score(events, fed_hp, mkt):
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
    return norm, comps

def get_signal(score, fed_hp, dxy_ch, us2y_ch):
    bc = (not np.isnan(dxy_ch) and dxy_ch<-0.3) or (not np.isnan(us2y_ch) and us2y_ch<-3)
    brc= (not np.isnan(dxy_ch) and dxy_ch>0.3) or (not np.isnan(us2y_ch) and us2y_ch>3)
    fh = fed_hp if not np.isnan(fed_hp) else 50
    if score>=60 and fh<=40 and bc:   return "STRONG BUY",  "sig-sbuy",  "HIGH"
    if score>=35 and fh<=55:          return "BUY",          "sig-buy",   "MEDIUM"
    if score<=-60 and fh>=60 and brc: return "STRONG SELL", "sig-ssell", "HIGH"
    if score<=-35 and fh>=45:         return "SELL",         "sig-sell",  "MEDIUM"
    return "NO TRADE","sig-nt","LOW"

def impact_label(surp, ev):
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
# LOAD DATA
# ─────────────────────────────────────────
mkt    = fetch_market()
events = get_events()
us2y_df= fetch_fred("DGS2", 30)
us10y_df=fetch_fred("DGS10",90)

us2y_val = float(us2y_df.iloc[-1]["value"]) if not us2y_df.empty else np.nan
us2y_ch  = float(us2y_df.iloc[-1]["value"]-us2y_df.iloc[-2]["value"]) if len(us2y_df)>=2 else np.nan
fed_hp   = DEMO_FED["hike"] if (DEMO_MODE or not TE_API_KEY) else np.nan
fed_ho   = DEMO_FED["hold"] if (DEMO_MODE or not TE_API_KEY) else np.nan
fed_cu   = DEMO_FED["cut"]  if (DEMO_MODE or not TE_API_KEY) else np.nan

gold_s = mkt.get("Gold",    pd.Series(dtype=float))
dxy_s  = mkt.get("DXY",     pd.Series(dtype=float))
btc_s  = mkt.get("BTC",     pd.Series(dtype=float))
ndx_s  = mkt.get("Nasdaq",  pd.Series(dtype=float))
spx_s  = mkt.get("S&P500",  pd.Series(dtype=float))
dow_s  = mkt.get("Dow",     pd.Series(dtype=float))
tnx_s  = mkt.get("US10Y",   pd.Series(dtype=float))

gv=safe_last(gold_s); dv=safe_last(dxy_s); bv=safe_last(btc_s)
nv=safe_last(ndx_s);  sv=safe_last(spx_s); dov=safe_last(dow_s); tv=safe_last(tnx_s)

gc=safe_pct(gold_s); dc=safe_pct(dxy_s); bc=safe_pct(btc_s)
nc=safe_pct(ndx_s);  sc=safe_pct(spx_s); doc=safe_pct(dow_s)
tc=safe_ch(tnx_s)*100

macro_score, comps = compute_score(events, fed_hp, mkt)
signal, sig_cls, conf = get_signal(macro_score, fed_hp, dc, us2y_ch)

upcoming = sorted([e for e in events if not e.get("Released") and e.get("Date")],
                  key=lambda x: str(x.get("Date","")))
next_ev = upcoming[0] if upcoming else None

# ─────────────────────────────────────────
# BR NAV BAR
# ─────────────────────────────────────────
demo_badge = '<span style="background:#C9A227;color:#000;font-size:0.55rem;font-weight:700;padding:2px 7px;border-radius:3px;letter-spacing:0.06em;margin-left:8px;">DEMO</span>' if (DEMO_MODE or not TE_API_KEY) else '<span style="display:inline-flex;align-items:center;gap:4px;color:#00c076;font-size:0.68rem;font-weight:600;margin-left:8px;"><span class="br-live-dot"></span>LIVE</span>'

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
    <a class="br-nav-link" href="#">Calendar</a>
    <a class="br-nav-link" href="#">Fed <span class="br-nav-badge">LIVE</span></a>
    <a class="br-nav-link" href="#">Gold Engine</a>
    <a class="br-nav-link" href="#">Impact</a>
    <a class="br-nav-link" href="#">Scenario</a>
    <a class="br-nav-link" href="#">History</a>
  </div>
  <div class="br-nav-right">
    <div class="br-time">{ist_now().strftime('%a, %d %b  %H:%M IST')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# LIVE TICKER STRIP
# ─────────────────────────────────────────
def tick(name, price, chg, prefix="", suffix=""):
    if np.isnan(price):
        return f'<div class="ticker-item"><span class="t-name">{name}</span><span class="t-price" style="color:#333">—</span></div>'
    arrow = '<span class="t-arrow-up">▲</span>' if chg>0 else '<span class="t-arrow-down">▼</span>'
    chg_cls = "t-up" if chg>0 else "t-down" if chg<0 else "t-neut"
    chg_str = f"{chg:+.2f}%" if not np.isnan(chg) else "—"
    return f'<div class="ticker-item">{arrow}<span class="t-name">{name}</span><span class="t-price">{prefix}{fp(price)}{suffix}</span><span class="{chg_cls}">{chg_str}</span></div>'

tnx_chpct = float((tnx_s.iloc[-1]/tnx_s.iloc[-2]-1)*100) if len(tnx_s)>=2 else np.nan
us2y_chpct= float(us2y_ch/us2y_val*100) if (not np.isnan(us2y_val) and not np.isnan(us2y_ch) and us2y_val!=0) else np.nan

ticker_html = "".join([
    tick("XAUUSD", gv,  gc, prefix="$"),
    tick("DXY",    dv,  dc),
    tick("US 2Y",  us2y_val, us2y_chpct, suffix="%"),
    tick("US 10Y", tv,  tnx_chpct, suffix="%"),
    tick("BTC",    bv,  bc, prefix="$"),
    tick("NASDAQ", nv,  nc),
    tick("S&P500", sv,  sc),
    tick("DOW",    dov, doc),
])
st.markdown(f'<div class="ticker-strip">{ticker_html}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────
st.markdown('<div class="me-content">', unsafe_allow_html=True)

# ─ TABS ─
t1,t2,t3,t4,t5,t6,t7 = st.tabs([
    "📊 OVERVIEW","📅 CALENDAR","🏛 FED","🏆 GOLD ENGINE","⚡ IMPACT","🔮 SCENARIO","📈 HISTORY"
])

# ══════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════
with t1:
    c1,c2,c3,c4 = st.columns([1.2,1,1,1])

    # Gold Score
    with c1:
        sc_cls = "score-bull" if macro_score>=35 else ("score-bear" if macro_score<=-35 else "score-neut")
        card_top = "me-card-green" if macro_score>=35 else ("me-card-red" if macro_score<=-35 else "me-card-gold")
        st.markdown(f"""
        <div class="me-card {card_top}">
          <div class="sec-label">Gold Macro Score</div>
          <div style="text-align:center;padding:8px 0 4px">
            <div class="score-number {sc_cls}">{macro_score:+.0f}</div>
            <div style="color:#333;font-size:0.62rem;margin-top:2px;letter-spacing:0.06em">
              −100 ← BEARISH &nbsp;|&nbsp; BULLISH → +100
            </div>
          </div>
          <div style="text-align:center;margin-top:10px">
            <span class="signal {sig_cls}">{signal}</span>
            <div style="color:#333;font-size:0.62rem;margin-top:5px">Confidence: {conf}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Next Event
    with c2:
        if next_ev:
            ne_d = next_ev.get("Date")
            fc_v = next_ev.get("Forecast")
            st.markdown(f"""
            <div class="me-card me-card-gold">
              <div class="sec-label">Next Major Release</div>
              <div style="color:#C9A227;font-weight:700;font-size:1rem;margin-top:4px">{next_ev['Indicator']}</div>
              <div style="color:#444;font-size:0.72rem;margin-top:2px">{fmt_ist(ne_d)}</div>
              <div style="font-family:'JetBrains Mono',monospace;color:#e8e8e8;font-size:1.4rem;font-weight:700;margin-top:8px">{countdown(ne_d)}</div>
              <div style="color:#333;font-size:0.65rem;margin-top:4px">Forecast: {fp(fc_v) if fc_v else '—'}</div>
            </div>
            """, unsafe_allow_html=True)

    # Fed
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

    # Confirmation
    with c4:
        dxy_dir = "↓ BEARISH" if (not np.isnan(dc) and dc<-0.3) else ("↑ BULLISH" if (not np.isnan(dc) and dc>0.3) else "→ NEUTRAL")
        d_col = "#00c076" if "BEARISH" in dxy_dir else ("#ff4d4d" if "BULLISH" in dxy_dir else "#C9A227")
        u2y_dir = "↓ FALLING" if (not np.isnan(us2y_ch) and us2y_ch<-3) else ("↑ RISING" if (not np.isnan(us2y_ch) and us2y_ch>3) else "→ STABLE")
        u_col = "#00c076" if "FALL" in u2y_dir else ("#ff4d4d" if "RISING" in u2y_dir else "#C9A227")
        bull_ok = "BEARISH" in dxy_dir or "FALL" in u2y_dir
        conf_lbl = "YES ✓" if bull_ok else "NO ✗"
        conf_col = "#00c076" if bull_ok else "#ff4d4d"
        st.markdown(f"""
        <div class="me-card">
          <div class="sec-label">Market Confirmation</div>
          <div style="margin-top:6px;display:flex;flex-direction:column;gap:6px">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#444;font-size:0.72rem">DXY 5D</span>
              <span style="color:{d_col};font-family:'JetBrains Mono',monospace;font-size:0.75rem">{dxy_dir}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#444;font-size:0.72rem">US 2Y</span>
              <span style="color:{u_col};font-family:'JetBrains Mono',monospace;font-size:0.75rem">{u2y_dir}</span>
            </div>
            <div style="border-top:1px solid #1a1a1a;margin-top:4px;padding-top:8px;display:flex;justify-content:space-between;align-items:center">
              <span style="color:#555;font-size:0.75rem;font-weight:600">GOLD CONFIRM</span>
              <span style="color:{conf_col};font-weight:700;font-size:0.9rem">{conf_lbl}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Why Gold explanation
    reasons=[]
    for ind,comp in comps.items():
        raw=comp["raw"]
        d=comp.get("data",{})
        a=d.get("Actual"); fc=d.get("Forecast")
        if ind=="Fed":
            if raw>0:  reasons.append(("🟢",f"Fed cut probability HIGH ({fed_cu:.0f}%) — dovish regime supports Gold"))
            elif raw<0:reasons.append(("🔴",f"Fed hike probability HIGH ({fed_hp:.0f}%) — hawkish headwind on Gold"))
        elif a is not None and fc is not None and not np.isnan(a) and not np.isnan(fc):
            surp=a-fc
            if raw>5:  reasons.append(("🟢",f"{ind}: Actual {a:.2f} vs Forecast {fc:.2f} → Surprise {surp:+.2f} → Gold BULLISH"))
            elif raw<-5:reasons.append(("🔴",f"{ind}: Actual {a:.2f} vs Forecast {fc:.2f} → Surprise {surp:+.2f} → Gold BEARISH"))

    if not np.isnan(dc):
        if dc<-0.5:  reasons.append(("🟢",f"DXY weakening 5D: {dc:+.2f}% — dollar selling confirms Gold bid"))
        elif dc>0.5: reasons.append(("🔴",f"DXY strengthening 5D: {dc:+.2f}% — dollar strength is headwind for Gold"))
    if not reasons:
        reasons=[("🟡","Connect TRADINGECONOMICS_API_KEY for live data. Demo mode active.")]

    bias_word = "BULLISH" if macro_score>=35 else ("BEARISH" if macro_score<=-35 else "NEUTRAL")
    bias_col  = "#00c076" if macro_score>=35 else ("#ff4d4d" if macro_score<=-35 else "#C9A227")
    row_html  = "".join([f'<div style="display:flex;gap:8px;align-items:flex-start;padding:5px 0;border-bottom:1px solid #0f0f0f"><span style="font-size:0.85rem">{ic}</span><span style="color:#888;font-size:0.78rem;line-height:1.5">{txt}</span></div>' for ic,txt in reasons])

    st.markdown(f"""
    <div class="me-card">
      <div class="sec-label">Why Gold is <span style="color:{bias_col}">{bias_word}</span> — Macro Interpretation</div>
      {row_html}
    </div>
    """, unsafe_allow_html=True)

    # Charts
    col_ch1, col_ch2 = st.columns(2)
    plot_cfg = dict(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(17,17,17,0.8)", margin=dict(l=8,r=8,t=32,b=8),
                    showlegend=False, height=220,
                    xaxis=dict(gridcolor="#1a1a1a",zeroline=False,showgrid=True),
                    yaxis=dict(gridcolor="#1a1a1a",zeroline=False,showgrid=True))

    with col_ch1:
        if len(gold_s)>5:
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=gold_s.index,y=gold_s.values,
                fill='tozeroy',fillcolor='rgba(201,162,39,0.07)',
                line=dict(color='#C9A227',width=2),name='XAUUSD'))
            fig.update_layout(title=dict(text="XAUUSD — Gold",font=dict(size=11,color='#555')),**plot_cfg)
            st.plotly_chart(fig,use_container_width=True)

    with col_ch2:
        if len(dxy_s)>5:
            dc_col='#ff4d4d' if dc>0 else '#00c076'
            fig2=go.Figure()
            fig2.add_trace(go.Scatter(x=dxy_s.index,y=dxy_s.values,
                line=dict(color=dc_col,width=2),name='DXY'))
            fig2.update_layout(title=dict(text="DXY — US Dollar Index",font=dict(size=11,color='#555')),**plot_cfg)
            st.plotly_chart(fig2,use_container_width=True)

    # Gauge
    gc2='#00c076' if macro_score>=35 else ('#ff4d4d' if macro_score<=-35 else '#C9A227')
    fig_g=go.Figure(go.Indicator(
        mode="gauge+number",value=macro_score,
        number={"suffix":" / 100","font":{"size":24,"color":"#e8e8e8","family":"JetBrains Mono"}},
        title={"text":"GOLD MACRO SCORE","font":{"size":11,"color":"#444"}},
        gauge={"axis":{"range":[-100,100],"tickwidth":0.5,"tickcolor":"#1a1a1a",
                       "tickfont":{"size":9,"color":"#333"}},
               "bar":{"color":gc2,"thickness":0.22},
               "bgcolor":"rgba(0,0,0,0)","borderwidth":0,
               "steps":[{"range":[-100,-60],"color":"rgba(80,10,10,0.5)"},
                        {"range":[-60,-35],"color":"rgba(60,15,15,0.4)"},
                        {"range":[-35,35],"color":"rgba(25,20,5,0.3)"},
                        {"range":[35,60],"color":"rgba(5,40,25,0.4)"},
                        {"range":[60,100],"color":"rgba(5,50,30,0.5)"}],
               "threshold":{"line":{"color":"white","width":2},"thickness":0.75,"value":macro_score}}
    ))
    fig_g.update_layout(height=240,paper_bgcolor="rgba(0,0,0,0)",
                        font={"color":"#555"},margin=dict(l=30,r=30,t=36,b=10))
    st.plotly_chart(fig_g,use_container_width=True)

    # Score breakdown
    st.markdown("### Score Breakdown")
    bd_rows=[]
    for ind,comp in comps.items():
        d=comp.get("data",{}); a=d.get("Actual"); fc=d.get("Forecast")
        surp=None if (a is None or fc is None) else (a-fc if not(np.isnan(a) or np.isnan(fc)) else None)
        bd_rows.append({"Indicator":ind,
            "Actual":f"{a:.2f}" if a is not None and not np.isnan(a) else "—",
            "Forecast":f"{fc:.2f}" if fc is not None and not np.isnan(fc) else "—",
            "Surprise":f"{surp:+.2f}" if surp is not None else "—",
            "Raw Score":f"{comp['raw']:+.0f}",
            "Weight":f"{comp['w']*100:.0f}%",
            "Contribution":f"{comp['contrib']:+.2f}"})
    st.dataframe(pd.DataFrame(bd_rows),use_container_width=True,hide_index=True)

    # Signal Box
    sig_colors={"sig-sbuy":("#002a18","#00c076","#00c07650"),
                "sig-buy": ("#001f12","#00c076","#00c07630"),
                "sig-nt":  ("#1a1500","#C9A227","#C9A22740"),
                "sig-sell":("#1f0000","#ff4d4d","#ff4d4d30"),
                "sig-ssell":("#2a0000","#ff4d4d","#ff4d4d50")}
    sbg,sfg,sbr=sig_colors.get(sig_cls,("#111","#aaa","#333"))
    st.markdown(f"""
    <div style="background:{sbg};border:1px solid {sbr};border-radius:10px;padding:20px;margin-top:8px;text-align:center">
      <div style="color:#333;font-size:0.62rem;letter-spacing:0.12em;font-weight:700;margin-bottom:6px">GOLD TRADER BIAS</div>
      <div style="color:{sfg};font-size:2.2rem;font-weight:800;font-family:'JetBrains Mono',monospace">{signal}</div>
      <div style="color:#333;font-size:0.65rem;margin-top:4px">Confidence: <span style="color:{sfg}">{conf}</span></div>
      <div style="color:#2a2a2a;font-size:0.68rem;margin-top:8px">Requires DXY + US2Y + price structure confirmation before entry</div>
    </div>
    <div class="warn-box" style="margin-top:10px">
      ⚠️ MacroEdge is an analytical tool for educational use. Market reactions can differ from historical tendencies.
      Always wait for price structure confirmation. Not financial advice.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 2 — CALENDAR
# ══════════════════════════════════════
with t2:
    st.markdown("### Economic Calendar — US Major Releases")
    f1,f2=st.columns([2,1])
    with f1: flt=st.selectbox("Filter",["All","Released Only","Upcoming Only"])
    with f2: show_s=st.checkbox("Show Surprise Cards",value=True)

    rows=[]
    for e in events:
        if flt=="Released Only" and not e.get("Released"): continue
        if flt=="Upcoming Only" and e.get("Released"):    continue
        a=e.get("Actual"); fc=e.get("Forecast"); pv=e.get("Previous")
        surp=(a-fc) if (a is not None and fc is not None and not np.isnan(a) and not np.isnan(fc)) else None
        il,_=impact_label(surp,e["Indicator"])
        rows.append({"Event":e["Indicator"],
            "Date IST":fmt_ist(e.get("Date")),
            "Status":"✅ Released" if e.get("Released") else f"⏳ {countdown(e.get('Date'))}",
            "Forecast":fp(fc) if fc else "—","Actual":fp(a) if a else "—","Previous":fp(pv) if pv else "—",
            "Surprise":f"{surp:+.2f}" if surp is not None else "—","Gold Impact":il})
    if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    if show_s:
        st.markdown("### Surprise Engine — Released Events")
        rel=[e for e in events if e.get("Released") and e.get("Actual") is not None]
        for e in rel[:8]:
            a=e.get("Actual"); fc=e.get("Forecast"); pv=e.get("Previous")
            surp=(a-fc) if (fc is not None and not np.isnan(fc)) else None
            il,ic=impact_label(surp,e["Indicator"]) if surp is not None else ("NEUTRAL","dp-nt")
            is_bull="BULL" in il; is_bear="BEAR" in il
            ctop="me-card-green" if is_bull else ("me-card-red" if is_bear else "")
            usd_dir="↓ BEARISH" if is_bull else ("↑ BULLISH" if is_bear else "→ NEUTRAL")
            gld_dir="↑ BULLISH" if is_bull else ("↓ BEARISH" if is_bear else "→ NEUTRAL")
            gc_c="dp-up" if is_bull else ("dp-dn" if is_bear else "dp-nt")
            ud_c="dp-dn" if is_bull else ("dp-up" if is_bear else "dp-nt")
            surp_col="#00c076" if (surp is not None and surp<0 and "CPI" in e["Indicator"]) else ("#ff4d4d" if (surp is not None and surp>0) else "#C9A227")
            st.markdown(f"""
            <div class="me-card {ctop}" style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                  <div style="color:#C9A227;font-weight:700;font-size:0.95rem">{e['Indicator']}</div>
                  <div style="color:#333;font-size:0.65rem">{fmt_ist(e.get('Date'))}</div>
                </div>
                <span class="dp {'dp-up' if is_bull else 'dp-dn' if is_bear else 'dp-nt'}" style="font-size:0.7rem">{il}</span>
              </div>
              <div style="display:flex;gap:20px;margin-top:10px;flex-wrap:wrap">
                <div><div style="color:#333;font-size:0.6rem">ACTUAL</div>
                  <div style="color:#e8e8e8;font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{fp(a)}</div></div>
                <div><div style="color:#333;font-size:0.6rem">FORECAST</div>
                  <div style="color:#888;font-family:'JetBrains Mono',monospace;font-size:1rem">{fp(fc) if fc else '—'}</div></div>
                <div><div style="color:#333;font-size:0.6rem">PREVIOUS</div>
                  <div style="color:#888;font-family:'JetBrains Mono',monospace;font-size:1rem">{fp(pv) if pv else '—'}</div></div>
                <div><div style="color:#333;font-size:0.6rem">SURPRISE</div>
                  <div style="color:{surp_col};font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{f'{surp:+.2f}' if surp is not None else '—'}</div></div>
              </div>
              <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">
                <span class="dp {ud_c}">USD {usd_dir}</span>
                <span class="dp {gc_c}">GOLD {gld_dir}</span>
                <span class="dp {gc_c}">BTC {gld_dir}</span>
                <span class="dp {gc_c}">STOCKS {gld_dir}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 3 — FED
# ══════════════════════════════════════
with t3:
    st.markdown("### Fed Policy Dashboard")
    fc1,fc2=st.columns(2)
    with fc1:
        st.markdown(f"""
        <div class="me-card me-card-gold">
          <div class="sec-label">Current Fed Rate</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:800;color:#C9A227;margin:8px 0">{DEMO_FED['rate']}</div>
          <div style="color:#444;font-size:0.72rem">Federal Funds Target Rate</div>
          <div style="border-top:1px solid #1a1a1a;margin-top:12px;padding-top:10px">
            <div style="color:#444;font-size:0.7rem">Next FOMC Meeting</div>
            <div style="color:#C9A227;font-size:0.9rem;font-weight:600">{DEMO_FED['next_fomc']}</div>
          </div>
        </div>
        <div class="me-card" style="margin-top:0">
          <div class="sec-label">CME FedWatch Probabilities</div>
          <div style="margin-top:8px;display:flex;flex-direction:column;gap:8px">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#555;font-size:0.82rem;font-weight:600">HIKE</span>
              <span style="color:#ff4d4d;font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{fed_hp:.1f}%</span>
              <span class="dp dp-dn">BEARISH GOLD</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#555;font-size:0.82rem;font-weight:600">HOLD</span>
              <span style="color:#C9A227;font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{fed_ho:.1f}%</span>
              <span class="dp dp-nt">NEUTRAL</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span style="color:#555;font-size:0.82rem;font-weight:600">CUT</span>
              <span style="color:#00c076;font-family:'JetBrains Mono',monospace;font-size:1rem;font-weight:700">{fed_cu:.1f}%</span>
              <span class="dp dp-up">BULLISH GOLD</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with fc2:
        fig_fed=go.Figure()
        fig_fed.add_trace(go.Bar(x=["HIKE","HOLD","CUT"],y=[fed_hp,fed_ho,fed_cu],
            marker_color=["#ff4d4d","#C9A227","#00c076"],
            text=[f"{v:.1f}%" for v in [fed_hp,fed_ho,fed_cu]],
            textposition="outside",textfont=dict(size=12,color="white",family="JetBrains Mono")))
        fig_fed.update_layout(title=dict(text="FOMC Outcome Probability",font=dict(size=11,color='#555')),
            height=260,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,17,17,0.8)',margin=dict(l=10,r=10,t=36,b=10),
            yaxis=dict(range=[0,100],gridcolor='#1a1a1a',ticksuffix="%",tickfont=dict(color="#444")),showlegend=False)
        st.plotly_chart(fig_fed,use_container_width=True)

        stance="DOVISH — Supports Gold" if fed_cu>30 else ("HAWKISH — Headwind" if fed_hp>40 else "NEUTRAL")
        sc_f="#00c076" if fed_cu>30 else ("#ff4d4d" if fed_hp>40 else "#C9A227")
        st.markdown(f"""
        <div class="me-card">
          <div class="sec-label">Fed → Gold Implication</div>
          <div style="display:flex;flex-direction:column;gap:5px;margin-top:6px">
            <div style="display:flex;justify-content:space-between;font-size:0.78rem;padding:4px 0;border-bottom:1px solid #111">
              <span style="color:#444">Hike &gt;60%</span><span style="color:#ff4d4d;font-weight:600">Gold ↓↓ Bearish</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.78rem;padding:4px 0;border-bottom:1px solid #111">
              <span style="color:#444">Hold ~50%</span><span style="color:#C9A227;font-weight:600">Gold → Neutral</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.78rem;padding:4px 0">
              <span style="color:#444">Cut &gt;40%</span><span style="color:#00c076;font-weight:600">Gold ↑↑ Bullish</span>
            </div>
          </div>
          <div style="margin-top:10px;padding-top:8px;border-top:1px solid #1a1a1a">
            <div style="color:#333;font-size:0.65rem">Current Fed stance</div>
            <div style="color:{sc_f};font-weight:700;font-size:0.9rem;margin-top:2px">{stance}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Treasury yields
    if not us10y_df.empty or not us2y_df.empty:
        fig_y=go.Figure()
        if not us10y_df.empty:
            fig_y.add_trace(go.Scatter(x=us10y_df["date"],y=us10y_df["value"],
                name="US 10Y",line=dict(color="#C9A227",width=2)))
        if not us2y_df.empty:
            fig_y.add_trace(go.Scatter(x=us2y_df["date"],y=us2y_df["value"],
                name="US 2Y",line=dict(color="#3a7eff",width=2)))
        fig_y.update_layout(title=dict(text="Treasury Yields — Source: FRED (Federal Reserve)",font=dict(size=11,color='#555')),
            height=280,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,17,17,0.8)',margin=dict(l=10,r=10,t=36,b=10),
            yaxis=dict(ticksuffix="%",gridcolor='#1a1a1a',tickfont=dict(color="#444")),
            legend=dict(x=0.01,y=0.99,bgcolor='rgba(0,0,0,0)',font=dict(size=11,color="#888")))
        st.plotly_chart(fig_y,use_container_width=True)
    else:
        st.markdown('<div class="info-box">Connect FRED_API_KEY to display live Treasury yield history. Register free at fredaccount.stlouisfed.org</div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 4 — GOLD ENGINE
# ══════════════════════════════════════
with t4:
    st.markdown("### Gold Macro Engine")
    g1,g2,g3=st.columns(3)
    with g1: st.metric("XAUUSD",f"${fp(gv)}",f"{gc:+.2f}%" if not np.isnan(gc) else "—")
    with g2: st.metric("DXY",fp(dv),f"{dc:+.2f}%" if not np.isnan(dc) else "—")
    with g3: st.metric("US 2Y",f"{fp(us2y_val)}%",f"{us2y_ch:+.2f}bp" if not np.isnan(us2y_ch) else "—")

    if len(gold_s)>5 and len(dxy_s)>5:
        fig_cmp=make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.05,
                              subplot_titles=("XAUUSD Price","DXY — Dollar Index"))
        fig_cmp.add_trace(go.Scatter(x=gold_s.index,y=gold_s.values,name="Gold",
            line=dict(color="#C9A227",width=2),fill='tozeroy',fillcolor='rgba(201,162,39,0.05)'),row=1,col=1)
        fig_cmp.add_trace(go.Scatter(x=dxy_s.index,y=dxy_s.values,name="DXY",
            line=dict(color="#3a7eff",width=2)),row=2,col=1)
        fig_cmp.update_layout(height=380,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,17,17,0.8)',margin=dict(l=8,r=8,t=36,b=8),showlegend=True,
            legend=dict(x=0.01,y=0.99,bgcolor='rgba(0,0,0,0)',font=dict(size=10,color="#888")))
        st.plotly_chart(fig_cmp,use_container_width=True)

    st.markdown("""
    <div class="me-card me-card-gold">
    <div class="sec-label">CPI Impact Matrix — Gold</div>
    <table>
    <thead><tr><th>CPI SURPRISE</th><th>vs FORECAST</th><th>GOLD</th><th>DXY</th><th>YIELDS</th></tr></thead>
    <tbody>
    <tr><td style="color:#00c076;font-weight:700">≤ −0.20pp</td><td style="color:#555">Actual &lt;&lt; Forecast</td><td><span class="dp dp-up">↑↑ STRONG BUY</span></td><td><span class="dp dp-dn">↓↓</span></td><td><span class="dp dp-dn">↓↓</span></td></tr>
    <tr><td style="color:#00a060;font-weight:700">−0.10 to −0.20</td><td style="color:#555">Actual &lt; Forecast</td><td><span class="dp dp-up">↑ BULLISH</span></td><td><span class="dp dp-dn">↓</span></td><td><span class="dp dp-dn">↓</span></td></tr>
    <tr><td style="color:#C9A227;font-weight:700">−0.05 to +0.05</td><td style="color:#555">In-line</td><td><span class="dp dp-nt">→ NEUTRAL</span></td><td><span class="dp dp-nt">→</span></td><td><span class="dp dp-nt">→</span></td></tr>
    <tr><td style="color:#cc3300;font-weight:700">+0.10 to +0.20</td><td style="color:#555">Actual &gt; Forecast</td><td><span class="dp dp-dn">↓ BEARISH</span></td><td><span class="dp dp-up">↑</span></td><td><span class="dp dp-up">↑</span></td></tr>
    <tr><td style="color:#ff4d4d;font-weight:700">≥ +0.20pp</td><td style="color:#555">Actual &gt;&gt; Forecast</td><td><span class="dp dp-dn">↓↓ STRONG SELL</span></td><td><span class="dp dp-up">↑↑</span></td><td><span class="dp dp-up">↑↑</span></td></tr>
    </tbody></table>
    <div style="color:#2a2a2a;font-size:0.68rem;margin-top:6px">Context matters — always cross-check with PCE, NFP, Fed & DXY confirmation before trade entry.</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 5 — IMPACT MATRIX
# ══════════════════════════════════════
with t5:
    st.markdown("### Full Cross-Asset Impact Matrix")
    matrix=[
        ("CPI Lower than forecast",   "↓","↑","↑","↑","↑",   "#00c076","Inflation cooling → Fed dovish"),
        ("CPI Higher than forecast",  "↑","↓","↓","↓","↓",   "#ff4d4d","Inflation hot → Fed hawkish"),
        ("NFP Weaker than forecast",  "↓","↑","↑","↑/mixed","↑","#00c076","Cross-check wages+revisions"),
        ("NFP Stronger than forecast","↑","↓","↓","↓","↓",   "#ff4d4d","Hot wages amplify bearish Gold"),
        ("PCE Lower than forecast",   "↓","↑","↑","↑","↑",   "#00c076","Fed's preferred inflation gauge"),
        ("PCE Higher than forecast",  "↑","↓","↓","↓","↓",   "#ff4d4d","Sticky core PCE = hawkish risk"),
        ("PPI Lower than forecast",   "↓","↑","↑","↑","↑",   "#00c076","Leading indicator for CPI"),
        ("PPI Higher than forecast",  "↑","↓","↓","↓","↓",   "#ff4d4d","Input cost pressure rising"),
        ("JOLTS Weaker",              "↓","↑","↑","↑","↑",   "#00c076","Labor demand cooling"),
        ("JOLTS Stronger",            "↑","↓","↓","↓","↓",   "#ff4d4d","Tight labor → wage pressure"),
        ("Claims Higher",             "↓","↑","↑","↑","↑",   "#00c076","Use 4-week avg not one print"),
        ("ISM Below 50",              "↓","↑","↑","↑","↑",   "#00c076","Contraction → safe-haven Gold"),
        ("ISM Above 55",              "↑","↓","↓","↓","↓",   "#ff4d4d","Strong growth = Fed stays hawkish"),
        ("FOMC Hawkish Surprise",     "↑","↓↓","↓↓","↓↓","↓","#ff4d4d","Rate-path repricing dominates ALL"),
        ("FOMC Dovish Surprise",      "↓","↑↑","↑↑","↑↑","↑","#00c076","Strongest Gold bull trigger"),
        ("Unemployment Higher",       "↓","↑","↑","↑","mixed","#00c076","Recession signal if 0.4%+ above"),
        ("Wages (AHE) Hotter",        "↑","↓","↓","↓","↓",  "#ff4d4d","Hawkish even if NFP weak"),
    ]
    def ac(v):
        if "↑↑" in v:return "#00ff88"
        if "↑" in v:  return "#00c076"
        if "↓↓" in v:return "#ff2020"
        if "↓" in v:  return "#ff4d4d"
        return "#444"

    rows_h="".join([f"""<tr style="border-bottom:1px solid #0f0f0f">
      <td style="color:{col};font-weight:600;font-size:0.75rem;padding:6px 8px">{out}</td>
      <td style="text-align:center;color:{ac(u)};font-weight:700;padding:6px 5px">{u}</td>
      <td style="text-align:center;color:{ac(g)};font-weight:700;padding:6px 5px">{g}</td>
      <td style="text-align:center;color:{ac(b)};font-weight:700;padding:6px 5px">{b}</td>
      <td style="text-align:center;color:{ac(n)};font-weight:700;padding:6px 5px">{n}</td>
      <td style="text-align:center;color:{ac(s)};font-weight:700;padding:6px 5px">{s}</td>
      <td style="color:#333;font-size:0.68rem;padding:6px 8px">{note}</td>
    </tr>""" for out,u,g,b,n,s,col,note in matrix])

    st.markdown(f"""
    <div class="me-card">
    <div class="sec-label">Event → Expected Cross-Asset Reaction</div>
    <div style="overflow-x:auto">
    <table>
    <thead><tr>
      <th>OUTCOME</th><th style="text-align:center">USD</th>
      <th style="text-align:center;color:#C9A227">GOLD</th>
      <th style="text-align:center">BTC</th>
      <th style="text-align:center">NASDAQ</th>
      <th style="text-align:center">S&P 500</th>
      <th>NOTE</th>
    </tr></thead>
    <tbody>{rows_h}</tbody>
    </table></div>
    </div>
    <div class="info-box">ℹ️ These are macro tendencies based on historical patterns, not guaranteed outcomes. Always combine with DXY + US2Y + price structure confirmation.</div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 6 — SCENARIO
# ══════════════════════════════════════
with t6:
    st.markdown("### What-If Scenario Simulator")
    st.markdown('<div class="info-box">Select hypothetical data outcomes. Engine estimates macro impact on all assets.</div>', unsafe_allow_html=True)
    s1,s2=st.columns(2)
    with s1:
        sc_cpi=st.selectbox("CPI (vs Forecast)",["Not Released","Much Lower (−0.2pp)","Lower (−0.1pp)","In-Line","Higher (+0.1pp)","Much Higher (+0.2pp)"])
        sc_nfp=st.selectbox("NFP (vs Forecast)",["Not Released","Much Weaker (−75K+)","Weaker (−50K)","In-Line (±25K)","Stronger (+50K)","Much Stronger (+75K+)"])
        sc_pce=st.selectbox("PCE (vs Forecast)",["Not Released","Much Lower","Lower","In-Line","Higher","Much Higher"])
    with s2:
        sc_fed=st.selectbox("Fed Stance",["Neutral","Strongly Dovish","Dovish","Hawkish","Strongly Hawkish"])
        sc_wg =st.selectbox("Wages (AHE)",["Not Released","Cool (below forecast)","In-Line","Hot (above forecast)"])
        sc_ism=st.selectbox("ISM Services",["Not Released","Deep Contraction (<47)","Contraction (47-50)","Expansion (50-54)","Strong (54+)"])

    sm={"Much Lower (−0.2pp)":(30,"CPI very cool → strongly bullish Gold"),
        "Lower (−0.1pp)":(20,"CPI lower → bullish Gold"),
        "In-Line":(0,"CPI in-line → neutral"),
        "Higher (+0.1pp)":(-20,"CPI hot → bearish Gold"),
        "Much Higher (+0.2pp)":(-30,"CPI very hot → strongly bearish Gold"),
        "Much Weaker (−75K+)":(30,"NFP very weak → bullish Gold"),
        "Weaker (−50K)":(22,"NFP weak → bullish Gold"),
        "In-Line (±25K)":(0,"NFP in-line → neutral"),
        "Stronger (+50K)":(-22,"NFP strong → bearish Gold"),
        "Much Stronger (+75K+)":(-30,"NFP very strong → bearish Gold"),
        "Much Lower":(25,"PCE very cool → dovish Fed + Gold bullish"),
        "Lower":(18,"PCE cool → bullish Gold"),
        "Higher":(-18,"PCE hot → bearish Gold"),
        "Much Higher":(-25,"PCE very hot → bearish Gold"),
        "Deep Contraction (<47)":(18,"ISM contraction → Gold safe-haven"),
        "Contraction (47-50)":(10,"ISM weak → mild Gold bid"),
        "Expansion (50-54)":(-6,"ISM moderate → mild Gold headwind"),
        "Strong (54+)":(-14,"ISM strong → bearish Gold"),
        "Cool (below forecast)":(10,"Cool wages → reduces hawkish pressure"),
        "Hot (above forecast)":(-15,"Hot wages → hawkish even if NFP weak")}
    fm={"Strongly Dovish":(30,"Fed strongly dovish → STRONG Gold bull"),
        "Dovish":(20,"Fed dovish → Gold bullish"),
        "Neutral":(0,"Fed neutral → no push"),
        "Hawkish":(-20,"Fed hawkish → Gold bearish"),
        "Strongly Hawkish":(-30,"Fed very hawkish → STRONG Gold bear")}

    sc_tot=0.0; sc_notes=[]
    for sel,w in [(sc_cpi,0.30),(sc_nfp,0.17),(sc_pce,0.15),(sc_ism,0.08),(sc_wg,0.10)]:
        if sel in sm: r,note=sm[sel]; sc_tot+=r*w; sc_notes.append(("🟢" if r>0 else "🔴" if r<0 else "🟡",note))
    if sc_fed in fm: r,note=fm[sc_fed]; sc_tot+=r*0.20; sc_notes.append(("🟢" if r>0 else "🔴" if r<0 else "🟡",note))
    sc_norm=max(-100,min(100,sc_tot*3.3))
    sc_gold="STRONGLY BULLISH" if sc_norm>=60 else ("BULLISH" if sc_norm>=35 else ("NEUTRAL" if abs(sc_norm)<35 else ("BEARISH" if sc_norm<=-35 else "STRONGLY BEARISH")))
    sc_usd="BEARISH" if sc_norm>=35 else ("BULLISH" if sc_norm<=-35 else "NEUTRAL")
    def sgc(l): return "#00c076" if "BULL" in l else ("#ff4d4d" if "BEAR" in l else "#C9A227")
    sc_sig,sc_sc,sc_cf=get_signal(sc_norm,50 if "Hawk" in sc_fed else 20,-1.0 if "Dovish" in sc_fed else 1.0,np.nan)
    sc_sbg,sc_sfg,sc_sbr={"sig-sbuy":("#002a18","#00c076","#00c07650"),"sig-buy":("#001f12","#00c076","#00c07630"),
        "sig-nt":("#1a1500","#C9A227","#C9A22740"),"sig-sell":("#1f0000","#ff4d4d","#ff4d4d30"),
        "sig-ssell":("#2a0000","#ff4d4d","#ff4d4d50")}.get(sc_sc,("#111","#aaa","#333"))
    notes_h="".join([f'<div style="display:flex;gap:8px;padding:4px 0"><span>{ic}</span><span style="color:#666;font-size:0.75rem">{t}</span></div>' for ic,t in sc_notes])
    st.markdown(f"""
    <div class="me-card {'me-card-green' if sc_norm>=35 else 'me-card-red' if sc_norm<=-35 else 'me-card-gold'}" style="margin-top:10px">
      <div class="sec-label">Scenario Result</div>
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px">
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">MACRO SCORE</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:1.8rem;font-weight:800;color:{sgc(sc_gold)}">{sc_norm:+.0f}</div></div>
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">GOLD</div>
          <div style="color:{sgc(sc_gold)};font-weight:700;font-size:0.85rem">{sc_gold}</div></div>
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">USD</div>
          <div style="color:{sgc('BEAR' if 'BEAR' in sc_usd else 'BULL')};font-weight:700;font-size:0.85rem">{sc_usd}</div></div>
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">BTC</div>
          <div style="color:{sgc(sc_gold)};font-weight:700;font-size:0.85rem">{sc_gold}</div></div>
        <div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">SIGNAL</div>
          <span class="signal {sc_sc}" style="font-size:0.68rem">{sc_sig}</span></div>
      </div>
      <div style="margin-top:12px;border-top:1px solid #1a1a1a;padding-top:10px">{notes_h}</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 7 — HISTORY
# ══════════════════════════════════════
with t7:
    st.markdown("### Historical Analysis")
    per=st.selectbox("Period",["1mo","3mo","6mo"],index=1)
    nd={"1mo":21,"3mo":63,"6mo":126}.get(per,63)
    fig_idx=go.Figure()
    for name,col in [("Gold","#C9A227"),("DXY","#3a7eff"),("BTC","#ff9900"),("Nasdaq","#00c076"),("S&P500","#a855f7")]:
        s=mkt.get(name,pd.Series(dtype=float))
        if len(s)>5:
            s2=s[-nd:] if len(s)>nd else s
            idx=s2/s2.iloc[0]*100
            fig_idx.add_trace(go.Scatter(x=idx.index,y=idx.values,name=name,line=dict(color=col,width=1.8)))
    fig_idx.add_hline(y=100,line=dict(color="#222",width=1,dash="dot"))
    fig_idx.update_layout(title=dict(text=f"Indexed Performance — {per} (Base = 100)",font=dict(size=11,color='#555')),
        height=300,template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(17,17,17,0.8)',
        margin=dict(l=8,r=8,t=36,b=8),
        legend=dict(x=0.01,y=0.99,bgcolor='rgba(0,0,0,0)',font=dict(size=10,color="#888")),
        yaxis=dict(gridcolor='#1a1a1a',tickfont=dict(color="#444")))
    st.plotly_chart(fig_idx,use_container_width=True)

    st.markdown("### Signal Reference Table")
    sig_ref=[["🟢 STRONG BUY","≥ +60","Fed cut >40%","DXY ↓ + US2Y ↓","HIGH","High-conviction Gold long"],
             ["🟢 BUY","+35 to +59","Fed hike not rising","DXY ↓ OR US2Y ↓","MEDIUM","Long bias — await structure"],
             ["🟡 NO TRADE","−34 to +34","Mixed","Disagrees","LOW","Wait for clarity"],
             ["🔴 SELL","−35 to −59","Fed hike rising","DXY ↑ OR US2Y ↑","MEDIUM","Short bias — await structure"],
             ["🔴 STRONG SELL","≤ −60","Fed hike >60%","DXY ↑ + US2Y ↑","HIGH","High-conviction Gold short"]]
    st.dataframe(pd.DataFrame(sig_ref,columns=["Signal","Score","Fed","Market","Confidence","Action"]),
                 use_container_width=True,hide_index=True)
    st.markdown('<div class="warn-box">⚠️ Educational tool only. MacroEdge signals are macro bias indicators. Not financial advice. Always use risk management.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div style="color:#C9A227;font-weight:800;font-size:1rem;margin-bottom:4px">⚡ MACROEDGE</div>', unsafe_allow_html=True)
    st.caption("BR Trading Academy — Macro Terminal")
    st.divider()
    st.markdown("**API Status**")
    st.write("FRED:", "✅" if FRED_API_KEY else "⚠️ Add key")
    st.write("Trading Economics:", "✅" if TE_API_KEY else "⚠️ Add key")
    st.write("Market Data:", "✅ yfinance live")
    st.write("Mode:", "🟡 Demo" if (DEMO_MODE or not TE_API_KEY) else "🟢 Live")
    st.divider()
    st.caption(f"Refreshes every {REFRESH_SEC}s")
    st.caption(f"Last: {ist_now().strftime('%H:%M:%S IST')}")
    st.divider()
    st.caption("Data: FRED • yfinance • TradingEconomics")
    st.caption("Not financial advice. Educational use only.")

# Auto-refresh
st.markdown(f'<script>setTimeout(()=>window.location.reload(),{REFRESH_SEC*1000})</script>', unsafe_allow_html=True)

"""MacroEdge V4 - BR Trading Academy - Clean Build"""
import os
from datetime import datetime, timezone, timedelta
import requests, pandas as pd, numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="MacroEdge - BR Trading Academy", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0a0a0a!important;}
.main{background:#0a0a0a!important;}.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stSidebar"]{background:#0f0f0f!important;border-right:1px solid #1e1e1e!important;}
#MainMenu,footer,header{visibility:hidden;}.stDeployButton{display:none;}
.br-nav{background:#0f0f0f;border-bottom:1px solid #1e1e1e;padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:52px;position:sticky;top:0;z-index:999;}
.br-logo{display:flex;align-items:center;gap:10px;}
.br-logo-box{width:32px;height:32px;background:#C9A227;border-radius:6px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.85rem;color:#000;}
.br-logo-text{color:#f0f0f0;font-size:0.85rem;font-weight:600;}
.br-logo-sub{color:#C9A227;font-size:0.6rem;letter-spacing:0.08em;text-transform:uppercase;}
.br-nav-links{display:flex;gap:4px;align-items:center;}
.br-nav-link{color:#555;font-size:0.72rem;font-weight:500;padding:5px 10px;border-radius:4px;text-decoration:none;letter-spacing:0.04em;text-transform:uppercase;}
.br-nav-link.active{color:#C9A227;background:rgba(201,162,39,0.08);}
.br-badge{background:#C9A227;color:#000;font-size:0.5rem;font-weight:800;padding:1px 4px;border-radius:2px;margin-left:3px;}
.br-time{color:#444;font-size:0.7rem;font-family:'JetBrains Mono',monospace;}
.br-live-dot{width:6px;height:6px;background:#00c076;border-radius:50%;display:inline-block;animation:pg 2s infinite;margin-right:3px;}
@keyframes pg{0%,100%{opacity:1}50%{opacity:0.3}}
.tstrip{background:#080808;border-bottom:1px solid #161616;padding:6px 20px;display:flex;gap:0;overflow-x:auto;scrollbar-width:none;white-space:nowrap;align-items:center;}
.tstrip::-webkit-scrollbar{display:none;}
.ti{display:inline-flex;align-items:center;gap:6px;padding:3px 14px 3px 0;border-right:1px solid #1a1a1a;margin-right:14px;flex-shrink:0;}
.ti:last-child{border-right:none;}
.tn{font-size:0.68rem;font-weight:700;color:#C9A227;letter-spacing:0.06em;}
.tp{font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#e8e8e8;}
.tu{font-size:0.68rem;color:#00c076;font-family:'JetBrains Mono',monospace;}
.td{font-size:0.68rem;color:#ff4d4d;font-family:'JetBrains Mono',monospace;}
.mc{padding:16px 18px;background:#111;border:1px solid #1e1e1e;border-radius:10px;margin-bottom:12px;}
.mc-g{border-top:2px solid #C9A227;}
.mc-gr{border-top:2px solid #00c076;}
.mc-re{border-top:2px solid #ff4d4d;}
.mc-bl{border-top:2px solid #3a7eff;}
.mc-pu{border-top:2px solid #a855f7;}
.sl{font-size:0.6rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#333;margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid #1a1a1a;}
.sn{font-family:'JetBrains Mono',monospace;font-size:3.2rem;font-weight:800;line-height:1;}
.sb{color:#00c076;}.sr{color:#ff4d4d;}.sn2{color:#C9A227;}
.sig{display:inline-block;padding:5px 16px;border-radius:4px;font-weight:700;font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;}
.sb2{background:#002a18;color:#00c076;border:1px solid #00c07640;}
.sb3{background:#001f12;color:#00c076;border:1px solid #00c07625;}
.sn3{background:#1a1500;color:#C9A227;border:1px solid #C9A22730;}
.sr2{background:#1f0000;color:#ff4d4d;border:1px solid #ff4d4d25;}
.sr3{background:#2a0000;color:#ff4d4d;border:1px solid #ff4d4d40;}
.dp{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:600;font-family:'JetBrains Mono',monospace;}
.dup{background:#001f12;color:#00c076;}.ddn{background:#1f0000;color:#ff4d4d;}.dnt{background:#141414;color:#555;}
[data-testid="metric-container"]{background:#111!important;border:1px solid #1e1e1e!important;border-radius:8px!important;padding:14px!important;}
[data-testid="stMetricValue"]{font-family:'JetBrains Mono',monospace!important;font-size:1.3rem!important;color:#e8e8e8!important;}
[data-testid="stMetricDelta"]{font-size:0.78rem!important;}
[data-testid="stMetricLabel"]{font-size:0.62rem!important;color:#444!important;font-weight:700!important;letter-spacing:0.08em!important;text-transform:uppercase!important;}
.stTabs [data-baseweb="tab-list"]{background:#0a0a0a!important;border-bottom:1px solid #1a1a1a!important;padding:0 20px!important;gap:2px!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#444!important;font-size:0.72rem!important;font-weight:600!important;letter-spacing:0.06em!important;text-transform:uppercase!important;padding:8px 14px!important;border-radius:4px 4px 0 0!important;}
.stTabs [aria-selected="true"]{background:#111!important;color:#C9A227!important;border-top:2px solid #C9A227!important;}
table{border-collapse:collapse;width:100%;}
th{color:#444;font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;padding:8px 10px;border-bottom:1px solid #1a1a1a;text-align:left;}
td{color:#c0c0c0;font-size:0.78rem;padding:7px 10px;border-bottom:1px solid #111;}
tr:hover td{background:#0f0f0f;}
hr{border-color:#1a1a1a!important;margin:12px 0!important;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:#080808;}
::-webkit-scrollbar-thumb{background:#222;border-radius:2px;}
@media(max-width:768px){.br-nav-links{display:none;}.sn{font-size:2.2rem;}}
</style>""", unsafe_allow_html=True)

# ── CONFIG ──
FRED_KEY = os.getenv("FRED_API_KEY", "")
TE_KEY   = os.getenv("TRADINGECONOMICS_API_KEY", "")
DEMO     = os.getenv("DEMO_MODE", "true").lower() == "true"
REFRESH  = int(os.getenv("REFRESH_SECONDS", "90"))
IST      = timedelta(hours=5, minutes=30)

WEIGHTS = {
    "CPI m/m":0.12,"Core CPI m/m":0.18,"PPI m/m":0.05,"Core PPI m/m":0.05,
    "PCE m/m":0.06,"Core PCE m/m":0.09,"NFP":0.12,"Unemployment Rate":0.05,
    "Average Hourly Earnings":0.05,"JOLTS":0.05,"Initial Claims":0.05,
    "ISM Manufacturing":0.04,"ISM Services":0.04,"Fed":0.10,
}

HIST = {
    "CPI m/m":         {"total":24,"below":9, "inline":10,"above":5, "avg":-0.04,"trend":"cooling","note":"Market expectations adjust ho jaati hain — ek direction mein consistent nahi."},
    "Core CPI m/m":    {"total":24,"below":8, "inline":12,"above":4, "avg":-0.02,"trend":"cooling","note":"Core sticky raha hai — below forecast rare but high impact hota hai."},
    "NFP":             {"total":24,"below":7, "inline":8, "above":9, "avg":+22.0,"trend":"mixed",  "note":"NFP historically upside surprise deta hai. Revisions bhi important hoti hain."},
    "PCE m/m":         {"total":24,"below":10,"inline":10,"above":4, "avg":-0.02,"trend":"cooling","note":"Fed ka preferred gauge — in-line print bhi dovish signal ho sakta hai."},
    "Core PCE m/m":    {"total":24,"below":9, "inline":11,"above":4, "avg":-0.01,"trend":"cooling","note":"Downside surprises increase ho rahe hain recent months mein."},
    "PPI m/m":         {"total":24,"below":8, "inline":9, "above":7, "avg":+0.01,"trend":"mixed",  "note":"Supply chain se connected — volatile hota hai."},
    "Initial Claims":  {"total":24,"below":9, "inline":10,"above":5, "avg":+4.0, "trend":"rising", "note":"4-week average use karo — ek print se trend nahi banta."},
    "ISM Services":    {"total":24,"below":8, "inline":10,"above":6, "avg":-0.8, "trend":"contracting","note":"50 ke aas-paas — contraction territory mein drift kar raha hai."},
    "ISM Manufacturing":{"total":24,"below":9,"inline":8, "above":7, "avg":-0.5, "trend":"contracting","note":"Already contraction mein — improvement limited hai."},
    "JOLTS":           {"total":24,"below":10,"inline":8, "above":6, "avg":-0.15,"trend":"cooling","note":"Job openings gradual decline mein — labor demand softening."},
}

GOLD_RXN = {
    "CPI m/m":       {"below":+0.52,"inline":-0.05,"above":-0.48},
    "Core CPI m/m":  {"below":+0.68,"inline":-0.08,"above":-0.55},
    "NFP":           {"below":+0.45,"inline":-0.02,"above":-0.38},
    "PCE m/m":       {"below":+0.38,"inline":+0.02,"above":-0.35},
    "Core PCE m/m":  {"below":+0.42,"inline":-0.05,"above":-0.40},
    "PPI m/m":       {"below":+0.22,"inline":-0.03,"above":-0.25},
    "Initial Claims":{"below":-0.15,"inline":-0.02,"above":+0.18},
    "ISM Services":  {"below":+0.25,"inline":+0.02,"above":-0.22},
    "ISM Manufacturing":{"below":+0.18,"inline":0.0,"above":-0.20},
    "JOLTS":         {"below":+0.20,"inline":0.0, "above":-0.18},
}

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
DEMO_FED = {"hike":12.0,"hold":68.0,"cut":20.0,"rate":"3.50-3.75%","fomc":"Sep 17, 2026"}

# ── HELPERS ──
def pn(v):
    if v is None: return None
    try: return float(str(v).replace("%","").replace("K","").strip())
    except: return None

def slast(s): return float(s.iloc[-1]) if s is not None and len(s) else np.nan
def spct(s,n=5):
    if s is None or len(s)<=n: return np.nan
    return float((s.iloc[-1]/s.iloc[-1-n]-1)*100)
def sch(s,n=1):
    if s is None or len(s)<=n: return np.nan
    return float(s.iloc[-1]-s.iloc[-1-n])
def fp(v,d=2): return f"{v:,.{d}f}" if v is not None and not np.isnan(v) else "—"
def ist_now(): return datetime.now(timezone.utc)+IST
def fmt_ist(dt):
    if dt is None: return "—"
    try:
        if hasattr(dt,"tzinfo") and dt.tzinfo:
            ist=dt.astimezone(timezone.utc).replace(tzinfo=timezone.utc)+IST
        else: ist=dt+IST
        return ist.strftime("%d %b %Y  %H:%M IST")
    except: return str(dt)
def cdown(dt):
    if dt is None: return "—"
    try:
        now=datetime.now(timezone.utc)
        diff=(dt-now) if (hasattr(dt,"tzinfo") and dt.tzinfo) else (dt-now.replace(tzinfo=None))
        if diff.total_seconds()<0: return "Released"
        d=diff.days; h=diff.seconds//3600; m=(diff.seconds%3600)//60
        return f"{d}d {h}h {m}m"
    except: return "—"
def hrs_until(dt):
    if dt is None: return 9999
    try:
        now=datetime.now(timezone.utc)
        diff=(dt-now) if (hasattr(dt,"tzinfo") and dt.tzinfo) else (dt-now.replace(tzinfo=None))
        return max(0, diff.total_seconds()/3600)
    except: return 9999

# ── DATA ──
@st.cache_data(ttl=60)
def fetch_mkt():
    syms={"Gold":"GC=F","DXY":"DX-Y.NYB","BTC":"BTC-USD","Nasdaq":"^NDX","SP500":"^GSPC","Dow":"^DJI","US10Y":"^TNX"}
    out={}
    for k,s in syms.items():
        try:
            raw=yf.download(s,period="6mo",interval="1d",progress=False,auto_adjust=False)
            cl=raw["Close"].iloc[:,0] if isinstance(raw.columns,pd.MultiIndex) else raw["Close"]
            out[k]=cl.dropna()
        except: out[k]=pd.Series(dtype=float)
    return out

@st.cache_data(ttl=300)
def fetch_fred(sid,lim=60):
    if not FRED_KEY: return pd.DataFrame()
    try:
        r=requests.get("https://api.stlouisfed.org/fred/series/observations",
            params={"series_id":sid,"api_key":FRED_KEY,"file_type":"json","sort_order":"desc","limit":lim},timeout=15)
        r.raise_for_status()
        df=pd.DataFrame(r.json().get("observations",[]))
        if df.empty: return df
        df["date"]=pd.to_datetime(df["date"])
        df["value"]=pd.to_numeric(df["value"],errors="coerce")
        return df.dropna(subset=["value"]).sort_values("date")
    except: return pd.DataFrame()

def get_events():
    return DEMO_EVENTS

# ── SCORING ──
def bscore(ev,actual,forecast):
    if actual is None or (isinstance(actual,float) and np.isnan(actual)): return 0.0
    a=float(actual)
    f=None if (forecast is None or (isinstance(forecast,float) and np.isnan(forecast))) else float(forecast)
    if ev in {"CPI m/m","Core CPI m/m","PPI m/m","Core PPI m/m","PCE m/m","Core PCE m/m"}:
        if f is not None:
            s=a-f
            if s<=-0.20: return 30
            if s<=-0.10: return 20
            if s<=-0.05: return 10
            if s<0.05:   return 0
            if s<0.10:   return -10
            if s<0.20:   return -20
            return -30
    if ev=="NFP":
        if f is not None:
            s=a-f
            if s<=-75: return 30
            if s<=-50: return 22
            if s<=-25: return 12
            if s<25:   return 0
            if s<50:   return -12
            if s<75:   return -22
            return -30
    if ev=="Initial Claims":
        if f is not None:
            s=a-f
            if s>=50:  return 22
            if s>=25:  return 14
            if s>=10:  return 7
            if s>-10:  return 0
            if s>-25:  return -10
            if s>-50:  return -18
            return -25
    if ev=="Unemployment Rate":
        if f is not None:
            s=a-f
            if s>=0.4:  return 20
            if s>=0.2:  return 12
            if s>=0.1:  return 6
            if s>-0.1:  return 0
            if s>-0.2:  return -8
            if s>-0.4:  return -15
            return -22
    if ev=="Average Hourly Earnings":
        if f is not None:
            s=a-f
            if s>=0.2:  return -15
            if s>=0.1:  return -8
            if s>-0.1:  return 0
            if s>-0.2:  return 10
            return 18
    if ev in {"ISM Manufacturing","ISM Services"}:
        if a<47: return 18
        if a<49: return 10
        if a<51: return 4
        if a<54: return -6
        if a<57: return -14
        return -20
    if ev=="JOLTS":
        if a<6.8: return 15
        if a<7.0: return 8
        if a<7.3: return 0
        if a<7.6: return -8
        return -15
    return 0.0

def fscore(hp):
    if hp is None or np.isnan(hp): return 0
    if hp>=80: return -30
    if hp>=65: return -20
    if hp>=55: return -10
    if hp>=45: return 0
    if hp>=35: return 10
    if hp>=20: return 20
    return 30

def compute(events,fed_hp,mkt):
    score=0.0; comps={}
    seen={}
    for e in sorted([x for x in events if x.get("Released") and x.get("Actual") is not None],key=lambda x:str(x.get("Date",""))):
        seen[e["Indicator"]]=e
    for name,e in seen.items():
        raw=bscore(name,e.get("Actual"),e.get("Forecast"))
        w=WEIGHTS.get(name,0)
        score+=raw*w
        comps[name]={"raw":raw,"w":w,"contrib":raw*w,"data":e}
    fs=fscore(fed_hp)
    score+=fs*WEIGHTS["Fed"]
    comps["Fed"]={"raw":fs,"w":WEIGHTS["Fed"],"contrib":fs*WEIGHTS["Fed"]}
    norm=max(-100,min(100,score*3.3))
    dxy=mkt.get("DXY",pd.Series(dtype=float))
    if len(dxy)>=6:
        dc=float((dxy.iloc[-1]/dxy.iloc[-6]-1)*100)
        if dc<-0.5: norm=min(100,norm+5)
        elif dc>0.5: norm=max(-100,norm-5)
    return norm,comps

def get_sig(score,fed_hp,dxy_ch,u2y_ch):
    bc=(not np.isnan(dxy_ch) and dxy_ch<-0.3) or (not np.isnan(u2y_ch) and u2y_ch<-3)
    brc=(not np.isnan(dxy_ch) and dxy_ch>0.3) or (not np.isnan(u2y_ch) and u2y_ch>3)
    fh=fed_hp if not np.isnan(fed_hp) else 50
    if score>=60 and fh<=40 and bc:   return "STRONG BUY","sb2","HIGH"
    if score>=35 and fh<=55:           return "BUY","sb3","MEDIUM"
    if score<=-60 and fh>=60 and brc: return "STRONG SELL","sr3","HIGH"
    if score<=-35 and fh>=45:          return "SELL","sr2","MEDIUM"
    return "NO TRADE","sn3","LOW"

def ilabel(surp,ev):
    if surp is None: return "NEUTRAL","dnt"
    if ev in {"CPI m/m","Core CPI m/m","PPI m/m","Core PPI m/m","PCE m/m","Core PCE m/m"}:
        if surp<=-0.20: return "STRONGLY BULLISH","dup"
        if surp<=-0.10: return "BULLISH","dup"
        if surp<0.10:   return "NEUTRAL","dnt"
        if surp<0.20:   return "BEARISH","ddn"
        return "STRONGLY BEARISH","ddn"
    if ev=="NFP":
        if surp<=-75: return "STRONGLY BULLISH","dup"
        if surp<=-50: return "BULLISH","dup"
        if surp<50:   return "NEUTRAL","dnt"
        return "BEARISH","ddn"
    return "NEUTRAL","dnt"

# ── PREDICTION ENGINE ──
def get_pred(ev_name, forecast, previous, cur_score):
    h=HIST.get(ev_name)
    if h is None: return None
    tot=h["total"]
    pb=round(h["below"]/tot*100)
    pi=round(h["inline"]/tot*100)
    pa=100-pb-pi
    trend=h.get("trend","mixed")
    if cur_score>=35 and trend=="cooling":
        pb=min(pb+8,65); pa=max(pa-5,5); pi=100-pb-pa
    elif cur_score<=-35 and trend not in ["cooling"]:
        pa=min(pa+8,55); pb=max(pb-5,5); pi=100-pb-pa
    tot2=pb+pi+pa
    pb=round(pb/tot2*100); pa=round(pa/tot2*100); pi=100-pb-pa
    ml="below" if (pb>=pi and pb>=pa) else ("above" if pa>=pb and pa>=pi else "inline")
    gr=GOLD_RXN.get(ev_name,{"below":+0.3,"inline":0.0,"above":-0.3})
    w=WEIGHTS.get(ev_name,0.05)
    sc_b=round(20*w*3.3,1); sc_i=0.0; sc_a=round(-20*w*3.3,1)
    fc=float(forecast) if forecast else 0
    if ev_name in {"CPI m/m","Core CPI m/m","PPI m/m","Core PPI m/m","PCE m/m","Core PCE m/m"}:
        cr=f"<= {fc-0.10:.2f}%"; ir=f"{fc-0.05:.2f}% to {fc+0.05:.2f}%"; hr=f">= {fc+0.10:.2f}%"
    elif ev_name=="NFP":
        cr=f"<= {fc-50:.0f}K"; ir=f"{fc-25:.0f}K to {fc+25:.0f}K"; hr=f">= {fc+50:.0f}K"
    elif ev_name=="Initial Claims":
        cr=f">= {fc+25:.0f}K (more claims)"; ir=f"{fc-10:.0f}K to {fc+10:.0f}K"; hr=f"<= {fc-25:.0f}K"
    else:
        cr=f"Below {fc:.2f}"; ir=f"Near {fc:.2f}"; hr=f"Above {fc:.2f}"
    return {"pb":pb,"pi":pi,"pa":pa,"ml":ml,"avg":h["avg"],"trend":trend,"note":h["note"],
            "gb":gr["below"],"gi":gr["inline"],"ga":gr["above"],
            "sb":sc_b,"si":sc_i,"sa":sc_a,"cr":cr,"ir":ir,"hr":hr,
            "ht":tot,"hb":h["below"],"ha":h["above"]}

def sc_assets(direction, ev_name):
    is_claims=(ev_name=="Initial Claims")
    bull=(direction=="above") if is_claims else (direction=="below")
    if bull:
        return {"USD":"DOWN BEARISH","Gold":"UP BULLISH","BTC":"UP BULLISH","Nasdaq":"UP BULLISH","US 2Y":"DOWN FALLING"}
    elif direction=="inline":
        return {"USD":"NEUTRAL","Gold":"NEUTRAL","BTC":"NEUTRAL","Nasdaq":"NEUTRAL","US 2Y":"STABLE"}
    else:
        return {"USD":"UP BULLISH","Gold":"DOWN BEARISH","BTC":"DOWN BEARISH","Nasdaq":"DOWN BEARISH","US 2Y":"UP RISING"}

# ── LOAD DATA ──
mkt=fetch_mkt()
events=get_events()
u2y_df=fetch_fred("DGS2",30)
u10y_df=fetch_fred("DGS10",90)
u2y_val=float(u2y_df.iloc[-1]["value"]) if not u2y_df.empty else np.nan
u2y_ch=float(u2y_df.iloc[-1]["value"]-u2y_df.iloc[-2]["value"]) if len(u2y_df)>=2 else np.nan
fed_hp=DEMO_FED["hike"]; fed_ho=DEMO_FED["hold"]; fed_cu=DEMO_FED["cut"]

gs=mkt.get("Gold",pd.Series(dtype=float))
ds=mkt.get("DXY",pd.Series(dtype=float))
bs=mkt.get("BTC",pd.Series(dtype=float))
ns=mkt.get("Nasdaq",pd.Series(dtype=float))
ss=mkt.get("SP500",pd.Series(dtype=float))
ws=mkt.get("Dow",pd.Series(dtype=float))
ts=mkt.get("US10Y",pd.Series(dtype=float))

gv=slast(gs); dv=slast(ds); bv=slast(bs); nv=slast(ns); sv=slast(ss); wv=slast(ws); tv=slast(ts)
gc=spct(gs); dc=spct(ds); bc=spct(bs); nc=spct(ns); sc2=spct(ss); wc=spct(ws)
tc=sch(ts)*100

mscore,comps=compute(events,fed_hp,mkt)
sig,scls,conf=get_sig(mscore,fed_hp,dc,u2y_ch)
upcoming=sorted([e for e in events if not e.get("Released") and e.get("Date")],key=lambda x:str(x.get("Date","")))
nxt=upcoming[0] if upcoming else None
pre_rel=[e for e in upcoming if hrs_until(e.get("Date"))<=72]

# ── NAV ──
dm='<span style="background:#C9A227;color:#000;font-size:0.55rem;font-weight:800;padding:2px 7px;border-radius:3px;margin-left:8px;">DEMO</span>'
lv='<span style="color:#00c076;font-size:0.68rem;font-weight:600;margin-left:8px;"><span class="br-live-dot"></span>LIVE</span>'
badge=dm if (DEMO or not TE_KEY) else lv

st.markdown(
    '<div class="br-nav">'
    '<div class="br-logo">'
    '<div class="br-logo-box">BR</div>'
    '<div><div class="br-logo-text">BR Trading Academy</div>'
    '<div class="br-logo-sub">MacroEdge Terminal</div></div>'
    + badge +
    '</div>'
    '<div class="br-nav-links">'
    '<a class="br-nav-link active" href="#">Overview</a>'
    '<a class="br-nav-link" href="#">Prediction <span class="br-badge">NEW</span></a>'
    '<a class="br-nav-link" href="#">Calendar</a>'
    '<a class="br-nav-link" href="#">Fed</a>'
    '<a class="br-nav-link" href="#">Gold</a>'
    '<a class="br-nav-link" href="#">Impact</a>'
    '</div>'
    '<div class="br-time">' + ist_now().strftime("%a, %d %b  %H:%M IST") + '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── TICKER ──
def tick(name,price,chg,pfx="",sfx=""):
    if np.isnan(price):
        return '<div class="ti"><span class="tn">'+name+'</span><span class="tp" style="color:#333">—</span></div>'
    arr='<span style="color:#00c076;font-size:0.6rem">▲</span>' if chg>0 else '<span style="color:#ff4d4d;font-size:0.6rem">▼</span>'
    cc="tu" if chg>0 else ("td" if chg<0 else "")
    cs=f"{chg:+.2f}%" if not np.isnan(chg) else "—"
    return f'<div class="ti">{arr}<span class="tn">{name}</span><span class="tp">{pfx}{fp(price)}{sfx}</span><span class="{cc}">{cs}</span></div>'

tc2=float((ts.iloc[-1]/ts.iloc[-2]-1)*100) if len(ts)>=2 else np.nan
u2pct=float(u2y_ch/u2y_val*100) if (not np.isnan(u2y_val) and not np.isnan(u2y_ch) and u2y_val!=0) else np.nan

thtml=(
    tick("XAUUSD",gv,gc,pfx="$")+tick("DXY",dv,dc)+tick("US 2Y",u2y_val,u2pct,sfx="%")+
    tick("US 10Y",tv,tc2,sfx="%")+tick("BTC",bv,bc,pfx="$")+tick("NASDAQ",nv,nc)+
    tick("S&P500",sv,sc2)+tick("DOW",wv,wc)
)
st.markdown('<div class="tstrip">'+thtml+'</div>', unsafe_allow_html=True)

# ── PRE-RELEASE BANNER ──
if pre_rel:
    names=" + ".join([e["Indicator"] for e in pre_rel[:3]])
    hrs=hrs_until(pre_rel[0].get("Date"))
    st.markdown(
        '<div style="background:#0d0020;border:1px solid #a855f740;border-left:4px solid #a855f7;'
        'padding:10px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">'
        '<div style="display:flex;align-items:center;gap:10px;">'
        '<span style="color:#a855f7;font-size:1rem;">⚡</span>'
        '<span style="color:#a855f7;font-weight:700;font-size:0.82rem;letter-spacing:0.06em;">PRE-RELEASE MODE ACTIVE</span>'
        '<span style="color:#555;font-size:0.75rem;">'+names+' — in '+str(int(hrs))+' hours</span>'
        '</div>'
        '<span style="color:#a855f7;font-size:0.72rem;font-weight:600;">→ See PREDICTION tab</span>'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown('<div style="padding:16px 20px 40px 20px">', unsafe_allow_html=True)

# ── TABS ──
t_ov,t_pred,t_cal,t_fed,t_gold,t_imp,t_sc,t_hist = st.tabs([
    "📊 OVERVIEW","🔮 PREDICTION","📅 CALENDAR","🏛 FED","🏆 GOLD","⚡ IMPACT","💡 SCENARIO","📈 HISTORY"
])

# ══ OVERVIEW ══
with t_ov:
    c1,c2,c3,c4=st.columns([1.2,1,1,1])
    with c1:
        sc="sb" if mscore>=35 else ("sr" if mscore<=-35 else "sn2")
        ct="mc-gr" if mscore>=35 else ("mc-re" if mscore<=-35 else "mc-g")
        st.markdown(
            f'<div class="mc {ct}"><div class="sl">Gold Macro Score</div>'
            f'<div style="text-align:center;padding:8px 0 4px">'
            f'<div class="sn {sc}">{mscore:+.0f}</div>'
            f'<div style="color:#333;font-size:0.62rem;margin-top:2px">-100 BEARISH | BULLISH +100</div>'
            f'</div><div style="text-align:center;margin-top:10px">'
            f'<span class="sig {scls}">{sig}</span>'
            f'<div style="color:#333;font-size:0.62rem;margin-top:5px">Confidence: {conf}</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with c2:
        if nxt:
            nd=nxt.get("Date"); fcv=nxt.get("Forecast")
            p=get_pred(nxt["Indicator"],fcv,nxt.get("Previous"),mscore)
            ml_txt=""
            if p:
                mlc="#00c076" if p["ml"]=="below" else ("#ff4d4d" if p["ml"]=="above" else "#C9A227")
                mlp=p[{"below":"pb","inline":"pi","above":"pa"}[p["ml"]]]
                mll="BELOW FORECAST" if p["ml"]=="below" else ("ABOVE FORECAST" if p["ml"]=="above" else "IN-LINE")
                ml_txt=f'<div style="margin-top:8px"><span style="color:{mlc};font-size:0.72rem;font-weight:700">{mlp}% chance {mll}</span></div>'
            st.markdown(
                f'<div class="mc mc-pu"><div class="sl">Next Major Release</div>'
                f'<div style="color:#C9A227;font-weight:700;font-size:1rem;margin-top:4px">{nxt["Indicator"]}</div>'
                f'<div style="color:#444;font-size:0.72rem;margin-top:2px">{fmt_ist(nd)}</div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;color:#e8e8e8;font-size:1.3rem;font-weight:700;margin-top:6px">{cdown(nd)}</div>'
                f'<div style="color:#333;font-size:0.65rem;margin-top:2px">Forecast: {fp(fcv) if fcv else "—"}</div>'
                f'{ml_txt}</div>',
                unsafe_allow_html=True
            )
    with c3:
        st.markdown(
            f'<div class="mc mc-bl"><div class="sl">FOMC Fed Policy</div>'
            f'<div style="color:#555;font-size:0.72rem;margin-top:4px">Rate: {DEMO_FED["rate"]}</div>'
            f'<div style="color:#333;font-size:0.65rem">Next: {DEMO_FED["fomc"]}</div>'
            f'<div style="margin-top:10px;display:flex;flex-direction:column;gap:5px">'
            f'<div style="display:flex;justify-content:space-between"><span style="color:#444;font-size:0.72rem">HIKE</span><span style="color:#ff4d4d;font-family:\'JetBrains Mono\',monospace;font-size:0.82rem">{fed_hp:.1f}%</span></div>'
            f'<div style="display:flex;justify-content:space-between"><span style="color:#444;font-size:0.72rem">HOLD</span><span style="color:#C9A227;font-family:\'JetBrains Mono\',monospace;font-size:0.82rem">{fed_ho:.1f}%</span></div>'
            f'<div style="display:flex;justify-content:space-between"><span style="color:#444;font-size:0.72rem">CUT</span><span style="color:#00c076;font-family:\'JetBrains Mono\',monospace;font-size:0.82rem">{fed_cu:.1f}%</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with c4:
        dd="DOWN BEARISH" if (not np.isnan(dc) and dc<-0.3) else ("UP BULLISH" if (not np.isnan(dc) and dc>0.3) else "NEUTRAL")
        dc2="#00c076" if "BEARISH" in dd else ("#ff4d4d" if "BULLISH" in dd else "#C9A227")
        ud="DOWN FALLING" if (not np.isnan(u2y_ch) and u2y_ch<-3) else ("UP RISING" if (not np.isnan(u2y_ch) and u2y_ch>3) else "STABLE")
        uc2="#00c076" if "FALL" in ud else ("#ff4d4d" if "RISING" in ud else "#C9A227")
        bok="BEARISH" in dd or "FALL" in ud
        st.markdown(
            f'<div class="mc"><div class="sl">Market Confirmation</div>'
            f'<div style="margin-top:6px;display:flex;flex-direction:column;gap:6px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center"><span style="color:#444;font-size:0.72rem">DXY 5D</span><span style="color:{dc2};font-family:\'JetBrains Mono\',monospace;font-size:0.72rem">{dd}</span></div>'
            f'<div style="display:flex;justify-content:space-between;align-items:center"><span style="color:#444;font-size:0.72rem">US 2Y</span><span style="color:{uc2};font-family:\'JetBrains Mono\',monospace;font-size:0.72rem">{ud}</span></div>'
            f'<div style="border-top:1px solid #1a1a1a;margin-top:4px;padding-top:8px;display:flex;justify-content:space-between">'
            f'<span style="color:#555;font-size:0.75rem;font-weight:600">GOLD CONFIRM</span>'
            f'<span style="color:{"#00c076" if bok else "#ff4d4d"};font-weight:700">{"YES" if bok else "NO"}</span>'
            f'</div></div></div>',
            unsafe_allow_html=True
        )

    # Why Gold
    reasons=[]
    for ind,comp in comps.items():
        raw=comp["raw"]; d=comp.get("data",{}); a=d.get("Actual"); fc=d.get("Forecast")
        if ind=="Fed":
            if raw>0: reasons.append(("🟢",f"Fed cut probability HIGH ({fed_cu:.0f}%) — dovish supports Gold"))
            elif raw<0: reasons.append(("🔴",f"Fed hike probability HIGH ({fed_hp:.0f}%) — hawkish headwind"))
        elif a is not None and fc is not None and not np.isnan(a) and not np.isnan(fc):
            s=a-fc
            if raw>5: reasons.append(("🟢",f"{ind}: Actual {a:.2f} vs Forecast {fc:.2f} — Surprise {s:+.2f} — Gold BULLISH"))
            elif raw<-5: reasons.append(("🔴",f"{ind}: Actual {a:.2f} vs Forecast {fc:.2f} — Surprise {s:+.2f} — Gold BEARISH"))
    if not np.isnan(dc):
        if dc<-0.5: reasons.append(("🟢",f"DXY weakening 5D: {dc:+.2f}% — dollar selling confirms Gold bid"))
        elif dc>0.5: reasons.append(("🔴",f"DXY strengthening 5D: {dc:+.2f}% — dollar strength headwind"))
    if not reasons: reasons=[("🟡","Demo mode — API keys add karo live data ke liye")]
    bw="BULLISH" if mscore>=35 else ("BEARISH" if mscore<=-35 else "NEUTRAL")
    bc3="#00c076" if mscore>=35 else ("#ff4d4d" if mscore<=-35 else "#C9A227")
    rh="".join([f'<div style="display:flex;gap:8px;align-items:flex-start;padding:5px 0;border-bottom:1px solid #0f0f0f"><span>{ic}</span><span style="color:#888;font-size:0.78rem;line-height:1.5">{t}</span></div>' for ic,t in reasons])
    st.markdown(f'<div class="mc"><div class="sl">Why Gold is <span style="color:{bc3}">{bw}</span></div>{rh}</div>', unsafe_allow_html=True)

    # Charts
    cc1,cc2=st.columns(2)
    pcfg=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(17,17,17,0.8)",
              margin=dict(l=8,r=8,t=32,b=8),showlegend=False,height=220,
              xaxis=dict(gridcolor="#1a1a1a",zeroline=False),yaxis=dict(gridcolor="#1a1a1a",zeroline=False))
    with cc1:
        if len(gs)>5:
            fig=go.Figure(); fig.add_trace(go.Scatter(x=gs.index,y=gs.values,fill="tozeroy",fillcolor="rgba(201,162,39,0.07)",line=dict(color="#C9A227",width=2)))
            fig.update_layout(title=dict(text="XAUUSD — Gold",font=dict(size=11,color="#555")),**pcfg)
            st.plotly_chart(fig,use_container_width=True)
    with cc2:
        if len(ds)>5:
            dc3="#ff4d4d" if dc>0 else "#00c076"
            fig2=go.Figure(); fig2.add_trace(go.Scatter(x=ds.index,y=ds.values,line=dict(color=dc3,width=2)))
            fig2.update_layout(title=dict(text="DXY — Dollar Index",font=dict(size=11,color="#555")),**pcfg)
            st.plotly_chart(fig2,use_container_width=True)

    # Gauge
    gc4="#00c076" if mscore>=35 else ("#ff4d4d" if mscore<=-35 else "#C9A227")
    fig_g=go.Figure(go.Indicator(mode="gauge+number",value=mscore,
        number={"suffix":" / 100","font":{"size":24,"color":"#e8e8e8","family":"JetBrains Mono"}},
        title={"text":"GOLD MACRO SCORE","font":{"size":11,"color":"#444"}},
        gauge={"axis":{"range":[-100,100],"tickwidth":0.5,"tickcolor":"#1a1a1a","tickfont":{"size":9,"color":"#333"}},
               "bar":{"color":gc4,"thickness":0.22},"bgcolor":"rgba(0,0,0,0)","borderwidth":0,
               "steps":[{"range":[-100,-60],"color":"rgba(80,10,10,0.5)"},{"range":[-60,-35],"color":"rgba(60,15,15,0.4)"},
                        {"range":[-35,35],"color":"rgba(25,20,5,0.3)"},{"range":[35,60],"color":"rgba(5,40,25,0.4)"},
                        {"range":[60,100],"color":"rgba(5,50,30,0.5)"}],
               "threshold":{"line":{"color":"white","width":2},"thickness":0.75,"value":mscore}}))
    fig_g.update_layout(height=240,paper_bgcolor="rgba(0,0,0,0)",font={"color":"#555"},margin=dict(l=30,r=30,t=36,b=10))
    st.plotly_chart(fig_g,use_container_width=True)

    # Score breakdown table
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

    # Signal box
    sc_c={"sb2":("#002a18","#00c076","#00c07650"),"sb3":("#001f12","#00c076","#00c07630"),
          "sn3":("#1a1500","#C9A227","#C9A22740"),"sr2":("#1f0000","#ff4d4d","#ff4d4d30"),
          "sr3":("#2a0000","#ff4d4d","#ff4d4d50")}
    sbg,sfg,sbr=sc_c.get(scls,("#111","#aaa","#333"))
    st.markdown(
        f'<div style="background:{sbg};border:1px solid {sbr};border-radius:10px;padding:20px;margin-top:8px;text-align:center">'
        f'<div style="color:#333;font-size:0.62rem;letter-spacing:0.12em;font-weight:700;margin-bottom:6px">GOLD TRADER BIAS</div>'
        f'<div style="color:{sfg};font-size:2.2rem;font-weight:800;font-family:\'JetBrains Mono\',monospace">{sig}</div>'
        f'<div style="color:#333;font-size:0.65rem;margin-top:4px">Confidence: <span style="color:{sfg}">{conf}</span></div>'
        f'</div>'
        f'<div style="background:#1a1200;border-left:3px solid #C9A227;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#9a7a20;margin-top:10px">'
        f'Educational tool only. Not financial advice. Always use risk management.</div>',
        unsafe_allow_html=True
    )

# ══ PREDICTION ══
with t_pred:
    st.markdown("### Pre-Release Prediction Engine")
    st.markdown(
        '<div style="background:#0d0020;border-left:3px solid #a855f7;border-radius:0 6px 6px 0;'
        'padding:10px 14px;font-size:0.78rem;color:#7030a0;margin-bottom:16px">'
        'Historical data (last 24 months) + current macro regime se probability calculate karta hai. '
        'Guarantee nahi — educated estimate hai.</div>',
        unsafe_allow_html=True
    )

    all_names=list(dict.fromkeys([e["Indicator"] for e in upcoming]))
    if not all_names:
        all_names=list(dict.fromkeys([e["Indicator"] for e in DEMO_EVENTS if not e.get("Released")]))

    sel_name=st.selectbox("Event select karo",all_names)
    sel_ev=next((e for e in upcoming if e["Indicator"]==sel_name),None)
    if not sel_ev:
        sel_ev=next((e for e in DEMO_EVENTS if e["Indicator"]==sel_name and not e.get("Released")),None)

    if sel_ev:
        fcv=sel_ev.get("Forecast"); pvv=sel_ev.get("Previous")
        pred=get_pred(sel_name,fcv,pvv,mscore)

        if pred:
            pb=pred["pb"]; pi=pred["pi"]; pa=pred["pa"]
            ml=pred["ml"]
            tc3=pred["trend"]
            tc4="#00c076" if tc3=="cooling" else ("#ff4d4d" if tc3=="hot" else "#C9A227")
            ac="#00c076" if pred["avg"]<0 else ("#ff4d4d" if pred["avg"]>0 else "#555")

            # Header info
            st.markdown(
                f'<div style="background:#0d0d1a;border:1px solid #1e1e3a;border-radius:12px;padding:18px 20px;margin-bottom:12px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">'
                f'<div><div style="font-size:1.1rem;font-weight:800;color:#e8e8ff">{sel_name}</div>'
                f'<div style="color:#444;font-size:0.72rem;margin-top:2px">{fmt_ist(sel_ev.get("Date"))}</div></div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;color:#C9A227;font-size:0.9rem;font-weight:700;'
                f'background:#1a1200;padding:4px 12px;border-radius:4px;border:1px solid #C9A22730">{cdown(sel_ev.get("Date"))}</div>'
                f'</div>'
                f'<div style="display:flex;gap:20px;flex-wrap:wrap">'
                f'<div><div style="color:#333;font-size:0.6rem;margin-bottom:2px">FORECAST</div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;color:#C9A227;font-size:1.1rem;font-weight:700">{fp(fcv) if fcv else "—"}</div></div>'
                f'<div><div style="color:#333;font-size:0.6rem;margin-bottom:2px">PREVIOUS</div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;color:#888;font-size:1.1rem">{fp(pvv) if pvv else "—"}</div></div>'
                f'<div><div style="color:#333;font-size:0.6rem;margin-bottom:2px">AVG SURPRISE (24M)</div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;color:{ac};font-size:1.1rem;font-weight:700">{pred["avg"]:+.2f}</div></div>'
                f'<div><div style="color:#333;font-size:0.6rem;margin-bottom:2px">RECENT TREND</div>'
                f'<div style="color:{tc4};font-size:0.85rem;font-weight:700;text-transform:uppercase">{tc3}</div></div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

            # Probability section header
            st.markdown(
                f'<div style="color:#5a5a8a;font-size:0.65rem;font-weight:700;letter-spacing:0.1em;margin-bottom:10px">'
                f'PROBABILITY DISTRIBUTION — Based on last {pred["ht"]} releases</div>',
                unsafe_allow_html=True
            )

            # BELOW bar
            st.markdown(
                f'<div style="background:#0d0d1a;border:1px solid #1e1e3a;border-radius:8px;padding:12px 16px;margin-bottom:8px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">'
                f'<span style="color:#00c076;font-size:0.78rem;font-weight:700">🟢 BELOW FORECAST — Gold Bullish</span>'
                f'<span style="color:#00c076;font-family:\'JetBrains Mono\',monospace;font-size:1.1rem;font-weight:800">{pb}%</span>'
                f'</div>'
                f'<div style="color:#333;font-size:0.65rem;margin-bottom:6px">{pred["cr"]} — Historical: {pred["hb"]}/{pred["ht"]} times</div>'
                f'<div style="background:#1a1a1a;border-radius:3px;height:10px;overflow:hidden">'
                f'<div style="width:{pb}%;height:100%;background:#00c076;border-radius:3px"></div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

            # IN-LINE bar
            st.markdown(
                f'<div style="background:#0d0d1a;border:1px solid #1e1e3a;border-radius:8px;padding:12px 16px;margin-bottom:8px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">'
                f'<span style="color:#C9A227;font-size:0.78rem;font-weight:700">🟡 IN-LINE — Neutral</span>'
                f'<span style="color:#C9A227;font-family:\'JetBrains Mono\',monospace;font-size:1.1rem;font-weight:800">{pi}%</span>'
                f'</div>'
                f'<div style="color:#333;font-size:0.65rem;margin-bottom:6px">{pred["ir"]}</div>'
                f'<div style="background:#1a1a1a;border-radius:3px;height:10px;overflow:hidden">'
                f'<div style="width:{pi}%;height:100%;background:#C9A227;border-radius:3px"></div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

            # ABOVE bar
            st.markdown(
                f'<div style="background:#0d0d1a;border:1px solid #1e1e3a;border-radius:8px;padding:12px 16px;margin-bottom:16px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">'
                f'<span style="color:#ff4d4d;font-size:0.78rem;font-weight:700">🔴 ABOVE FORECAST — Gold Bearish</span>'
                f'<span style="color:#ff4d4d;font-family:\'JetBrains Mono\',monospace;font-size:1.1rem;font-weight:800">{pa}%</span>'
                f'</div>'
                f'<div style="color:#333;font-size:0.65rem;margin-bottom:6px">{pred["hr"]} — Historical: {pred["ha"]}/{pred["ht"]} times</div>'
                f'<div style="background:#1a1a1a;border-radius:3px;height:10px;overflow:hidden">'
                f'<div style="width:{pa}%;height:100%;background:#ff4d4d;border-radius:3px"></div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

            # Analyst note
            st.markdown(
                f'<div style="background:#0a0a1a;border:1px solid #1e1e3a;border-radius:8px;padding:10px 14px;margin-bottom:16px">'
                f'<div style="color:#5a5a8a;font-size:0.65rem;font-weight:700;letter-spacing:0.1em">ANALYST NOTE</div>'
                f'<div style="color:#888;font-size:0.78rem;margin-top:4px">{pred["note"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            # 3 Scenario cards
            st.markdown("### 3 Scenarios — Agar Data Aaya Toh...")

            ac_cool=sc_assets("below",  sel_name)
            ac_inln=sc_assets("inline", sel_name)
            ac_hot =sc_assets("above",  sel_name)

            def sc_card(label, emoji, color, bg, assets, prob, gold_pct, sc_delta, rng, is_ml):
                badge2=f' <span style="background:{color}20;color:{color};font-size:0.55rem;padding:2px 6px;border-radius:2px;font-weight:700">MOST LIKELY</span>' if is_ml else ""
                rows=""
                for aname,aval in assets.items():
                    if "UP" in aval or "BULLISH" in aval or "FALLING" in aval:
                        acol="#00c076"
                    elif "DOWN" in aval or "BEARISH" in aval or "RISING" in aval:
                        acol="#ff4d4d"
                    else:
                        acol="#555"
                    disp=aval.replace("UP ","↑ ").replace("DOWN ","↓ ")
                    rows+=(f'<div style="display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid #111;font-size:0.7rem">'
                           f'<span style="color:#444">{aname}</span>'
                           f'<span style="color:{acol};font-weight:700;font-family:\'JetBrains Mono\',monospace">{disp}</span></div>')
                ns2=max(-100,min(100,mscore+sc_delta))
                sdc="#00c076" if sc_delta>0 else ("#ff4d4d" if sc_delta<0 else "#555")
                return (
                    f'<div style="background:{bg};border:1px solid {color}30;border-radius:8px;padding:14px">'
                    f'<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{color};margin-bottom:4px">'
                    f'{emoji} {label}{badge2}</div>'
                    f'<div style="color:#444;font-size:0.68rem;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px">{rng}</div>'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">'
                    f'<span style="color:{color};font-size:0.85rem;font-weight:800">Gold: {gold_pct:+.2f}%</span>'
                    f'<span style="color:#444;font-size:0.7rem">{prob}% chance</span></div>'
                    f'{rows}'
                    f'<div style="margin-top:8px;padding-top:6px;border-top:1px solid #111;font-size:0.68rem">'
                    f'<span style="color:#333">Score impact: </span>'
                    f'<span style="color:{sdc};font-family:\'JetBrains Mono\',monospace;font-weight:700">{sc_delta:+.1f} → {ns2:.0f}</span>'
                    f'</div></div>'
                )

            s1,s2,s3=st.columns(3)
            with s1:
                st.markdown(sc_card("BELOW FORECAST","🟢","#00c076","#001810",ac_cool,pb,pred["gb"],pred["sb"],pred["cr"],ml=="below"), unsafe_allow_html=True)
            with s2:
                st.markdown(sc_card("IN-LINE","🟡","#C9A227","#1a1200",ac_inln,pi,pred["gi"],pred["si"],pred["ir"],ml=="inline"), unsafe_allow_html=True)
            with s3:
                st.markdown(sc_card("ABOVE FORECAST","🔴","#ff4d4d","#1a0000",ac_hot,pa,pred["ga"],pred["sa"],pred["hr"],ml=="above"), unsafe_allow_html=True)

            # Stats
            st.markdown("### Historical Stats — Last 24 Months")
            gr2=GOLD_RXN.get(sel_name,{})
            h1,h2,h3,h4=st.columns(4)
            def hbox(val,lbl,col="#e8e8e8"):
                st.markdown(f'<div style="background:#0f0f0f;border:1px solid #1a1a1a;border-radius:8px;padding:12px;text-align:center"><div style="font-family:\'JetBrains Mono\',monospace;font-size:1.4rem;font-weight:800;color:{col}">{val}</div><div style="font-size:0.62rem;color:#444;letter-spacing:0.08em;text-transform:uppercase;margin-top:2px">{lbl}</div></div>',unsafe_allow_html=True)
            with h1: hbox(f'{pred["hb"]}/{pred["ht"]}','Below forecast','#00c076')
            with h2: hbox(f'{pred["ha"]}/{pred["ht"]}','Above forecast','#ff4d4d')
            with h3: hbox(f'{gr2.get("below",0):+.2f}%','Gold avg (cool)','#00c076')
            with h4: hbox(f'{gr2.get("above",0):+.2f}%','Gold avg (hot)','#ff4d4d')

            ns3=max(-100,min(100,mscore+pred[f's{ml[0]}']))
            st.markdown(
                f'<div style="background:#1a1200;border-left:3px solid #C9A227;border-radius:0 6px 6px 0;'
                f'padding:10px 14px;font-size:0.78rem;color:#9a7a20;margin-top:12px">'
                f'Probability estimate historical patterns par based hai — guarantee nahi. '
                f'Release ke baad DXY + US2Y reaction zaroor dekho.<br><br>'
                f'Current score <b>{mscore:+.0f}</b> — agar <b>{ml}</b> scenario aaya toh score ~<b>{ns3:.0f}</b> ho sakta hai.'
                f'</div>',
                unsafe_allow_html=True
            )

        else:
            st.info(f"{sel_name} ke liye historical data nahi hai.")
    else:
        st.info("Event load nahi hua.")

    # Quick view all upcoming
    st.markdown("### Sabhi Upcoming Events — Quick View")
    for e in upcoming[:8]:
        p2=get_pred(e["Indicator"],e.get("Forecast"),e.get("Previous"),mscore)
        if not p2: continue
        ml2=p2["ml"]
        mc2="#00c076" if ml2=="below" else ("#ff4d4d" if ml2=="above" else "#C9A227")
        mp2=p2[{"below":"pb","inline":"pi","above":"pa"}[ml2]]
        ml2l=f"Below {mp2}%" if ml2=="below" else (f"Above {mp2}%" if ml2=="above" else f"In-line {mp2}%")
        hrs2=hrs_until(e.get("Date"))
        urg="🔴" if hrs2<24 else ("🟡" if hrs2<72 else "⚪")
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'padding:8px 14px;background:#111;border-radius:6px;margin-bottom:6px;border-left:3px solid {mc2}">'
            f'<div style="display:flex;align-items:center;gap:10px">'
            f'<span>{urg}</span>'
            f'<span style="color:#C9A227;font-weight:600;font-size:0.82rem">{e["Indicator"]}</span>'
            f'<span style="color:#333;font-size:0.7rem">{fmt_ist(e.get("Date"))}</span>'
            f'</div>'
            f'<div style="display:flex;align-items:center;gap:12px">'
            f'<span style="color:#444;font-size:0.7rem">Fc: {fp(e.get("Forecast")) if e.get("Forecast") else "—"}</span>'
            f'<span style="color:{mc2};font-weight:700;font-size:0.78rem">Most likely: {ml2l}</span>'
            f'<span style="color:#555;font-size:0.7rem;font-family:\'JetBrains Mono\',monospace">{cdown(e.get("Date"))}</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )

# ══ CALENDAR ══
with t_cal:
    st.markdown("### Economic Calendar")
    f1,f2=st.columns([2,1])
    with f1: flt=st.selectbox("Filter",["All","Released Only","Upcoming Only"])
    with f2: show_s=st.checkbox("Surprise Cards",value=True)
    rows=[]
    for e in events:
        if flt=="Released Only" and not e.get("Released"): continue
        if flt=="Upcoming Only" and e.get("Released"): continue
        a=e.get("Actual"); fc=e.get("Forecast"); pv=e.get("Previous")
        surp=(a-fc) if (a is not None and fc is not None and not np.isnan(a) and not np.isnan(fc)) else None
        il,_=ilabel(surp,e["Indicator"])
        rows.append({"Event":e["Indicator"],"Date IST":fmt_ist(e.get("Date")),
            "Status":"Released" if e.get("Released") else cdown(e.get("Date")),
            "Forecast":fp(fc) if fc else "—","Actual":fp(a) if a else "—",
            "Previous":fp(pv) if pv else "—",
            "Surprise":f"{surp:+.2f}" if surp is not None else "—","Gold Impact":il})
    if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    if show_s:
        st.markdown("### Surprise Engine")
        for e in [x for x in events if x.get("Released") and x.get("Actual") is not None][:8]:
            a=e.get("Actual"); fc=e.get("Forecast"); pv=e.get("Previous")
            surp=(a-fc) if (fc is not None and not np.isnan(fc)) else None
            il,ic=ilabel(surp,e["Indicator"]) if surp is not None else ("NEUTRAL","dnt")
            is_bull="BULL" in il; is_bear="BEAR" in il
            ctop="mc-gr" if is_bull else ("mc-re" if is_bear else "")
            sc3=f"{surp:+.2f}" if surp is not None else "—"
            scol="#00c076" if (surp and surp<0 and "CPI" in e["Indicator"]) else ("#ff4d4d" if (surp and surp>0) else "#C9A227")
            ud2="DOWN BEARISH" if is_bull else ("UP BULLISH" if is_bear else "NEUTRAL")
            gd="UP BULLISH" if is_bull else ("DOWN BEARISH" if is_bear else "NEUTRAL")
            st.markdown(
                f'<div class="mc {ctop}" style="margin-bottom:8px">'
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
                f'<div><div style="color:#C9A227;font-weight:700;font-size:0.95rem">{e["Indicator"]}</div>'
                f'<div style="color:#333;font-size:0.65rem">{fmt_ist(e.get("Date"))}</div></div>'
                f'<span class="dp {ic}">{il}</span></div>'
                f'<div style="display:flex;gap:20px;margin-top:10px;flex-wrap:wrap">'
                f'<div><div style="color:#333;font-size:0.6rem">ACTUAL</div><div style="color:#e8e8e8;font-family:\'JetBrains Mono\',monospace;font-size:1rem;font-weight:700">{fp(a)}</div></div>'
                f'<div><div style="color:#333;font-size:0.6rem">FORECAST</div><div style="color:#888;font-family:\'JetBrains Mono\',monospace;font-size:1rem">{fp(fc) if fc else "—"}</div></div>'
                f'<div><div style="color:#333;font-size:0.6rem">PREVIOUS</div><div style="color:#888;font-family:\'JetBrains Mono\',monospace;font-size:1rem">{fp(pv) if pv else "—"}</div></div>'
                f'<div><div style="color:#333;font-size:0.6rem">SURPRISE</div><div style="color:{scol};font-family:\'JetBrains Mono\',monospace;font-size:1rem;font-weight:700">{sc3}</div></div>'
                f'</div>'
                f'<div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">'
                f'<span class="dp {"dup" if is_bull else "ddn" if is_bear else "dnt"}">USD {ud2}</span>'
                f'<span class="dp {"dup" if is_bull else "ddn" if is_bear else "dnt"}">GOLD {gd}</span>'
                f'<span class="dp {"dup" if is_bull else "ddn" if is_bear else "dnt"}">BTC {gd}</span>'
                f'</div></div>',
                unsafe_allow_html=True
            )

# ══ FED ══
with t_fed:
    st.markdown("### Fed Policy Dashboard")
    fc1,fc2=st.columns(2)
    with fc1:
        st.markdown(
            f'<div class="mc mc-g"><div class="sl">Current Fed Rate</div>'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:2rem;font-weight:800;color:#C9A227;margin:8px 0">{DEMO_FED["rate"]}</div>'
            f'<div style="color:#444;font-size:0.72rem">Federal Funds Target Rate</div>'
            f'<div style="border-top:1px solid #1a1a1a;margin-top:12px;padding-top:10px">'
            f'<div style="color:#444;font-size:0.7rem">Next FOMC</div>'
            f'<div style="color:#C9A227;font-size:0.9rem;font-weight:600">{DEMO_FED["fomc"]}</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="mc"><div class="sl">CME FedWatch Probabilities</div>'
            f'<div style="margin-top:8px;display:flex;flex-direction:column;gap:8px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<span style="color:#555;font-size:0.82rem;font-weight:600">HIKE</span>'
            f'<span style="color:#ff4d4d;font-family:\'JetBrains Mono\',monospace;font-size:1rem;font-weight:700">{fed_hp:.1f}%</span>'
            f'<span class="dp ddn">BEARISH GOLD</span></div>'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<span style="color:#555;font-size:0.82rem;font-weight:600">HOLD</span>'
            f'<span style="color:#C9A227;font-family:\'JetBrains Mono\',monospace;font-size:1rem;font-weight:700">{fed_ho:.1f}%</span>'
            f'<span class="dp dnt">NEUTRAL</span></div>'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<span style="color:#555;font-size:0.82rem;font-weight:600">CUT</span>'
            f'<span style="color:#00c076;font-family:\'JetBrains Mono\',monospace;font-size:1rem;font-weight:700">{fed_cu:.1f}%</span>'
            f'<span class="dp dup">BULLISH GOLD</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with fc2:
        fig_f=go.Figure()
        fig_f.add_trace(go.Bar(x=["HIKE","HOLD","CUT"],y=[fed_hp,fed_ho,fed_cu],
            marker_color=["#ff4d4d","#C9A227","#00c076"],
            text=[f"{v:.1f}%" for v in [fed_hp,fed_ho,fed_cu]],
            textposition="outside",textfont=dict(size=12,color="white",family="JetBrains Mono")))
        fig_f.update_layout(title=dict(text="FOMC Probability",font=dict(size=11,color="#555")),
            height=260,template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(17,17,17,0.8)",
            margin=dict(l=10,r=10,t=36,b=10),yaxis=dict(range=[0,100],gridcolor="#1a1a1a",ticksuffix="%"),showlegend=False)
        st.plotly_chart(fig_f,use_container_width=True)
    if not u10y_df.empty or not u2y_df.empty:
        fig_y=go.Figure()
        if not u10y_df.empty: fig_y.add_trace(go.Scatter(x=u10y_df["date"],y=u10y_df["value"],name="US 10Y",line=dict(color="#C9A227",width=2)))
        if not u2y_df.empty:  fig_y.add_trace(go.Scatter(x=u2y_df["date"],y=u2y_df["value"],name="US 2Y",line=dict(color="#3a7eff",width=2)))
        fig_y.update_layout(title=dict(text="Treasury Yields — FRED",font=dict(size=11,color="#555")),
            height=280,template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(17,17,17,0.8)",
            margin=dict(l=10,r=10,t=36,b=10),yaxis=dict(ticksuffix="%",gridcolor="#1a1a1a"),
            legend=dict(x=0.01,y=0.99,bgcolor="rgba(0,0,0,0)",font=dict(size=11,color="#888")))
        st.plotly_chart(fig_y,use_container_width=True)
    else:
        st.markdown('<div style="background:#001020;border-left:3px solid #3a7eff;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#4a80cc">FRED_API_KEY add karo live Treasury yields ke liye.</div>', unsafe_allow_html=True)

# ══ GOLD ENGINE ══
with t_gold:
    st.markdown("### Gold Macro Engine")
    g1,g2,g3=st.columns(3)
    with g1: st.metric("XAUUSD",f"${fp(gv)}",f"{gc:+.2f}%" if not np.isnan(gc) else "—")
    with g2: st.metric("DXY",fp(dv),f"{dc:+.2f}%" if not np.isnan(dc) else "—")
    with g3: st.metric("US 2Y",f"{fp(u2y_val)}%",f"{u2y_ch:+.2f}bp" if not np.isnan(u2y_ch) else "—")
    if len(gs)>5 and len(ds)>5:
        fig_c=make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.05,subplot_titles=("XAUUSD","DXY"))
        fig_c.add_trace(go.Scatter(x=gs.index,y=gs.values,name="Gold",line=dict(color="#C9A227",width=2),fill="tozeroy",fillcolor="rgba(201,162,39,0.05)"),row=1,col=1)
        fig_c.add_trace(go.Scatter(x=ds.index,y=ds.values,name="DXY",line=dict(color="#3a7eff",width=2)),row=2,col=1)
        fig_c.update_layout(height=380,template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(17,17,17,0.8)",margin=dict(l=8,r=8,t=36,b=8))
        st.plotly_chart(fig_c,use_container_width=True)
    st.markdown("### Score Breakdown")
    bd2=[]
    for ind,comp in comps.items():
        d=comp.get("data",{}); a=d.get("Actual"); fc=d.get("Forecast")
        surp=None if (a is None or fc is None) else (a-fc if not(np.isnan(a) or np.isnan(fc)) else None)
        bd2.append({"Indicator":ind,"Actual":f"{a:.2f}" if a is not None and not np.isnan(a) else "—",
            "Forecast":f"{fc:.2f}" if fc is not None and not np.isnan(fc) else "—",
            "Surprise":f"{surp:+.2f}" if surp is not None else "—",
            "Raw Score":f"{comp['raw']:+.0f}","Weight":f"{comp['w']*100:.0f}%","Contribution":f"{comp['contrib']:+.2f}"})
    st.dataframe(pd.DataFrame(bd2),use_container_width=True,hide_index=True)

# ══ IMPACT ══
with t_imp:
    st.markdown("### Full Cross-Asset Impact Matrix")
    matrix=[
        ("CPI Lower","down","up","up","up","up","#00c076","Cooling inflation"),
        ("CPI Higher","up","down","down","down","down","#ff4d4d","Hot inflation"),
        ("NFP Weaker","down","up","up","up/mixed","up","#00c076","Check wages+revisions"),
        ("NFP Stronger","up","down","down","down","down","#ff4d4d","Hot wages amplify"),
        ("PCE Lower","down","up","up","up","up","#00c076","Fed preferred gauge"),
        ("PCE Higher","up","down","down","down","down","#ff4d4d","Sticky inflation"),
        ("JOLTS Weaker","down","up","up","up","up","#00c076","Labor demand cooling"),
        ("ISM Below 50","down","up","up","up","up","#00c076","Contraction — safe-haven"),
        ("ISM Above 55","up","down","down","down","down","#ff4d4d","Strong growth"),
        ("FOMC Hawkish","up","down down","down down","down down","down","#ff4d4d","Strongest move"),
        ("FOMC Dovish","down","up up","up up","up up","up","#00c076","Best Gold catalyst"),
        ("Wages Hotter","up","down","down","down","down","#ff4d4d","Hawkish even if NFP weak"),
    ]
    def ac2(v):
        v2=v.lower()
        if "up up" in v2: return "#00ff88"
        if "up" in v2:   return "#00c076"
        if "down down" in v2: return "#ff2020"
        if "down" in v2: return "#ff4d4d"
        return "#444"
    rh2="".join([
        f'<tr style="border-bottom:1px solid #0f0f0f">'
        f'<td style="color:{col};font-weight:600;font-size:0.75rem;padding:6px 8px">{out}</td>'
        f'<td style="text-align:center;color:{ac2(u)};font-weight:700;padding:6px 5px">{u}</td>'
        f'<td style="text-align:center;color:{ac2(g)};font-weight:700;padding:6px 5px">{g}</td>'
        f'<td style="text-align:center;color:{ac2(b)};font-weight:700;padding:6px 5px">{b}</td>'
        f'<td style="text-align:center;color:{ac2(n)};font-weight:700;padding:6px 5px">{n}</td>'
        f'<td style="text-align:center;color:{ac2(s)};font-weight:700;padding:6px 5px">{s}</td>'
        f'<td style="color:#333;font-size:0.68rem;padding:6px 8px">{note}</td>'
        f'</tr>'
        for out,u,g,b,n,s,col,note in matrix
    ])
    st.markdown(
        '<div class="mc"><div class="sl">Event to Cross-Asset Reaction</div>'
        '<div style="overflow-x:auto"><table><thead><tr>'
        '<th>OUTCOME</th><th style="text-align:center">USD</th>'
        '<th style="text-align:center;color:#C9A227">GOLD</th>'
        '<th style="text-align:center">BTC</th>'
        '<th style="text-align:center">NASDAQ</th>'
        '<th style="text-align:center">S&P</th>'
        '<th>NOTE</th></tr></thead><tbody>'+rh2+'</tbody></table></div></div>'
        '<div style="background:#001020;border-left:3px solid #3a7eff;border-radius:0 6px 6px 0;'
        'padding:10px 14px;font-size:0.78rem;color:#4a80cc">'
        'Macro tendencies only. Always confirm with DXY + US2Y + price structure before trade entry.</div>',
        unsafe_allow_html=True
    )

# ══ SCENARIO ══
with t_sc:
    st.markdown("### What-If Scenario Simulator")
    s1,s2=st.columns(2)
    with s1:
        sc_cpi=st.selectbox("CPI",["Not Released","Much Lower (-0.2pp)","Lower (-0.1pp)","In-Line","Higher (+0.1pp)","Much Higher (+0.2pp)"])
        sc_nfp=st.selectbox("NFP",["Not Released","Much Weaker (-75K+)","Weaker (-50K)","In-Line (25K)","Stronger (+50K)","Much Stronger (+75K+)"])
        sc_pce=st.selectbox("PCE",["Not Released","Much Lower","Lower","In-Line","Higher","Much Higher"])
    with s2:
        sc_fed=st.selectbox("Fed",["Neutral","Strongly Dovish","Dovish","Hawkish","Strongly Hawkish"])
        sc_wg=st.selectbox("Wages",["Not Released","Cool (below forecast)","In-Line","Hot (above forecast)"])
        sc_ism=st.selectbox("ISM",["Not Released","Deep Contraction (<47)","Contraction (47-50)","Expansion (50-54)","Strong (54+)"])
    sm2={
        "Much Lower (-0.2pp)":(30,"CPI very cool"),"Lower (-0.1pp)":(20,"CPI lower"),"In-Line":(0,"In-line"),
        "Higher (+0.1pp)":(-20,"CPI hot"),"Much Higher (+0.2pp)":(-30,"CPI very hot"),
        "Much Weaker (-75K+)":(30,"NFP very weak"),"Weaker (-50K)":(22,"NFP weak"),
        "In-Line (25K)":(0,"NFP in-line"),"Stronger (+50K)":(-22,"NFP strong"),"Much Stronger (+75K+)":(-30,"NFP very strong"),
        "Much Lower":(25,"PCE very cool"),"Lower":(18,"PCE cool"),"Higher":(-18,"PCE hot"),"Much Higher":(-25,"PCE very hot"),
        "Deep Contraction (<47)":(18,"ISM contraction"),"Contraction (47-50)":(10,"ISM weak"),
        "Expansion (50-54)":(-6,"ISM ok"),"Strong (54+)":(-14,"ISM strong"),
        "Cool (below forecast)":(10,"Cool wages"),"Hot (above forecast)":(-15,"Hot wages"),
    }
    fm2={"Strongly Dovish":(30,"Fed strongly dovish"),"Dovish":(20,"Fed dovish"),"Neutral":(0,"Fed neutral"),
         "Hawkish":(-20,"Fed hawkish"),"Strongly Hawkish":(-30,"Fed very hawkish")}
    st2=0.0; sn4=[]
    for sel,w in [(sc_cpi,0.30),(sc_nfp,0.17),(sc_pce,0.15),(sc_ism,0.08),(sc_wg,0.10)]:
        if sel in sm2: r,note=sm2[sel]; st2+=r*w; sn4.append(("🟢" if r>0 else "🔴" if r<0 else "🟡",note))
    if sc_fed in fm2: r,note=fm2[sc_fed]; st2+=r*0.20; sn4.append(("🟢" if r>0 else "🔴" if r<0 else "🟡",note))
    sn5=max(-100,min(100,st2*3.3))
    sg2="STRONGLY BULLISH" if sn5>=60 else ("BULLISH" if sn5>=35 else ("NEUTRAL" if abs(sn5)<35 else ("BEARISH" if sn5<=-35 else "STRONGLY BEARISH")))
    su2="BEARISH" if sn5>=35 else ("BULLISH" if sn5<=-35 else "NEUTRAL")
    def sgc2(l): return "#00c076" if "BULL" in l else ("#ff4d4d" if "BEAR" in l else "#C9A227")
    ss2,sc4,sc5=get_sig(sn5,50 if "Hawk" in sc_fed else 20,-1.0 if "Dovish" in sc_fed else 1.0,np.nan)
    sb4,sf4,_={"sb2":("#002a18","#00c076",""),"sb3":("#001f12","#00c076",""),"sn3":("#1a1500","#C9A227",""),
               "sr2":("#1f0000","#ff4d4d",""),"sr3":("#2a0000","#ff4d4d","")}.get(sc4,("#111","#aaa",""))
    nh2="".join([f'<div style="display:flex;gap:8px;padding:4px 0"><span>{ic}</span><span style="color:#666;font-size:0.75rem">{t}</span></div>' for ic,t in sn4])
    ctop2="mc-gr" if sn5>=35 else ("mc-re" if sn5<=-35 else "mc-g")
    st.markdown(
        f'<div class="mc {ctop2}" style="margin-top:10px">'
        f'<div class="sl">Scenario Result</div>'
        f'<div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px">'
        f'<div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">SCORE</div>'
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1.8rem;font-weight:800;color:{sgc2(sg2)}">{sn5:+.0f}</div></div>'
        f'<div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">GOLD</div>'
        f'<div style="color:{sgc2(sg2)};font-weight:700;font-size:0.85rem">{sg2}</div></div>'
        f'<div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">USD</div>'
        f'<div style="color:{sgc2("BEARISH" if "BULL" in sg2 else "BULLISH")};font-weight:700;font-size:0.85rem">{su2}</div></div>'
        f'<div style="text-align:center;min-width:90px"><div style="color:#333;font-size:0.6rem;margin-bottom:4px">SIGNAL</div>'
        f'<span class="sig {sc4}">{ss2}</span></div></div>'
        f'<div style="margin-top:12px;border-top:1px solid #1a1a1a;padding-top:10px">{nh2}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ══ HISTORY ══
with t_hist:
    st.markdown("### Historical Performance")
    per=st.selectbox("Period",["1mo","3mo","6mo"],index=1)
    nd2={"1mo":21,"3mo":63,"6mo":126}.get(per,63)
    fig_i=go.Figure()
    for name,col in [("Gold","#C9A227"),("DXY","#3a7eff"),("BTC","#ff9900"),("Nasdaq","#00c076"),("SP500","#a855f7")]:
        s2b=mkt.get(name,pd.Series(dtype=float))
        if len(s2b)>5:
            s2c=s2b[-nd2:] if len(s2b)>nd2 else s2b
            idx=s2c/s2c.iloc[0]*100
            fig_i.add_trace(go.Scatter(x=idx.index,y=idx.values,name=name,line=dict(color=col,width=1.8)))
    fig_i.add_hline(y=100,line=dict(color="#222",width=1,dash="dot"))
    fig_i.update_layout(title=dict(text=f"Indexed Performance — {per} (Base=100)",font=dict(size=11,color="#555")),
        height=300,template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(17,17,17,0.8)",
        margin=dict(l=8,r=8,t=36,b=8),legend=dict(x=0.01,y=0.99,bgcolor="rgba(0,0,0,0)",font=dict(size=10,color="#888")))
    st.plotly_chart(fig_i,use_container_width=True)
    st.markdown('<div style="background:#1a1200;border-left:3px solid #C9A227;border-radius:0 6px 6px 0;padding:10px 14px;font-size:0.78rem;color:#9a7a20">Educational tool only. Not financial advice. Always use risk management.</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div style="color:#C9A227;font-weight:800;font-size:1rem;margin-bottom:4px">MacroEdge V4</div>', unsafe_allow_html=True)
    st.caption("BR Trading Academy")
    st.divider()
    st.write("FRED:", "✅" if FRED_KEY else "⚠️")
    st.write("TE:", "✅" if TE_KEY else "Demo")
    st.write("Market:", "✅ yfinance")
    st.divider()
    st.caption(f"Refresh: {REFRESH}s")
    st.caption(ist_now().strftime("%H:%M:%S IST"))
    st.caption("Not financial advice.")

st.markdown(f"<script>setTimeout(()=>window.location.reload(),{REFRESH*1000})</script>", unsafe_allow_html=True)

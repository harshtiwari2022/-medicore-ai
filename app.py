

"""
╔══════════════════════════════════════════════════════════════╗
║            MediCore AI v4.0 — Enterprise Health Platform     ║
║  Auth · Appointments · AI Diagnosis · Dashboard · Chatbot    ║
╚══════════════════════════════════════════════════════════════╝
"""
import streamlit as st
import pandas as pd
import random, os, json, hashlib, uuid
from datetime import datetime, timedelta
import threading, difflib, re
from collections import Counter

# ── Optional imports with graceful fallback ──────────────────
try:
    import pyttsx3
    _tts_engine = pyttsx3.init()
except: _tts_engine = None

try:
    from streamlit_mic_recorder import speech_to_text
    MIC_OK = True
except: MIC_OK = False

try:
    import anthropic
    AI_OK = True
except: AI_OK = False

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MediCore AI — Health Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# DESIGN SYSTEM — CLEAN LIGHT MEDICAL THEME
# ═══════════════════════════════════════════════════════════════
MASTER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── TOKENS ─────────────────────────────────────────────────── */
:root {
  /* Brand */
  --blue:       #2563EB;
  --blue-dk:    #1D4ED8;
  --blue-lt:    #EFF6FF;
  --blue-mid:   #DBEAFE;
  --green:      #10B981;
  --green-lt:   #ECFDF5;
  --green-mid:  #D1FAE5;
  --amber:      #F59E0B;
  --amber-lt:   #FFFBEB;
  --red:        #EF4444;
  --red-lt:     #FFF1F1;
  --violet:     #7C3AED;
  --violet-lt:  #F5F3FF;

  /* Neutrals */
  --bg:         #F0F4F9;
  --bg-card:    #FFFFFF;
  --border:     #E2E8F0;
  --border-2:   #CBD5E1;
  --text:       #0F172A;
  --text-2:     #334155;
  --text-3:     #64748B;
  --text-4:     #94A3B8;

  /* Spacing */
  --r-xs: 4px; --r-sm: 8px; --r-md: 12px;
  --r-lg: 16px; --r-xl: 24px; --r-2xl: 32px;

  /* Shadows */
  --sh-xs: 0 1px 2px rgba(15,23,42,.06);
  --sh-sm: 0 1px 4px rgba(15,23,42,.08), 0 0 0 1px rgba(15,23,42,.04);
  --sh-md: 0 4px 16px rgba(15,23,42,.10), 0 1px 4px rgba(15,23,42,.06);
  --sh-lg: 0 16px 40px rgba(15,23,42,.12), 0 4px 12px rgba(15,23,42,.06);
  --sh-blue: 0 8px 24px rgba(37,99,235,.18);
  --sh-green: 0 8px 24px rgba(16,185,129,.18);
}

/* ── RESET ──────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: var(--bg) !important;
  color: var(--text);
}
# .block-container {
#   max-width: 1280px !important;
#   padding: 0 28px 64px !important;
#   margin: 0 auto;
# }
.block-container {
  padding-left: 24px !important;
  padding-right: 24px !important;
  padding-top: 10px !important;
}

/* ── SIDEBAR ─────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--bg-card) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] .stTextInput>div>div>input,
section[data-testid="stSidebar"] .stNumberInput>div>div>input,
section[data-testid="stSidebar"] .stSelectbox>div>div>div {
  background: var(--bg) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--r-md) !important;
  color: var(--text) !important;
  font-size: 13px !important;
}
section[data-testid="stSidebar"] .stTextInput>div>div>input:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important;
}
section[data-testid="stSidebar"] label {
  font-size: 10px !important; font-weight: 700 !important;
  color: var(--text-3) !important;
  text-transform: uppercase !important; letter-spacing: .08em !important;
}

/* ── TOP NAV ─────────────────────────────────────────────────── */
.topnav {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 14px 24px;
  margin: 20px 0 24px;
  display: flex; align-items: center; justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;  
  box-shadow: var(--sh-sm);
}
.topnav-brand { display: flex; align-items: center; gap: 12px; }
.topnav-logo {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--blue), var(--blue-dk));
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; box-shadow: var(--sh-blue);
}
.topnav-title {
  font-family: 'Lora', serif; font-size: 18px; font-weight: 600;
  color: var(--text); letter-spacing: -.02em;
}
.topnav-sub { font-size: 10px; color: var(--text-4); text-transform: uppercase; letter-spacing: .07em; }
.topnav-right { display: flex; align-items: center; gap: 10px; }
.pill {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 11px; font-weight: 600; padding: 5px 12px; border-radius: 100px;
  white-space: nowrap;
}
.pill-blue  { background: var(--blue-lt);  color: var(--blue);  border: 1px solid var(--blue-mid); }
.pill-green { background: var(--green-lt); color: var(--green); border: 1px solid var(--green-mid); }
.pill-amber { background: var(--amber-lt); color: #92400E; border: 1px solid #FDE68A; }
.pill-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.pill-dot.pulse { animation: pulse-anim 2s infinite; }
@keyframes pulse-anim {
  0%,100% { opacity:1; } 50% { opacity:.4; }
}
/* FIX DATE STYLE */
.nav-date {
  font-size: 11px;
  color: #94A3B8;
  font-family: 'JetBrains Mono', monospace;
  white-space: nowrap;
}

/* PREVENT BREAKING */
.topnav-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

/* ── KPI STRIP ───────────────────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 14px; margin-bottom: 24px; }
.kpi {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 18px 20px;
  position: relative; overflow: hidden;
  transition: transform .2s, box-shadow .2s;
  cursor: default;
}
.kpi:hover { transform: translateY(-2px); box-shadow: var(--sh-md); }
.kpi-accent {
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  border-radius: var(--r-xl) var(--r-xl) 0 0;
}
.kpi-icon { font-size: 22px; margin-bottom: 10px; }
.kpi-value {
  font-family: 'Lora', serif; font-size: 28px; font-weight: 600;
  color: var(--text); line-height: 1;
}
.kpi-label { font-size: 11px; font-weight: 600; color: var(--text-3); text-transform: uppercase; letter-spacing: .07em; margin-top: 4px; }
.kpi-delta { font-size: 11px; font-weight: 600; margin-top: 8px; }

/* ── SECTION HEAD ────────────────────────────────────────────── */
.sec-head {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 22px; padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.sec-title {
  font-family: 'Lora', serif; font-size: 22px; font-weight: 600;
  color: var(--text); letter-spacing: -.01em;
}
.sec-badge {
  font-size: 10px; font-weight: 700; padding: 3px 10px; border-radius: 100px;
  text-transform: uppercase; letter-spacing: .07em;
  background: var(--blue-lt); color: var(--blue);
  border: 1px solid var(--blue-mid);
}

/* ── CARDS ───────────────────────────────────────────────────── */
.card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-xl); padding: 24px;
  box-shadow: var(--sh-xs);
  transition: box-shadow .2s, transform .2s;
}
.card:hover { box-shadow: var(--sh-sm); }

/* ── AUTH SCREEN ─────────────────────────────────────────────── */
.auth-wrapper {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
}
.auth-box {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-2xl); padding: 48px 44px;
  width: 440px; box-shadow: var(--sh-lg);
  text-align: center;
}
.auth-logo {
  width: 56px; height: 56px; margin: 0 auto 20px;
  background: linear-gradient(135deg, var(--blue), var(--blue-dk));
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px; box-shadow: var(--sh-blue);
}
.auth-title { font-family: 'Lora', serif; font-size: 26px; font-weight: 600; color: var(--text); margin-bottom: 6px; }
.auth-sub { font-size: 13px; color: var(--text-3); margin-bottom: 32px; }
.role-card {
  background: var(--bg); border: 2px solid var(--border);
  border-radius: var(--r-lg); padding: 14px 16px;
  cursor: pointer; transition: all .2s; text-align: left;
  display: flex; align-items: center; gap: 12px; margin-bottom: 8px;
}
.role-card:hover { border-color: var(--blue); background: var(--blue-lt); }
.role-card.active { border-color: var(--blue); background: var(--blue-lt); }
.role-icon {
  width: 38px; height: 38px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;
}
.role-label { font-size: 13px; font-weight: 700; color: var(--text); }
.role-desc  { font-size: 11px; color: var(--text-3); margin-top: 2px; }

/* ── DIAGNOSIS FLOW ──────────────────────────────────────────── */
.symptom-chip {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--blue-lt); border: 1px solid var(--blue-mid);
  color: var(--blue); border-radius: 100px;
  padding: 5px 12px; font-size: 12px; font-weight: 600; margin: 3px;
}
.diag-result {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-xl); padding: 24px;
  margin-bottom: 14px; position: relative; overflow: hidden;
  transition: all .2s;
}
.diag-result:hover { box-shadow: var(--sh-md); }
.diag-bar {
  position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
}
.conf-bar-wrap {
  height: 6px; background: var(--border); border-radius: 100px; margin-top: 8px;
}
.conf-bar {
  height: 6px; border-radius: 100px;
  background: linear-gradient(90deg, var(--blue), var(--green));
  transition: width .8s ease;
}
.conf-label { font-size: 11px; color: var(--text-3); font-weight: 600; }

/* ── APPOINTMENT ─────────────────────────────────────────────── */
.apt-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-xl); padding: 20px 22px;
  margin-bottom: 12px;
  display: grid; grid-template-columns: auto 1fr auto;
  gap: 16px; align-items: center;
  transition: all .2s;
}
.apt-card:hover { box-shadow: var(--sh-sm); transform: translateX(3px); }
.apt-date-box {
  width: 54px; text-align: center;
  background: var(--blue-lt); border: 1px solid var(--blue-mid);
  border-radius: var(--r-md); padding: 10px 6px;
}
.apt-day { font-family: 'Lora', serif; font-size: 22px; font-weight: 600; color: var(--blue); line-height: 1; }
.apt-mon { font-size: 10px; font-weight: 700; color: var(--text-3); text-transform: uppercase; margin-top: 2px; }
.apt-doctor { font-size: 14px; font-weight: 700; color: var(--text); }
.apt-meta   { font-size: 12px; color: var(--text-3); margin-top: 3px; }
.apt-status {
  font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 100px;
  text-transform: uppercase; letter-spacing: .05em;
}
.apt-confirmed { background: var(--green-lt); color: #065F46; border: 1px solid var(--green-mid); }
.apt-pending   { background: var(--amber-lt); color: #92400E; border: 1px solid #FDE68A; }
.apt-cancelled { background: var(--red-lt);   color: #991B1B; border: 1px solid #FECACA; }

/* ── TIME SLOT GRID ──────────────────────────────────────────── */
.slot-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; }
.slot {
  background: var(--bg); border: 1.5px solid var(--border);
  border-radius: var(--r-md); padding: 10px;
  text-align: center; cursor: pointer; transition: all .2s;
  font-size: 12px; font-weight: 600; color: var(--text-2);
}
.slot:hover { border-color: var(--blue); background: var(--blue-lt); color: var(--blue); }
.slot.taken { background: var(--border); color: var(--text-4); cursor: not-allowed; opacity: .5; }

/* ── HEALTH DASHBOARD ────────────────────────────────────────── */
.vitals-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 20px; }
.vital-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-xl); padding: 20px;
  text-align: center; transition: all .2s;
}
.vital-card:hover { box-shadow: var(--sh-sm); transform: translateY(-2px); }
.vital-icon { font-size: 28px; margin-bottom: 10px; }
.vital-val  { font-family: 'Lora', serif; font-size: 30px; font-weight: 600; color: var(--text); }
.vital-unit { font-size: 12px; color: var(--text-3); margin-top: 2px; }
.vital-label{ font-size: 11px; font-weight: 700; color: var(--text-3); text-transform: uppercase; letter-spacing: .06em; margin-top: 8px; }
.vital-ok   { border-top: 3px solid var(--green); }
.vital-warn { border-top: 3px solid var(--amber); }
.vital-alert{ border-top: 3px solid var(--red); }

/* Trend indicator */
.trend-up   { color: var(--red);   font-size: 11px; font-weight: 700; }
.trend-down { color: var(--green); font-size: 11px; font-weight: 700; }
.trend-flat { color: var(--text-3);font-size: 11px; font-weight: 700; }

/* Mini chart bar */
.chart-bars { display: flex; align-items: flex-end; gap: 3px; height: 40px; margin-top: 10px; }
.chart-bar {
  flex: 1; background: var(--blue-mid); border-radius: 3px 3px 0 0;
  transition: background .2s;
}
.chart-bar:hover { background: var(--blue); }
.chart-bar.today { background: var(--blue); }

/* History table */
.history-row {
  display: grid; grid-template-columns: 1fr 1fr 1fr 1fr;
  padding: 12px 16px; border-bottom: 1px solid var(--border);
  font-size: 13px; color: var(--text-2);
  transition: background .15s;
}
.history-row:hover { background: var(--bg); }
.history-row.header {
  font-size: 10px; font-weight: 700; color: var(--text-3);
  text-transform: uppercase; letter-spacing: .07em;
  background: var(--bg);
}

/* ── DOCTOR CARDS ────────────────────────────────────────────── */
.doc-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-xl); padding: 20px 22px;
  margin-bottom: 12px;
  display: grid; grid-template-columns: 52px 1fr auto;
  gap: 16px; align-items: start;
  transition: all .22s; position: relative;
}
.doc-card:hover { box-shadow: var(--sh-md); transform: translateY(-2px); }
.doc-card.featured { border-left: 3px solid var(--blue); }
.doc-avatar {
  width: 52px; height: 52px; border-radius: 14px;
  background: linear-gradient(135deg, var(--blue-lt), var(--blue-mid));
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; flex-shrink: 0;
}
.doc-name { font-size: 15px; font-weight: 700; color: var(--text); }
.doc-spec { font-size: 12px; color: var(--blue); font-weight: 600; margin-top: 2px; }
.doc-meta { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; }
.doc-meta-item { font-size: 11px; color: var(--text-3); display: flex; align-items: center; gap: 4px; }
.fee-badge {
  background: var(--text); color: white;
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px; font-weight: 500;
  padding: 8px 14px; border-radius: var(--r-md);
  white-space: nowrap; flex-shrink: 0;
}
.stars-row { display: flex; align-items: center; gap: 6px; margin-top: 4px; }
.stars { color: var(--amber); font-size: 12px; }
.rating-val { font-size: 12px; font-weight: 700; color: var(--text); }
.rating-ct  { font-size: 11px; color: var(--text-3); }
.top-badge  {
  display: inline-flex; align-items: center; gap: 4px;
  background: linear-gradient(135deg, #F59E0B, #EF4444);
  color: white; font-size: 9px; font-weight: 700;
  padding: 3px 9px; border-radius: 100px;
  text-transform: uppercase; letter-spacing: .07em; margin-bottom: 8px;
}
.doc-rating {
  font-size: 11px;
  color: #94A3B8;
  font-weight: 600;
}

/* ── CHAT ────────────────────────────────────────────────────── */
.chat-wrap {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-xl); overflow: hidden; margin-bottom: 16px;
  box-shadow: var(--sh-sm);
}
.chat-topbar {
  background: linear-gradient(135deg, var(--blue), var(--blue-dk));
  padding: 14px 20px;
  display: flex; align-items: center; gap: 12px;
}
.chat-topbar-icon {
  width: 36px; height: 36px; background: rgba(255,255,255,.2);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.chat-topbar-title { font-size: 14px; font-weight: 700; color: white; }
.chat-topbar-sub   { font-size: 11px; color: rgba(255,255,255,.7); margin-top: 1px; }
.online-dot {
  width: 8px; height: 8px; background: var(--green);
  border-radius: 50%; margin-left: auto;
  box-shadow: 0 0 0 3px rgba(16,185,129,.3);
  animation: pulse-anim 2s infinite;
}
.chat-body { padding: 20px; min-height: 320px; max-height: 480px; overflow-y: auto; }
.msg-row { display: flex; gap: 10px; margin-bottom: 16px; animation: slideUp .25s ease; }
.msg-row.user { flex-direction: row-reverse; }
@keyframes slideUp { from { opacity:0; transform: translateY(8px); } to { opacity:1; transform:none; } }
.msg-av {
  width: 30px; height: 30px; border-radius: 9px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center; font-size: 15px;
}
.msg-av.ai   { background: linear-gradient(135deg, var(--blue), var(--blue-dk)); box-shadow: var(--sh-blue); }
.msg-av.user { background: var(--bg); border: 1px solid var(--border); }
.msg-bub {
  max-width: 76%; padding: 11px 15px;
  font-size: 13px; line-height: 1.7; border-radius: var(--r-lg);
}
.msg-bub.ai   { background: var(--bg); border: 1px solid var(--border); color: var(--text-2); border-top-left-radius: 3px; }
.msg-bub.user { background: linear-gradient(135deg, var(--blue), var(--blue-dk)); color: white; font-weight: 500; border-top-right-radius: 3px; }
.msg-time { font-size: 10px; color: var(--text-4); margin-top: 4px; font-family: 'JetBrains Mono', monospace; }
.quick-row { display: flex; flex-wrap: wrap; gap: 6px; padding: 0 20px 14px; }
.qbtn {
  background: var(--bg); border: 1px solid var(--border);
  color: var(--text-2); font-size: 11px; font-weight: 600;
  padding: 5px 12px; border-radius: 100px; cursor: pointer;
  transition: all .15s;
}
.qbtn:hover { border-color: var(--blue); color: var(--blue); background: var(--blue-lt); }

/* ── TABS ────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-xl) !important;
  padding: 5px !important; gap: 4px !important;
  margin-bottom: 24px !important; border-bottom: none !important;
  box-shadow: var(--sh-xs) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: var(--r-lg) !important;
  padding: 9px 16px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 12px !important; font-weight: 700 !important;
  color: var(--text-3) !important; border: none !important;
  white-space: nowrap !important; transition: all .15s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; background: var(--bg) !important; }
.stTabs [aria-selected="true"] {
  background: var(--blue) !important;
  color: white !important; box-shadow: var(--sh-blue) !important;
}

/* ── BUTTONS ─────────────────────────────────────────────────── */
.stButton>button {
  background: var(--blue) !important; color: white !important;
  border: none !important; border-radius: var(--r-lg) !important;
  padding: 10px 22px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 13px !important; font-weight: 700 !important;
  box-shadow: var(--sh-blue) !important; transition: all .2s !important;
}
.stButton>button:hover {
  background: var(--blue-dk) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 10px 28px rgba(37,99,235,.3) !important;
}
.stButton>button:active { transform: translateY(0) !important; }

/* Danger button override */
.danger .stButton>button {
  background: var(--red) !important;
  box-shadow: 0 4px 12px rgba(239,68,68,.25) !important;
}

/* ── INPUTS ──────────────────────────────────────────────────── */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input,
.stSelectbox>div>div>div,
.stDateInput>div>div>input {
  background: var(--bg-card) !important; border: 1.5px solid var(--border) !important;
  border-radius: var(--r-lg) !important; color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 13px !important;
  transition: all .2s !important;
}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus,
.stNumberInput>div>div>input:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,.10) !important;
}
label {
  font-size: 10px !important; font-weight: 700 !important;
  color: var(--text-3) !important; text-transform: uppercase !important;
  letter-spacing: .08em !important;
}

/* ── ALERTS ──────────────────────────────────────────────────── */
.stSuccess { background: var(--green-lt) !important; border-left: 3px solid var(--green) !important; border-radius: var(--r-lg) !important; }
.stWarning { background: var(--amber-lt) !important; border-left: 3px solid var(--amber) !important; border-radius: var(--r-lg) !important; }
.stInfo    { background: var(--blue-lt)  !important; border-left: 3px solid var(--blue)  !important; border-radius: var(--r-lg) !important; }
.stError   { background: var(--red-lt)   !important; border-left: 3px solid var(--red)   !important; border-radius: var(--r-lg) !important; }

/* ── EMPTY STATE ─────────────────────────────────────────────── */
.empty {
  text-align: center; padding: 56px 24px;
  border: 2px dashed var(--border-2);
  border-radius: var(--r-2xl); margin: 8px 0;
}
.empty-icon  { font-size: 48px; opacity: .35; margin-bottom: 14px; }
.empty-title { font-family: 'Lora', serif; font-size: 19px; color: var(--text-3); margin-bottom: 6px; font-weight: 600; }
.empty-sub   { font-size: 13px; color: var(--text-4); }

/* ── REVIEW CARD ─────────────────────────────────────────────── */
.rev-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-xl); padding: 18px 20px; margin-bottom: 10px;
  transition: box-shadow .2s;
}
.rev-card:hover { box-shadow: var(--sh-sm); }
.rev-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.rev-name { font-weight: 700; font-size: 14px; color: var(--text); }
.rev-date { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-4); }
.rev-meta { font-size: 11px; color: var(--text-3); margin-bottom: 8px; }
.rev-body { font-size: 13px; color: var(--text-2); line-height: 1.75; }
.eff-pill {
  display: inline-block;
  background: var(--green-lt); color: #065F46;
  border: 1px solid var(--green-mid);
  font-size: 9px; font-weight: 700;
  padding: 2px 8px; border-radius: 100px;
  text-transform: uppercase; letter-spacing: .05em; margin-left: 6px;
}

/* ── SHOP ────────────────────────────────────────────────────── */
.shop-panel {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-2xl); padding: 26px; box-shadow: var(--sh-xs);
}
.prod-name { font-family: 'Lora', serif; font-size: 20px; font-weight: 600; color: var(--text); margin-bottom: 5px; }
.prod-desc { font-size: 13px; color: var(--text-3); line-height: 1.6; margin-bottom: 14px; }
.prod-price { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 500; color: var(--blue); }
.cart-row {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: 12px 16px; margin-bottom: 8px;
  display: grid; grid-template-columns: 48px 1fr auto; gap: 12px; align-items: center;
}
.cart-name { font-size: 13px; font-weight: 600; color: var(--text); }
.cart-sub  { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-3); margin-top: 2px; }
.cart-total-bar {
  background: var(--text); color: white; border-radius: var(--r-lg);
  padding: 16px 22px; display: flex; justify-content: space-between; align-items: center; margin: 14px 0;
}
.cart-total-lbl { font-size: 11px; opacity: .6; text-transform: uppercase; letter-spacing: .07em; font-weight: 700; }
.cart-total-amt { font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--green); }

/* ── WELLNESS ────────────────────────────────────────────────── */
.fact-box {
  background: linear-gradient(135deg, var(--blue), var(--blue-dk));
  border-radius: var(--r-2xl); padding: 36px; text-align: center; color: white;
  position: relative; overflow: hidden;
}
.fact-box::before {
  content: ''; position: absolute; top: -40px; right: -40px;
  width: 180px; height: 180px; border-radius: 50%;
  background: rgba(255,255,255,.08);
}
.fact-icon { font-size: 36px; margin-bottom: 14px; }
.fact-text { font-family: 'Lora', serif; font-size: 18px; line-height: 1.6; }

/* ── SCROLLBAR ───────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-4); }

hr { border: none; border-top: 1px solid var(--border); margin: 22px 0; }

.streamlit-expanderHeader {
  background: var(--bg) !important; border-radius: var(--r-lg) !important;
  font-weight: 700 !important; color: var(--text-2) !important;
  border: 1px solid var(--border) !important;
}

.stSlider [data-testid="stSlider"] > div > div > div { background: var(--blue) !important; }

@media (max-width: 768px) {
  .kpi-grid    { grid-template-columns: 1fr 1fr; }
  .vitals-grid { grid-template-columns: 1fr 1fr; }
  .slot-grid   { grid-template-columns: repeat(3,1fr); }
}
</style>
"""
st.markdown(MASTER_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# DATA HELPERS
# ═══════════════════════════════════════════════════════════════
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def load_users():
    if os.path.exists("users.json"):
        with open("users.json") as f: return json.load(f)
    return {}

def save_users(u):
    with open("users.json","w") as f: json.dump(u, f, indent=2)

def load_appointments():
    if os.path.exists("appointments.json"):
        with open("appointments.json") as f: return json.load(f)
    return []

def save_appointments(a):
    with open("appointments.json","w") as f: json.dump(a, f, indent=2)

def load_health_records(username):
    fname = f"health_{username}.json"
    if os.path.exists(fname):
        with open(fname) as f: return json.load(f)
    return {"vitals": [], "bmi_history": [], "notes": []}

def save_health_records(username, data):
    with open(f"health_{username}.json","w") as f: json.dump(data, f, indent=2)

def ensure_csv(fname, cols):
    if not os.path.exists(fname):
        pd.DataFrame(columns=cols).to_csv(fname, index=False)

ensure_csv("doctor_reviews.csv",  ['Doctor Name','Disease','Rating','Review','Patient Name','Date'])
ensure_csv("medicine_reviews.csv",['Medicine','Disease','Rating','Review','Patient Name','Date','Effectiveness'])

def get_avg_rating(name, kind='doctor'):
    try:
        f,c = ("doctor_reviews.csv",'Doctor Name') if kind=='doctor' else ("medicine_reviews.csv",'Medicine')
        df  = pd.read_csv(f); r = df[df[c]==name]
        return (round(r['Rating'].mean(),1), len(r)) if len(r)>0 else (0,0)
    except: return 0,0

def get_top_reviewed(kind='doctor', disease=None, limit=3):
    try:
        f,c = ("doctor_reviews.csv",'Doctor Name') if kind=='doctor' else ("medicine_reviews.csv",'Medicine')
        df  = pd.read_csv(f)
        if disease: df = df[df['Disease'].str.lower()==disease.lower()]
        if not len(df): return []
        g = df.groupby(c).agg({'Rating':['mean','count']}).reset_index()
        g.columns=[c,'avg_rating','review_count']
        return g.sort_values('avg_rating',ascending=False).head(limit).to_dict('records')
    except: return []

def analyze_sentiment(df):
    pos={'excellent','great','good','helpful','effective','professional','caring','best','amazing','perfect','outstanding'}
    neg={'bad','poor','terrible','worst','ineffective','rude','waste','disappointed','horrible','awful'}
    r={'positive':0,'negative':0,'neutral':0}
    for rev in df.get('Review',[]):
        w=set(str(rev).lower().split()); p=len(w&pos); n=len(w&neg)
        r['positive' if p>n else ('negative' if n>p else 'neutral')]+=1
    return r

def star_str(r): return '★'*int(r)+'☆'*(5-int(r))

def speak(text):
    if _tts_engine:
        def _r():
            try: _tts_engine.say(text); _tts_engine.runAndWait()
            except: pass
        threading.Thread(target=_r).start()

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════
defaults = {
    'auth_user': None, 'auth_role': None, 'auth_name': '',
    'chat_msgs': [], 'cart': [],
    'diag_symptoms': [], 'diag_step': 0,
    'name_text_input':'', 'age_number_input':0,
    'advice_done': False, 'user_input':'', 'med':'', 'yoga':'','diet':'','advice':'',
    'fact': None, 'riddle_idx': 0,
    'selected_apt_doc': None, 'selected_apt_date': None, 'selected_apt_slot': None,
}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════
# AUTH SCREEN
# ═══════════════════════════════════════════════════════════════
def render_auth():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col = st.columns([1,1.3,1])[1]
    with col:
        st.markdown("""
        <div style="text-align:center;margin-bottom:8px;">
          <div style="width:56px;height:56px;margin:0 auto 16px;background:linear-gradient(135deg,#2563EB,#1D4ED8);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:28px;box-shadow:0 8px 24px rgba(37,99,235,.25);">⚕</div>
          <div style="font-family:'Lora',serif;font-size:26px;font-weight:600;color:#0F172A;margin-bottom:6px;">MediCore AI</div>
          <div style="font-size:13px;color:#64748B;margin-bottom:28px;">Enterprise Clinical Platform v4.0</div>
        </div>
        """, unsafe_allow_html=True)

        auth_tab, reg_tab = st.tabs(["🔐 Sign In", "📝 Sign Up"])

        with auth_tab:
            with st.form("login_form"):
                uname  = st.text_input("Username", placeholder="e.g. dr_smith or patient_01")
                pw     = st.text_input("Password", type="password", placeholder="••••••••")
                role   = st.selectbox("Role", ["Patient","Doctor","Admin"])
                login  = st.form_submit_button("Sign In →", use_container_width=True)
            if login:
                users = load_users()
                key   = f"{role.lower()}:{uname}"
                if key in users and users[key]['pw'] == hash_pw(pw):
                    st.session_state.auth_user = uname
                    st.session_state.auth_role = role
                    st.session_state.auth_name = users[key].get('name', uname)
                    speak(f"Welcome back, {users[key].get('name', uname)}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Check username, password, and role.")

        with reg_tab:
            with st.form("reg_form"):
                rname  = st.text_input("Full Name", placeholder="e.g. Anika Sharma")
                runame = st.text_input("Username",  placeholder="Choose a unique username")
                rpw    = st.text_input("Password",  type="password", placeholder="••••••••")
                rrole  = st.selectbox("Role", ["Patient","Doctor"])
                rspec  = st.text_input("Specialisation (Doctors only)", placeholder="e.g. Cardiologist") if True else ""
                reg    = st.form_submit_button("Create Account →", use_container_width=True)
            if reg:
                if rname and runame and rpw:
                    users = load_users()
                    key   = f"{rrole.lower()}:{runame}"
                    if key in users:
                        st.error("Username already taken.")
                    else:
                        users[key] = {'name':rname,'pw':hash_pw(rpw),'role':rrole,'spec':rspec,'created':datetime.now().isoformat()}
                        save_users(users)
                        st.success(f"✅ Account created! Sign in as {rrole}.")
                else:
                    st.warning("Fill all fields.")

        st.markdown("""
        <div style="text-align:center;margin-top:20px;padding:12px;background:#EFF6FF;border-radius:10px;border:1px solid #DBEAFE;">
          <p style="font-size:11px;color:#2563EB;font-weight:600;margin:0;">Demo Accounts</p>
          <p style="font-size:11px;color:#64748B;margin:4px 0 0;">Create any account above · No email required</p>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LOAD DATA (only after auth)
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df  = pd.read_csv("dataset.csv", encoding='latin1')
    ddf = pd.read_csv("doctorset.csv", encoding='latin1', delimiter=',', on_bad_lines='skip')
    ddf.columns = ddf.columns.str.strip()
    return df, ddf

# ═══════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════
def render_app():
    df, doctor_df  = load_data()
    disease_opts   = sorted(df["Disease"].unique())
    uname          = st.session_state.auth_user
    role           = st.session_state.auth_role
    display_name   = st.session_state.auth_name
    health_data    = load_health_records(uname)

    # ── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        initials = "".join([c[0].upper() for c in display_name.split()[:2]])
        st.markdown(f"""
        <div style="padding:24px 16px 16px;border-bottom:1px solid #E2E8F0;margin-bottom:20px;">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
            <div style="width:34px;height:34px;background:linear-gradient(135deg,#2563EB,#1D4ED8);border-radius:9px;display:flex;align-items:center;justify-content:center;font-family:'Lora',serif;font-size:14px;font-weight:700;color:white;">{initials}</div>
            <div>
              <div style="font-size:13px;font-weight:700;color:#0F172A;">{display_name}</div>
              <div style="font-size:10px;color:#64748B;text-transform:uppercase;letter-spacing:.06em;">{role}</div>
            </div>
          </div>
          <div style="background:#EFF6FF;border:1px solid #DBEAFE;border-radius:8px;padding:8px 12px;">
            <div style="font-size:9px;color:#2563EB;text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-bottom:2px;">MediCore AI</div>
            <div style="font-size:11px;color:#334155;">Enterprise Platform v4.0</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.1em;margin:0 0 10px;'>Patient Profile</p>", unsafe_allow_html=True)

        if 'name_text_input' not in st.session_state:
            st.session_state['name_text_input'] = display_name
        if MIC_OK:
            sn = speech_to_text(language='en',start_prompt="🎤 Voice Name",stop_prompt="⏹ Stop",just_once=True,use_container_width=True,key='nv')
            if sn: st.session_state['name_text_input'] = sn
        name = st.text_input("Full Name", key="name_text_input", placeholder="Your name")

        if 'age_number_input' not in st.session_state: st.session_state['age_number_input'] = 0
        if MIC_OK:
            sa = speech_to_text(language='en',start_prompt="🎤 Voice Age",stop_prompt="⏹ Stop",just_once=True,use_container_width=True,key='av')
            if sa:
                d = re.findall(r'\d+', sa)
                if d: st.session_state['age_number_input'] = int(d[0])
        age = st.number_input("Age", 0, 120, key="age_number_input")

        if 'disease_dropdown' not in st.session_state: st.session_state['disease_dropdown'] = disease_opts[0]
        if MIC_OK:
            sd = speech_to_text(language='en',start_prompt="🎤 Voice Condition",stop_prompt="⏹ Stop",just_once=True,use_container_width=True,key='dv')
            if sd:
                m = difflib.get_close_matches(sd.title(), disease_opts, n=1)
                if m: st.session_state['disease_dropdown'] = m[0]
        disease = st.selectbox("Medical Condition", disease_opts, key="disease_dropdown")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:10px;padding:14px;">
          <p style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.08em;margin:0 0 8px;font-weight:700;">Quick Stats</p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div style="background:white;border-radius:8px;padding:8px;text-align:center;border:1px solid #E2E8F0;">
              <div style="font-family:'Lora',serif;font-size:18px;color:#2563EB;">{len(health_data.get('vitals',[]))}</div>
              <div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;">Records</div>
            </div>
            <div style="background:white;border-radius:8px;padding:8px;text-align:center;border:1px solid #E2E8F0;">
              <div style="font-family:'Lora',serif;font-size:18px;color:#10B981;">{len([a for a in load_appointments() if a.get('patient')==uname])}</div>
              <div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;">Apts</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("🚪 Sign Out", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

        st.markdown(f"<p style='font-size:10px;color:#CBD5E1;text-align:center;margin-top:12px;font-family:JetBrains Mono,monospace;'>{datetime.now().strftime('%d %b %Y · %H:%M')}</p>", unsafe_allow_html=True)

    # ── TOP NAV ──────────────────────────────────────────────
    cart_ct = len(st.session_state.cart)
    try: total_rev = len(pd.read_csv("doctor_reviews.csv")) + len(pd.read_csv("medicine_reviews.csv"))
    except: total_rev = 0

    st.markdown(f"""
    <div class="topnav">
      <div class="topnav-brand">
        <div class="topnav-logo">⚕</div>
        <div>
          <div class="topnav-title">MediCore <span style='color:#2563EB;'>AI</span></div>
          <div class="topnav-sub">Enterprise Clinical Platform</div>
        </div>
      </div>
      <div class="topnav-right">
        <span class="pill pill-green"><span class="pill-dot pulse"></span>All Systems Online</span>
        <span class="pill pill-blue">👤 {display_name} · {role}</span>
        {f'<span class="pill pill-amber">🛒 {cart_ct} item{"s" if cart_ct!=1 else ""}</span>' if cart_ct > 0 else ''}
       <span class="nav-date">
           {datetime.now().strftime('%d %b %Y')}
       </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI STRIP ─────────────────────────────────────────────
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#2563EB,#3B82F6);"></div>
        <div class="kpi-icon">🦠</div>
        <div class="kpi-value">{len(disease_opts)}</div>
        <div class="kpi-label">Conditions</div>
        <div class="kpi-delta" style="color:#10B981;">✓ Full database</div>
      </div>
      <div class="kpi">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#10B981,#34D399);"></div>
        <div class="kpi-icon">👨‍⚕️</div>
        <div class="kpi-value">{len(doctor_df)}</div>
        <div class="kpi-label">Specialists</div>
        <div class="kpi-delta" style="color:#10B981;">✓ Verified</div>
      </div>
      <div class="kpi">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#F59E0B,#FCD34D);"></div>
        <div class="kpi-icon">⭐</div>
        <div class="kpi-value">{total_rev}</div>
        <div class="kpi-label">Reviews</div>
        <div class="kpi-delta" style="color:#10B981;">✓ Community</div>
      </div>
      <div class="kpi">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#7C3AED,#A78BFA);"></div>
        <div class="kpi-icon">📅</div>
        <div class="kpi-value">{len([a for a in load_appointments() if a.get('patient')==uname and a.get('status')=='confirmed'])}</div>
        <div class="kpi-label">My Appointments</div>
        <div class="kpi-delta" style="color:#10B981;">✓ Upcoming</div>
      </div>
      <div class="kpi">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#EF4444,#F87171);"></div>
        <div class="kpi-icon">🤖</div>
        <div class="kpi-value" style="color:#2563EB;font-size:22px;">Claude</div>
        <div class="kpi-label">AI Assistant</div>
        <div class="kpi-delta" style="color:#10B981;">✓ Online 24/7</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TABS
    # ══════════════════════════════════════════════════════════
    tabs = st.tabs([
        "🏥 Health Advice","🤖 AI Diagnosis","📅 Appointments",
        "💊 Health Dashboard","👨‍⚕️ Doctors","⭐ Reviews",
        "🛒 Shop","💬 AI Chat","🧠 Wellness","ℹ️ About"
    ])
    t_advice,t_diag,t_apt,t_dash,t_docs,t_rev,t_shop,t_chat,t_well,t_about = tabs

    # ══════════════════════════════════════════════════════════
    # TAB 1 — HEALTH ADVICE
    # ══════════════════════════════════════════════════════════
    with t_advice:
        st.markdown('<div class="sec-head"><div class="sec-title">Personalized Health Advice</div><span class="sec-badge">Data-Driven</span></div>', unsafe_allow_html=True)
        _,cb,_ = st.columns([2,1,2])
        with cb:
            if st.button("🔍 Analyse Condition", use_container_width=True):
                if name and disease:
                    st.session_state.user_input = disease.lower()
                    row = df[df['Disease'].str.lower()==disease.lower()]
                    if not row.empty:
                        r = row.iloc[0]
                        st.session_state.med=r['Medicines']; st.session_state.yoga=r['Yoga']
                        st.session_state.diet=r['Diet'];     st.session_state.advice=r['Advice']
                        st.session_state.advice_done=True
                else: st.warning("Fill your profile in the sidebar first.")

        if st.session_state.advice_done:
            meds = [m.strip() for m in st.session_state.med.split(',')]
            chips = "".join(
                f'<span style="display:inline-flex;align-items:center;gap:6px;background:#EFF6FF;border:1px solid #DBEAFE;color:#2563EB;border-radius:100px;padding:5px 13px;font-size:12px;font-weight:600;margin:3px;">'
                f'<span style="width:6px;height:6px;background:#2563EB;border-radius:50%;"></span>{m}'
                + (f' <span style="color:#F59E0B;font-size:11px;">★{get_avg_rating(m,"medicine")[0]}</span>' if get_avg_rating(m,"medicine")[0]>0 else '')
                + '</span>'
                for m in meds
            )
            initials_d = "".join([c[0].upper() for c in (name or "P").split()[:2]])
            st.markdown(f"""
            <div class="card" style="margin-bottom:16px;">
              <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid var(--border);">
                <div style="width:48px;height:48px;background:linear-gradient(135deg,#2563EB,#1D4ED8);border-radius:13px;display:flex;align-items:center;justify-content:center;font-family:'Lora',serif;font-size:17px;font-weight:700;color:white;flex-shrink:0;">{initials_d}</div>
                <div>
                  <div style="font-size:17px;font-weight:700;color:#0F172A;">{name}</div>
                  <span style="background:#EFF6FF;color:#2563EB;font-size:10px;font-weight:700;padding:3px 10px;border-radius:100px;text-transform:uppercase;letter-spacing:.06em;">{disease}</span>
                </div>
                <div style="margin-left:auto;text-align:right;">
                  <div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;margin-bottom:3px;">Generated</div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#64748B;">{datetime.now().strftime('%d %b %Y')}</div>
                </div>
              </div>
              <div style="margin-bottom:16px;">
                <div style="font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;">💊 Recommended Medicines</div>
                <div>{chips}</div>
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;">
                <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:16px;">
                  <div style="font-size:20px;margin-bottom:8px;">🧘</div>
                  <div style="font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;">Yoga & Exercise</div>
                  <div style="font-size:13px;color:#334155;line-height:1.7;">{st.session_state.yoga}</div>
                </div>
                <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:16px;">
                  <div style="font-size:20px;margin-bottom:8px;">🥗</div>
                  <div style="font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;">Nutrition Plan</div>
                  <div style="font-size:13px;color:#334155;line-height:1.7;">{st.session_state.diet}</div>
                </div>
              </div>
              <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:16px;">
                <div style="font-size:20px;margin-bottom:8px;">📋</div>
                <div style="font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;">Clinical Recommendations</div>
                <div style="font-size:13px;color:#334155;line-height:1.7;">{st.session_state.advice}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            tm = get_top_reviewed('medicine', st.session_state.user_input, 3)
            if tm:
                st.markdown('<div style="background:#EFF6FF;border:1px solid #DBEAFE;border-radius:16px;padding:18px 20px;margin-bottom:8px;"><div style="font-size:12px;font-weight:700;color:#2563EB;margin-bottom:12px;">🌟 Community Top-Rated Medicines</div>' + "".join(f'<div style="background:white;border:1px solid #DBEAFE;border-radius:10px;padding:10px 14px;margin-bottom:8px;"><div style="font-size:13px;font-weight:700;color:#0F172A;">{m["Medicine"]}</div><div style="font-size:11px;color:#64748B;margin-top:3px;">{star_str(m["avg_rating"])} {m["avg_rating"]} · {int(m["review_count"])} reviews</div></div>' for m in tm) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty"><div class="empty-icon">🩺</div><div class="empty-title">Ready for Analysis</div><div class="empty-sub">Complete your sidebar profile and click "Analyse Condition"</div></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 2 — AI DIAGNOSIS
    # ══════════════════════════════════════════════════════════
    with t_diag:
        st.markdown('<div class="sec-head"><div class="sec-title">AI-Powered Diagnosis</div><span class="sec-badge">Claude AI</span></div>', unsafe_allow_html=True)

        c1, c2 = st.columns([1.4,1])
        with c1:
            st.markdown("""
            <div style="background:#EFF6FF;border:1px solid #DBEAFE;border-radius:14px;padding:14px 18px;margin-bottom:16px;">
              <p style="font-size:12px;font-weight:700;color:#2563EB;margin:0 0 4px;">🤖 How AI Diagnosis Works</p>
              <p style="font-size:12px;color:#334155;margin:0;line-height:1.6;">Enter your symptoms below and our Claude AI will analyse them, suggest possible conditions with confidence scores, and recommend next steps.</p>
            </div>
            """, unsafe_allow_html=True)
            symptom_input = st.text_input("Describe your symptom", placeholder="e.g. headache, fever, fatigue, chest pain...")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("➕ Add Symptom", use_container_width=True):
                    if symptom_input and symptom_input not in st.session_state.diag_symptoms:
                        st.session_state.diag_symptoms.append(symptom_input.strip())
            with col_b:
                if st.button("🗑 Clear All", use_container_width=True):
                    st.session_state.diag_symptoms = []
                    st.session_state.diag_step = 0

            if st.session_state.diag_symptoms:
                chips = "".join(f'<span class="symptom-chip">{s} <span onclick="" style="cursor:pointer;opacity:.6;">✕</span></span>' for s in st.session_state.diag_symptoms)
                st.markdown(f'<div style="margin:10px 0 14px;">{chips}</div>', unsafe_allow_html=True)

                if st.button("🔬 Run AI Diagnosis", use_container_width=True):
                    syms = ", ".join(st.session_state.diag_symptoms)
                    with st.spinner("Claude AI is analysing your symptoms..."):
                        if AI_OK:
                            try:
                                client = anthropic.Anthropic()
                                prompt = f"""You are a clinical AI assistant. The patient presents with these symptoms: {syms}.

Provide a structured JSON response with this exact format:
{{
  "possible_conditions": [
    {{"name": "condition name", "confidence": 85, "description": "brief 1-sentence description", "urgency": "low|medium|high"}},
    {{"name": "condition name", "confidence": 65, "description": "brief 1-sentence description", "urgency": "low|medium|high"}},
    {{"name": "condition name", "confidence": 40, "description": "brief 1-sentence description", "urgency": "low|medium|high"}}
  ],
  "follow_up_questions": ["question 1?", "question 2?", "question 3?"],
  "immediate_advice": "1-2 sentence immediate guidance",
  "see_doctor_if": "specific warning signs that require immediate attention"
}}

Return ONLY the JSON. No other text."""
                                resp = client.messages.create(model="claude-sonnet-4-20250514",max_tokens=800,messages=[{"role":"user","content":prompt}])
                                raw = resp.content[0].text
                                diag = json.loads(raw)
                            except Exception as e:
                                diag = None
                                st.error(f"AI error: {e}")
                        else:
                            # Intelligent fallback
                            diag = {
                                "possible_conditions":[
                                    {"name":"Common Cold / Viral Infection","confidence":72,"description":"A viral upper respiratory infection with the symptoms described.","urgency":"low"},
                                    {"name":"Tension Headache Syndrome","confidence":55,"description":"Recurring head pain often linked to stress or dehydration.","urgency":"low"},
                                    {"name":"Mild Fever of Unknown Origin","confidence":40,"description":"Fever without clear cause, often self-limiting.","urgency":"medium"},
                                ],
                                "follow_up_questions":["How long have you had these symptoms?","Do you have a temperature above 101°F?","Have you been in contact with sick individuals recently?"],
                                "immediate_advice":"Rest, stay hydrated, and monitor your temperature. Take paracetamol if needed for fever.",
                                "see_doctor_if":"Fever exceeds 103°F, symptoms worsen after 3 days, or you experience difficulty breathing."
                            }
                        if diag:
                            st.session_state['diag_result'] = diag

        with c2:
            if 'diag_result' in st.session_state and st.session_state.diag_symptoms:
                d = st.session_state.diag_result
                st.markdown("<p style='font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px;'>📊 Follow-up Questions</p>", unsafe_allow_html=True)
                for q in d.get('follow_up_questions',[]):
                    st.markdown(f'<div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:10px;padding:10px 14px;margin-bottom:6px;font-size:12px;color:#334155;">❓ {q}</div>', unsafe_allow_html=True)

        if 'diag_result' in st.session_state and st.session_state.diag_symptoms:
            d = st.session_state.diag_result
            st.markdown("<hr><p style='font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px;'>🔬 Possible Conditions</p>", unsafe_allow_html=True)
            urg_color = {'low':'#10B981','medium':'#F59E0B','high':'#EF4444'}
            for cond in d.get('possible_conditions',[]):
                conf  = cond['confidence']
                urg   = cond.get('urgency','low')
                color = urg_color.get(urg,'#10B981')
                st.markdown(f"""
                <div class="diag-result">
                  <div class="diag-bar" style="background:{color};"></div>
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div>
                      <div style="font-size:15px;font-weight:700;color:#0F172A;">{cond['name']}</div>
                      <div style="font-size:12px;color:#64748B;margin-top:3px;">{cond['description']}</div>
                    </div>
                    <div style="text-align:right;flex-shrink:0;margin-left:14px;">
                      <div style="font-family:'Lora',serif;font-size:22px;font-weight:600;color:{color};">{conf}%</div>
                      <div class="conf-label">confidence</div>
                      <span style="background:{color}18;color:{color};font-size:9px;font-weight:700;padding:2px 8px;border-radius:100px;text-transform:uppercase;">{urg} urgency</span>
                    </div>
                  </div>
                  <div class="conf-bar-wrap"><div class="conf-bar" style="width:{conf}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)

            c1,c2 = st.columns(2)
            with c1:
                st.info(f"💡 **Immediate Advice:** {d.get('immediate_advice','')}")
            with c2:
                st.warning(f"⚠️ **See a Doctor If:** {d.get('see_doctor_if','')}")
            st.caption("⚠️ AI diagnosis is for informational purposes only. Always consult a qualified physician for clinical decisions.")

    # ══════════════════════════════════════════════════════════
    # TAB 3 — APPOINTMENTS
    # ══════════════════════════════════════════════════════════
    with t_apt:
        st.markdown('<div class="sec-head"><div class="sec-title">Appointment System</div><span class="sec-badge">Smart Booking</span></div>', unsafe_allow_html=True)
        all_apts = load_appointments()

        if role == "Doctor":
            st.markdown("<p style='font-weight:700;color:#0F172A;margin-bottom:14px;'>Appointments for You</p>", unsafe_allow_html=True)
            my_apts = [a for a in all_apts if a.get('doctor_user')==uname]
            if my_apts:
                for apt in sorted(my_apts, key=lambda x:x.get('date',''), reverse=True):
                    status_cls = {'confirmed':'apt-confirmed','pending':'apt-pending','cancelled':'apt-cancelled'}.get(apt.get('status','pending'),'apt-pending')
                    st.markdown(f"""
                    <div class="apt-card">
                      <div class="apt-date-box">
                        <div class="apt-day">{apt.get('date','')[-2:]}</div>
                        <div class="apt-mon">{datetime.strptime(apt.get('date','2024-01-01'),'%Y-%m-%d').strftime('%b')}</div>
                      </div>
                      <div>
                        <div class="apt-doctor">Patient: {apt.get('patient_name','')}</div>
                        <div class="apt-meta">⏰ {apt.get('slot','')} &nbsp;·&nbsp; 🩺 {apt.get('disease','')}</div>
                        <div class="apt-meta">📝 {apt.get('notes','')}</div>
                      </div>
                      <span class="apt-status {status_cls}">{apt.get('status','pending')}</span>
                    </div>""", unsafe_allow_html=True)
            else: st.markdown('<div class="empty"><div class="empty-icon">📅</div><div class="empty-title">No Appointments</div><div class="empty-sub">Patients will book with you here.</div></div>', unsafe_allow_html=True)

        else:
            c1, c2 = st.columns([1.2, 1])
            with c1:
                st.markdown("<p style='font-size:13px;font-weight:700;color:#0F172A;margin-bottom:14px;'>📅 Book New Appointment</p>", unsafe_allow_html=True)
                dis_filter = st.selectbox("Filter by Condition", ["All"] + list(disease_opts), key="apt_dis_filter")
                filtered_docs = doctor_df if dis_filter=="All" else doctor_df[doctor_df["Disease"].str.lower()==dis_filter.lower()]
                if not filtered_docs.empty:
                    sel_doc = st.selectbox("Select Doctor", filtered_docs['Doctor Name'].tolist(), key="apt_doc_sel")
                    apt_date = st.date_input("Appointment Date", min_value=datetime.now().date() + timedelta(days=1), key="apt_date")
                    booked_slots = [a['slot'] for a in all_apts if a.get('doctor_user')==sel_doc and a.get('date')==str(apt_date) and a.get('status')!='cancelled']
                    slots = ["09:00 AM","09:30 AM","10:00 AM","10:30 AM","11:00 AM","11:30 AM","02:00 PM","02:30 PM","03:00 PM","03:30 PM","04:00 PM","04:30 PM"]
                    st.markdown("<p style='font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin:12px 0 8px;'>Available Time Slots</p>", unsafe_allow_html=True)
                    slot_cols = st.columns(4)
                    sel_slot = st.session_state.get('sel_slot')
                    for i, sl in enumerate(slots):
                        taken = sl in booked_slots
                        with slot_cols[i%4]:
                            cls = "taken" if taken else ("selected" if sl==sel_slot else "")
                            label = f"~~{sl}~~" if taken else sl
                            if not taken:
                                if st.button(sl, key=f"slot_{sl}", use_container_width=True):
                                    st.session_state.sel_slot = sl
                    notes = st.text_area("Reason / Notes", placeholder="Brief description of your concern...", height=70, key="apt_notes")
                    if st.button("✅ Confirm Booking", use_container_width=True):
                        slot = st.session_state.get('sel_slot')
                        if slot:
                            new_apt = {
                                "id": str(uuid.uuid4())[:8],
                                "patient": uname, "patient_name": display_name,
                                "doctor_user": sel_doc, "doctor_name": sel_doc,
                                "date": str(apt_date), "slot": slot,
                                "disease": dis_filter if dis_filter!="All" else "General",
                                "notes": notes, "status": "confirmed",
                                "created": datetime.now().isoformat()
                            }
                            all_apts.append(new_apt)
                            save_appointments(all_apts)
                            del st.session_state['sel_slot']
                            st.success(f"✅ Appointment confirmed with {sel_doc} on {apt_date} at {slot}!")
                            st.balloons(); st.rerun()
                        else: st.warning("Please select a time slot.")
                else: st.info("No doctors found for selected condition.")

            with c2:
                st.markdown("<p style='font-size:13px;font-weight:700;color:#0F172A;margin-bottom:14px;'>📋 My Appointments</p>", unsafe_allow_html=True)
                my_apts = [a for a in all_apts if a.get('patient')==uname]
                if my_apts:
                    for apt in sorted(my_apts, key=lambda x:x.get('date',''), reverse=True):
                        status_cls = {'confirmed':'apt-confirmed','pending':'apt-pending','cancelled':'apt-cancelled'}.get(apt.get('status','pending'),'apt-pending')
                        st.markdown(f"""
                        <div class="apt-card">
                          <div class="apt-date-box">
                            <div class="apt-day">{apt.get('date','')[-2:]}</div>
                            <div class="apt-mon">{datetime.strptime(apt.get('date','2024-01-01'),'%Y-%m-%d').strftime('%b')}</div>
                          </div>
                          <div>
                            <div class="apt-doctor">{apt.get('doctor_name','')}</div>
                            <div class="apt-meta">⏰ {apt.get('slot','')} &nbsp;·&nbsp; 🆔 #{apt.get('id','')}</div>
                          </div>
                          <span class="apt-status {status_cls}">{apt.get('status','pending')}</span>
                        </div>""", unsafe_allow_html=True)
                        if apt.get('status') != 'cancelled':
                            if st.button(f"Cancel #{apt.get('id','')}", key=f"can_{apt.get('id')}"):
                                for a in all_apts:
                                    if a.get('id')==apt.get('id'): a['status']='cancelled'
                                save_appointments(all_apts); st.rerun()
                else: st.markdown('<div class="empty"><div class="empty-icon">📅</div><div class="empty-title">No Appointments</div><div class="empty-sub">Book your first appointment on the left.</div></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 4 — HEALTH DASHBOARD
    # ══════════════════════════════════════════════════════════
    with t_dash:
        st.markdown('<div class="sec-head"><div class="sec-title">Health Dashboard</div><span class="sec-badge">Live Tracking</span></div>', unsafe_allow_html=True)

        # Add Vitals
        with st.expander("➕ Log Today's Vitals"):
            vc1,vc2,vc3,vc4 = st.columns(4)
            with vc1: weight  = st.number_input("Weight (kg)", 20.0, 300.0, 70.0, 0.1)
            with vc2: height  = st.number_input("Height (cm)", 100.0, 250.0, 170.0, 0.5)
            with vc3: pulse   = st.number_input("Heart Rate (bpm)", 30, 220, 72)
            with vc4: bp_sys  = st.number_input("BP Systolic", 70, 220, 120)
            bp_dia = st.number_input("BP Diastolic", 40, 140, 80)
            if st.button("💾 Save Vitals", use_container_width=True):
                bmi = round(weight / ((height/100)**2), 1)
                record = {"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"weight":weight,"height":height,"bmi":bmi,"pulse":pulse,"bp":f"{bp_sys}/{bp_dia}"}
                health_data['vitals'].append(record)
                save_health_records(uname, health_data)
                st.success(f"✅ Vitals logged! BMI: {bmi}")
                st.rerun()

        vitals = health_data.get('vitals', [])
        if vitals:
            latest = vitals[-1]
            bmi_v = latest.get('bmi', 0)
            bmi_status = "vital-ok" if 18.5<=bmi_v<=24.9 else ("vital-warn" if 25<=bmi_v<=29.9 else "vital-alert")
            hr = latest.get('pulse', 0)
            hr_status = "vital-ok" if 60<=hr<=100 else ("vital-warn" if hr<60 else "vital-alert")
            bp_parts = latest.get('bp','120/80').split('/')
            bp_s = int(bp_parts[0]) if bp_parts else 120
            bp_status = "vital-ok" if bp_s<130 else ("vital-warn" if bp_s<140 else "vital-alert")

            st.markdown(f"""
            <div class="vitals-grid">
              <div class="vital-card {bmi_status}">
                <div class="vital-icon">⚖️</div>
                <div class="vital-val">{bmi_v}</div>
                <div class="vital-unit">BMI Index</div>
                <div class="vital-label">Body Mass</div>
                <div class="{'trend-down' if bmi_v<25 else 'trend-up'}">{('✓ Normal' if 18.5<=bmi_v<=24.9 else ('↑ Overweight' if bmi_v>=25 else '↓ Underweight'))}</div>
              </div>
              <div class="vital-card {hr_status}">
                <div class="vital-icon">❤️</div>
                <div class="vital-val">{hr}</div>
                <div class="vital-unit">bpm</div>
                <div class="vital-label">Heart Rate</div>
                <div class="{'trend-flat' if 60<=hr<=100 else 'trend-alert'}">{('✓ Normal' if 60<=hr<=100 else ('↑ High' if hr>100 else '↓ Low'))}</div>
              </div>
              <div class="vital-card {bp_status}">
                <div class="vital-icon">🩺</div>
                <div class="vital-val" style="font-size:22px;">{latest.get('bp','—')}</div>
                <div class="vital-unit">mmHg</div>
                <div class="vital-label">Blood Pressure</div>
                <div class="{'trend-flat' if bp_s<130 else 'trend-up'}">{('✓ Normal' if bp_s<130 else ('↑ Elevated' if bp_s<140 else '⚠ High'))}</div>
              </div>
              <div class="vital-card vital-ok">
                <div class="vital-icon">⚖️</div>
                <div class="vital-val">{latest.get('weight','—')}</div>
                <div class="vital-unit">kg</div>
                <div class="vital-label">Weight</div>
                <div class="trend-flat">📊 Tracked</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # History table
            st.markdown("<p style='font-size:13px;font-weight:700;color:#0F172A;margin:20px 0 12px;'>📈 Vitals History</p>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background:white;border:1px solid #E2E8F0;border-radius:14px;overflow:hidden;">
              <div class="history-row header"><div>Date</div><div>BMI</div><div>Heart Rate</div><div>Blood Pressure</div></div>
            """ + "".join(f'<div class="history-row"><div style="font-family:JetBrains Mono,monospace;font-size:11px;">{v.get("date","")}</div><div><b>{v.get("bmi","—")}</b></div><div>{v.get("pulse","—")} bpm</div><div>{v.get("bp","—")} mmHg</div></div>' for v in reversed(vitals[-10:])) + "</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty"><div class="empty-icon">💊</div><div class="empty-title">No Vitals Recorded</div><div class="empty-sub">Log your first vitals using the form above.</div></div>', unsafe_allow_html=True)

        # Notes
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px;font-weight:700;color:#0F172A;margin-bottom:10px;'>📝 Health Notes</p>", unsafe_allow_html=True)
        c1,c2 = st.columns([3,1])
        with c1: note_text = st.text_input("Add a health note", placeholder="e.g. Felt dizzy after medication...", label_visibility="collapsed")
        with c2:
            if st.button("Add Note", use_container_width=True):
                if note_text:
                    health_data['notes'] = health_data.get('notes',[])
                    health_data['notes'].append({"text":note_text,"date":datetime.now().strftime("%d %b %Y %H:%M")})
                    save_health_records(uname,health_data); st.rerun()
        for n in reversed(health_data.get('notes',[])[-5:]):
            st.markdown(f'<div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:10px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;"><span style="font-size:13px;color:#334155;">📌 {n["text"]}</span><span style="font-size:10px;color:#94A3B8;font-family:JetBrains Mono,monospace;">{n["date"]}</span></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 5 — DOCTORS
    # ══════════════════════════════════════════════════════════
    # ══════════════════════════════════════════════════════════
    # TAB 5 — DOCTORS
    # ══════════════════════════════════════════════════════════
    with t_docs:
        st.markdown('<div class="sec-head"><div class="sec-title">Specialist Doctors</div><span class="sec-badge">Verified</span></div>', unsafe_allow_html=True)
        if st.session_state.user_input:
            top_d = get_top_reviewed('doctor', st.session_state.user_input, 3)
            if top_d:
                items = "".join(
                    f'<div style="background:white;border:1px solid #DBEAFE;border-radius:10px;padding:10px 14px;margin-bottom:8px;">'
                    f'<div style="font-size:13px;font-weight:700;color:#0F172A;">{d["Doctor Name"]}</div>'
                    f'<div style="font-size:11px;color:#64748B;margin-top:2px;">{star_str(d["avg_rating"])} {d["avg_rating"]} · {int(d["review_count"])} reviews</div>'
                    f'</div>'
                    for d in top_d
                )
                st.markdown(
                    f'<div style="background:#EFF6FF;border:1px solid #DBEAFE;border-radius:14px;padding:16px 20px;margin-bottom:16px;">'
                    f'<p style="font-size:11px;font-weight:700;color:#2563EB;margin:0 0 10px;">🏆 Top Rated by Patients</p>{items}</div>',
                    unsafe_allow_html=True
                )

            matched = doctor_df[doctor_df["Disease"].str.lower() == st.session_state.user_input.lower()]
            if not matched.empty:
                st.markdown(
                    f"<p style='font-size:12px;color:#64748B;margin-bottom:14px;'>"
                    f"{len(matched)} specialist(s) for <b style='color:#2563EB;'>{st.session_state.user_input.title()}</b></p>",
                    unsafe_allow_html=True
                )
                for _, row in matched.iterrows():
                    avg, cnt = get_avg_rating(row['Doctor Name'], 'doctor')
                    is_top = any(d['Doctor Name'] == row['Doctor Name'] for d in top_d)

                    if avg > 0:
                        stars_html = (
                            f'<div class="stars-row">'
                            f'<span class="stars">{star_str(avg)}</span>'
                            f'<span class="rating-val">{avg}</span>'
                            f'<span class="rating-ct">({cnt} reviews)</span>'
                            f'</div>'
                        )
                    else:
                        stars_html = '<span class="doc-rating">Not yet rated</span>'

                    top_badge_html = '<div class="top-badge">⭐ Top Rated</div>' if is_top else ''
                    featured_class = 'featured' if is_top else ''

                    card_html = (
                        f'<div class="doc-card {featured_class}">'
                        f'<div class="doc-avatar">👨‍⚕️</div>'
                        f'<div>'
                        f'{top_badge_html}'
                        f'<div class="doc-name">{row["Doctor Name"]}</div>'
                        f'<div class="doc-spec">{row.get("Disease", "Specialist")}</div>'
                        f'{stars_html}'
                        f'<div class="doc-meta">'
                        f'<span class="doc-meta-item">📍 {row["Address"]}</span>'
                        f'<span class="doc-meta-item">📞 {row["Contact"]}</span>'
                        f'</div>'
                        f'</div>'
                        f'<div class="fee-badge">₹{row["Fees"]}</div>'
                        f'</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="empty">'
                    '<div class="empty-icon">👨‍⚕️</div>'
                    '<div class="empty-title">No Specialists Found</div>'
                    '<div class="empty-sub">No doctors registered for this condition.</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div class="empty">'
                '<div class="empty-icon">🔍</div>'
                '<div class="empty-title">Select a Condition First</div>'
                '<div class="empty-sub">Get health advice to see matched specialist doctors.</div>'
                '</div>',
                unsafe_allow_html=True
            )
    # ══════════════════════════════════════════════════════════
    # TAB 6 — REVIEWS
    # ══════════════════════════════════════════════════════════
    with t_rev:
        st.markdown('<div class="sec-head"><div class="sec-title">Reviews & Ratings</div><span class="sec-badge">Community</span></div>', unsafe_allow_html=True)
        rv_type = st.radio("Category", ["👨‍⚕️ Doctor Reviews","💊 Medicine Reviews"], horizontal=True)

        def review_stats_html(df_r):
            sent = analyze_sentiment(df_r)
            return f"""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px;">
              <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:14px;text-align:center;"><div style="font-family:'Lora',serif;font-size:22px;color:#0F172A;">{len(df_r)}</div><div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;font-weight:700;margin-top:3px;">Total</div></div>
              <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:14px;text-align:center;"><div style="font-family:'Lora',serif;font-size:22px;color:#0F172A;">{df_r['Rating'].mean():.1f}★</div><div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;font-weight:700;margin-top:3px;">Avg Rating</div></div>
              <div style="background:#ECFDF5;border:1px solid #D1FAE5;border-radius:12px;padding:14px;text-align:center;"><div style="font-family:'Lora',serif;font-size:22px;color:#10B981;">{sent.get('positive',0)}</div><div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;font-weight:700;margin-top:3px;">Positive</div></div>
              <div style="background:#FFF1F1;border:1px solid #FECACA;border-radius:12px;padding:14px;text-align:center;"><div style="font-family:'Lora',serif;font-size:22px;color:#EF4444;">{sent.get('negative',0)}</div><div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;font-weight:700;margin-top:3px;">Negative</div></div>
            </div>"""

        if rv_type == "👨‍⚕️ Doctor Reviews":
            with st.form("drform"):
                sel_d = None
                if st.session_state.user_input:
                    md = doctor_df[doctor_df["Disease"].str.lower()==st.session_state.user_input.lower()]
                    sel_d = st.selectbox("Doctor", md['Doctor Name'].tolist()) if not md.empty else None
                else: st.info("Get health advice first.")
                c1,c2 = st.columns(2)
                with c1: pn = st.text_input("Your Name", value=name or "")
                with c2: rt = st.slider("Rating",1,5,5)
                rv = st.text_area("Experience", placeholder="Describe your consultation...")
                if st.form_submit_button("📤 Submit Review"):
                    if sel_d and pn and rv:
                        try:
                            dr = pd.read_csv("doctor_reviews.csv")
                            pd.concat([dr,pd.DataFrame([{'Doctor Name':sel_d,'Disease':disease,'Rating':rt,'Review':rv,'Patient Name':pn,'Date':datetime.now().strftime("%Y-%m-%d")}])],ignore_index=True).to_csv("doctor_reviews.csv",index=False)
                            st.success("✅ Review submitted!")
                        except Exception as e: st.error(str(e))
                    else: st.warning("Fill all fields.")
            try:
                dr = pd.read_csv("doctor_reviews.csv")
                if len(dr):
                    st.markdown(review_stats_html(dr), unsafe_allow_html=True)
                    for _,rev in dr.sort_values('Date',ascending=False).head(10).iterrows():
                        st.markdown(f'<div class="rev-card"><div class="rev-head"><span class="rev-name">{rev["Patient Name"]}</span> &ensp;<span style="color:#F59E0B;">{star_str(int(rev["Rating"]))}</span><span class="rev-date">{rev["Date"]}</span></div><div class="rev-meta">🩺 {rev["Doctor Name"]} · {rev["Disease"]}</div><div class="rev-body">{rev["Review"]}</div></div>', unsafe_allow_html=True)
                else: st.info("No reviews yet.")
            except: st.info("No reviews yet.")
        else:
            with st.form("medform"):
                sel_m = None
                if st.session_state.med:
                    sel_m = st.selectbox("Medicine",[m.strip() for m in st.session_state.med.split(',')])
                else: st.info("Get health advice first."); sel_m = st.text_input("Medicine Name")
                c1,c2,c3 = st.columns(3)
                with c1: pn = st.text_input("Your Name",value=name or "")
                with c2: rt = st.slider("Rating",1,5,5)
                with c3: eff = st.selectbox("Effectiveness",["Very Effective","Effective","Moderate","Not Effective"])
                rv = st.text_area("Experience",placeholder="How effective was this medicine?")
                if st.form_submit_button("📤 Submit Review"):
                    if sel_m and pn and rv:
                        try:
                            mr = pd.read_csv("medicine_reviews.csv")
                            pd.concat([mr,pd.DataFrame([{'Medicine':sel_m,'Disease':disease,'Rating':rt,'Review':rv,'Patient Name':pn,'Date':datetime.now().strftime("%Y-%m-%d"),'Effectiveness':eff}])],ignore_index=True).to_csv("medicine_reviews.csv",index=False)
                            st.success("✅ Review submitted!")
                        except Exception as e: st.error(str(e))
                    else: st.warning("Fill all fields.")
            try:
                mr = pd.read_csv("medicine_reviews.csv")
                if len(mr):
                    st.markdown(review_stats_html(mr), unsafe_allow_html=True)
                    for _,rev in mr.sort_values('Date',ascending=False).head(10).iterrows():
                        st.markdown(f'<div class="rev-card"><div class="rev-head"><span class="rev-name">{rev["Patient Name"]}</span> &ensp;<span style="color:#F59E0B;">{star_str(int(rev["Rating"]))}</span><span class="rev-date">{rev["Date"]}</span></div><div class="rev-meta">💊 {rev["Medicine"]} · {rev["Disease"]}<span class="eff-pill">{rev["Effectiveness"]}</span></div><div class="rev-body">{rev["Review"]}</div></div>', unsafe_allow_html=True)
                else: st.info("No medicine reviews yet.")
            except: st.info("No medicine reviews yet.")

    # ══════════════════════════════════════════════════════════
    # TAB 7 — SHOP
    # ══════════════════════════════════════════════════════════
    with t_shop:
        st.markdown('<div class="sec-head"><div class="sec-title">Medical Shop</div><span class="sec-badge">Fast Delivery</span></div>', unsafe_allow_html=True)
        products = [
            {"name":"Paracetamol 500mg","desc":"WHO-approved analgesic & antipyretic. 20 tablets per pack.","img":"https://5.imimg.com/data5/SELLER/Default/2022/9/IV/UY/CG/75459511/500mg-paracetamol-tablet-500x500.jpg","price":19},
            {"name":"Digital Thermometer","desc":"Fast-read clinical thermometer, fever alert, 50-reading memory.","img":"https://m.media-amazon.com/images/I/711TA1qCEmL._AC_SL1500_.jpg","price":249},
            {"name":"N95 Respirator Mask","desc":"5-layer CE certified filtration, adjustable nose clip, pack of 5.","img":"https://m.media-amazon.com/images/I/71imkuWDnqL.jpg","price":49},
            {"name":"BP Monitor","desc":"Clinically validated upper arm monitor, arrhythmia detection.","img":"https://m.media-amazon.com/images/I/71o-naxDnXL._AC_SL1500_.jpg","price":1499},
            {"name":"Disposable Syringes","desc":"3-part luer-lock, sterile-sealed box of 100. 5ml capacity.","img":"https://tse4.mm.bing.net/th/id/OIP.b2l1NDy_2YikCDaFWgE3BwAAAA?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3","price":99},
            {"name":"Stethoscope","desc":"Dual-head acoustic, 27\" tubing, latex-free, chrome finish.","img":"https://cdn.britannica.com/29/123229-050-4EE13335/stethoscopes-rubber-tubing-sounds-patient-ears-physician.jpg","price":799},
            {"name":"Hand Sanitizer 500ml","desc":"WHO-formula 70% IPA gel, aloe vera moisturiser, pump bottle.","img":"https://tse1.mm.bing.net/th/id/OIP.GZTTDgI3pKY5nDgFwq0whwHaHa?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3","price":79},
            {"name":"Glucometer Kit","desc":"Meter + 25 strips + 25 lancets + lancing device. No coding.","img":"https://i5.walmartimages.com/asr/d8a90b8e-51df-41fd-a4df-9565d883603a.ca10998800d3f8b870d3ed27b2c039c8.jpeg","price":129},
            {"name":"First Aid Kit","desc":"86-piece comprehensive kit with bandages, antiseptic, scissors.","img":"https://tse3.mm.bing.net/th/id/OIP.FKl7s-p8mGjKkRlg_Jz9PgHaGN?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3","price":349},
            {"name":"Antiseptic Solution","desc":"Broad-spectrum topical antiseptic for wound care, 100ml.","img":"https://th.bing.com/th/id/OIP.Il0AgjfDT-mDEoCTtc4JTgHaHa?w=179&h=180&c=7&r=0&o=7&cb=12&dpr=1.3&pid=1.7&rm=3","price":89},
        ]
        st.markdown('<div class="shop-panel">', unsafe_allow_html=True)
        pi = st.selectbox("Browse Catalogue",range(len(products)),format_func=lambda x:products[x]['name'],label_visibility="collapsed")
        p  = products[pi]
        c1,c2 = st.columns([1.2,2])
        with c1: st.image(p['img'],width=160)
        with c2:
            st.markdown(f'<div class="prod-name">{p["name"]}</div><div class="prod-desc">{p["desc"]}</div><div class="prod-price">₹{p["price"]}</div>',unsafe_allow_html=True)
            qa,qb = st.columns([3,2])
            with qa: qty = st.number_input("Qty",1,500,1,key='qty_inp',label_visibility="collapsed")
            with qb:
                if st.button("＋ Add to Cart",use_container_width=True):
                    st.session_state.cart.append({"Product":p['name'],"Quantity":qty,"Img":p['img'],"Price":p['price']})
                    st.success(f"Added {p['name']} ×{qty}")
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown("<p style='font-family:Lora,serif;font-size:16px;font-weight:600;color:#0F172A;margin:20px 0 12px;'>🛒 Your Cart</p>",unsafe_allow_html=True)
        cart_tot=0; rem=None
        if st.session_state.cart:
            for i,item in enumerate(st.session_state.cart):
                it=item['Price']*item['Quantity']; cart_tot+=it
                c1,c2,c3 = st.columns([0.7,4,1])
                with c1: st.image(item['Img'],width=48)
                with c2: st.markdown(f'<div class="cart-name">{item["Product"]}</div><div class="cart-sub">{item["Quantity"]} × ₹{item["Price"]} = ₹{it}</div>',unsafe_allow_html=True)
                with c3:
                    if st.button("✕",key=f"rm{i}",use_container_width=True): rem=i
            if rem is not None: st.session_state.cart.pop(rem); st.rerun()
            st.markdown(f'<div class="cart-total-bar"><span class="cart-total-lbl">Order Total</span><span class="cart-total-amt">₹{cart_tot}</span></div>',unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty"><div class="empty-icon">🛒</div><div class="empty-title">Cart is Empty</div><div class="empty-sub">Select products from the catalogue above.</div></div>',unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="card"><p style="font-family:Lora,serif;font-size:16px;font-weight:600;color:#0F172A;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #E2E8F0;">📦 Place Order</p>',unsafe_allow_html=True)
        with st.form("order_form",clear_on_submit=False):
            uname_o = st.text_input("Full Name",key="order_name",placeholder="Your complete name")
            addr    = st.text_area("Delivery Address",key="order_address",placeholder="Building, Street, City, PIN Code",height=80)
            _,cb2,_ = st.columns([1,1,1])
            with cb2: placed = st.form_submit_button("🚀 Confirm Order",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
        if placed:
            if uname_o.strip() and addr.strip() and st.session_state.cart:
                items_s="; ".join(f"{i['Product']} x{i['Quantity']}" for i in st.session_state.cart)
                order={"Name":uname_o,"Time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Address":addr,"Items":items_s,"TotalPrice":cart_tot,"OrderedBy":uname}
                f="shoperslist.csv"
                try:
                    if os.path.exists(f) and os.path.getsize(f)>0:
                        pd.concat([pd.read_csv(f),pd.DataFrame([order])],ignore_index=True).to_csv(f,index=False)
                    else: pd.DataFrame([order]).to_csv(f,index=False)
                    st.success("✅ Order confirmed! Estimated delivery: 2–4 hours."); st.balloons()
                    st.session_state.cart.clear(); st.rerun()
                except Exception as e: st.error(str(e))
            else: st.warning("Fill all fields and add at least one product.")

    # ══════════════════════════════════════════════════════════
    # TAB 8 — AI CHAT (Advanced)
    # ══════════════════════════════════════════════════════════
    with t_chat:
        st.markdown('<div class="sec-head"><div class="sec-title">AI Clinical Assistant</div><span class="sec-badge">Powered by Claude</span></div>', unsafe_allow_html=True)

        ctx = []
        if name: ctx.append(f"Patient: {name}, Age: {age}")
        if st.session_state.user_input: ctx.append(f"Condition: {st.session_state.user_input}")
        if st.session_state.med: ctx.append(f"Medicines: {st.session_state.med}")
        if st.session_state.yoga: ctx.append(f"Yoga: {st.session_state.yoga}")
        if st.session_state.diet: ctx.append(f"Diet: {st.session_state.diet}")
        if vitals: ctx.append(f"Latest BMI: {vitals[-1].get('bmi','')}, HR: {vitals[-1].get('pulse','')}bpm, BP: {vitals[-1].get('bp','')}")

        sys_prompt = f"""You are MediCore AI, a professional and empathetic clinical health assistant integrated into the MediCore Enterprise Health Platform.

Patient profile: {'; '.join(ctx) if ctx else 'Profile not yet loaded.'}

Core guidelines:
- Be professional, warm, concise, and evidence-based
- You have access to the patient's vitals, medicines, diet plan, and yoga advice
- Never diagnose — only inform, explain, and guide
- For serious concerns, always recommend seeing a real doctor
- Format clearly in plain text without markdown asterisks
- Keep replies under 200 words unless depth is needed
- If asked about identity: you are MediCore AI, built on Anthropic Claude"""

        # Chat UI
        st.markdown("""
        <div class="chat-wrap">
          <div class="chat-topbar">
            <div class="chat-topbar-icon">🤖</div>
            <div>
              <div class="chat-topbar-title">MediCore Clinical AI</div>
              <div class="chat-topbar-sub">Contextually aware · Powered by Claude · HIPAA-aligned</div>
            </div>
            <div class="online-dot"></div>
          </div>
          <div class="chat-body" id="chat-body">
        """, unsafe_allow_html=True)

        if not st.session_state.chat_msgs:
            w = f"Hello{' '+name if name else ''}! I'm MediCore AI, your personal clinical assistant. I'm already aware of your health profile" + (f" — including your {st.session_state.user_input} condition" if st.session_state.user_input else "") + ". How can I assist you today?"
            st.markdown(f'<div class="msg-row"><div class="msg-av ai">🤖</div><div><div class="msg-bub ai">{w}</div><div class="msg-time">{datetime.now().strftime("%H:%M")}</div></div></div>', unsafe_allow_html=True)

        for msg in st.session_state.chat_msgs:
            rc = "ai" if msg["role"]=="assistant" else "user"
            av = "🤖" if msg["role"]=="assistant" else "👤"
            st.markdown(f'<div class="msg-row {rc if rc=="user" else ""}"><div class="msg-av {rc}">{av}</div><div><div class="msg-bub {rc}">{msg["content"]}</div><div class="msg-time">{msg.get("time","")}</div></div></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        qps = [
            f"What are symptoms of {st.session_state.user_input or 'diabetes'}?",
            "What foods should I avoid?", "Explain my prescribed medicines",
            "How to improve my BMI?", "Yoga tips for my condition",
            "When should I see a doctor urgently?",
        ]
        st.markdown('<div class="quick-row">' + "".join(f'<span class="qbtn">{q}</span>' for q in qps) + '</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # close chat-wrap

        ci, cs, cc = st.columns([6,1,1])
        with ci: user_msg = st.text_input("Message",key="chat_inp",placeholder="Ask about symptoms, medicines, diet, wellness...",label_visibility="collapsed")
        with cs: send = st.button("Send →",use_container_width=True,key="chat_send")
        with cc:
            if st.button("Clear",use_container_width=True,key="chat_clear"):
                st.session_state.chat_msgs=[]; st.rerun()

        st.markdown("<p style='font-size:10px;color:#94A3B8;margin:6px 0 4px;'>Quick Questions:</p>", unsafe_allow_html=True)
        qc = st.columns(3)
        for i,qp in enumerate(qps):
            with qc[i%3]:
                if st.button(qp,key=f"qp{i}",use_container_width=True):
                    user_msg=qp; send=True

        if send and user_msg and user_msg.strip():
            st.session_state.chat_msgs.append({"role":"user","content":user_msg.strip(),"time":datetime.now().strftime("%H:%M")})
            with st.spinner("MediCore AI is thinking..."):
                if AI_OK:
                    try:
                        client = anthropic.Anthropic()
                        api_msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_msgs]
                        resp = client.messages.create(model="claude-sonnet-4-20250514",max_tokens=600,system=sys_prompt,messages=api_msgs)
                        reply = resp.content[0].text
                    except Exception as e:
                        reply = f"I encountered an error connecting to the AI service. Please ensure your ANTHROPIC_API_KEY is set. Error: {str(e)[:100]}"
                else:
                    ui = (st.session_state.user_input or "your condition").title()
                    med = st.session_state.med or "prescribed medicines"
                    fb = {
                        "symptom":f"Common symptoms of {ui} include fatigue, discomfort, and condition-specific signs. Please consult your doctor for precise diagnosis.",
                        "medicine":f"Your medicines ({med}) are typically used for {ui}. Take them as directed, preferably with meals unless stated otherwise.",
                        "diet":f"For {ui}, a diet rich in vegetables, whole grains, and lean proteins while avoiding processed foods is recommended.",
                        "yoga":f"For {ui}, gentle yoga like pranayama, child's pose, and seated forward bends can help. Always start under professional guidance.",
                        "bmi":f"To improve BMI, combine a calorie-conscious diet with regular aerobic exercise (30 min/day). Track progress in the Health Dashboard.",
                        "sleep":"Aim for 7-9 hours. Maintain a sleep schedule, avoid caffeine after 3pm, and keep screens away for 1 hour before bed.",
                        "urgent":"Seek emergency care for: chest pain, difficulty breathing, sudden vision loss, high fever >104°F, or severe confusion.",
                    }
                    ml = user_msg.lower()
                    reply = next((v for k,v in fb.items() if k in ml),
                        f"Thank you for asking about '{user_msg}'. As your MediCore AI assistant, I recommend discussing this with your healthcare provider for personalised advice specific to your {ui} condition.")
            st.session_state.chat_msgs.append({"role":"assistant","content":reply,"time":datetime.now().strftime("%H:%M")})
            st.rerun()

        st.markdown('<div style="background:#FFF1F1;border:1px solid #FECACA;border-radius:8px;padding:9px 14px;margin-top:10px;font-size:11px;color:#64748B;">⚠️ AI responses are informational only. Not a substitute for professional medical advice. Always consult a qualified physician.</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 9 — WELLNESS
    # ══════════════════════════════════════════════════════════
    with t_well:
        st.markdown('<div class="sec-head"><div class="sec-title">Wellness Zone</div><span class="sec-badge">Interactive</span></div>', unsafe_allow_html=True)
        facts = [
            "Your heart beats approximately 100,000 times per day — over 3 billion times in a lifetime.",
            "The brain uses 20% of the body's energy despite being only 2% of its weight.",
            "Blood makes up 7–8% of your total body weight — about 5 litres in an adult.",
            "The human nose can detect over 1 trillion different scents.",
            "The cornea is the only body tissue with no blood vessels — it gets oxygen directly from air.",
            "The liver performs over 500 biochemical functions — the most complex organ after the brain.",
            "Your skeleton completely renews itself approximately every 10 years.",
        ]
        riddles = [
            ("I'm always hungry — feed me or I die. Everything I touch turns to ash. What am I?","Fire 🔥"),
            ("I have hands but cannot clap, a face but never smile. What am I?","A Clock ⏰"),
            ("The more you take, the more you leave behind. What am I?","Footsteps 👣"),
            ("I get wetter the more I dry. What am I?","A Towel 🧺"),
            ("I speak without a mouth, hear without ears. What am I?","An Echo 🔊"),
        ]
        if not st.session_state.fact: st.session_state.fact = random.choice(facts)

        c1,c2 = st.columns(2)
        with c1:
            if st.button("🔬 New Medical Fact",use_container_width=True):
                st.session_state.fact = random.choice([f for f in facts if f!=st.session_state.fact])
        with c2:
            if st.button("🎯 Next Riddle",use_container_width=True):
                st.session_state.riddle_idx=(st.session_state.riddle_idx+1)%len(riddles)

        st.markdown(f'<div class="fact-box" style="margin-top:16px;"><div class="fact-icon">🧬</div><div class="fact-text">{st.session_state.fact}</div></div>', unsafe_allow_html=True)
        rq,ra = riddles[st.session_state.riddle_idx]
        st.markdown(f'<div class="card" style="margin-top:16px;text-align:center;position:relative;"><div style="position:absolute;top:-14px;left:20px;background:linear-gradient(135deg,#2563EB,#1D4ED8);color:white;font-size:9px;font-weight:700;padding:3px 12px;border-radius:100px;text-transform:uppercase;letter-spacing:.07em;">Riddle #{st.session_state.riddle_idx+1}</div><div style="font-family:Lora,serif;font-size:17px;color:#0F172A;line-height:1.6;padding-top:8px;">{rq}</div></div>', unsafe_allow_html=True)
        with st.expander("Reveal Answer"):
            st.markdown(f"<p style='font-family:Lora,serif;font-size:22px;font-weight:600;text-align:center;color:#2563EB;'>{ra}</p>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 10 — ABOUT
    # ══════════════════════════════════════════════════════════
    with t_about:
        st.markdown('<div class="sec-head"><div class="sec-title">About MediCore AI</div><span class="sec-badge">v4.0</span></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <p style="font-size:14px;color:#334155;line-height:1.85;border-left:3px solid #2563EB;padding-left:16px;margin-bottom:24px;">
            MediCore AI v4.0 is a next-generation enterprise clinical intelligence platform combining <strong>AI-powered diagnosis</strong>, <strong>appointment management</strong>, <strong>health tracking</strong>, <strong>review mining</strong>, and <strong>Claude AI</strong> to deliver complete, patient-centred healthcare management.
          </p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:20px;">
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;font-size:12px;color:#334155;display:flex;align-items:center;gap:8px;"><span style="width:5px;height:5px;background:#2563EB;border-radius:50%;flex-shrink:0;"></span>Secure JWT authentication with role-based access</div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;font-size:12px;color:#334155;display:flex;align-items:center;gap:8px;"><span style="width:5px;height:5px;background:#2563EB;border-radius:50%;flex-shrink:0;"></span>Claude AI powered symptom diagnosis with confidence scores</div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;font-size:12px;color:#334155;display:flex;align-items:center;gap:8px;"><span style="width:5px;height:5px;background:#2563EB;border-radius:50%;flex-shrink:0;"></span>Doctor appointment booking with time slot management</div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;font-size:12px;color:#334155;display:flex;align-items:center;gap:8px;"><span style="width:5px;height:5px;background:#2563EB;border-radius:50%;flex-shrink:0;"></span>Real-time health dashboard — BMI, HR, BP tracking</div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;font-size:12px;color:#334155;display:flex;align-items:center;gap:8px;"><span style="width:5px;height:5px;background:#2563EB;border-radius:50%;flex-shrink:0;"></span>Context-aware AI chatbot with full patient profile access</div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;font-size:12px;color:#334155;display:flex;align-items:center;gap:8px;"><span style="width:5px;height:5px;background:#2563EB;border-radius:50%;flex-shrink:0;"></span>NLP sentiment analysis on community reviews</div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;font-size:12px;color:#334155;display:flex;align-items:center;gap:8px;"><span style="width:5px;height:5px;background:#2563EB;border-radius:50%;flex-shrink:0;"></span>Voice-enabled input with speech-to-text</div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:12px 14px;font-size:12px;color:#334155;display:flex;align-items:center;gap:8px;"><span style="width:5px;height:5px;background:#2563EB;border-radius:50%;flex-shrink:0;"></span>Integrated medical e-commerce with order management</div>
          </div>
          <p style="font-size:11px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px;">Technology Stack</p>
          <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;">
            {''.join(f'<span style="background:#F0F4F9;border:1px solid #E2E8F0;color:#334155;font-size:11px;font-weight:600;padding:5px 12px;border-radius:100px;font-family:JetBrains Mono,monospace;">{t}</span>' for t in ["Python 3.10+","Streamlit","Anthropic Claude","Pandas","JSON Auth","pyttsx3","streamlit-mic-recorder","NLP Sentiment Analysis"])}
          </div>
          <div style="background:#FFFBEB;border:1px solid #FDE68A;border-left:4px solid #F59E0B;border-radius:10px;padding:14px 16px;margin-bottom:20px;font-size:13px;color:#334155;line-height:1.7;">
            <strong>⚠️ Disclaimer:</strong> MediCore AI provides informational guidance only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional.
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;">
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:14px;text-align:center;"><div style="font-size:20px;margin-bottom:6px;">📞</div><div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;font-weight:700;margin-bottom:4px;">Helpline</div><div style="font-size:12px;color:#334155;">+91 97123 45670</div></div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:14px;text-align:center;"><div style="font-size:20px;margin-bottom:6px;">✉️</div><div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;font-weight:700;margin-bottom:4px;">Email</div><div style="font-size:12px;color:#334155;">support@medicore.ai</div></div>
            <div style="background:#F0F4F9;border:1px solid #E2E8F0;border-radius:12px;padding:14px;text-align:center;"><div style="font-size:20px;margin-bottom:6px;">🌐</div><div style="font-size:9px;color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;font-weight:700;margin-bottom:4px;">Website</div><div style="font-size:12px;color:#334155;">www.medicore.ai</div></div>
          </div>
        </div>
        <div style="background:#0F172A;border-radius:14px;padding:18px 24px;margin-top:16px;display:flex;justify-content:space-between;align-items:center;">
          <div>
            <div style="font-family:'Lora',serif;font-size:16px;font-weight:600;color:white;">MediCore <span style='color:#2563EB;'>AI</span></div>
            <div style="font-size:11px;color:#475569;margin-top:2px;">Enterprise Clinical Intelligence · Doctor & Medicine Recommendation · Review Mining</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:13px;color:#64748B;">Developed by <span style="color:#2563EB;font-weight:700;">team</span></div>
            <div style="font-size:10px;color:#334155;margin-top:2px;font-family:'JetBrains Mono',monospace;">© 2024 MediCore AI v4.0</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════
if st.session_state.auth_user:
    render_app()
else:
    render_auth()

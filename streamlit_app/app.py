"""
BrandSphere AI — NovaTech Automated Branding Assistant
CRS Capstone Project 2025-26 | Scenario 1
Run:  streamlit run app.py
"""

import os, json, re, zipfile, tempfile, warnings
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import streamlit as st
warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BrandSphere AI | NovaTech",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Path resolution (works locally + Streamlit Cloud) ─────────────────────────
APP_DIR   = Path(__file__).parent
ROOT_DIR  = APP_DIR.parent
DATA_DIR  = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "models"

# ── NovaTech Logo SVG ─────────────────────────────────────────────────────────
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="{w}" height="{h}">
  <rect width="400" height="400" fill="transparent"/>
  <g transform="translate(200, 175)">
    <path d="M 0,0 C -10,-18 -30,-38 -55,-48 C -80,-58 -100,-52 -115,-42
             C -95,-44 -72,-36 -52,-20 C -35,-6 -18,8 0,28
             C 18,8 35,-6 52,-20 C 72,-36 95,-44 115,-42
             C 100,-52 80,-58 55,-48 C 30,-38 10,-18 0,0 Z"
      fill="#1A1A1A"/>
    <ellipse cx="0" cy="8" rx="3.5" ry="22" fill="#F9F9F7"/>
  </g>
  <text x="200" y="248" text-anchor="middle"
        font-family="Optima,Didot,Palatino Linotype,serif"
        font-size="15" font-weight="400" letter-spacing="11"
        fill="#1A1A1A">NOVATECH</text>
</svg>"""

LOGO_SM  = LOGO_SVG.format(w=90,  h=90)
LOGO_MD  = LOGO_SVG.format(w=160, h=160)
LOGO_LG_BG = LOGO_SVG.format(w=200, h=200).replace("fill=\"transparent\"","fill=\"#f0f2ff\"")

# ── Brand constants ────────────────────────────────────────────────────────────
NOVATECH_PALETTE = {
    "Onyx Black":    "#1A1A1A",
    "Warm Ivory":    "#F9F9F7",
    "Deep Navy":     "#0D1B3E",
    "Electric Blue": "#5055D8",
    "Silver":        "#C0C0C8",
}
COLOR_PSY = {
    "Onyx Black":    "Premium, sophisticated & minimalist — commands authority",
    "Warm Ivory":    "Clean, approachable & human-centred warmth",
    "Deep Navy":     "Trust, stability & authority — ideal for B2B tech",
    "Electric Blue": "Innovation, digital-native energy & forward momentum",
    "Silver":        "Precision, technology & modern efficiency",
}
INDUSTRY_PALETTES = {
    "Technology":        {"Primary":"#0D1B3E","Accent":"#5055D8","Light":"#E8F0FF","Neutral":"#F4F4F8"},
    "Healthcare":        {"Primary":"#004E89","Accent":"#00B4D8","Light":"#E0F7FA","Neutral":"#F5FAFA"},
    "Fashion & Apparel": {"Primary":"#1A1A1A","Accent":"#C9A84C","Light":"#FFF8EC","Neutral":"#F8F8F8"},
    "Food & Beverage":   {"Primary":"#B33000","Accent":"#FF8C00","Light":"#FFF3E0","Neutral":"#FFFAF5"},
    "Finance":           {"Primary":"#003366","Accent":"#1F8A70","Light":"#E8F5F0","Neutral":"#F5F8FF"},
    "Education":         {"Primary":"#2D3A8C","Accent":"#F4A261","Light":"#FEF6EC","Neutral":"#F0F2FF"},
    "E-Commerce":        {"Primary":"#FF6B35","Accent":"#004E89","Light":"#E8F4FD","Neutral":"#FFF9F7"},
    "Sustainability":    {"Primary":"#1B4332","Accent":"#52B788","Light":"#D8F3DC","Neutral":"#F8FFF9"},
    "Real Estate":       {"Primary":"#5C4033","Accent":"#C9A84C","Light":"#FDF5E6","Neutral":"#FAF7F2"},
    "Travel":            {"Primary":"#023E8A","Accent":"#00B4D8","Light":"#CAF0F8","Neutral":"#F0F9FF"},
    "Entertainment":     {"Primary":"#10002B","Accent":"#E040FB","Light":"#F3E5F5","Neutral":"#FDF4FF"},
    "Other":             {"Primary":"#2D3436","Accent":"#6C5CE7","Light":"#EEE8FF","Neutral":"#F8F8F8"},
}
FONT_MAP = {
    "Minimalist":               {"primary":"Inter","secondary":"Helvetica Neue","weight":"Light 300","reason":"Clean, modern, highly legible across all digital surfaces"},
    "Tech-Forward & Innovative":{"primary":"Optima","secondary":"Space Grotesk","weight":"Regular 400","reason":"Humanist serif blended with digital-first geometry — NovaTech's signature"},
    "Luxury & Premium":         {"primary":"Didot","secondary":"Cormorant Garamond","weight":"Light 300","reason":"High contrast serif for premium brand positioning"},
    "Bold & Vibrant":           {"primary":"Bebas Neue","secondary":"Montserrat Bold","weight":"Bold 700","reason":"Strong display font for maximum visual impact"},
    "Youthful & Playful":       {"primary":"Nunito","secondary":"Quicksand","weight":"SemiBold 600","reason":"Rounded sans-serif conveys friendliness and energy"},
    "Professional & Corporate": {"primary":"Source Sans Pro","secondary":"Open Sans","weight":"Regular 400","reason":"Neutral, universally legible, trusted corporate voice"},
    "Eco-Friendly":             {"primary":"Lato","secondary":"Merriweather","weight":"Regular 400","reason":"Organic warmth and approachability for green brands"},
}
CHANNEL_BENCH = {
    "Instagram":  {"ctr_mult":1.15,"eng_boost":1.20,"roi_base":5.5},
    "Facebook":   {"ctr_mult":1.10,"eng_boost":1.10,"roi_base":5.2},
    "Email":      {"ctr_mult":1.05,"eng_boost":0.90,"roi_base":6.0},
    "Google Ads": {"ctr_mult":1.20,"eng_boost":1.00,"roi_base":5.8},
    "YouTube":    {"ctr_mult":0.90,"eng_boost":1.30,"roi_base":4.8},
    "Website":    {"ctr_mult":1.00,"eng_boost":0.95,"roi_base":5.0},
    "LinkedIn":   {"ctr_mult":1.08,"eng_boost":1.05,"roi_base":5.6},
}
CAMPAIGN_BENCH = {
    "Social Media": {"eng_boost":1.30,"roi_mult":1.10},
    "Influencer":   {"eng_boost":1.40,"roi_mult":1.20},
    "Display":      {"eng_boost":0.90,"roi_mult":0.95},
    "Email":        {"eng_boost":0.85,"roi_mult":1.15},
    "Search":       {"eng_boost":1.00,"roi_mult":1.05},
}

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { background:#0f0f1a; }
[data-testid="stSidebar"] * { color:#e8e8f0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label { color:#9090b8 !important; font-size:12px !important; }

.kpi-card {
    background:#f8f9ff; border:1px solid #dde0f5;
    border-radius:12px; padding:1.1rem 0.8rem;
    text-align:center; margin-bottom:0.5rem;
}
.kpi-val   { font-size:1.7rem; font-weight:700; color:#1a1a3e; line-height:1.1; }
.kpi-label { font-size:0.68rem; color:#888; letter-spacing:0.5px; text-transform:uppercase; margin-top:4px; }

.tagline-card {
    background:linear-gradient(135deg,#f0f2ff 0%,#fff 100%);
    border-left:4px solid #5055d8; border-radius:0 10px 10px 0;
    padding:0.75rem 1.1rem; margin-bottom:0.5rem;
    color:#1a1a3e; line-height:1.5;
}
.section-hdr {
    color:#1a1a3e; font-size:1.05rem; font-weight:600;
    border-bottom:2px solid #5055d8;
    padding-bottom:0.35rem; margin-bottom:1rem;
}
.badge {
    display:inline-block; padding:3px 10px;
    border-radius:20px; font-size:0.72rem;
    font-weight:600; letter-spacing:0.5px;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def swatch(hex_c, name, tip="", height=76):
    r,g,b = int(hex_c[1:3],16), int(hex_c[3:5],16), int(hex_c[5:7],16)
    tc = "#ffffff" if (r*.299+g*.587+b*.114)<128 else "#1a1a3e"
    return f"""<div style="background:{hex_c};color:{tc};height:{height}px;border-radius:10px;
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        font-size:10px;font-weight:700;letter-spacing:0.5px;text-align:center;padding:4px;margin-bottom:4px">
        {name}<br><span style="opacity:.85;font-size:9px">{hex_c}</span></div>
        <div style="font-size:9px;color:#888;text-align:center;line-height:1.3">{tip[:50]}</div>"""

def tagline_html(n, text):
    return f'<div class="tagline-card">#{n} &nbsp; <strong>{text}</strong></div>'

def gemini_call(model, prompt):
    try:
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        return f"[API Error: {e}]"

def predict(channel, ctype, budget, dur_days):
    bch = CHANNEL_BENCH.get(channel,  {"ctr_mult":1.0,"eng_boost":1.0,"roi_base":5.0})
    bct = CAMPAIGN_BENCH.get(ctype,   {"eng_boost":1.0,"roi_mult":1.0})
    imp  = budget * 80
    clk  = imp * 0.14 * bch["ctr_mult"]
    ctr  = round((clk/max(imp,1))*100, 2)
    roi  = round(bch["roi_base"] * bct["roi_mult"], 2)
    eng  = round(min(5.5 * bch["eng_boost"] * bct["eng_boost"], 10.0), 1)
    conv = round(0.08 * bch["ctr_mult"] * 100, 2)
    return {"CTR (%)": ctr, "ROI (x)": roi, "Engagement /10": eng, "Conv. Rate (%)": conv}

# ── Data loaders ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_marketing():
    p = DATA_DIR / "marketing_campaign_dataset.csv"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p)
    df["Acquisition_Cost"] = df["Acquisition_Cost"].astype(str).str.replace("[$,]","",regex=True).astype(float)
    df["Duration_Days"]    = df["Duration"].str.extract(r"(\d+)").astype(int)
    df["CTR"]              = (df["Clicks"] / df["Impressions"] * 100).round(3)
    return df.sample(n=min(20000,len(df)), random_state=42)

@st.cache_data(show_spinner=False)
def load_slogans():
    p = DATA_DIR / "sloganlist.csv"
    if not p.exists():
        return pd.DataFrame(columns=["Company","Slogan"])
    df = pd.read_csv(p)
    df.columns = ["Company","Slogan"]
    df["Slogan"] = df["Slogan"].astype(str).str.strip()
    return df.dropna()

@st.cache_data(show_spinner=False)
def load_startups():
    p = DATA_DIR / "startups.csv"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p)
    return df.dropna(subset=["tagline"]) if "tagline" in df.columns else df

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(LOGO_SM, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🏢 Brand Details")
    company  = st.text_input("Company name",      value="NovaTech")
    industry = st.selectbox("Industry",           list(INDUSTRY_PALETTES.keys()))
    tone     = st.selectbox("Brand personality",  list(FONT_MAP.keys()), index=1)
    audience = st.text_input("Target audience",   value="Tech-savvy professionals 25–40")
    region   = st.selectbox("Target region",      ["Global","India","USA","Europe","Middle East","Southeast Asia","Latin America"])

    st.markdown("---")
    st.markdown("### 🤖 Gemini API")
    gkey = st.text_input("API Key", type="password",
                          help="Free key → aistudio.google.com")
    if gkey and st.session_state.get("gkey") != gkey:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gkey)
            gm = genai.GenerativeModel("gemini-1.5-flash")
            gm.generate_content("Hi")
            st.session_state.update({"gm": gm, "gkey": gkey})
            st.success("Gemini connected ✓")
        except Exception as e:
            st.error(str(e))

    gemini_ok = "gm" in st.session_state
    if not gemini_ok:
        st.caption("Add API key to unlock AI generation")
    st.markdown("---")
    st.caption("BrandSphere AI • CRS Capstone 2025-26 • Scenario 1")

# ── Header ─────────────────────────────────────────────────────────────────────
h1, h2 = st.columns([1,5])
with h1:
    st.markdown(LOGO_SM, unsafe_allow_html=True)
with h2:
    st.markdown(f"""
    <div style="padding:.6rem 0">
    <h1 style="margin:0;color:#1a1a3e;letter-spacing:3px;font-size:1.75rem">BRANDSPHERE AI</h1>
    <p style="color:#5055d8;margin:2px 0 0;font-size:.82rem;letter-spacing:1px">
    AI-Powered Branding Assistant &nbsp;·&nbsp; {company.upper()} &nbsp;·&nbsp; {industry}
    </p></div>""", unsafe_allow_html=True)
st.markdown("---")

# Load data
df_mkt   = load_marketing()
df_sl    = load_slogans()
df_start = load_startups()

# ── Tabs ────────────────────────────────────────────────────────────────────────
T = st.tabs(["🏠 Overview","🎨 Logo & Colours","✍️ Creative Content",
             "📊 Campaign Studio","🌍 Multilingual","💬 Feedback","📦 Download Kit"])

# ════════════════════════════════════════════════════════════════════
# TAB 0  OVERVIEW
# ════════════════════════════════════════════════════════════════════
with T[0]:
    # KPIs
    kpis = [
        ("200,000","Campaign records"),
        ("1,162","Brand slogans"),
        ("42,038","Startup profiles"),
        (f"{df_mkt['CTR'].mean():.1f}%" if not df_mkt.empty else "14.0%","Avg dataset CTR"),
        (f"{df_mkt['ROI'].mean():.2f}x" if not df_mkt.empty else "5.00x","Avg dataset ROI"),
        (f"{df_mkt['Engagement_Score'].mean():.1f}/10" if not df_mkt.empty else "5.5/10","Avg Engagement"),
    ]
    cols = st.columns(6)
    for col,(v,l) in zip(cols,kpis):
        col.markdown(f'<div class="kpi-card"><div class="kpi-val">{v}</div>'
                     f'<div class="kpi-label">{l}</div></div>', unsafe_allow_html=True)

    st.markdown("### 📈 Marketing Dataset Analytics (200,000 real records)")

    if not df_mkt.empty:
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            ch = df_mkt.groupby("Channel_Used").agg(
                CTR=("CTR","mean"), Engagement=("Engagement_Score","mean"),
                Count=("Campaign_ID","count")).reset_index().round(3)
            fig = px.bar(ch, x="Channel_Used", y="CTR", color="Engagement",
                         color_continuous_scale="Blues",
                         title="Avg CTR by Channel (shade = Engagement)",
                         text=ch["CTR"].round(1).astype(str)+"%")
            fig.update_layout(plot_bgcolor="white",height=300,
                              coloraxis_colorbar_title="Eng.")
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        with r1c2:
            ct = df_mkt.groupby("Campaign_Type").agg(
                CTR=("CTR","mean"), ROI=("ROI","mean"),
                Count=("Campaign_ID","count")).reset_index().round(3)
            fig2 = px.scatter(ct, x="CTR", y="ROI", size="Count",
                              color="Campaign_Type", text="Campaign_Type",
                              title="ROI vs CTR by Campaign Type")
            fig2.update_layout(plot_bgcolor="white",height=300,showlegend=False)
            fig2.update_traces(textposition="top center")
            st.plotly_chart(fig2, use_container_width=True)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            loc = df_mkt.groupby("Location")["Engagement_Score"].mean().reset_index()
            fig3 = px.bar(loc.sort_values("Engagement_Score"), x="Engagement_Score",
                          y="Location", orientation="h",
                          title="Avg Engagement by Location",
                          color="Engagement_Score",color_continuous_scale="Purples")
            fig3.update_layout(plot_bgcolor="white",height=280)
            st.plotly_chart(fig3, use_container_width=True)

        with r2c2:
            seg = df_mkt.groupby("Customer_Segment").agg(
                CTR=("CTR","mean"),ROI=("ROI","mean")).reset_index().round(2)
            fig4 = px.bar(seg, x="Customer_Segment", y=["CTR","ROI"], barmode="group",
                          title="CTR vs ROI by Customer Segment",
                          color_discrete_sequence=["#5055d8","#1A1A1A"])
            fig4.update_layout(plot_bgcolor="white",height=280)
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🚀 Startup Tagline Explorer (42,038 profiles)")
    if not df_start.empty and "tagline" in df_start.columns:
        q = st.text_input("Search by keyword", placeholder="AI, automation, future, scale…")
        view = df_start[df_start["tagline"].astype(str).str.contains(q,case=False,na=False)] if q else df_start
        st.dataframe(view[["name","city","tagline"]].head(20), use_container_width=True)

# ════════════════════════════════════════════════════════════════════
# TAB 1  LOGO & COLOURS
# ════════════════════════════════════════════════════════════════════
with T[1]:
    st.markdown('<div class="section-hdr">🎨 Logo Preview & Colour Intelligence</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns([1,2])

    with c1:
        st.markdown(
            f'<div style="background:#f0f2ff;border-radius:14px;padding:2rem;'
            f'text-align:center">{LOGO_LG_BG}</div>', unsafe_allow_html=True)
        st.caption("NovaTech Falcon-Wing Emblem — Minimalist luxury mark")
        st.markdown("""
| Attribute | Value |
|---|---|
| Style | Minimalist emblem |
| Symbol | Falcon wing — speed, precision, vision |
| Wordmark font | Optima (humanist serif) |
| Letter-spacing | +11 px |
| Tone | Premium & tech-forward |
""")

    with c2:
        st.markdown("#### NovaTech Brand Palette")
        pc = st.columns(5)
        for col,(name,hx) in zip(pc, NOVATECH_PALETTE.items()):
            col.markdown(swatch(hx, name, COLOR_PSY[name]), unsafe_allow_html=True)

        st.markdown(f"---\n#### {industry} Industry Recommended Palette")
        ip = INDUSTRY_PALETTES.get(industry, INDUSTRY_PALETTES["Technology"])
        ic = st.columns(len(ip))
        for col,(name,hx) in zip(ic, ip.items()):
            col.markdown(swatch(hx, name, height=68), unsafe_allow_html=True)

        st.markdown("---\n#### 🔤 Font Recommendation Engine")
        fr = FONT_MAP.get(tone, FONT_MAP["Tech-Forward & Innovative"])
        fa,fb,fc = st.columns(3)
        fa.metric("Primary Font",   fr["primary"])
        fb.metric("Secondary Font", fr["secondary"])
        fc.metric("Weight",         fr["weight"])
        st.info(f"**Why this pairing:** {fr['reason']}")

        if st.button("📤 Export Palette as CSV"):
            pal_df = pd.DataFrame([{"Colour":n,"HEX":h,
                "R":int(h[1:3],16),"G":int(h[3:5],16),"B":int(h[5:7],16),
                "Psychology":COLOR_PSY.get(n,"")}
                for n,h in NOVATECH_PALETTE.items()])
            st.download_button("⬇️ Download colour_palette.csv",
                               pal_df.to_csv(index=False).encode(),
                               "novatech_colour_palette.csv","text/csv")

# ════════════════════════════════════════════════════════════════════
# TAB 2  CREATIVE CONTENT
# ════════════════════════════════════════════════════════════════════
with T[2]:
    st.markdown('<div class="section-hdr">✍️ Creative Content & Gen AI Hub</div>',
                unsafe_allow_html=True)
    c1,c2 = st.columns([1,1])

    with c1:
        comm_tone = st.selectbox("Communication style", [
            "Bold & Confident","Formal & Professional",
            "Youthful & Energetic","Inspirational",
            "Minimalist & Clean","Witty & Clever"])
        n_tl = st.slider("Number of taglines", 3, 8, 5)
        prod = st.text_area("Product / service description",
            value="NovaTech delivers AI-powered enterprise automation software "
                  "that helps businesses scale faster with intelligent, data-driven workflows.")

        ref_slogans = df_sl["Slogan"].dropna().sample(
            min(15, len(df_sl)), random_state=42).tolist() if not df_sl.empty else []

        if st.button("✨ Generate Taglines, Narrative & Positioning", type="primary"):
            if not gemini_ok:
                st.warning("Enter your Gemini API key in the sidebar.")
            else:
                gm = st.session_state["gm"]
                with st.spinner("Generating with Gemini 1.5 Flash…"):
                    # Taglines
                    ref = "\n".join(f"  - {s}" for s in ref_slogans[:12])
                    tp = f"""You are a world-class brand strategist for {company} ({industry}).
Context: {prod}
Tone: {tone} | Style: {comm_tone} | Audience: {audience} | Region: {region}

Real brand slogans for style inspiration only (DO NOT copy):
{ref}

Generate exactly {n_tl} ORIGINAL, punchy taglines for {company}.
Rules: 3–8 words each | specific to {industry} | match {comm_tone}
Avoid: excellence, world-class, leading, innovative, revolutionize, transforming
Each must feel distinctly different.

Return ONLY a valid JSON array — no explanation, no markdown:
["Tagline one", "Tagline two"]"""
                    raw = gemini_call(gm, tp)
                    m = re.search(r'\[.*?\]', raw, re.DOTALL)
                    tls = json.loads(m.group()) if m else [raw]
                    st.session_state["taglines"] = tls

                    # Narrative
                    np_ = f"""Write a 3-paragraph brand narrative for {company} ({industry}).
Context: {prod} | Tone: {comm_tone} | Audience: {audience}
Para 1: brand origin & mission | Para 2: differentiation | Para 3: brand promise
Under 170 words. Plain text only."""
                    st.session_state["narrative"] = gemini_call(gm, np_)

                    # Positioning
                    pp = f"""Write ONE brand positioning sentence for {company} ({industry}).
Format: "For [audience] who [need], {company} is the [category] that [benefit] because [reason]."
Context: {prod}. Under 40 words. Plain text only."""
                    st.session_state["positioning"] = gemini_call(gm, pp)

    with c2:
        if "taglines" in st.session_state:
            st.markdown("#### Generated Taglines")
            for i,t in enumerate(st.session_state["taglines"],1):
                st.markdown(tagline_html(i,t), unsafe_allow_html=True)

            if "positioning" in st.session_state:
                st.markdown("#### Brand Positioning Statement")
                st.success(st.session_state["positioning"])

            if "narrative" in st.session_state:
                st.markdown("#### Brand Narrative")
                st.markdown(
                    f'<div style="background:#f8f9ff;border-radius:10px;padding:1rem;'
                    f'border:1px solid #dde0f5;font-size:.88rem;line-height:1.75;color:#1a1a3e">'
                    f'{st.session_state["narrative"]}</div>', unsafe_allow_html=True)

    st.markdown("---\n#### 📚 Slogan Dataset Explorer — 1,162 Real Brand Slogans")
    if not df_sl.empty:
        sq = st.text_input("Search by keyword", placeholder="love, best, future, world…", key="sl_search")
        view = df_sl[df_sl["Slogan"].str.contains(sq,case=False,na=False)] if sq else df_sl
        st.dataframe(view.head(25), use_container_width=True)
        st.caption(f"Showing {min(25,len(view))} of {len(view)} matching slogans")

# ════════════════════════════════════════════════════════════════════
# TAB 3  CAMPAIGN STUDIO
# ════════════════════════════════════════════════════════════════════
with T[3]:
    st.markdown('<div class="section-hdr">📊 Smart Social & Brand Campaign Studio</div>',
                unsafe_allow_html=True)
    c1,c2 = st.columns([1,1])

    with c1:
        platform  = st.selectbox("Channel", ["Instagram","Facebook","Email",
                                              "Google Ads","YouTube","Website","LinkedIn"])
        ctype     = st.selectbox("Campaign type", ["Social Media","Influencer",
                                                    "Search","Display","Email"])
        cobj      = st.selectbox("Objective", ["Brand Awareness","Engagement",
                                                "Lead Generation","Conversion","Retention"])
        budget    = st.number_input("Budget (USD)", 500, 500000, 10000, 500)
        duration  = st.select_slider("Duration", ["15 days","30 days","45 days","60 days"])

        aud_opts  = df_mkt["Target_Audience"].unique().tolist() if not df_mkt.empty else ["All Ages"]
        seg_opts  = df_mkt["Customer_Segment"].unique().tolist() if not df_mkt.empty else ["Tech Enthusiasts"]
        aud_sel   = st.selectbox("Audience group", aud_opts)
        seg_sel   = st.selectbox("Customer segment", seg_opts)
        prod_c    = st.text_area("Product description",
                                  value="AI-powered enterprise automation for mid-size businesses.")

        if st.button("🚀 Predict Metrics & Generate Campaign Post", type="primary"):
            dur_d = int(duration.split()[0])
            preds = predict(platform, ctype, budget, dur_d)
            st.session_state["predictions"] = preds
            st.session_state["camp_meta"]   = {
                "platform":platform,"type":ctype,"obj":cobj,
                "budget":budget,"duration":duration}

            if gemini_ok:
                gm = st.session_state["gm"]
                cp = f"""Create a professional {platform} marketing post.
Company: {company} ({industry}) | Goal: {cobj} | Audience: {aud_sel}
Segment: {seg_sel} | Product: {prod_c} | Region: {region} | Tone: {tone}

Return ONLY valid JSON (no markdown):
{{"caption":"<150 chars, no hashtags>","hashtags":["word1","word2","word3","word4","word5","word6","word7"],"cta":"<20 words>","best_time":"<posting time recommendation>","content_type":"Image|Video|Carousel"}}"""
                raw = gemini_call(gm, cp)
                m = re.search(r'\{.*?\}', raw, re.DOTALL)
                if m:
                    try: st.session_state["camp_post"] = json.loads(m.group())
                    except: st.session_state["camp_post"] = {}

    with c2:
        if "predictions" in st.session_state:
            p = st.session_state["predictions"]
            m1,m2 = st.columns(2)
            m3,m4 = st.columns(2)
            avg = df_mkt["CTR"].mean() if not df_mkt.empty else 14.0
            m1.metric("CTR",          f'{p["CTR (%)"]:.2f}%',   delta=f'{p["CTR (%)"]-avg:+.1f}% vs avg')
            m2.metric("ROI",          f'{p["ROI (x)"]:.2f}x')
            m3.metric("Engagement",   f'{p["Engagement /10"]:.1f}/10')
            m4.metric("Conversion",   f'{p["Conv. Rate (%)"]:.1f}%')

            vals = [
                min(p["CTR (%)"]/30*10, 10),
                min(p["ROI (x)"]/8*10,  10),
                p["Engagement /10"],
                min(p["Conv. Rate (%)"]/15*10, 10),
            ]
            fig = go.Figure(go.Scatterpolar(
                r=vals+[vals[0]], theta=["CTR","ROI","Engagement","Conversion","CTR"],
                fill="toself", fillcolor="rgba(80,85,216,0.18)",
                line=dict(color="#5055d8",width=2)
            ))
            fig.update_layout(polar=dict(radialaxis=dict(range=[0,10])),
                              showlegend=False, height=240,
                              margin=dict(t=20,b=20,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True)

        if "camp_post" in st.session_state:
            cc = st.session_state["camp_post"]
            st.markdown("#### 📱 Generated Campaign Post")
            if cc.get("caption"):
                st.markdown(tagline_html("Caption", cc["caption"]), unsafe_allow_html=True)
            if cc.get("hashtags"):
                tags = " ".join(f"#{h}" for h in cc["hashtags"])
                st.markdown(f'<div style="color:#5055d8;font-size:.85rem;margin:6px 0">{tags}</div>',
                            unsafe_allow_html=True)
            if cc.get("cta"):          st.success(f'**CTA:** {cc["cta"]}')
            if cc.get("best_time"):    st.info(f'⏰ **Best time:** {cc["best_time"]}')
            if cc.get("content_type"): st.caption(f'Recommended format: {cc["content_type"]}')

    # Full analytics
    st.markdown("---\n#### 📈 Campaign Analytics Dashboard — 200,000 records")
    if not df_mkt.empty:
        ta,tb,tc = st.tabs(["By Channel","By Campaign Type","Audience × Segment"])
        with ta:
            cdf = df_mkt.groupby("Channel_Used").agg(
                Campaigns=("Campaign_ID","count"), CTR=("CTR","mean"),
                ROI=("ROI","mean"), Engagement=("Engagement_Score","mean"),
                Conversion=("Conversion_Rate","mean")).reset_index().round(3)
            fig = px.bar(cdf, x="Channel_Used", y=["CTR","ROI","Engagement"],
                         barmode="group", title="Key Metrics by Channel",
                         color_discrete_sequence=["#5055d8","#1A1A1A","#C0C0C8"])
            fig.update_layout(plot_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(cdf, use_container_width=True)

        with tb:
            cdf2 = df_mkt.groupby("Campaign_Type").agg(
                CTR=("CTR","mean"), ROI=("ROI","mean"),
                Engagement=("Engagement_Score","mean"),
                Conversion=("Conversion_Rate","mean")).reset_index().round(3)
            fig2 = px.bar(cdf2, x="Campaign_Type", y="CTR", color="Engagement",
                          color_continuous_scale="Blues",
                          title="CTR by Campaign Type (colour = Engagement)",
                          text=cdf2["CTR"].round(1).astype(str)+"%")
            fig2.update_layout(plot_bgcolor="white")
            st.plotly_chart(fig2, use_container_width=True)
            st.dataframe(cdf2, use_container_width=True)

        with tc:
            cdf3 = df_mkt.groupby(["Target_Audience","Customer_Segment"]).agg(
                Engagement=("Engagement_Score","mean")).reset_index().round(3)
            fig3 = px.density_heatmap(cdf3, x="Target_Audience",
                                       y="Customer_Segment", z="Engagement",
                                       color_continuous_scale="Purples",
                                       title="Engagement Heatmap: Audience × Segment")
            fig3.update_layout(plot_bgcolor="white")
            st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════════
# TAB 4  MULTILINGUAL
# ════════════════════════════════════════════════════════════════════
with T[4]:
    st.markdown('<div class="section-hdr">🌍 Multilingual Campaign Generator</div>',
                unsafe_allow_html=True)

    langs = st.multiselect("Target languages", [
        "Hindi","Spanish","French","Mandarin","Arabic","Portuguese",
        "German","Japanese","Korean","Swahili","Tamil","Urdu"],
        default=["Hindi","Spanish","French"])

    default_src = st.session_state["taglines"][0] \
        if "taglines" in st.session_state else "Powering tomorrow, today."
    src = st.text_area("Content to translate", value=default_src)

    if st.button("🌐 Translate & Localise", type="primary"):
        if not gemini_ok:
            st.warning("Gemini API key required.")
        elif not langs:
            st.warning("Select at least one language.")
        else:
            gm = st.session_state["gm"]
            with st.spinner(f"Translating into {len(langs)} languages…"):
                p = f"""Translate this brand tagline into: {", ".join(langs)}

Original (English): "{src}"
Brand: {company} | Industry: {industry} | Tone: {tone}

Rules: Preserve emotional tone | Sound natural not literal | Adapt culturally | Keep punchy

Return ONLY valid JSON — no markdown, no explanation:
{{{", ".join(f'"{l}": "..."' for l in langs)}}}"""

                raw = gemini_call(gm, p)
                m = re.search(r'\{.*?\}', raw, re.DOTALL)
                if m:
                    try:
                        st.session_state["translations"] = json.loads(m.group())
                    except:
                        st.error("Parse error. Raw:")
                        st.code(raw)
                else:
                    st.error("Unexpected response")

    if "translations" in st.session_state:
        FLAGS = {"Hindi":"🇮🇳","Spanish":"🇪🇸","French":"🇫🇷","Mandarin":"🇨🇳",
                 "Arabic":"🇸🇦","Portuguese":"🇧🇷","German":"🇩🇪","Japanese":"🇯🇵",
                 "Korean":"🇰🇷","Swahili":"🇰🇪","Tamil":"🇮🇳","Urdu":"🇵🇰"}
        st.markdown(tagline_html("🇬🇧 EN", src), unsafe_allow_html=True)
        for lang,text in st.session_state["translations"].items():
            st.markdown(
                tagline_html(f"{FLAGS.get(lang,'🌐')} {lang}", text),
                unsafe_allow_html=True)

        # Export as CSV
        tr_df = pd.DataFrame([{"Language":"English","Translation":src}] +
                              [{"Language":l,"Translation":t}
                               for l,t in st.session_state["translations"].items()])
        st.download_button("⬇️ Download Translations CSV",
                           tr_df.to_csv(index=False).encode(),
                           "translations.csv","text/csv")

# ════════════════════════════════════════════════════════════════════
# TAB 5  FEEDBACK
# ════════════════════════════════════════════════════════════════════
with T[5]:
    st.markdown('<div class="section-hdr">💬 Feedback Intelligence & Model Refinement</div>',
                unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        st.markdown("#### Rate Generated Assets (1 = Poor, 5 = Excellent)")
        r_logo = st.slider("🎨 Logo & Colour Palette",     1, 5, 3, key="r1")
        r_tl   = st.slider("✍️ Taglines & Slogans",        1, 5, 3, key="r2")
        r_camp = st.slider("📊 Campaign Content & Post",   1, 5, 3, key="r3")
        r_mul  = st.slider("🌍 Multilingual Translations",  1, 5, 3, key="r4")
        comments = st.text_area("Suggestions & comments (optional)")

        if st.button("💾 Submit Feedback", type="primary"):
            fb = {
                "timestamp": datetime.now().isoformat(),
                "company": company, "industry": industry, "brand_tone": tone,
                "logo_rating": r_logo, "tagline_rating": r_tl,
                "campaign_rating": r_camp, "multilingual_rating": r_mul,
                "avg_rating": round(np.mean([r_logo,r_tl,r_camp,r_mul]),2),
                "comments": comments
            }
            fb_path = ROOT_DIR / "feedback_data.csv"
            pd.DataFrame([fb]).to_csv(
                fb_path, mode="a", header=not fb_path.exists(), index=False)
            st.success("Feedback recorded ✓ Thank you!")
            st.balloons()

    with c2:
        st.markdown("#### Feedback Analytics")
        fb_path = ROOT_DIR / "feedback_data.csv"
        if fb_path.exists():
            fb_df = pd.read_csv(fb_path)
            if len(fb_df):
                avgs = fb_df[["logo_rating","tagline_rating",
                               "campaign_rating","multilingual_rating"]].mean().reset_index()
                avgs.columns = ["Module","Rating"]
                avgs["Module"] = (avgs["Module"]
                    .str.replace("_rating","").str.replace("_"," ").str.title())
                fig = px.bar(avgs, x="Module", y="Rating", color="Rating",
                             color_continuous_scale="Purples",
                             title=f"Avg Ratings — {len(fb_df)} submissions",
                             text=avgs["Rating"].round(2).astype(str)+"/5")
                fig.update_layout(yaxis_range=[0,5], plot_bgcolor="white")
                fig.update_traces(textposition="outside")
                st.plotly_chart(fig, use_container_width=True)
                mc1,mc2 = st.columns(2)
                mc1.metric("Total Submissions", len(fb_df))
                mc2.metric("Overall Avg", f"{fb_df['avg_rating'].mean():.2f} / 5")

                if len(fb_df) >= 5:
                    trend = fb_df.tail(20)[["avg_rating"]].reset_index(drop=True)
                    fig2 = px.line(trend, y="avg_rating",
                                   title="Rating Trend (last 20 submissions)",
                                   markers=True)
                    fig2.update_layout(plot_bgcolor="white",
                                       yaxis_range=[0,5], showlegend=False)
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No feedback yet. Submit your first rating!")

# ════════════════════════════════════════════════════════════════════
# TAB 6  DOWNLOAD KIT
# ════════════════════════════════════════════════════════════════════
with T[6]:
    st.markdown('<div class="section-hdr">📦 Download Complete Branding Kit</div>',
                unsafe_allow_html=True)

    items = [
        (True,                                "NovaTech Logo (SVG)"),
        (True,                                "Brand Colour Palette (HEX codes + CSV)"),
        (True,                                "Font Recommendations"),
        ("taglines"     in st.session_state,  "AI-Generated Taglines"),
        ("narrative"    in st.session_state,  "Brand Narrative"),
        ("positioning"  in st.session_state,  "Brand Positioning Statement"),
        ("camp_post"    in st.session_state,  "Campaign Post, Hashtags & CTA"),
        ("predictions"  in st.session_state,  "Predicted Campaign Metrics"),
        ("translations" in st.session_state,  "Multilingual Translations"),
    ]
    for ok,label in items:
        icon = "✅" if ok else "⬜"
        st.markdown(f"{icon} {label}")

    not_done = sum(1 for ok,_ in items if not ok)
    if not_done:
        st.caption(f"☝️ Complete {not_done} more module(s) to enrich your kit")

    st.markdown("---")
    if st.button("📥 Generate & Download Complete Branding Kit", type="primary"):
        with st.spinner("Packaging your branding kit…"):
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)

                # ── 1. Logo SVG ──────────────────────────────────────────────
                with open(tmp/"novatech_logo.svg","w") as f:
                    f.write(LOGO_SVG.format(w=400,h=400)
                              .replace("fill=\"transparent\"","fill=\"#F9F9F7\""))

                # ── 2. Colour palette CSV ────────────────────────────────────
                pd.DataFrame([{
                    "Colour":n, "HEX":h,
                    "R":int(h[1:3],16),"G":int(h[3:5],16),"B":int(h[5:7],16),
                    "Psychology":COLOR_PSY.get(n,"")}
                    for n,h in NOVATECH_PALETTE.items()]
                ).to_csv(tmp/"colour_palette.csv", index=False)

                # ── 3. Brand summary JSON ────────────────────────────────────
                fr = FONT_MAP.get(tone, FONT_MAP["Tech-Forward & Innovative"])
                summary = {
                    "brand": company, "industry": industry, "brand_tone": tone,
                    "audience": audience, "region": region,
                    "generated": datetime.now().isoformat(),
                    "colour_palette": NOVATECH_PALETTE,
                    "fonts": {"primary": fr["primary"], "secondary": fr["secondary"],
                              "weight": fr["weight"], "rationale": fr["reason"]},
                }
                for k in ["taglines","narrative","positioning",
                          "camp_post","predictions","translations"]:
                    if k in st.session_state:
                        summary[k] = st.session_state[k]
                with open(tmp/"brand_summary.json","w",encoding="utf-8") as f:
                    json.dump(summary, f, ensure_ascii=False, indent=2)

                # ── 4. Brand report TXT ──────────────────────────────────────
                lines = [
                    "═"*58,
                    "  BRANDSPHERE AI — COMPLETE BRAND REPORT",
                    f"  {company.upper()} · {industry}",
                    f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    "═"*58,"",
                    "BRAND IDENTITY","─"*34,
                    f"  Company    : {company}",
                    f"  Industry   : {industry}",
                    f"  Tone       : {tone}",
                    f"  Audience   : {audience}",
                    f"  Region     : {region}","",
                    "COLOUR PALETTE","─"*34,
                ] + [f"  {n:15s}: {h}  — {COLOR_PSY.get(n,'')}"
                     for n,h in NOVATECH_PALETTE.items()] + [
                    "","TYPOGRAPHY","─"*34,
                    f"  Primary font   : {fr['primary']}",
                    f"  Secondary font : {fr['secondary']}",
                    f"  Weight         : {fr['weight']}",
                    f"  Rationale      : {fr['reason']}","",
                ]
                if "taglines" in summary:
                    lines += ["TAGLINES","─"*34]
                    for i,t in enumerate(summary["taglines"],1):
                        lines.append(f"  {i}. {t}")
                    lines.append("")
                if "positioning" in summary:
                    lines += ["POSITIONING STATEMENT","─"*34,
                               f"  {summary['positioning']}",""]
                if "narrative" in summary:
                    lines += ["BRAND NARRATIVE","─"*34, summary["narrative"],""]
                if "camp_post" in summary:
                    cc = summary["camp_post"]
                    lines += ["CAMPAIGN POST","─"*34,
                               f"  Caption  : {cc.get('caption','')}",
                               f"  Hashtags : {' '.join('#'+h for h in cc.get('hashtags',[]))}",
                               f"  CTA      : {cc.get('cta','')}",
                               f"  Timing   : {cc.get('best_time','')}",""]
                if "predictions" in summary:
                    lines += ["PREDICTED METRICS","─"*34]
                    for k,v in summary["predictions"].items():
                        lines.append(f"  {k}: {v}")
                    lines.append("")
                if "translations" in summary:
                    lines += ["MULTILINGUAL TAGLINES","─"*34]
                    if "taglines" in summary and summary["taglines"]:
                        lines.append(f"  EN: {summary['taglines'][0]}")
                    for l,t in summary["translations"].items():
                        lines.append(f"  {l[:2].upper()}: {t}")
                    lines.append("")
                lines += ["═"*58,
                           "  BrandSphere AI · CRS Capstone 2025-26 · Scenario 1",
                           "═"*58]
                with open(tmp/"brand_report.txt","w",encoding="utf-8") as f:
                    f.write("\n".join(lines))

                # ── 5. Translations CSV ──────────────────────────────────────
                if "translations" in st.session_state:
                    tr_rows = [{"Language":"English",
                                "Translation":st.session_state["taglines"][0]
                                if "taglines" in st.session_state else ""}]
                    tr_rows += [{"Language":l,"Translation":t}
                                for l,t in st.session_state["translations"].items()]
                    pd.DataFrame(tr_rows).to_csv(tmp/"translations.csv", index=False)

                # ── 6. ZIP everything ────────────────────────────────────────
                zp = tmp.parent / f"{company.replace(' ','_')}_BrandingKit.zip"
                with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as zf:
                    for fp_ in tmp.iterdir():
                        zf.write(fp_, fp_.name)
                zip_bytes = open(zp,"rb").read()

        st.download_button(
            "⬇️ Download Complete Branding Kit (ZIP)",
            data=zip_bytes,
            file_name=f"{company.replace(' ','_')}_BrandingKit_{datetime.now().strftime('%Y%m%d')}.zip",
            mime="application/zip"
        )
        st.success(f"✅ Kit ready! Contains: Logo SVG, Colour palette CSV, "
                   f"Brand report TXT, Brand summary JSON"
                   + (", Translations CSV" if "translations" in st.session_state else ""))

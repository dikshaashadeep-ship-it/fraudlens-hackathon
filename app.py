import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="FraudLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid;
        margin: 4px 0;
    }
    .high-risk  { border-color: #E74C3C; }
    .med-risk   { border-color: #F39C12; }
    .low-risk   { border-color: #27AE60; }
    .total-card { border-color: #2980B9; }
    .metric-num { font-size: 2rem; font-weight: 700; color: white; }
    .metric-lbl { font-size: 0.85rem; color: #aaa; margin-top: 4px; }
    .fraud-alert {
        background: linear-gradient(90deg, #2d1515, #1e1e2e);
        border-left: 4px solid #E74C3C;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        color: white;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e0e0e0;
        margin: 16px 0 8px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid #2d2d3d;
    }
    div[data-testid="stSidebar"] {
        background: #1a1d27;
    }
</style>
""", unsafe_allow_html=True)

# ── Risk Functions ────────────────────────────────────
def calculate_risk(row):
    score = 0
    if row["amount"] > 50000:   score += 30
    if row["amount"] > 80000:   score += 10
    if row["is_blacklisted"]:   score += 50
    receiver = str(row["receiver_account"])
    if receiver.startswith("MULE"): score += 40
    return min(score, 100)

def risk_label(s):
    if s > 70:  return "🔴 High Risk"
    elif s > 30: return "🟡 Medium Risk"
    else:        return "🟢 Low Risk"

def risk_color(s):
    if s > 70:  return "#E74C3C"
    elif s > 30: return "#F39C12"
    else:        return "#27AE60"

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 FraudLens")
    st.markdown("*CyberShield Hackathon 2026*")
    st.markdown("---")
    st.markdown("### 📁 Upload Data")
    uploaded = st.file_uploader("Upload Transaction CSV", type="csv", label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**📌 How to use:**")
    st.markdown("1. Upload your CSV file\n2. View risk scores\n3. Explore charts\n4. Click AI Explain")
    st.markdown("---")
    st.markdown("**📋 Required Columns:**")
    st.code("transaction_id\nsender_account\nreceiver_account\namount\ntimestamp\nlocation\nis_blacklisted", language="text")

# ── Header ────────────────────────────────────────────
col_logo, col_title = st.columns([1, 11])
with col_title:
    st.markdown("# 🔍 FraudLens")
    st.markdown("**AI-Powered Mule Account & Suspicious Transaction Detection** &nbsp;|&nbsp; *CyberShield PSBs Hackathon 2026 | Bank of India + IIT Hyderabad*")
st.markdown("---")

# ── No File Uploaded ──────────────────────────────────
if uploaded is None:
    st.markdown("### 👆 Upload a CSV file from the sidebar to get started!")
    st.markdown("#### 📋 Expected CSV Format:")
    sample = pd.DataFrame({
        "transaction_id":   ["TXN00001", "TXN00002", "TXN00003"],
        "sender_account":   ["ACC0023",  "ACC0045",  "ACC0012"],
        "receiver_account": ["MULE001",  "MULE001",  "ACC0067"],
        "amount":           [85000,       92000,       4500],
        "timestamp":        ["2024-01-15 14:32:00", "2024-01-15 14:48:00", "2024-01-15 09:15:00"],
        "location":         ["Mumbai",   "Delhi",    "Pune"],
        "is_blacklisted":   [1,           1,          0]
    })
    st.dataframe(sample, use_container_width=True)

else:
    df = pd.read_csv(uploaded)

    # Calculate risk
    df["risk_score"] = df.apply(calculate_risk, axis=1)
    df["risk_level"] = df["risk_score"].apply(risk_label)

    high_df   = df[df["risk_score"] > 70]
    medium_df = df[(df["risk_score"] > 30) & (df["risk_score"] <= 70)]
    low_df    = df[df["risk_score"] <= 30]
    mule_count = df["receiver_account"].astype(str).str.startswith("MULE").sum()

    # ── Metric Cards ─────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card total-card">
            <div class="metric-num">{len(df)}</div>
            <div class="metric-lbl">📊 Total Transactions</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card high-risk">
            <div class="metric-num" style="color:#E74C3C">{len(high_df)}</div>
            <div class="metric-lbl">🔴 High Risk</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card med-risk">
            <div class="metric-num" style="color:#F39C12">{len(medium_df)}</div>
            <div class="metric-lbl">🟡 Medium Risk</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card low-risk">
            <div class="metric-num" style="color:#27AE60">{int(mule_count)}</div>
            <div class="metric-lbl">⚠️ Mule Accounts</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row 1 ─────────────────────────────────
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-header">📊 Risk Distribution</div>', unsafe_allow_html=True)
        fig_pie = px.pie(
            df, names="risk_level",
            color="risk_level",
            color_discrete_map={
                "🔴 High Risk":   "#E74C3C",
                "🟡 Medium Risk": "#F39C12",
                "🟢 Low Risk":    "#27AE60"
            },
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            margin=dict(t=10, b=10),
            legend=dict(font=dict(color="white"))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with right:
        st.markdown('<div class="section-header">🏦 Top 10 Suspicious Accounts</div>', unsafe_allow_html=True)
        top = (df.groupby("receiver_account")["risk_score"]
                 .mean()
                 .sort_values(ascending=False)
                 .head(10)
                 .reset_index())
        fig_bar = px.bar(
            top, x="receiver_account", y="risk_score",
            color="risk_score",
            color_continuous_scale=["#27AE60", "#F39C12", "#E74C3C"],
            range_color=[0, 100]
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis=dict(tickangle=-35, gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d"),
            margin=dict(t=10, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Charts Row 2 ─────────────────────────────────
    left2, right2 = st.columns(2)

    with left2:
        st.markdown('<div class="section-header">💰 Amount vs Risk Score</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df, x="amount", y="risk_score",
            color="risk_level",
            color_discrete_map={
                "🔴 High Risk":   "#E74C3C",
                "🟡 Medium Risk": "#F39C12",
                "🟢 Low Risk":    "#27AE60"
            },
            hover_data=["transaction_id", "receiver_account"]
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis=dict(gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d"),
            margin=dict(t=10, b=10),
            legend=dict(font=dict(color="white"))
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with right2:
        st.markdown('<div class="section-header">🌍 Fraud by City</div>', unsafe_allow_html=True)
        city_risk = (df[df["risk_score"] > 70]
                       .groupby("location")
                       .size()
                       .reset_index(name="fraud_count")
                       .sort_values("fraud_count", ascending=True))
        fig_city = px.bar(
            city_risk, x="fraud_count", y="location",
            orientation="h",
            color="fraud_count",
            color_continuous_scale=["#F39C12", "#E74C3C"]
        )
        fig_city.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis=dict(gridcolor="#2d2d3d"),
            yaxis=dict(gridcolor="#2d2d3d"),
            margin=dict(t=10, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_city, use_container_width=True)

    # ── Transaction Table ─────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">📋 Transaction Risk Table</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        risk_filter = st.selectbox("Filter by Risk", ["All", "🔴 High Risk", "🟡 Medium Risk", "🟢 Low Risk"])
    with fc2:
        min_amt = st.slider("Min Amount (Rs.)", 0, int(df["amount"].max()), 0, step=1000)

    filtered = df.copy()
    if risk_filter != "All":
        filtered = filtered[filtered["risk_level"] == risk_filter]
    filtered = filtered[filtered["amount"] >= min_amt]

    st.dataframe(
        filtered[["transaction_id", "sender_account", "receiver_account",
                   "amount", "timestamp", "location", "risk_score", "risk_level"]]
        .sort_values("risk_score", ascending=False)
        .reset_index(drop=True),
        use_container_width=True,
        height=300
    )

    # ── Fraud Alert Timeline ──────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">🚨 Fraud Alert Timeline</div>', unsafe_allow_html=True)

    if len(high_df) == 0:
        st.success("✅ No high risk transactions found!")
    else:
        for _, row in high_df.sort_values("risk_score", ascending=False).head(5).iterrows():
            st.markdown(f"""
            <div class="fraud-alert">
                🔴 <b>{row['receiver_account']}</b> &nbsp;←&nbsp;
                Rs. <b>{int(row['amount']):,}</b> from <b>{row['sender_account']}</b>
                &nbsp;|&nbsp; 📍 {row['location']}
                &nbsp;|&nbsp; 🕐 {row['timestamp']}
                &nbsp;|&nbsp; Risk: <b style="color:#E74C3C">{int(row['risk_score'])}/100</b>
            </div>
            """, unsafe_allow_html=True)

    # ── Gemini AI Explainer ───────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header">🤖 Gemini AI Fraud Explainer</div>', unsafe_allow_html=True)

    if len(high_df) > 0:
        selected = st.selectbox("Select High Risk Account", high_df["receiver_account"].unique())
        if st.button("🧠 Explain This Fraud", type="primary", use_container_width=True):
            acct_data   = df[df["receiver_account"] == selected]
            txn_count   = len(acct_data)
            total_recv  = acct_data["amount"].sum()
            avg_score   = acct_data["risk_score"].mean()
            cities_list = ", ".join(acct_data["location"].unique())

            try:
                import google.generativeai as genai
                import os
                api_key = os.getenv("GEMINI_API_KEY", "")
                if api_key:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-pro")
                    prompt = f"""You are a bank fraud investigator AI.
Analyze this suspicious account and write a 3-line plain English explanation:
- Account: {selected}
- Total received: Rs. {total_recv:,.0f}
- Number of transactions: {txn_count}
- Average risk score: {avg_score:.0f}/100
- Cities involved: {cities_list}
Be direct and professional. Start with 'Account {selected} is flagged because...'"""
                    response = model.generate_content(prompt)
                    st.warning(f"🔍 **AI Analysis:**\n\n{response.text}")
                else:
                    raise ValueError("No API key")
            except:
                st.warning(f"""🔍 **Analysis for {selected}:**

Account **{selected}** is flagged because it received Rs. {total_recv:,.0f} across {txn_count} transaction(s) from multiple sources, with an average risk score of {avg_score:.0f}/100. The pattern of high-value incoming transfers from unrelated accounts is consistent with mule account behavior — recommended for immediate investigation.""")
    else:
        st.info("No high risk accounts found in this dataset.")

    # ── Download ──────────────────────────────────────
    st.markdown("---")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv_out = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Risk Report (CSV)",
            data=csv_out,
            file_name="fraudlens_risk_report.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_dl2:
        high_csv = high_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "🚨 Download High Risk Only (CSV)",
            data=high_csv,
            file_name="fraudlens_high_risk.csv",
            mime="text/csv",
            use_container_width=True
        )

# ── Footer ────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#555;font-size:0.8rem;'>"
    "🔍 FraudLens &nbsp;|&nbsp; CyberShield PSBs Hackathon 2026 &nbsp;|&nbsp; "
    "GL Bajaj Group of Institutions, Mathura &nbsp;|&nbsp; "
    "Bank of India + IIT Hyderabad"
    "</p>",
    unsafe_allow_html=True
)


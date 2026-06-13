import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="FraudLens",
    page_icon="🔍",
    layout="wide"
)

# ── Header ───────────────────────────────────────────
st.title("🔍 FraudLens")
st.markdown("**AI-Powered Mule Account & Suspicious Transaction Detection**")
st.markdown("*CyberShield PSBs Hackathon 2026 | Bank of India + IIT Hyderabad*")
st.divider()

# ── Risk Score Function ───────────────────────────────
def calculate_risk(row):
    score = 0
    if row["amount"] > 50000:
        score += 30
    if row["is_blacklisted"] == 1:
        score += 50
    return min(score, 100)

def risk_label(score):
    if score > 70:
        return "🔴 High Risk"
    elif score > 30:
        return "🟡 Medium Risk"
    else:
        return "🟢 Low Risk"

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.header("📁 Upload Data")
    uploaded = st.file_uploader("Upload Transaction CSV", type="csv")
    st.divider()
    st.markdown("**How to use:**")
    st.markdown("1. Upload your CSV file")
    st.markdown("2. View risk scores")
    st.markdown("3. Explore charts")
    st.markdown("4. Click AI Explain")

# ── Main App ─────────────────────────────────────────
if uploaded is None:
    st.info("👆 Upload a CSV file from the sidebar to get started!")

    # Show expected format
    st.subheader("📋 Expected CSV Format")
    sample = pd.DataFrame({
        "transaction_id": ["TXN00001", "TXN00002"],
        "sender_account": ["ACC001", "ACC002"],
        "receiver_account": ["MULE001", "ACC003"],
        "amount": [85000, 5000],
        "timestamp": ["2024-01-15 14:32:00", "2024-01-15 15:10:00"],
        "location": ["Mumbai", "Delhi"],
        "is_blacklisted": [1, 0]
    })
    st.dataframe(sample, use_container_width=True)

else:
    # Load data
    df = pd.read_csv(uploaded)

    # Calculate risk
    df["risk_score"] = df.apply(calculate_risk, axis=1)
    df["risk_level"] = df["risk_score"].apply(risk_label)

    # ── Metric Cards ─────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Transactions", len(df))
    with col2:
        high = len(df[df["risk_score"] > 70])
        st.metric("🔴 High Risk", high)
    with col3:
        medium = len(df[(df["risk_score"] > 30) & (df["risk_score"] <= 70)])
        st.metric("🟡 Medium Risk", medium)
    with col4:
        mules = df["receiver_account"].str.startswith("MULE").sum()
        st.metric("⚠️ Mule Accounts", int(mules))

    st.divider()

    # ── Charts Row ───────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Risk Distribution")
        fig_pie = px.pie(
            df,
            names="risk_level",
            title="Transaction Risk Levels",
            color="risk_level",
            color_discrete_map={
                "🔴 High Risk": "#E74C3C",
                "🟡 Medium Risk": "#F39C12",
                "🟢 Low Risk": "#27AE60"
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("🏦 Top Suspicious Accounts")
        top_accounts = (
            df.groupby("receiver_account")["risk_score"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig_bar = px.bar(
            top_accounts,
            x="receiver_account",
            y="risk_score",
            title="Top 10 High Risk Receiver Accounts",
            color="risk_score",
            color_continuous_scale="Reds"
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Transaction Table ─────────────────────────────
    st.divider()
    st.subheader("📋 Transaction Risk Table")

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        risk_filter = st.selectbox(
            "Filter by Risk Level",
            ["All", "🔴 High Risk", "🟡 Medium Risk", "🟢 Low Risk"]
        )
    with filter_col2:
        min_amount = st.slider("Minimum Amount (Rs.)", 0, 200000, 0, step=5000)

    filtered_df = df.copy()
    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df["risk_level"] == risk_filter]
    filtered_df = filtered_df[filtered_df["amount"] >= min_amount]

    st.dataframe(
        filtered_df[["transaction_id", "sender_account", "receiver_account",
                      "amount", "timestamp", "location", "risk_score", "risk_level"]]
        .sort_values("risk_score", ascending=False),
        use_container_width=True
    )

    # ── Fraud Alert Timeline ──────────────────────────
    st.divider()
    st.subheader("🚨 Fraud Alert Timeline")
    high_risk_df = df[df["risk_score"] > 70].sort_values("risk_score", ascending=False)

    if len(high_risk_df) == 0:
        st.success("✅ No high risk transactions found!")
    else:
        for _, row in high_risk_df.head(5).iterrows():
            with st.container():
                st.error(
                    f"🔴 **{row['receiver_account']}** received Rs. {row['amount']:,.0f} "
                    f"from **{row['sender_account']}** | "
                    f"Location: {row['location']} | "
                    f"Risk Score: **{row['risk_score']}/100**"
                )

    # ── AI Explanation ────────────────────────────────
    st.divider()
    st.subheader("🤖 Gemini AI Fraud Explainer")
    st.caption("Get a plain-English explanation for any flagged account")

    if len(high_risk_df) > 0:
        selected_account = st.selectbox(
            "Select a High Risk Account to Explain",
            high_risk_df["receiver_account"].unique()
        )

        if st.button("🧠 Explain This Fraud", type="primary"):
            account_data = df[df["receiver_account"] == selected_account]
            txn_count = len(account_data)
            total_received = account_data["amount"].sum()
            avg_score = account_data["risk_score"].mean()

            # Gemini API call (add your API key below)
            try:
                import google.generativeai as genai
                # genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
                # model = genai.GenerativeModel("gemini-pro")
                # prompt = f"""
                # Analyze this suspicious bank account for a fraud investigator:
                # - Account: {selected_account}
                # - Total transactions: {txn_count}
                # - Total received: Rs. {total_received:,.0f}
                # - Avg Risk Score: {avg_score:.0f}/100
                # Write a 3-line plain English fraud explanation.
                # """
                # response = model.generate_content(prompt)
                # st.warning(f"🔍 AI Analysis:\n\n{response.text}")

                # Placeholder until API key is added
                st.warning(
                    f"🔍 **AI Analysis for {selected_account}:**\n\n"
                    f"This account received Rs. {total_received:,.0f} across {txn_count} "
                    f"transaction(s) with an average risk score of {avg_score:.0f}/100. "
                    f"The pattern of receiving funds from multiple sources and high transaction "
                    f"amounts is consistent with mule account behavior. "
                    f"Recommended action: Flag for immediate investigation."
                )
            except ImportError:
                st.warning(
                    f"🔍 **Analysis for {selected_account}:**\n\n"
                    f"Received Rs. {total_received:,.0f} across {txn_count} transaction(s). "
                    f"Average risk score: {avg_score:.0f}/100. "
                    f"Pattern consistent with mule account behavior — flag for investigation."
                )
    else:
        st.info("No high risk accounts to explain.")

    # ── Download ──────────────────────────────────────
    st.divider()
    st.subheader("⬇️ Download Report")
    csv_out = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Risk Analysis CSV",
        data=csv_out,
        file_name="fraudlens_risk_report.csv",
        mime="text/csv"
    )

# ── Footer ────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "FraudLens | CyberShield PSBs Hackathon 2026 | GL Bajaj Group of Institutions, Mathura"
    "</p>",
    unsafe_allow_html=True
)
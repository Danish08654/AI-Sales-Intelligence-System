import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

campaigns = pd.read_csv("data/campaigns.csv")
performance = pd.read_csv("data/performance.csv")
leads = pd.read_csv("data/leads.csv")

st.title("📊 Executive Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Campaigns",
    len(campaigns)
)

col2.metric(
    "Average ROAS",
    round(performance["roas"].mean(), 2)
)

col3.metric(
    "Average CTR",
    round(performance["ctr"].mean(), 2)
)

col4.metric(
    "Qualified Leads",
    len(leads)
)

st.divider()

st.subheader("Platform Spend Distribution")

platform_spend = campaigns.groupby(
    "platform"
)["spend"].sum().reset_index()

st.bar_chart(
    platform_spend.set_index("platform")
)

st.divider()

st.subheader("Recent Campaign Performance")

st.dataframe(
    performance,
    use_container_width=True
)

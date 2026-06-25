import streamlit as st
import pandas as pd
import plotly.express as px

performance = pd.read_csv(
    "data/performance.csv"
)

st.title("📈 Campaign Intelligence")

platform = st.selectbox(
    "Platform",
    performance["platform"].unique()
)

filtered = performance[
    performance["platform"] == platform
]

st.dataframe(
    filtered,
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        filtered,
        x="campaign_name",
        y="roas",
        color="campaign_name",
        title="ROAS Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.bar(
        filtered,
        x="campaign_name",
        y="ctr",
        color="campaign_name",
        title="CTR Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("AI Insights")

for _, row in filtered.iterrows():

    if row["roas"] < 2:

        st.error(
            f"{row['campaign_name']} → Poor ROAS. Reduce spend."
        )

    elif row["ctr"] < 1.5:

        st.warning(
            f"{row['campaign_name']} → Improve creative testing."
        )

    else:

        st.success(
            f"{row['campaign_name']} → Ready to scale."
        )

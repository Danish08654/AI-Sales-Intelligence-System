import streamlit as st
import pandas as pd

performance = pd.read_csv(
    "data/performance.csv"
)

st.title("🤖 AI Recommendations")

for _, row in performance.iterrows():

    st.subheader(
        row["campaign_name"]
    )

    if row["roas"] < 2:

        st.error(
            """
Reduce budget by 20%.

Launch 3 new creatives.

Test broader audience.
"""
        )

    elif row["ctr"] < 1.5:

        st.warning(
            """
CTR is below benchmark.

Refresh headlines.

Improve hooks and offers.
"""
        )

    else:

        st.success(
            """
Campaign exceeds benchmark.

Increase budget by 15%.

Expand targeting.

Duplicate winning ad sets.
"""
        )

    st.divider()

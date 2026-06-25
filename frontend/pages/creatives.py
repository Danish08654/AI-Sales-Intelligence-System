import streamlit as st
import pandas as pd

creatives = pd.read_csv(
    "data/creatives.csv"
)

st.title("🎨 Creative Intelligence")

st.subheader("Creative Library")

st.dataframe(
    creatives,
    use_container_width=True
)

st.divider()

st.subheader("Generate New Creative")

product = st.text_input(
    "Product"
)

audience = st.text_input(
    "Audience"
)

platform = st.selectbox(
    "Platform",
    [
        "Meta",
        "Google",
        "TikTok",
        "Taboola"
    ]
)

if st.button(
    "Generate Creative"
):

    headline = (
        f"🚀 {product} For {audience}"
    )

    description = (
        f"Increase conversions using "
        f"{product}. Optimized for "
        f"{platform} campaigns."
    )

    st.success(
        "Creative Generated"
    )

    st.markdown(
        f"""
### {headline}

{description}

**CTA:** Start Today
"""
    )

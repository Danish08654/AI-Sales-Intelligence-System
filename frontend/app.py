import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="AI Sales Intelligence",
    page_icon="🚀",
    layout="wide"
)

# ==================================
# SESSION STATE
# ==================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==================================
# SIMPLE AI LOGIC
# ==================================

def calculate_score(industry, employees):

    score = 40

    if industry == "Technology":
        score += 25
    elif industry == "Finance":
        score += 20
    elif industry == "Healthcare":
        score += 15

    if employees > 1000:
        score += 25
    elif employees > 200:
        score += 15
    elif employees > 50:
        score += 10

    return min(score, 100)


def generate_insights(industry, employees):

    insights = []

    if employees > 1000:
        insights.append("Enterprise company with large budget potential.")

    if industry == "Technology":
        insights.append("Technology companies adopt AI solutions faster.")

    if industry == "Finance":
        insights.append("Compliance and security messaging is important.")

    if industry == "Healthcare":
        insights.append("Healthcare buyers value automation and efficiency.")

    return insights


def generate_email(company, industry):

    return f"""
Subject: Helping {company} Scale Faster

Hi Team,

I noticed {company} operates in the {industry} industry.

Our AI solutions help organizations improve lead generation,
sales productivity, and marketing performance.

Would you be open to a short conversation this week?

Best Regards
AI Sales Team
"""


# ==================================
# HERO
# ==================================

st.title(" AI Sales Intelligence System")

# ==================================
# INPUTS
# ==================================

col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("Lead Information")

    company = st.text_input("Company")

    industry = st.selectbox(
        "Industry",
        [
            "Technology",
            "Finance",
            "Healthcare",
            "Retail",
            "Supply Chain"
        ]
    )

    employees = st.number_input(
        "Employees",
        min_value=1,
        value=100
    )

    analyze = st.button(
        "🚀 Analyze Lead",
        use_container_width=True
    )

# ==================================
# RESULTS
# ==================================

with col2:

    if analyze:

        if not company:

            st.error("Enter company name")

        else:

            score = calculate_score(
                industry,
                employees
            )

            insights = generate_insights(
                industry,
                employees
            )

            email = generate_email(
                company,
                industry
            )

            result = {
                "company": company,
                "industry": industry,
                "employees": employees,
                "score": score,
                "insights": insights,
                "email": email
            }

            st.session_state.history.append(result)

            c1, c2 = st.columns(2)

            c1.metric(
                "Lead Score",
                f"{score}/100"
            )

            tier = (
                "Hot"
                if score >= 80
                else "Warm"
                if score >= 60
                else "Cold"
            )

            c2.metric("Lead Tier", tier)

            st.subheader("AI Insights")

            for item in insights:
                st.success(item)

            st.subheader("Cold Email")

            st.code(email)

            st.download_button(
                "Download Email",
                email,
                f"{company}_email.txt"
            )

# ==================================
# HISTORY
# ==================================

if st.session_state.history:

    st.divider()

    st.subheader("Analysis History")

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

    st.download_button(
        "Export History",
        json.dumps(
            st.session_state.history,
            indent=2
        ),
        "history.json"
    )

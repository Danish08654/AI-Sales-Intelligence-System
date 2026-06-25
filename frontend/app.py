# frontend/app.py

import streamlit as st
import pandas as pd
import json

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Sales Intelligence System",
    page_icon="🚀",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==================================================
# SCORING ENGINE
# ==================================================

def calculate_score(industry, employees):

    score = 40

    industry_weight = {
        "Technology": 25,
        "Finance": 20,
        "Healthcare": 15,
        "Retail": 10,
        "Supply Chain": 12
    }

    score += industry_weight.get(industry, 0)

    if employees > 1000:
        score += 25
    elif employees > 200:
        score += 15
    elif employees > 50:
        score += 10

    return min(score, 100)

# ==================================================
# INSIGHTS
# ==================================================

def generate_insights(industry, employees):

    insights = []

    if employees > 1000:
        insights.append(
            "Large enterprise with significant purchasing power."
        )

    elif employees > 200:
        insights.append(
            "Mid-market company with strong growth potential."
        )

    else:
        insights.append(
            "SMB company suitable for fast sales cycles."
        )

    if industry == "Technology":
        insights.append(
            "Technology firms rapidly adopt AI solutions."
        )

    elif industry == "Finance":
        insights.append(
            "Security and compliance messaging is critical."
        )

    elif industry == "Healthcare":
        insights.append(
            "Healthcare companies value automation and efficiency."
        )

    return insights

# ==================================================
# EMAIL GENERATOR
# ==================================================

def generate_email(company, industry):

    return f"""
Subject: Helping {company} Scale Faster

Hi Team,

I noticed {company} operates in the {industry} industry.

Our AI platform helps companies improve:

• Lead Generation
• Sales Productivity
• Revenue Growth
• Marketing Performance

Would you be open to a brief discussion next week?

Best Regards,
AI Sales Team
"""

# ==================================================
# HERO
# ==================================================

st.title("AI Sales Intelligence System")



# ==================================================
# INPUT SECTION
# ==================================================

col1, col2 = st.columns([1,2])

with col1:

    st.subheader("Lead Information")

    company = st.text_input(
        "Company Name"
    )

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

    c1, c2 = st.columns(2)

    with c1:
        analyze = st.button(
            "🚀 Analyze",
            use_container_width=True
        )

    with c2:
        clear_form = st.button(
            "🔄 Clear Form",
            use_container_width=True
        )

# ==================================================
# RESULTS
# ==================================================

with col2:

    if analyze:

        if not company:

            st.error(
                "Please enter company name."
            )

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

            if score >= 80:
                tier = "🔥 Hot Lead"

            elif score >= 60:
                tier = "🟡 Warm Lead"

            else:
                tier = "❄️ Cold Lead"

            result = {
                "Company": company,
                "Industry": industry,
                "Employees": employees,
                "Score": score,
                "Tier": tier
            }

            st.session_state.history.append(
                result
            )

            st.success(
                "Analysis Completed"
            )

            m1, m2 = st.columns(2)

            m1.metric(
                "Lead Score",
                f"{score}/100"
            )

            m2.metric(
                "Lead Tier",
                tier
            )

            st.progress(
                score / 100
            )

            st.divider()

            st.subheader(
                "🧠 AI Insights"
            )

            for item in insights:
                st.success(item)

            st.divider()

            st.subheader(
                "📧 Personalized Email"
            )

            st.code(email)

            st.download_button(
                "📥 Download Email",
                data=email,
                file_name=f"{company}_email.txt",
                mime="text/plain"
            )

# ==================================================
# HISTORY
# ==================================================

if st.session_state.history:

    st.divider()

    st.subheader(
        "📊 Analysis History"
    )

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

    export_type = st.selectbox(
        "Export Format",
        [
            "CSV",
            "JSON"
            "pdf"
            "word"
        ]
    )

    if export_type == "CSV":

        csv = history_df.to_csv(
            index=False
        )

        st.download_button(
            "📥 Download CSV",
            csv,
            "analysis_history.csv",
            "text/csv"
        )

    else:

        st.download_button(
            "📥 Download JSON",
            json.dumps(
                st.session_state.history,
                indent=2
            ),
            "analysis_history.json",
            "application/json"
        )

    if st.button(
        "🗑️ Clear History"
    ):

        st.session_state.history = []

        st.rerun()

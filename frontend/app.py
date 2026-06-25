import streamlit as st

st.set_page_config(
    page_title="AI Sales Intelligence",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Sales Intelligence Agent")

st.markdown("""
Analyze leads, generate insights, calculate lead scores,
and create personalized outreach emails.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:

    company = st.text_input(
        "Company Name"
    )

    industry = st.selectbox(
        "Industry",
        [
            "Finance",
            "Healthcare",
            "Supply Chain",
            "Retail",
            "Technology"
        ]
    )

with col2:

    employees = st.number_input(
        "Employees",
        min_value=1,
        value=50
    )

analyze = st.button(
    "🚀 Analyze Lead",
    use_container_width=True
)

# ==================================
# ANALYSIS
# ==================================

if analyze:

    if not company:

        st.error(
            "Please enter company name"
        )
        st.stop()

    # Lead Score Logic

    score = min(
        round(employees * 0.5),
        100
    )

    # AI Insights

    insights = []

    if employees > 500:

        insights.append(
            "Large enterprise with significant buying potential."
        )

    elif employees > 100:

        insights.append(
            "Mid-market company with strong growth opportunities."
        )

    else:

        insights.append(
            "Small business with moderate purchasing capacity."
        )

    if industry == "Technology":

        insights.append(
            "Technology companies typically adopt AI solutions quickly."
        )

    elif industry == "Finance":

        insights.append(
            "Financial organizations prioritize efficiency and automation."
        )

    elif industry == "Healthcare":

        insights.append(
            "Healthcare companies focus heavily on compliance and data management."
        )

    elif industry == "Retail":

        insights.append(
            "Retail businesses benefit from customer intelligence solutions."
        )

    else:

        insights.append(
            "Supply chain companies value operational optimization."
        )

    # Outreach Email

    email = f"""
Hi {company} Team,

I noticed that your organization operates in the {industry} industry
with approximately {employees} employees.

Many companies similar to yours are using AI-powered sales intelligence
to improve lead qualification, outreach automation, and revenue growth.

I'd love to show how our platform can help your team identify
high-value opportunities and increase conversion rates.

Would you be available for a short discussion next week?

Best Regards,
AI Sales Team
"""

    # ==================================
    # RESULTS
    # ==================================

    st.divider()

    st.subheader("📊 Analysis Results")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Lead Score",
            f"{score}/100"
        )

    with col2:

        if score >= 80:

            st.success("High Priority Lead")

        elif score >= 50:

            st.warning("Medium Priority Lead")

        else:

            st.info("Low Priority Lead")

    st.subheader("🏢 Company")

    st.write(company)

    st.subheader("🧠 AI Insights")

    for insight in insights:

        st.success(insight)

    st.subheader("📧 Personalized Outreach Email")

    st.code(email)

    st.subheader("🎯 Recommended Next Actions")

    st.write("✅ Schedule discovery call")
    st.write("✅ Send product brochure")
    st.write("✅ Share relevant case study")
    st.write("✅ Follow up within 3 days")

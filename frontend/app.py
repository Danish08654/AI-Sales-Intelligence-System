import streamlit as st
import requests


st.set_page_config(
    page_title="AI Sales Intelligence",
    layout="wide"
)

st.title(" AI Sales Intelligence Agent")

col1, col2 = st.columns(2)

with col1:
    company = st.text_input("Company Name")
    industry = st.selectbox(
        "Industry",
        ["Finance", "Healthcare", "Supply Chain", "Retail", "Technology"]
    )
    employees = st.number_input("Employees", min_value=1, value=50)

    analyze = st.button("🚀 Analyze Lead")

if analyze:

    if not company:
        st.error("Please enter company name")
        st.stop()

    try:
        res = requests.post(
            f"{API_URL}/analyze",
            json={
                "company": company,
                "industry": industry,
                "employees": employees
            },
            timeout=30
        )

        # ✅ HANDLE BAD STATUS
        if res.status_code != 200:
            st.error(f"Server Error: {res.text}")
            st.stop()

        # ✅ SAFE JSON PARSE
        try:
            data = res.json()
        except Exception:
            st.error("Invalid JSON response from backend")
            st.code(res.text)
            st.stop()

    except Exception as e:
        st.error(f"API connection failed: {e}")
        st.stop()

    # ======================
    # OUTPUT UI
    # ======================
    st.subheader("📊 Results")

    st.write("### 🏢 Company")
    st.write(data.get("company", "N/A"))

    st.write("### 🧠 Insights")

    for i in data.get("insights", []):
        st.success(i)

    st.write("### 🎯 Score")
    st.metric("Lead Score", f"{data.get('score', 0)}/100")

    st.write("### 📧 AI Email")

    email = data.get("email", "No email generated")
    st.code(email)

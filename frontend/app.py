"""
AI Sales Intelligence System - Streamlit Cloud Edition
Main entry point for deployment on Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your existing services
try:
    from utils.services.sales_service import process_lead
except ImportError:
    st.error("⚠️ Error: Could not import sales_service. Ensure utils folder structure is correct.")
    st.stop()

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AI Sales Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "AI Sales Intelligence System v1.0"
    }
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM STYLING
# ═══════════════════════════════════════════════════════════════

st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        border-radius: 10px;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    
    /* Email box styling */
    .email-box {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
    }
    
    /* Insight badges */
    .insight-badge {
        display: inline-block;
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# INITIALIZE SESSION STATE
# ═══════════════════════════════════════════════════════════════

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# ═══════════════════════════════════════════════════════════════
# HEADER & NAVIGATION
# ═══════════════════════════════════════════════════════════════

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["🚀 Lead Analyzer", "📊 History", "ℹ️ About"])

with tab1:
    # ═══════════════════════════════════════════════════════════════
    # MAIN ANALYSIS INTERFACE
    # ═══════════════════════════════════════════════════════════════
    
    st.title("🤖 AI Sales Intelligence System")
    st.markdown("**Analyze leads, generate insights, score opportunities & create personalized cold emails**")
    
    # Create layout
    col_input, col_result = st.columns([1, 2], gap="medium")
    
    with col_input:
        st.subheader("📝 Lead Information")
        
        # Input fields
        company = st.text_input(
            "Company Name",
            placeholder="e.g., Acme Corporation",
            help="Enter the target company name"
        )
        
        industry = st.selectbox(
            "Industry Sector",
            ["Finance", "Healthcare", "Supply Chain", "Retail", "Technology"],
            help="Select the industry that best describes the company"
        )
        
        employees = st.number_input(
            "Number of Employees",
            min_value=1,
            max_value=500000,
            value=50,
            step=10,
            help="Approximate company size"
        )
        
        # Button group
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            analyze_btn = st.button(
                "🚀 Analyze Lead",
                use_container_width=True,
                type="primary"
            )
        
        with col_btn2:
            clear_btn = st.button(
                "🔄 Clear",
                use_container_width=True
            )
        
        if clear_btn:
            st.session_state.current_analysis = None
            st.rerun()
    
    # ═══════════════════════════════════════════════════════════════
    # ANALYSIS LOGIC
    # ═══════════════════════════════════════════════════════════════
    
    with col_result:
        if analyze_btn:
            # Validation
            if not company or company.strip() == "":
                st.error("⚠️ Please enter a company name", icon="❌")
            else:
                # Show loading state
                with st.spinner("🔄 Analyzing lead... This may take a moment"):
                    try:
                        # Call the service
                        result = process_lead(
                            company=company.strip(),
                            industry=industry,
                            employees=int(employees)
                        )
                        
                        # Store in session state
                        st.session_state.current_analysis = {
                            'timestamp': datetime.now().isoformat(),
                            'company': company,
                            'industry': industry,
                            'employees': employees,
                            'result': result
                        }
                        
                        # Add to history
                        st.session_state.analysis_history.insert(0, st.session_state.current_analysis)
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}", icon="❌")
                        st.exception(e)
        
        # ═══════════════════════════════════════════════════════════════
        # DISPLAY RESULTS
        # ═══════════════════════════════════════════════════════════════
        
        if st.session_state.current_analysis:
            result = st.session_state.current_analysis['result']
            
            st.success("✅ Analysis Complete!", icon="✅")
            
            # Company Profile Section
            st.subheader("🏢 Company Profile")
            company_info = f"**{result.get('company', 'N/A')}** • {industry} • {employees:,} employees"
            st.info(company_info)
            
            # Divider
            st.divider()
            
            # AI Insights Section
            st.subheader("🧠 AI-Powered Insights")
            insights = result.get('insights', [])
            
            if insights:
                for i, insight in enumerate(insights, 1):
                    st.markdown(f"""
                    <div class="insight-badge">
                    <strong>{i}.</strong> {insight}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No insights available", icon="⚠️")
            
            st.divider()
            
            # Lead Score Section
            st.subheader("📊 Lead Score & Tier")
            
            score = result.get('score', 0)
            if not isinstance(score, (int, float)):
                try:
                    score = int(score)
                except:
                    score = 0
            
            # Determine tier
            if score >= 80:
                tier = "🔥 Hot"
                tier_color = "🔴"
                tier_desc = "High priority - Enterprise opportunity"
            elif score >= 60:
                tier = "🟡 Warm"
                tier_color = "🟠"
                tier_desc = "Medium priority - Growth potential"
            else:
                tier = "❄️ Cold"
                tier_color = "🔵"
                tier_desc = "Lower priority - Future prospect"
            
            col_score1, col_score2 = st.columns(2)
            
            with col_score1:
                st.metric("Lead Score", f"{score}/100")
            
            with col_score2:
                st.metric("Tier", tier)
            
            st.info(f"{tier_color} {tier_desc}")
            
            st.divider()
            
            # Email Generation Section
            st.subheader("📧 Personalized Cold Email")
            
            email_content = result.get('email', 'No email generated')
            
            # Display email
            st.code(email_content, language="text")
            
            # Email actions
            col_email1, col_email2, col_email3 = st.columns(3)
            
            with col_email1:
                st.button(
                    "📋 Copy to Clipboard",
                    use_container_width=True,
                    help="Copy email text (note: manual copy needed)"
                )
            
            with col_email2:
                st.download_button(
                    label="📥 Download Email",
                    data=email_content,
                    file_name=f"{company.replace(' ', '_')}_email.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_email3:
                st.download_button(
                    label="📊 Export Results",
                    data=json.dumps(result, indent=2),
                    file_name=f"{company.replace(' ', '_')}_analysis.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            st.divider()
            
            # Recommendation Section
            st.subheader("💡 Recommendations")
            
            recommendations = []
            
            if score < 40:
                recommendations.append("🎯 Consider additional research before outreach")
            if employees < 50:
                recommendations.append("👥 Small company - personalize message for decision maker")
            if employees > 5000:
                recommendations.append("🏢 Large enterprise - consider account-based marketing")
            if industry.lower() in ['finance', 'healthcare']:
                recommendations.append("🔐 Emphasize compliance and security features")
            
            if recommendations:
                for rec in recommendations:
                    st.info(rec)
            else:
                st.success("No specific recommendations - ready to outreach!")

# ═══════════════════════════════════════════════════════════════
# HISTORY TAB
# ═══════════════════════════════════════════════════════════════

with tab2:
    st.subheader("📊 Analysis History")
    
    if st.session_state.analysis_history:
        # Display history as table
        history_data = []
        for item in st.session_state.analysis_history:
            history_data.append({
                'Company': item['company'],
                'Industry': item['industry'],
                'Employees': item['employees'],
                'Score': item['result'].get('score', 0),
                'Time': item['timestamp'][:10]  # Just date
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)
        
        # Export all history
        st.download_button(
            label="📥 Download All History",
            data=json.dumps(st.session_state.analysis_history, indent=2),
            file_name="analysis_history.json",
            mime="application/json"
        )
        
        # Clear history
        if st.button("🗑️ Clear History"):
            st.session_state.analysis_history = []
            st.rerun()
    else:
        st.info("No analysis history yet. Start by analyzing a lead!")

# ═══════════════════════════════════════════════════════════════
# ABOUT TAB
# ═══════════════════════════════════════════════════════════════

with tab3:
    st.subheader("ℹ️ About This Application")
    
    st.markdown("""
    ### 🤖 AI Sales Intelligence System
    
    An intelligent platform for analyzing sales leads, generating insights, and creating personalized outreach emails.
    
    #### Features:
    - **Lead Analysis**: AI-powered analysis based on company size and industry
    - **Scoring System**: Automated lead scoring (0-100)
    - **Email Generation**: Personalized cold email templates
    - **History Tracking**: Keep track of all analyses
    - **Data Export**: Download results in JSON format
    
    #### How It Works:
    1. **Input**: Enter company information
    2. **Analyze**: AI processes the data
    3. **Score**: Get a lead score and tier
    4. **Outreach**: Use the generated email for cold outreach
    
    #### Scoring Tiers:
    - 🔥 **Hot** (80-100): Enterprise opportunities with high conversion potential
    - 🟡 **Warm** (60-79): Growing companies with good potential
    - ❄️ **Cold** (0-59): Prospects requiring more research
    
    #### Industries Supported:
    - Finance
    - Healthcare
    - Supply Chain
    - Retail
    - Technology
    
    #### API Endpoints:
    This application runs on **Streamlit Cloud** with all processing happening server-side.
    
    #### Version Info:
    - **Version**: 1.0.0
    - **Platform**: Streamlit Cloud
    - **Language**: Python 3.9+
    - **Last Updated**: 2024
    
    #### Privacy & Data:
    - No data is stored permanently
    - Each session is independent
    - Analysis results are available for download only
    
    #### Support:
    For issues or feature requests, please refer to the GitHub repository.
    """)
    
    st.divider()
    
    # System info
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.info("📱 **Responsive Design** - Works on desktop and mobile")
    
    with col_info2:
        st.success("⚡ **Fast Processing** - Results in seconds")

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.title("📌 Quick Guide")
    
    st.markdown("""
    ### Getting Started:
    1. **Enter Company Details**
       - Company name
       - Industry sector
       - Employee count
    
    2. **Click Analyze**
       - AI processes your input
       - Generates insights
       - Creates lead score
       - Generates email
    
    3. **Review Results**
       - Check AI insights
       - Review lead score and tier
       - Copy or download email
    
    4. **Take Action**
       - Send personalized email
       - Track results
       - Iterate and improve
    
    ### Pro Tips:
    ✅ Be specific with company names
    ✅ Select accurate industry
    ✅ Use realistic employee counts
    ✅ Download results for your records
    ✅ Track performance metrics
    
    ### Key Metrics:
    - **Lead Score**: 0-100 scale
    - **Tier**: Hot/Warm/Cold classification
    - **Insights**: AI-generated observations
    - **Email**: Ready-to-send template
    """)
    
    st.divider()
    
    # Stats
    st.subheader("📈 Session Stats")
    
    total_analyses = len(st.session_state.analysis_history)
    avg_score = (
        sum(item['result'].get('score', 0) for item in st.session_state.analysis_history) / total_analyses
        if total_analyses > 0 else 0
    )
    
    col_stat1, col_stat2 = st.columns(2)
    
    with col_stat1:
        st.metric("Analyses", total_analyses)
    
    with col_stat2:
        st.metric("Avg Score", f"{int(avg_score)}/100")
    
    st.divider()
    
    # Footer
    st.caption("🚀 Powered by Streamlit Cloud")
    st.caption("© 2024 AI Sales Intelligence System")

from app.agents.outreach_agent import OutreachAgent
from app.agents.lead_agent import analyze_lead
from app.agents.scoring_agent import score_lead


def process_lead(company: str, industry: str, employees: int):
    """
    Main AI pipeline:
    1. Analyze lead (insights)
    2. Score lead
    3. Generate personalized email
    4. Return structured response
    """

    # -------------------------
    # INPUT VALIDATION
    # -------------------------
    if not company or not industry or employees is None:
        return {
            "company": company or "Unknown",
            "insights": ["Insufficient lead data provided"],
            "score": 0,
            "email": "ERROR: Missing required input fields"
        }

    try:
        # -------------------------
        # STEP 1: INSIGHTS
        # -------------------------
        insights = analyze_lead(company, industry, employees)

        if not isinstance(insights, list):
            insights = ["Invalid insights generated"]

        # -------------------------
        # STEP 2: SCORE
        # -------------------------
        score = score_lead(industry, employees)

        if score is None:
            score = 0

        score = int(score)

        # -------------------------
        # STEP 3: EMAIL GENERATION (FIXED)
        # -------------------------
        email_agent = OutreachAgent()
        email = email_agent.generate_email(
            company=company,
            industry=industry,
            employees=employees,
            score=score,
            insights=insights
        )

        if not email or email.startswith("ERROR"):
            email = "Email generation failed"

        # -------------------------
        # FINAL RESPONSE
        # -------------------------
        return {
            "company": company,
            "insights": insights,
            "score": score,
            "email": email
        }

    except Exception as e:
        return {
            "company": company,
            "insights": ["System error during processing"],
            "score": 0,
            "email": f"ERROR: {str(e)}"
        }
from langchain_groq import ChatGroq
from utils.helpers import get_env


class OutreachAgent:
    """
    AI Email Generation Agent
    Generates structured, personalized B2B cold emails using LLM context.
    """

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=get_env("GROQ_API_KEY"),
            temperature=0.4
        )

    def generate_email(
        self,
        company: str,
        industry: str,
        employees: int,
        score: int,
        insights: list
    ) -> str:

        # -------------------------
        # INPUT VALIDATION
        # -------------------------
        if not company or not isinstance(company, str):
            return "ERROR: Invalid company name"

        if not industry or not isinstance(industry, str):
            return "ERROR: Invalid industry"

        if not isinstance(employees, int):
            employees = 0

        if not isinstance(score, int):
            score = 0

        if not insights:
            insights = ["No insights available"]

        try:
            # -------------------------
            # SCORE-BASED TONE CONTROL
            # -------------------------
            if score >= 80:
                tone = "high urgency, strong conversion focus"
            elif score >= 50:
                tone = "consultative, balanced professional tone"
            else:
                tone = "soft nurturing, awareness-focused tone"

            # -------------------------
            # PROMPT ENGINEERING
            # -------------------------
            prompt = f"""
You are a world-class B2B sales strategist and AI SDR.

TASK:
Write a HIGHLY personalized cold email.

OUTPUT FORMAT (STRICT):
Subject: <short compelling subject line>

Body:
<email body>

Signature:
<professional signature (no placeholders like [Your Name])>

RULES:
- No placeholders anywhere
- No explanations or comments
- Must sound human-written
- Must include at least 2 insights naturally
- Must reference company size meaningfully
- Must reflect AI opportunity based on score
- Tone: {tone}
- Keep total email under 180 words

CONTEXT:
Company: {company}
Industry: {industry}
Employees: {employees}
Lead Score: {score}

Insights:
{chr(10).join(insights)}
"""

            # -------------------------
            # LLM CALL
            # -------------------------
            response = self.llm.invoke(prompt)

            # -------------------------
            # RESPONSE VALIDATION
            # -------------------------
            if not response or not hasattr(response, "content"):
                return "ERROR: Empty LLM response"

            email = response.content.strip()

            # basic sanity check
            if len(email) < 30:
                return "ERROR: Email too short or invalid output"

            return email

        except Exception as e:
            return f"EMAIL_ERROR: {str(e)}"
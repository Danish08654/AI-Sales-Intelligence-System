from typing import List

def analyze_lead(company: str, industry: str, employees: int) -> List[str]:

    insights = []

    if not company or not industry:
        return ["Invalid lead data"]

    industry = industry.lower().strip()

    if employees >= 1000:
        insights.append("Enterprise-level organization with high deal value")
    elif employees >= 100:
        insights.append("Mid-sized company with scaling potential")
    else:
        insights.append("Small business with early-stage opportunity")

    high_ai_industries = ["finance", "healthcare", "supply chain", "retail", "technology"]

    if industry in high_ai_industries:
        insights.append("High AI adoption potential")

    insights.append(f"Industry segment: {industry.title()}")

    return insights
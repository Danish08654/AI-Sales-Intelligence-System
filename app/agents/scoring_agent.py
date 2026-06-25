def score_lead(industry: str, employees: int) -> int:

    score = 40

    if employees > 1000:
        score += 30
    elif employees > 100:
        score += 20
    else:
        score += 10

    if industry.lower() in ["finance", "healthcare", "supply chain"]:
        score += 30
    elif industry.lower() in ["technology", "retail"]:
        score += 20

    return min(score, 100)
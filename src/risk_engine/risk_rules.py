def risk_level(score: float) -> str:
    pct = score * 100
    if pct < 35:
        return "low"
    if pct < 70:
        return "medium"
    return "high"

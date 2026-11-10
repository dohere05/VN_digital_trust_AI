def percent(value: float | None, digits: int = 1) -> str:
    if value is None:
        return "N/A"
    return f"{max(0.0, min(1.0, float(value))) * 100:.{digits}f}%"

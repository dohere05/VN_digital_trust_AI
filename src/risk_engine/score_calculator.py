def weighted_score(items: list[tuple[float | None, float]]) -> float:
    numerator = 0.0
    denominator = 0.0

    for value, weight in items:
        if value is None:
            continue
        numerator += max(0.0, min(1.0, float(value))) * weight
        denominator += weight

    if denominator == 0:
        return 0.0

    return max(0.0, min(1.0, numerator / denominator))

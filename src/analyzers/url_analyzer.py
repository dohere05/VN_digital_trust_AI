from src.validators.url_validator import validate_url
from src.detectors.malicious_url_detector import predict_malicious_url
from src.risk_engine.risk_engine import calculate_url_risk

def analyze_url(url: str) -> dict:
    validation = validate_url(url)
    detection = predict_malicious_url(url)

    risk = calculate_url_risk(
        detection.get("malicious_probability"),
        validation["valid_syntax"],
        validation["dns_exists"],
        validation["https"],
    )

    return {
        "validation": validation,
        "detection": detection,
        "risk": risk,
    }

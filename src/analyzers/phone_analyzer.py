from src.validators.phone_validator import validate_phone
from src.validators.hotline_validator import validate_hotline
from src.risk_engine.risk_engine import calculate_phone_risk

def analyze_phone(phone: str) -> dict:
    phone_result = validate_phone(phone)
    hotline_result = validate_hotline(phone)
    hotline_verified = hotline_result["verified"] if hotline_result["provided"] else None

    risk = calculate_phone_risk(
        phone_result["valid"],
        phone_result["is_voip"],
        hotline_verified,
    )

    return {
        "phone": phone_result,
        "hotline": hotline_result,
        "risk": risk,
    }

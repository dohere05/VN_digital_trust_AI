from src.risk_engine.score_calculator import weighted_score
from src.risk_engine.risk_rules import risk_level

def calculate_sms_risk(spam_probability, scam_score, url_risk=None, sender_verified=None):
    sender_risk = None
    if sender_verified is not None:
        sender_risk = 0.0 if sender_verified else 0.45

    score = weighted_score([
        (spam_probability, 0.45),
        (scam_score, 0.25),
        (url_risk, 0.20),
        (sender_risk, 0.10),
    ])
    return {"score": score, "level": risk_level(score)}

def calculate_email_risk(valid_format: bool, disposable: bool, dns_exists: bool, has_mx: bool):
    score = 0.0
    if not valid_format:
        score += 0.70
    if disposable:
        score += 0.55
    if valid_format and not dns_exists:
        score += 0.20
    if valid_format and not has_mx:
        score += 0.20
    score = min(1.0, score)
    return {"score": score, "level": risk_level(score)}

def calculate_phone_risk(valid: bool, is_voip: bool, hotline_verified: bool | None = None):
    score = 0.0 if valid else 0.75
    if is_voip:
        score += 0.20
    if hotline_verified is False:
        score += 0.15
    score = min(1.0, score)
    return {"score": score, "level": risk_level(score)}

def calculate_url_risk(malicious_probability: float | None, valid_syntax: bool, dns_exists: bool, https: bool):
    score = malicious_probability if malicious_probability is not None else 0.0
    if not valid_syntax:
        score = max(score, 0.85)
    elif not dns_exists:
        score = max(score, 0.60)
    elif not https:
        score = min(1.0, score + 0.10)
    return {"score": score, "level": risk_level(score)}

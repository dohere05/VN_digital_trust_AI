from config.paths import DISPOSABLE_EMAIL_FILE
from src.validators.email_validator import validate_email_address
from src.validators.domain_validator import validate_domain
from src.risk_engine.risk_engine import calculate_email_risk

def _load_disposable_domains() -> set[str]:
    if not DISPOSABLE_EMAIL_FILE.exists():
        return set()
    domains = set()
    for line in DISPOSABLE_EMAIL_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip().lower()
        if line and not line.startswith("#"):
            domains.add(line)
    return domains

def analyze_email(email: str) -> dict:
    base = validate_email_address(email)
    if not base["valid_format"]:
        risk = calculate_email_risk(False, False, False, False)
        return {"email": base, "domain": {}, "disposable": False, "risk": risk}

    domain_result = validate_domain(base["domain"])
    disposable = base["domain"] in _load_disposable_domains()

    risk = calculate_email_risk(
        True,
        disposable,
        domain_result["dns_exists"],
        bool(domain_result["mx_records"]),
    )
    return {
        "email": base,
        "domain": domain_result,
        "disposable": disposable,
        "risk": risk,
    }

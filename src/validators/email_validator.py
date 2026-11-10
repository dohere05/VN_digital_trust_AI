from email_validator import validate_email, EmailNotValidError

def validate_email_address(email: str) -> dict:
    try:
        result = validate_email(email, check_deliverability=False)
        return {
            "valid_format": True,
            "normalized": result.normalized,
            "domain": result.domain.lower(),
            "error": None,
        }
    except EmailNotValidError as exc:
        return {
            "valid_format": False,
            "normalized": None,
            "domain": None,
            "error": str(exc),
        }

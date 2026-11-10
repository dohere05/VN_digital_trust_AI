from src.validators.email_validator import validate_email_address

def test_valid_email():
    result = validate_email_address("test@example.com")
    assert result["valid_format"] is True

def test_invalid_email():
    result = validate_email_address("abc@@example")
    assert result["valid_format"] is False

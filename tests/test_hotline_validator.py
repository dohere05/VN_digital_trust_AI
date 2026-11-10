from src.validators.hotline_validator import validate_hotline

def test_empty_sender():
    result = validate_hotline("")
    assert result["provided"] is False

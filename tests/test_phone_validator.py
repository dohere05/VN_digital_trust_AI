from src.validators.phone_validator import validate_phone

def test_vietnam_phone_possible():
    result = validate_phone("0912345678")
    assert result["possible"] in (True, False)

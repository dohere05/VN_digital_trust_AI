from src.preprocessing.feature_extractor import extract_url_features

def test_url_features():
    result = extract_url_features("https://example.com/login")
    assert "url_length" in result
    assert result["uses_https"] == 1

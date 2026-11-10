from src.detectors.spam_detector import predict_spam

def test_spam_detector_graceful_without_model():
    result = predict_spam("Xin chào")
    assert "available" in result

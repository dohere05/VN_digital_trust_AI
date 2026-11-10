from src.detectors.fake_news_detector import predict_fake_news

def test_fake_detector_graceful_without_model():
    result = predict_fake_news("", "Nội dung mẫu")
    assert "available" in result

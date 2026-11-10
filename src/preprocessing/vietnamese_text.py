from src.preprocessing.text_preprocessor import clean_text

try:
    from underthesea import word_tokenize
except Exception:
    word_tokenize = None

def preprocess_vietnamese(text: str) -> str:
    cleaned = clean_text(text)
    if word_tokenize is None:
        return cleaned
    try:
        return word_tokenize(cleaned, format="text")
    except Exception:
        return cleaned

import json
from config.paths import SPAM_MODEL_DIR, FAKE_MODEL_DIR, URL_MODEL_DIR

def show(name, path):
    print(f"\n=== {name} ===")
    if path.exists():
        print(json.dumps(json.loads(path.read_text(encoding='utf-8')), ensure_ascii=False, indent=2))
    else:
        print("Chưa có metrics.")

def main():
    show("Spam", SPAM_MODEL_DIR / "metrics.json")
    show("Fake News", FAKE_MODEL_DIR / "metrics.json")
    show("Malicious URL", URL_MODEL_DIR / "metrics.json")

if __name__ == "__main__":
    main()

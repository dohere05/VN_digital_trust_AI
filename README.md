# Vietnam Digital Trust AI

Hệ thống kiểm tra thông tin số dành cho người Việt, gồm:

- Phân loại tin nhắn thường / spam / dấu hiệu lừa đảo.
- Phân loại tin thật / tin giả.
- Kiểm tra email và email tạm.
- Kiểm tra số điện thoại / hotline.
- Phân tích URL và phát hiện URL đáng ngờ.
- Tổng hợp nhiều tín hiệu bằng Risk Engine.

## Cài đặt

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Huấn luyện mô hình

Đặt dataset đúng cấu trúc trong `data/raw/`, sau đó:

```bash
python train/train_spam.py
python train/train_fake_news.py
python train/train_url.py
python train/evaluate_models.py
```

Ứng dụng vẫn khởi động được nếu chưa có model; giao diện sẽ báo cần huấn luyện mô hình.

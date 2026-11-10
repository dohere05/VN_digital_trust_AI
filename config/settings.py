import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Vietnam Digital Trust AI"
APP_SUBTITLE = "Hệ thống AI kiểm tra độ tin cậy của thông tin số dành cho người Việt"
APP_ENV = os.getenv("APP_ENV", "development")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "5"))

RISK_LOW_MAX = 34
RISK_MEDIUM_MAX = 69

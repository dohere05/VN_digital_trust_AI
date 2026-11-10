import streamlit as st

from src.analyzers.sms_analyzer import (
    analyze_sms,
)

from ui.components.confidence_bar import (
    render_confidence,
)

from ui.components.risk_badge import (
    render_risk_badge,
)
from src.services.history_service import record_check


def severity_icon(
    severity,
):

    if severity == "high":
        return "🚨"

    if severity == "medium":
        return "⚠️"

    return "ℹ️"


def render():

    st.subheader(
        "💬 Kiểm tra tin nhắn"
    )

    st.caption(
        "AI phân tích nội dung tiếng Việt và "
        "kết hợp nhiều tín hiệu để đánh giá nguy cơ."
    )

    # ==================================
    # INPUT
    # ==================================

    text = st.text_area(
        "Nội dung tin nhắn *",
        height=190,
        placeholder=(
            "Dán nội dung SMS hoặc tin nhắn "
            "cần kiểm tra..."
        ),
    )

    sender = st.text_input(
        "SĐT / Hotline người gửi (không bắt buộc)",
        placeholder=(
            "Ví dụ: 191 hoặc 09xxxxxxxx"
        ),
    )

    analyze_clicked = st.button(
        "Phân tích tin nhắn",
        type="primary",
        use_container_width=True,
    )

    result = st.session_state.get("last_sms_result")

    if analyze_clicked and not text.strip():

        st.warning(
            "Vui lòng nhập nội dung tin nhắn."
        )

        return

    # ==================================
    # ANALYZE
    # ==================================

    if analyze_clicked:
        with st.spinner(
            "Đang phân tích tin nhắn..."
        ):

            result = analyze_sms(
                text,
                sender,
            )

        record_check(
            "sms",
            {"Nội dung tin nhắn": text, "SĐT / Hotline người gửi": sender},
            result,
        )
        st.session_state["last_sms_result"] = result
        st.toast("Đã lưu kết quả vào lịch sử phiên này.", icon="🕘")

    if result is None:
        return

    st.divider()

    # ==================================
    # RISK
    # ==================================

    render_risk_badge(
        result["risk"]["level"],
        result["risk"]["score"],
    )

    # ==================================
    # AI MODEL
    # ==================================

    st.write(
        "### 🤖 Phân tích AI"
    )

    spam = result["spam"]

    if spam["available"]:

        if spam["label"] == "spam":

            st.error(
                "AI đánh giá nội dung "
                "có dấu hiệu Spam / Lừa đảo."
            )

        else:

            st.success(
                "AI đánh giá nội dung "
                "gần với tin nhắn thông thường."
            )

        render_confidence(
            spam["spam_probability"],
            "Khả năng Spam / Lừa đảo",
        )

    else:

        st.info(
            spam["message"]
        )

    # ==================================
    # SIGNALS
    # ==================================

    scam = result["scam"]

    st.write(
        "### 🔎 Dấu hiệu phát hiện"
    )

    if not scam["signals"]:

        st.success(
            "Không phát hiện mẫu lừa đảo "
            "rõ ràng bằng bộ luật hiện tại."
        )

    else:

        for signal in scam["signals"]:

            icon = severity_icon(
                signal["severity"]
            )

            st.markdown(
                f"""
**{icon} {signal['title']}**

Phát hiện: `{
    ", ".join(signal["matches"])
}`
"""
            )

    # ==================================
    # SENDER
    # ==================================

    st.write(
        "### 📱 Xác minh người gửi"
    )

    sender_result = result[
        "sender"
    ]

    if not sender_result["provided"]:

        st.info(
            "Bạn chưa cung cấp SĐT/Hotline "
            "người gửi nên hệ thống không thể "
            "xác minh nguồn gửi."
        )

    elif sender_result["verified"]:

        organization = (
            sender_result.get(
                "organization"
            )
            or "Không xác định"
        )

        st.success(
            f"Hotline có trong danh sách "
            f"đã xác minh: {organization}"
        )

    else:

        st.warning(
            "Không tìm thấy số này trong "
            "danh sách hotline chính thức "
            "đã được hệ thống xác minh."
        )

        st.caption(
            "Điều này không đồng nghĩa "
            "chắc chắn đây là số giả hoặc "
            "số lừa đảo."
        )

    # ==================================
    # URL
    # ==================================

    st.write(
        "### 🔗 Phân tích liên kết"
    )

    if not result["urls"]:

        st.success(
            "Không phát hiện URL "
            "trong nội dung tin nhắn."
        )

    else:

        for item in result["urls"]:

            validation = item[
                "validation"
            ]

            risk = item[
                "risk"
            ]

            st.write(
                f"**URL:** "
                f"`{validation['normalized']}`"
            )

            st.write(
                f"Rủi ro URL: "
                f"**{risk['score'] * 100:.1f}/100**"
            )

            st.write(
                "HTTPS:",
                "✅ Có"
                if validation["https"]
                else "⚠️ Không",
            )

            st.write(
                "Domain tồn tại:",
                "✅ Có"
                if validation["dns_exists"]
                else "❌ Không xác nhận được",
            )

    # ==================================
    # THỐNG KÊ PHÂN TÍCH
    # ==================================

    with st.expander(
        "📊 Chi tiết phân tích kỹ thuật"
    ):

        st.write(
            "**Số dấu hiệu phát hiện:**",
            scam["signal_count"],
        )

        st.write(
            "**Điểm rule-based:**",
            f"{scam['score'] * 100:.1f}/100",
        )

        st.write(
            "**Số URL:**",
            len(
                scam["urls"]
            ),
        )

        st.write(
            "**Số SĐT trong nội dung:**",
            len(
                scam["phones"]
            ),
        )

        if scam["money"]:

            st.write(
                "**Giá trị tài chính phát hiện:**",
                scam["money"],
            )

    # ==================================
    # RECOMMENDATION
    # ==================================

    if result["risk"]["level"] in [
        "medium",
        "high",
    ]:

        st.write(
            "### 🛡️ Khuyến nghị an toàn"
        )

        st.warning(
            """
- Không cung cấp **OTP, mật khẩu hoặc mã PIN**.
- Không cung cấp **CCCD hoặc thông tin ngân hàng** khi chưa xác minh.
- Không chuyển tiền để **nhận thưởng hoặc nhận quà**.
- Không truy cập liên kết đáng ngờ trong SMS.
- Nếu người gửi tự xưng là doanh nghiệp/ngân hàng, hãy liên hệ qua **hotline chính thức**.
- Không coi tên thương hiệu hiển thị trong SMS là bằng chứng tuyệt đối về người gửi.
"""
        )

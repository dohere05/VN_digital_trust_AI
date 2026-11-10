import streamlit as st

from src.analyzers.news_analyzer import (
    analyze_news,
)

from ui.components.confidence_bar import (
    render_confidence,
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
        "📰 Kiểm tra Tin thật / Tin giả"
    )

    st.caption(
        "AI phân tích nội dung tiếng Việt "
        "để đánh giá khả năng nội dung "
        "có dấu hiệu Tin thật hoặc Tin giả."
    )

    # ==================================================
    # INPUT
    # ==================================================

    title = st.text_input(
        "Tiêu đề (không bắt buộc)",
        placeholder=
            "Nhập tiêu đề bài viết hoặc bài đăng...",
    )

    content = st.text_area(
        "Nội dung cần kiểm tra *",
        height=300,
        placeholder=
            "Dán nội dung bài báo, bài đăng "
            "hoặc thông tin cần kiểm tra...",
    )

    analyze_clicked = st.button(
        "Phân tích tin tức",
        type="primary",
        use_container_width=True,
    )

    result = st.session_state.get("last_news_result")

    if analyze_clicked and not content.strip():

        st.warning(
            "Vui lòng nhập nội dung cần kiểm tra."
        )

        return

    # ==================================================
    # ANALYZE
    # ==================================================

    if analyze_clicked:
        with st.spinner(
            "AI đang phân tích nội dung..."
        ):

            result = analyze_news(
                title,
                content,
            )

        record_check(
            "news",
            {"Tiêu đề": title, "Nội dung": content},
            result,
        )
        st.session_state["last_news_result"] = result
        st.toast("Đã lưu kết quả vào lịch sử phiên này.", icon="🕘")

    if result is None:
        return

    prediction = (
        result["prediction"]
    )

    st.divider()

    # ==================================================
    # MODEL NOT AVAILABLE
    # ==================================================

    if not prediction["available"]:

        st.info(
            prediction["message"]
        )

        return

    # ==================================================
    # KẾT QUẢ CHÍNH
    # ==================================================

    if prediction["label"] == "fake":

        st.error(
            "🚨 AI ĐÁNH GIÁ: "
            "CÓ DẤU HIỆU TIN GIẢ"
        )

    else:

        st.success(
            "✅ AI ĐÁNH GIÁ: "
            "CÓ DẤU HIỆU TIN THẬT"
        )

    # ==================================================
    # AI PROBABILITY
    # ==================================================

    st.write(
        "### 🤖 Kết quả AI"
    )

    col1, col2 = st.columns(2)

    fake_probability = (
        prediction.get(
            "fake_probability"
        )
    )

    real_probability = (
        prediction.get(
            "real_probability"
        )
    )

    with col1:

        if fake_probability is not None:

            st.metric(
                "Khả năng Tin giả",
                f"{fake_probability * 100:.1f}%",
            )

    with col2:

        if real_probability is not None:

            st.metric(
                "Khả năng Tin thật",
                f"{real_probability * 100:.1f}%",
            )

    render_confidence(
        prediction.get(
            "confidence"
        ),
        "Độ tin cậy của dự đoán",
    )

    # ==================================================
    # DIỄN GIẢI
    # ==================================================

    fake_prob = (
        fake_probability
        if fake_probability is not None
        else 0
    )

    if fake_prob >= 0.80:

        st.warning(
            "Mô hình phát hiện mức tương đồng cao "
            "với các mẫu Tin giả trong dữ liệu huấn luyện."
        )

    elif fake_prob >= 0.60:

        st.info(
            "Nội dung có một số đặc điểm "
            "tương đồng với Tin giả. "
            "Nên kiểm tra thêm nguồn độc lập."
        )

    elif fake_prob >= 0.40:

        st.info(
            "Kết quả chưa đủ rõ ràng. "
            "Không nên kết luận chỉ dựa trên mô hình."
        )

    else:

        st.success(
            "Mô hình nhận thấy nội dung "
            "gần với nhóm Tin thật hơn."
        )

    # ==================================================
    # SIGNALS
    # ==================================================

    st.write(
        "### 🔎 Dấu hiệu đáng chú ý"
    )

    signals = (
        result[
            "signals"
        ]
    )

    if not signals["signals"]:

        st.info(
            "Không phát hiện mẫu ngôn ngữ "
            "đáng ngờ rõ ràng bằng "
            "bộ luật hiện tại."
        )

    else:

        for signal in signals["signals"]:

            icon = severity_icon(
                signal["severity"]
            )

            matches = ", ".join(
                signal["matches"]
            )

            st.markdown(
                f"""
**{icon} {signal['title']}**

Phát hiện: `{matches}`
"""
            )

    # ==================================================
    # THỐNG KÊ
    # ==================================================

    with st.expander(
        "📊 Chi tiết phân tích kỹ thuật"
    ):

        statistics = (
            result[
                "statistics"
            ]
        )

        st.write(
            "**Số ký tự:**",
            statistics[
                "characters"
            ],
        )

        st.write(
            "**Số từ:**",
            statistics[
                "words"
            ],
        )

        st.write(
            "**Số dấu hiệu ngôn ngữ:**",
            signals[
                "signal_count"
            ],
        )

        st.write(
            "**Nhãn model:**",
            prediction[
                "label"
            ],
        )

        if fake_probability is not None:

            st.write(
                "**Fake probability:**",
                f"{fake_probability * 100:.2f}%",
            )

        if real_probability is not None:

            st.write(
                "**Real probability:**",
                f"{real_probability * 100:.2f}%",
            )

    # ==================================================
    # FACT CHECK GUIDANCE
    # ==================================================

    st.write(
        "### 🛡️ Khuyến nghị xác minh"
    )

    st.info(
        """
- Kiểm tra **nguồn đăng, tác giả và ngày đăng**.
- Đối chiếu với **nhiều nguồn báo chí độc lập**.
- Nếu nội dung nhắc đến cơ quan nhà nước hoặc doanh nghiệp, hãy kiểm tra **website/kênh chính thức** của đơn vị đó.
- Không vội chia sẻ chỉ vì tiêu đề gây sốc hoặc mang tính khẩn cấp.
- Kiểm tra hình ảnh/video nếu nội dung sử dụng chúng làm bằng chứng.
- Với thông tin quan trọng, nên thực hiện **fact-checking độc lập** trước khi tin hoặc chia sẻ.
"""
    )

    st.caption(
        "AI chỉ dự đoán dựa trên các mẫu ngôn ngữ "
        "đã học từ dataset tiếng Việt. "
        "Kết quả không phải bằng chứng tuyệt đối "
        "rằng một sự kiện là thật hay giả."
    )

import streamlit as st
import fitz  # PyMuPDF
import io

st.title("🔄 Thay thế hàng loạt trong PDF")

uploaded_file = st.file_uploader("Tải file PDF", type=["pdf"])
old_text = st.text_input("Chuỗi cần thay thế", value="VIETCARE MADRID 2018 S.L")
new_text = st.text_input("Chuỗi thay thế", value="SUNFLOWER LOGISTIC SL")

if uploaded_file and old_text and new_text:
    if st.button("Thay thế và tải PDF"):
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Duyệt từng trang và thay thế
        for page in doc:
            areas = page.search_for(old_text)
            for rect in areas:
                # Che text cũ
                page.add_redact_annot(rect, fill=(1, 1, 1))
            if areas:
                page.apply_redactions()
                for rect in areas:
                    # Viết text mới vào cùng vị trí
                    page.insert_text(
                        rect.tl,
                        new_text,
                        fontsize=11,
                        fontname="helv"
                    )

        output_bytes = io.BytesIO()
        doc.save(output_bytes)
        doc.close()
        output_bytes.seek(0)

        st.success("✅ Đã thay thế thành công!")
        st.download_button(
            label="Tải PDF đã sửa",
            data=output_bytes,
            file_name="pdf_thay_the.pdf",
            mime="application/pdf"
        )

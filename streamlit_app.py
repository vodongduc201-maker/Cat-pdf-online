import streamlit as st
import PyPDF2
import io

# Cấu hình giao diện Web
st.set_page_config(page_title="Công cụ Tách PDF Tự Động", page_icon="✂️")
st.title("✂️ Trạm Tách PDF Thông Minh")
st.write("Tự động bỏ 2.5cm đầu trang và chia 4 phần bằng nhau.")

# 1. Thành phần Upload file
uploaded_file = st.file_uploader("Chọn file PDF cần tách", type="pdf")

if uploaded_file is not None:
    # Đọc file từ bộ nhớ đệm
    reader = PyPDF2.PdfReader(uploaded_file)
    writer = PyPDF2.PdfWriter()
    
    # Thông số cắt
    loai_bo_cm = 2.5
    pt_per_cm = 28.35
    loai_bo_pt = loai_bo_cm * pt_per_cm

    for page in reader.pages:
        box = page.mediabox
        width = box.width
        height = box.height
        
        remaining_height = height - loai_bo_pt
        h_chunk = remaining_height / 4

        # Tọa độ 4 phần cần giữ
        vung_giu = [
            (h_chunk * 3, height - loai_bo_pt),
            (h_chunk * 2, h_chunk * 3),
            (h_chunk, h_chunk * 2),
            (0, h_chunk)
        ]

        for y_min, y_max in vung_giu:
            new_page = PyPDF2.PageObject.create_blank_page(width=width, height=h_chunk)
            new_page.merge_page(page)
            new_page.mediabox.lower_left = (0, y_min)
            new_page.mediabox.upper_right = (width, y_max)
            writer.add_page(new_page)

    # Xuất file ra bộ nhớ tạm để người dùng tải về
    output_stream = io.BytesIO()
    writer.write(output_stream)
    
    st.success("Đã xử lý xong!")
    st.download_button(
        label="📥 Tải file đã tách về máy",
        data=output_stream.getvalue(),
        file_name="pdf_da_tach.pdf",
        mime="application/pdf"
    )

st.info("Lưu ý: Công cụ này không lưu trữ file của bạn. Mọi xử lý đều diễn ra tức thì.")

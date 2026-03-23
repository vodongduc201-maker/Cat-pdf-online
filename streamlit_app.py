import streamlit as st
import PyPDF2
import io

st.set_page_config(page_title="Công cụ Tách PDF Tùy Chỉnh", page_icon="✂️")
st.title("✂️ Trạm Tách PDF Thông Minh")

# Thêm logo vào Sidebar
st.sidebar.image("https://raw.githubusercontent.com/vodongduc201-maker/logo/main/LON_S%C3%81_X%E1%BB%8A_320_ml-removebg-preview.png", use_container_width=True)
st.sidebar.markdown("---") # Đường kẻ ngang ngăn cách cho đẹp

# --- Phần nút tùy chỉnh ở thanh bên (Sidebar) ---
st.sidebar.header("Cấu hình cắt")
loai_bo_cm = st.sidebar.slider("Độ cao bỏ đi từ đầu trang (cm)", 0.0, 10.0, 2.5)
so_phan = st.sidebar.number_input("Số phần cần chia đều", min_value=1, max_value=20, value=4)

pt_per_cm = 28.35
loai_bo_pt = loai_bo_cm * pt_per_cm

uploaded_file = st.file_uploader("Chọn file PDF cần tách", type="pdf")

if uploaded_file is not None:
    reader = PyPDF2.PdfReader(uploaded_file)
    writer = PyPDF2.PdfWriter()
    
    for page in reader.pages:
        box = page.mediabox
        width = box.width
        height = box.height
        
        # Sử dụng biến so_phan thay vì số 4 cố định
        remaining_height = height - loai_bo_pt
        h_chunk = remaining_height / so_phan

        # Tạo danh sách các vùng cắt dựa trên số phần người dùng chọn
        vung_giu = []
        for i in range(so_phan):
            y_max = height - loai_bo_pt - (i * h_chunk)
            y_min = y_max - h_chunk
            vung_giu.append((max(0, y_min), y_max))

        for y_min, y_max in vung_giu:
            new_page = PyPDF2.PageObject.create_blank_page(width=width, height=y_max - y_min)
            new_page.merge_page(page)
            new_page.mediabox.lower_left = (0, y_min)
            new_page.mediabox.upper_right = (width, y_max)
            writer.add_page(new_page)

    output_stream = io.BytesIO()
    writer.write(output_stream)
    
    st.success(f"Đã xử lý xong! Đã chia thành {so_phan} phần.")
    st.download_button(
        label="📥 Tải file về máy",
        data=output_stream.getvalue(),
        file_name="pdf_tuy_chinh.pdf",
        mime="application/pdf"
    )

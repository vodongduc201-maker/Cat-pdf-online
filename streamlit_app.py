import streamlit as st
import PyPDF2
import io
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Công cụ Tách PDF Tùy Chỉnh", page_icon="✂️")
st.title("✂️ Trạm Tách PDF Thông Minh")

# --- Sidebar (Chỉ giữ lại cấu hình kỹ thuật) ---
st.sidebar.image("https://raw.githubusercontent.com/vodongduc201-maker/logo/main/LON_S%C3%81_X%E1%BB%8A_320_ml-removebg-preview.png", use_container_width=True)
st.sidebar.markdown("---") 

st.sidebar.header("⚙️ Cấu hình cắt")
loai_bo_cm = st.sidebar.slider("Độ cao bỏ đi từ đầu trang (cm)", 0.0, 15.0, 2.0)
so_phan = st.sidebar.number_input("Số phần cần chia đều", min_value=1, max_value=50, value=4)

# --- Giao diện chính ---

# 1. Ô nhập ngày (Đặt trên cùng)
ngay_mac_dinh = datetime.now().strftime("%d-%m")
ngay_nhap = st.text_input("📅 Nhập ngày in (Ví dụ: 13-04)", value=ngay_mac_dinh)

# Chuyển đổi đơn vị
pt_per_cm = 72 / 2.54
loai_bo_pt = loai_bo_cm * pt_per_cm
ten_file_xuat = f"Tem Co.op in 2 lan_{ngay_nhap}.pdf"

# 2. Bộ chọn file PDF
uploaded_file = st.file_uploader("📂 Chọn file PDF cần tách", type="pdf")

if uploaded_file is not None:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        writer = PyPDF2.PdfWriter()
        
        for page_index in range(len(reader.pages)):
            for i in range(so_phan):
                # Copy trang gốc
                page = reader.pages[page_index]
                
                width = float(page.mediabox.width)
                height = float(page.mediabox.height)
                
                remaining_height = height - loai_bo_pt
                h_chunk = remaining_height / so_phan
                
                y_max = height - loai_bo_pt - (i * h_chunk)
                y_min = y_max - h_chunk
                
                # Thực hiện cắt
                page.mediabox.lower_left = (0, max(0, y_min))
                page.mediabox.upper_right = (width, y_max)
                
                writer.add_page(page)

        # Xuất file
        output_stream = io.BytesIO()
        writer.write(output_stream)
        
        st.success(f"✅ Đã xử lý xong! File của bạn: {ten_file_xuat}")
        st.download_button(
            label="📥 Tải file về máy",
            data=output_stream.getvalue(),
            file_name=ten_file_xuat,
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {e}")

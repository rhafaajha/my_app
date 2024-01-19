import streamlit as st
import cv2
import numpy as np
import io
from PIL import Image
from io import BytesIO

# Global variable
original_image = None

# Mengatur judul halaman browser
st.set_page_config(
    page_title="UAS Pengolahan Citra | Menghitung Jumlah Objek pada Citra",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """## UAS Pengolahan Citra. \n\n
        Anggota Kelompok:
    1. BEBY SHAFFIRA \t\t 20102294
    2. ANNISA AZKA PUTRI ZAHRA \t 20102306
    3. RAIHAN AHMAD FAHREZI \t 20102313
    4. FADHILA KHAIRUNNISA \t\t 20102319 \n
    Kelas: S1 IF-09-MM4 \n\n\n\n """
    }
)

def main():
    # Make original_image a global variable
    global original_image 

    st.title("Menghitung Jumlah Objek pada Citra")
    try:
        uploaded_image = st.file_uploader(
            "Upload Image", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            st.sidebar.header("Image Processing")
            kernel = st.sidebar.number_input("Masukkan Threshold kernel", min_value=0, max_value=255, value=178)

            original_image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
            proses = process_image(original_image, kernel)

            col1, col2 = st.columns(2)
            with col1:
                save_image(proses)

            with col2:
                jumlah_objek(original_image, kernel)
            

            col1, col2 = st.columns(2)
            with col1:
                st.image(original_image, channels="BGR", caption="Original Image", use_column_width=True)

            with col2:
                st.image(proses, channels="BGR", caption="Processed Image", use_column_width=True)
        else:
            st.sidebar.info(f"""Harap masukkan gambar terlebih dahulu""")
    except Exception as e:
        st.sidebar.error(f"Terjadi kesalahan: {str(e)}")

def process_image(img, kernel):
    st.sidebar.header("Setting Line")
    box_color_hex = st.sidebar.color_picker(label="Box Color", value='#0000ff')

    # Convert hex color to scalar (r, g, b)
    box_color_rgb = tuple(int(box_color_hex[i:i+2], 16) for i in (1, 3, 5))
    box_color_bgr = tuple(reversed(box_color_rgb))  # Convert to BGR

    opsi = st.sidebar.selectbox("Pilih Shape", options=["Outline", "Fill"])
    if opsi == "Outline":
        width = st.sidebar.number_input(label="Thickness", min_value=1, max_value=25, value=5)
    elif opsi == "Fill":
        width = cv2.FILLED

    img_copy = img.copy()
    grayscale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(grayscale_image, kernel, 255, cv2.THRESH_BINARY)[1]
    image = ~binary_image

    (cnt, _) = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    # processed_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    img_copy = cv2.drawContours(img_copy, cnt, -1, box_color_bgr, width)
    return img_copy

def jumlah_objek(img, kernel):
    grayscale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(grayscale_image, kernel, 255, cv2.THRESH_BINARY)[1]
    image = ~binary_image

    (cnt, _) = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    object_count = len(cnt)
    st.info(f"Jumlah Objek pada Citra: {object_count}")
    return object_count

def save_image(image):
    # Menggunakan BytesIO untuk menyimpan gambar tanpa menyimpan ke file
    image_bytes = BytesIO()
    Image.fromarray(image).save(image_bytes, format="JPEG")
    if st.download_button(
        label="Download Processed Image",
        data=image_bytes.getvalue(),
        file_name="download_processed.jpg",
        mime="image/jpeg"
    ):
        st.toast(f"Gambar telah berhasil diunduh")

if __name__ == "__main__":
    main()

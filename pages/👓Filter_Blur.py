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
    page_title="UAS Pengolahan Citra | Filter Blur",
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
    st.title("Filter Blur")

    try:
        uploaded_image = st.file_uploader(
            "Upload Image", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            st.sidebar.header("Image Processing")
            process_image(uploaded_image)
            save_image(original_image)
            col1, col2 = st.columns(2)
            with col1:
                display_image_asli(uploaded_image)

            with col2:
                display_image_edit()

        else:
            st.sidebar.info(f"""Harap masukkan gambar terlebih dahulu""")

    except Exception as e:
        st.sidebar.error(f"Terjadi kesalahan: {str(e)}")


def process_image(uploaded_image):
    global original_image
    original_image = cv2.cvtColor(cv2.imdecode(np.fromstring(
        uploaded_image.read(), np.uint8), 1), cv2.COLOR_BGR2RGB)

    filter_name = st.sidebar.selectbox(
        "Choose Filter", ["None", "Median Blur", "Gaussian Blur", "Bilateral Filter"])
    if filter_name != "None":
        apply_filter(filter_name)


def apply_filter(filter_name):
    global original_image
    if filter_name == "Median Blur":
        original_image = cv2.medianBlur(original_image, 5)
    elif filter_name == "Gaussian Blur":
        original_image = cv2.GaussianBlur(original_image, (5, 5), 0)
    elif filter_name == "Bilateral Filter":
        original_image = cv2.bilateralFilter(original_image, 9, 75, 75)


def save_image(image):
    edited_image = Image.fromarray(image)

    # Menggunakan BytesIO untuk menyimpan gambar tanpa menyimpan ke file
    image_bytes = io.BytesIO()
    edited_image.save(image_bytes, format="JPEG")
    if st.download_button(
        label="Download Processed Image",
        data=image_bytes.getvalue(),
        file_name="download_filter.jpg",
        mime="image/jpeg"
    ):
        st.toast(f"Gambar telah berhasil diunduh")


def display_image_asli(uploaded_image):
    st.image(uploaded_image, caption="Original Image", use_column_width=True)


def display_image_edit():
    st.image(original_image, caption="Processed Image", use_column_width=True)


if __name__ == "__main__":
    main()

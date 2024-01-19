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
        global original_image
        uploaded_image = st.file_uploader(
            "Upload Image", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            st.sidebar.header("Image Processing")
            original_image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)

            # Get user input for filter parameters
            filter_type = st.sidebar.selectbox("Select Filter", [
                                               "None", "Lowpass", "Highpass", "High-Boost", "Emboss", "Gaussian", "Median", "Bilateral"])

            if filter_type == "Lowpass" or filter_type == "Highpass" or filter_type == "High-Boost" or filter_type == "Gaussian":
                kernel_size = st.sidebar.slider("Kernel Size", 1, 25, 3)

            if filter_type == "High-Boost":
                boost_factor = st.sidebar.slider("Boost Factor", 1.0, 5.0, 2.0)

            # Apply selected filter
            if filter_type == "Lowpass":
                original_image = apply_lowpass_filter(
                    original_image, kernel_size)
            elif filter_type == "Highpass":
                original_image = apply_highpass_filter(
                    original_image, kernel_size)
            elif filter_type == "High-Boost":
                original_image = apply_high_boost_filter(
                    original_image, kernel_size, boost_factor)
            elif filter_type == "Emboss":
                original_image = apply_emboss_filter(original_image)
            elif filter_type == "Gaussian":
                original_image = apply_gaussian_filter(
                    original_image, kernel_size)
            elif filter_type == "Median":
                original_image = medianBlur(original_image)
            elif filter_type == "Bilateral":
                original_image = bilateralFilter(original_image)

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


def medianBlur(img):
    kernel_size = st.sidebar.slider("Kernel Size", 1, 25, 5)
    return cv2.medianBlur(img, kernel_size)


def bilateralFilter(img):
    return cv2.bilateralFilter(img, 9, 75, 75)


def apply_lowpass_filter(img, kernel_size):
    # Apply lowpass filter (e.g., averaging)
    blurred_img = cv2.blur(img, (kernel_size, kernel_size))
    return blurred_img


def apply_highpass_filter(img, kernel_size):
    # Apply highpass filter (e.g., using Laplacian)
    blurred_img = cv2.blur(img, (kernel_size, kernel_size))
    highpass_img = img - blurred_img
    return highpass_img


def apply_high_boost_filter(img, kernel_size, boost_factor):
    # Apply high-boost filter (enhances edges)
    blurred_img = cv2.blur(img, (kernel_size, kernel_size))
    highpass_img = img - blurred_img
    high_boost_img = img + boost_factor * highpass_img
    return high_boost_img


def apply_emboss_filter(img):
    # Apply emboss filter
    kernel = np.array([[0, -1, -1],
                       [1,  0, -1],
                       [1,  1,  0]])
    emboss_img = cv2.filter2D(img, -1, kernel)
    return emboss_img


def apply_gaussian_filter(img, kernel_size):
    # Apply Gaussian filter
    gaussian_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    return gaussian_img


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
    st.image(uploaded_image, channels="BGR", caption="Original Image", use_column_width=True)


def display_image_edit():
    st.image(original_image, channels="BGR",  caption="Processed Image", use_column_width=True)


if __name__ == "__main__":
    main()

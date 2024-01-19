import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

# Global variable
original_image = None

# Mengatur judul halaman browser
st.set_page_config(
    page_title="UAS Pengolahan Citra | Restorasi Citra",
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


def degrade_image(img, degradation_level):
    # Simulate image degradation (e.g., blur)
    kernel_size = int(degradation_level)
    blurred_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    return blurred_img


def add_noise(img, noise_level):
    # Simulate image noise addition
    noise = np.random.normal(0, noise_level, img.shape)
    noisy_img = np.clip(img + noise, 0, 255).astype(np.uint8)
    return noisy_img


def denoise_image(img, denoise_strength):
    # Apply image denoising (e.g., using Non-Local Means Denoising)
    denoised_img = cv2.fastNlMeansDenoisingColored(
        img, None, denoise_strength, None, 7, 21)
    return denoised_img


def main():
    st.title("Restorasi Citra")

    uploaded_image = st.file_uploader(
        "Upload Image", type=["jpg", "jpeg", "png"])

    try:
        if uploaded_image is not None:
            st.sidebar.header("Image Processing")
            # Read the uploaded image
            img = cv2.imdecode(np.frombuffer(
                uploaded_image.read(), np.uint8), 1)

            # Get user input for image degradation, noise, and denoising strength
            opsi = st.sidebar.selectbox("Pilih Shape", options=[
                                        "Degradasi", "Noise", "Denoising"])

            if opsi == "Degradasi":
                degradation_level = st.sidebar.slider(
                    "Image Degradation Level", 1, 15, 1)
                # Apply image degradation
                edited_image = degrade_image(img, degradation_level)
            elif opsi == "Noise":
                noise_level = st.sidebar.slider("Noise Level", 0.0, 50.0, 0.0)
                # Apply noise addition
                edited_image = add_noise(img, noise_level)
            elif opsi == "Denoising":
                denoise_strength = st.sidebar.slider(
                    "Denoising Strength", 1.0, 100.0, 10.0)
                # Apply denoising
                edited_image = denoise_image(img, denoise_strength)

            save_image(edited_image)

            # Display the original and edited images
            col1, col2 = st.columns(2)
            with col1:
                st.image(img, channels="BGR",
                         caption="Original Image", use_column_width=True)

            with col2:
                st.image(edited_image, channels="BGR",
                         caption="Processed Image", use_column_width=True)
        else:
            st.sidebar.info(f"""Harap masukkan gambar terlebih dahulu""")
    except Exception as e:
        st.sidebar.error(f"Terjadi kesalahan: {str(e)}")


def save_image(image):
    # Menggunakan BytesIO untuk menyimpan gambar tanpa menyimpan ke file
    image_bytes = BytesIO()
    Image.fromarray(image).save(image_bytes, format="JPEG")
    if st.download_button(
        label="Download Processed Image",
        data=image_bytes.getvalue(),
        file_name="download_restorasi.jpg",
        mime="image/jpeg"
    ):
        st.toast(f"Gambar telah berhasil diunduh")


if __name__ == "__main__":
    main()

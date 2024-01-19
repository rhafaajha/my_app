import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

# Global variable
original_image = None

# Mengatur judul halaman browser
st.set_page_config(
    page_title="UAS Pengolahan Citra | Edit Citra",
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


def adjust_image(img, hue, saturation, brightness, contrast):
    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert RGB to PIL Image
    pil_img = Image.fromarray(img_rgb)

    # Adjust hue, saturation, brightness, and contrast using PIL
    pil_img = pil_img.convert("HSV")

    # Adjust hue
    pil_img = pil_img.point(lambda i: (i + hue) % 256)

    # Adjust saturation
    pil_img = pil_img.point(lambda i: max(0, min(255, i + saturation)))

    # Adjust brightness
    pil_img = pil_img.point(lambda i: max(0, min(255, i + brightness)))

    # Adjust contrast
    pil_img = pil_img.point(lambda i: max(
        0, min(255, int((i - 128) * contrast) + 128)))

    # Convert back to RGB
    img_rgb = pil_img.convert("RGB")

    # Convert RGB to BGR
    img_result = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2BGR)

    return img_result


def main():
    st.title("Edit Citra")

    uploaded_image = st.file_uploader(
        "Upload Image", type=["jpg", "jpeg", "png"])

    try:
        if uploaded_image is not None:
            st.sidebar.header("Image Processing")
            # Read the uploaded image
            img = cv2.imdecode(np.frombuffer(
                uploaded_image.read(), np.uint8), 1)

            # Get user input for adjustments
            hue = st.sidebar.slider("Hue", -180, 180, 0)
            saturation = st.sidebar.slider("Saturation", -100, 100, 0)
            brightness = st.sidebar.slider("Brightness", -100, 100, 0)
            contrast = st.sidebar.slider("Contrast", 0.0, 3.0, 1.0)

            # Apply adjustments to the image
            edited_image = adjust_image(
                img, hue, saturation, brightness, contrast)

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
        file_name="download_edit.jpg",
        mime="image/jpeg"
    ):
        st.toast(f"Gambar telah berhasil diunduh")


if __name__ == "__main__":
    main()

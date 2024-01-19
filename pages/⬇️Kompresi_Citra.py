import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Mengatur judul halaman browser
st.set_page_config(
    page_title="UAS Pengolahan Citra | Kompresi Citra",
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


def compress_image(img, format, quality):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]

    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert RGB to PIL Image
    pil_img = Image.fromarray(img_rgb)

    # Convert PIL Image to bytes
    img_bytes = io.BytesIO()
    pil_img.save(img_bytes, format=format, quality=quality)

    # Read bytes and decode to BGR
    img_compressed = cv2.imdecode(np.frombuffer(
        img_bytes.getvalue(), dtype=np.uint8), 1)

    return img_compressed


def main():
    st.title("Kompresi Citra")

    try:
        uploaded_image = st.file_uploader(
            "Upload Image", type=["jpg", "jpeg", "png"])

        if uploaded_image is not None:
            st.sidebar.header("Image Processing")
            # Read the uploaded image
            img = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)

            # Get user input for compression options
            compression_format = st.sidebar.selectbox(
                "Compression Format", ["JPEG", "PNG"])
            compression_quality = st.sidebar.slider(
                "Compression Quality", 0, 1000, 500)

            # Apply compression
            compressed_image = compress_image(img, compression_format.lower(), compression_quality)
            save_image(compressed_image)

            col1, col2 = st.columns(2)
            with col1:
                # Display the original image
                st.image(img, channels="BGR",
                         caption="Original Image", use_column_width=True)

            with col2:
                # Display the compressed image
                st.image(compressed_image, channels="BGR",
                         caption="Processed Image", use_column_width=True)
        else:
            st.sidebar.info(f"""Harap masukkan gambar terlebih dahulu""")
    except Exception as e:
        st.sidebar.error(f"Terjadi kesalahan: {str(e)}")


# Adjust the save_image function to take the image parameter
def save_image(image):
    edited_image = Image.fromarray(image)

    # Menggunakan BytesIO untuk menyimpan gambar tanpa menyimpan ke file
    image_bytes = io.BytesIO()
    edited_image.save(image_bytes, format="JPEG")
    if st.download_button(
        label="Download Processed Image",
        data=image_bytes.getvalue(),
        file_name="download_kompres.jpg",
        mime="image/jpeg"
    ):
        st.toast("Gambar telah berhasil diunduh")


if __name__ == "__main__":
    main()

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
    page_title="UAS Pengolahan Citra | Resize Citra",
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
    st.title("Resize Citra")
    try:
        uploaded_image = st.file_uploader(
            "Upload Image", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            st.sidebar.header("Image Processing")
            process_image(uploaded_image)
            save_image(original_image)
            display_image_asli(uploaded_image)
            display_image_edit()
        else:
            st.sidebar.info(f"""Harap masukkan gambar terlebih dahulu""")
    except Exception as e:
        st.sidebar.error(f"Terjadi kesalahan: {str(e)}")


# Inisialisasi session_state
if 'width' not in st.session_state:
    st.session_state.width = None

if 'height' not in st.session_state:
    st.session_state.height = None

if 'clear_cache' not in st.session_state:
    st.session_state.clear_cache = False


def process_image(uploaded_image):
    global original_image

    # Cek apakah clear_cache sudah di-set
    if st.session_state.clear_cache:
        st.session_state.width = None
        st.session_state.height = None
        st.session_state.clear_cache = False

    original_image = cv2.cvtColor(cv2.imdecode(np.fromstring(
        uploaded_image.read(), np.uint8), 1), cv2.COLOR_BGR2RGB)

    # Check if session_state is initialized
    if st.session_state.width is None:
        st.session_state.width = original_image.shape[1]

    if st.session_state.height is None:
        st.session_state.height = original_image.shape[0]

    # Slider to resize image
    width = st.sidebar.number_input(
        "Resize Width", min_value=1, value=st.session_state.width)
    height = st.sidebar.number_input(
        "Resize Height", min_value=1, value=st.session_state.height)

    # Reset button
    button_reset = st.sidebar.button("Reset")

    # Check if Reset button is clicked
    if button_reset:
        st.session_state.width = original_image.shape[1]
        st.session_state.height = original_image.shape[0]
        resize_image(st.session_state.width, st.session_state.height)
        st.session_state.clear_cache = True

    elif width != st.session_state.width or height != st.session_state.height:
        st.session_state.width = width
        st.session_state.height = height
        resize_image(width, height)
        st.session_state.clear_cache = True


def resize_image(width, height):
    global original_image
    original_image = cv2.resize(
        original_image, (width, height), interpolation=cv2.INTER_CUBIC)


def save_image(image):
    edited_image = Image.fromarray(image)

    # Menggunakan BytesIO untuk menyimpan gambar tanpa menyimpan ke file
    image_bytes = io.BytesIO()
    edited_image.save(image_bytes, format="JPEG")
    if st.download_button(
        label="Download Processed Image",
        data=image_bytes.getvalue(),
        file_name="download_resize.jpg",
        mime="image/jpeg"
    ):
        st.toast(f"Gambar telah berhasil diunduh")


def display_image_asli(uploaded_image):
    st.image(uploaded_image, caption="Original Image", use_column_width=False)


def display_image_edit():
    st.image(original_image, caption="Processed Image", use_column_width=False)


if __name__ == "__main__":
    main()

import streamlit as st
import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline
from PIL import Image
import io

# Global variable
original_image = None

# Mengatur judul halaman browser
st.set_page_config(
    page_title="UAS Pengolahan Citra | Filter Warna",
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
    # """Fungsi utama aplikasi"""
    st.title("Filter Warna")
    try:
        uploaded_image = st.file_uploader(
            "Upload Image", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            st.sidebar.header("Image Processing")
            filter_type = st.sidebar.selectbox("Select Filter", [
                                               "None", "Pencil Sketch", "Warming Filter", "Cooling Filter", "Cartoonizer", "Grayscale", "Invert"])
            apply_filter(uploaded_image, filter_type)
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


def pencil_sketch(img_rgb, bg_gray='uas\\my_app\\asset\\pencilsketch_bg.jpg'):
    # """Menerapkan efek pensil pada citra"""

    # Mendapatkan ukuran gambar
    height, width, _ = img_rgb.shape

    # Membaca gambar latar belakang jika tersedia
    canvas = cv2.imread(bg_gray, cv2.IMREAD_GRAYSCALE)
    if canvas is not None:
        canvas = cv2.resize(canvas, (width, height))

    # Mengubah gambar RGB menjadi skala abu-abu
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Melakukan Gaussian blur pada gambar skala abu-abu
    img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0)

    # Membuat efek pensil dengan membagi gambar skala abu-abu dengan gambar blur
    img_blend = cv2.divide(img_gray, img_blur, scale=256)

    # Jika canvas (latar belakang) tersedia, campurkan dengan gambar hasil
    if canvas is not None:
        img_blend = cv2.multiply(img_blend, canvas, scale=1.5 / 256)

    # Konversi kembali ke format RGB
    img_result = cv2.cvtColor(img_blend, cv2.COLOR_GRAY2RGB)

    return img_result



def warming_filter(img_rgb):
    # """Menerapkan filter pemanasan pada citra"""
    incr_ch_lut = create_LUT_8UC1(
        [0, 64, 128, 192, 256], [0, 70, 140, 210, 256])
    decr_ch_lut = create_LUT_8UC1(
        [0, 64, 128, 192, 256], [0, 30,  80, 120, 192])

    c_r, c_g, c_b = cv2.split(img_rgb)
    c_r = cv2.LUT(c_r, incr_ch_lut).astype(np.uint8)
    c_b = cv2.LUT(c_b, decr_ch_lut).astype(np.uint8)
    img_rgb = cv2.merge((c_r, c_g, c_b))

    c_h, c_s, c_v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
    c_s = cv2.LUT(c_s, incr_ch_lut).astype(np.uint8)

    return cv2.cvtColor(cv2.merge((c_h, c_s, c_v)), cv2.COLOR_HSV2RGB)


def cooling_filter(img_rgb):
    # """Menerapkan filter pendinginan pada citra"""
    incr_ch_lut = create_LUT_8UC1(
        [0, 64, 128, 192, 256], [0, 70, 140, 210, 256])
    decr_ch_lut = create_LUT_8UC1(
        [0, 64, 128, 192, 256], [0, 30,  80, 120, 192])

    c_r, c_g, c_b = cv2.split(img_rgb)
    c_r = cv2.LUT(c_r, decr_ch_lut).astype(np.uint8)
    c_b = cv2.LUT(c_b, incr_ch_lut).astype(np.uint8)
    img_rgb = cv2.merge((c_r, c_g, c_b))

    c_h, c_s, c_v = cv2.split(cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV))
    c_s = cv2.LUT(c_s, decr_ch_lut).astype(np.uint8)

    return cv2.cvtColor(cv2.merge((c_h, c_s, c_v)), cv2.COLOR_HSV2RGB)


def cartoonizer(img_rgb):
    # """Menerapkan efek kartun pada citra"""
    numDownSamples = 2
    numBilateralFilters = 7

    img_color = img_rgb
    for _ in range(numDownSamples):
        img_color = cv2.pyrDown(img_color)

    for _ in range(numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

    for _ in range(numDownSamples):
        img_color = cv2.pyrUp(img_color)

    img_color = cv2.resize(img_color, img_rgb.shape[:2])

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    img_edge = cv2.adaptiveThreshold(
        img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)

    return cv2.bitwise_and(img_color, img_edge)


def grayscale_image(img_rgb):
    return cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)


def invert_image(img_rgb):
    return cv2.bitwise_not(img_rgb)


def apply_filter(uploaded_image, filter_type):
    global original_image

    # Konversi UploadedFile menjadi Numpy Array
    image_np = np.array(Image.open(uploaded_image))

    # Menerapkan filter tertentu pada citra
    if filter_type == 'Pencil Sketch':
        original_image = pencil_sketch(image_np)
    elif filter_type == 'Warming Filter':
        original_image = warming_filter(image_np)
    elif filter_type == 'Cooling Filter':
        original_image = cooling_filter(image_np)
    elif filter_type == 'Cartoonizer':
        original_image = cartoonizer(image_np)
    elif filter_type == 'Grayscale':
        original_image = grayscale_image(image_np)
    elif filter_type == 'Invert':
        original_image = invert_image(image_np)
    else:
        original_image = image_np

    return original_image


def create_LUT_8UC1(x, y):
    spl = UnivariateSpline(x, y)
    return spl(range(256))


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

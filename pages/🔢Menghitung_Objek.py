import streamlit as st
import cv2
import io
import numpy as np
from PIL import Image
from io import BytesIO
from streamlit_cropper import st_cropper

# Set Streamlit page configuration
st.set_page_config(
    page_title="UAS Pengolahan Citra | Cropped Citra",
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


def save_image(image):
    edited_image = Image.fromarray(image)

    # Menggunakan BytesIO untuk menyimpan gambar tanpa menyimpan ke file
    image_bytes = io.BytesIO()
    edited_image.save(image_bytes, format="JPEG")
    st.sidebar.header("Download Button")
    if st.sidebar.download_button(
        label="Download Processed Image",
        data=image_bytes.getvalue(),
        file_name="download.jpg",
        mime="image/jpeg"
    ):
        st.toast("Gambar telah berhasil diunduh")


def main():
    # Global variable
    original_image = None

    st.title("Cropped Citra")

    try:
        img_file = st.file_uploader(
            "Upload an image", type=["jpg", "jpeg", "png"])

        if img_file is not None:
            st.sidebar.header("Image Processing")

            box_color = st.sidebar.color_picker(
                label="Box Color", value='#0000FF')

            aspect_choice = st.sidebar.selectbox(label="Aspect Ratio", options=[
                                                 "1:1", "16:9", "4:3", "2:3", "Free"])
            aspect_dict = {
                "1:1": (1, 1),
                "16:9": (16, 9),
                "4:3": (4, 3),
                "2:3": (2, 3),
                "Free": None
            }
            aspect_ratio = aspect_dict[aspect_choice]

            img = Image.open(img_file)
            return_type = 'box'
            if return_type:
                rect = st_cropper(
                    img,
                    realtime_update=True,
                    box_color=box_color,
                    aspect_ratio=aspect_ratio,
                    return_type=return_type,
                    stroke_width=3
                )

                raw_image = np.asarray(img).astype('uint8')
                left, top, width, height = tuple(map(int, rect.values()))

            col1, col2 = st.columns(2)
            with col1:
                st.image(img, caption='Original Image', use_column_width=True)

            with col2:
                original_image = raw_image[top:top + height, left:left + width]
                st.image(Image.fromarray(original_image),
                         caption='Processed Image', use_column_width=True)

            save_image(original_image)

        else:
            st.sidebar.info("Harap masukkan gambar terlebih dahulu")
    except Exception as e:
        st.sidebar.error(f"Terjadi kesalahan: {str(e)}")


if __name__ == "__main__":
    main()

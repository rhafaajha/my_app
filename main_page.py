import streamlit as st
import cv2
import numpy as np
import io
from PIL import Image
from io import BytesIO

#clear cache
st.cache_data.clear()

# Mengatur judul halaman browser
st.set_page_config(
    page_title="UAS Pengolahan Citra | Main Page",
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

st.markdown("# 🌟 Selamat Datang di Web Studio Citra 🌟")
st.sidebar.success(f"Select a page above.")
st.text(""" Temukan Kreativitas Tanpa Batas dalam Setiap Pixel!""")

st.markdown("### 📸 Fitur Unggulan Kami:")
st.text("""1. Rekayasa Citra Canggih: Transformasikan citra biasa menjadi karya seni luar biasa dengan teknologi rekayasa citra
   tingkat tinggi.
2. Segmentasi Otomatis: Pisahkan objek dengan sempurna dalam hitungan detik menggunakan algoritma segmentasi otomatis.
3. Penyempurnaan Warna: Tambahkan kehidupan pada gambar Anda dengan fitur penyempurnaan warna yang intuitif
   dan mudah digunakan.
4. Filter Artistik: Berikan sentuhan seni pada setiap citra dengan beragam filter artistik yang tersedia.
5. Peningkatan Resolusi: Jelajahi setiap detail dengan peningkatan resolusi cerdas untuk citra yang tajam dan jelas.""")

st.markdown("### 🚀 Mengapa Memilih Kami?")
st.text("""1. Antarmuka Pengguna yang Ramah Pengguna: Pengalaman pengguna yang mulus dan intuitif untuk pengolahan
   citra yang menyenangkan.
2. Kecepatan dan Efisiensi: Proses cepat untuk memastikan pengolahan citra yang efisien dan tanpa hambatan.
3. Kompabilitas Multi-Platform: Nikmati fungsionalitas lengkap di berbagai perangkat dan platform.

   Dari pemula hingga profesional, Kami hadir untuk memenuhi semua kebutuhan pengolahan citra Anda.
Mari bersama-sama menciptakan keindahan visual yang tak terlupakan!""")
st.markdown("### 🔗 Mulai Petualangan Citra Anda Sekarang!")


st.markdown("### ⚠️ Kredit")
st.text("""Dibuat oleh:
1. BEBY SHAFFIRA \t\t 20102294
2. ANNISA AZKA PUTRI ZAHRA \t 20102306
3. RAIHAN AHMAD FAHREZI \t 20102313
4. FADHILA KHAIRUNNISA \t\t 20102319 \n
Kelas: S1 IF-09-MM4

Dibuat untuk memenuhi tugas akhir mata kuliah pengolahan citra
 """)
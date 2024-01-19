## Getting Started

First, run the development server:

```bash
streamlit run main_page.py
```

Open [http://localhost:8501](http://localhost:8501) with your browser to see the result.

## Instalasi

Untuk menggunakan proyek ini, ikuti langkah-langkah instalasi berikut:

1. Pastikan Anda memiliki Python yang terinstal di sistem Anda. Jika belum, Anda dapat mengunduhnya dari [situs resmi Python](https://www.python.org/).

2. Buka terminal atau command prompt.

3. Buat virtual environment (opsional, tapi disarankan):

    ```bash
    python -m venv env
    ```

4. Aktifkan virtual environment (opsional):

    - Windows:

      ```bash
      .\env\Scripts\activate
      ```

    - macOS/Linux:

      ```bash
      source env/bin/activate
      ```

5. Install dependensi menggunakan pip:

    ```bash
    pip install streamlit opencv-python Pillow streamlit-cropper
    ```

## Penggunaan

Setelah instalasi selesai, Anda dapat mengimpor library seperti berikut:

```python
import streamlit as st
import cv2
import io
import numpy as np
from PIL import Image
from io import BytesIO
from streamlit_cropper import st_cropper
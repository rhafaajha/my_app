## Menjalankan Aplikasi

1. Pertama, buka terminal atau command prompt.
2. Kedua, masuk ke direktori yang menampung file aplikasi:

```bash
cd my_app
# or
cd my_app-main
```

3. Kedua, jalankan server pengembangan:

```bash
streamlit run main_page.py
```

Buka [http://localhost:8501](http://localhost:8501) dengan browser Anda untuk melihat hasilnya.

## Instalasi

Untuk menggunakan proyek ini, ikuti langkah-langkah instalasi berikut:

1. Pastikan Anda memiliki Python yang terinstal di sistem Anda. Jika belum, Anda dapat mengunduhnya dari [situs resmi Python](https://www.python.org/).

2. Buka terminal atau command prompt.

3. Clone repository ini ke komputer lokal Anda:

   ```bash
   git clone https://github.com/rhafaajha/my_app.git
   ```

4. Buat virtual environment (opsional, tapi disarankan):

    ```bash
    python -m venv env
    ```

5. Aktifkan virtual environment (opsional):

    - Windows:

      ```bash
      .\env\Scripts\activate
      ```

    - macOS/Linux:

      ```bash
      source env/bin/activate
      ```

6. Install dependensi menggunakan pip:

    ```bash
    pip install streamlit opencv-python Pillow streamlit-cropper scipy
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
```

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, harap ikuti langkah-langkah berikut:

1. Fork repository ini.
2. Buat branch baru: ```git checkout -b fitur-baru```.
3. Lakukan perubahan yang diperlukan.
4. Commit perubahan Anda: ```git commit -m 'Menambahkan fitur baru'```.
5. Push ke branch: ```git push origin fitur-baru```.
6. Buat pull request.

Terima kasih telah berkontribusi!
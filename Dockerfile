# Menggunakan citra dasar Python
FROM python:3.9-slim

# Menetapkan direktori kerja di dalam kontainer
WORKDIR /app

# Menyalin file requirements.txt dan menginstal semua dependensi
# Menggunakan --no-cache-dir untuk mengurangi ukuran citra
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin semua file aplikasi dari direktori lokal ke direktori kontainer
COPY . .

# Menentukan perintah untuk menjalankan aplikasi saat kontainer dimulai
# Gunicorn akan mendengarkan di port yang disediakan oleh Cloud Run ($PORT)
CMD exec gunicorn --bind :$PORT main:app
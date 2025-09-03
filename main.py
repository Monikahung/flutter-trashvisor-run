from flask import Flask, request, jsonify
from google.cloud import storage
import datetime
import os

app = Flask(__name__)

# Nama bucket dari Google Cloud Storage
BUCKET_NAME = "trashvisor-dataset"

@app.route("/generate-signed-url", methods=["POST"])
def generate_signed_url():
    """
    Menghasilkan URL yang ditandatangani (signed URL) untuk mengunggah file ke Google Cloud Storage.
    """
    data = request.get_json()
    file_name = data.get("file_name")
    user_id = data.get("user_id")

    if not file_name or not user_id:
        return jsonify({"error": "file_name dan user_id diperlukan"}), 400

    # Membuat path blob dengan user_id sebagai folder
    blob_path = f"{user_id}/{file_name}"

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_path)

        # Menghasilkan URL yang ditandatangani untuk mengunggah file
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=15),  # URL berlaku selama 15 menit
            method="PUT",
            content_type="image/jpeg"
        )

        return jsonify({"signed_url": url})
    except Exception as e:
        # Menangani kesalahan jika terjadi
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Mengambil port dari variabel lingkungan yang disediakan oleh Cloud Run
    port = int(os.environ.get("PORT", 8080))
    # Menjalankan aplikasi, mendengarkan di semua antarmuka jaringan (0.0.0.0)
    # Ini sangat penting agar Cloud Run dapat mengarahkan traffic ke kontainer Anda
    app.run(host="0.0.0.0", port=port)
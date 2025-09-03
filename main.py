import os
import datetime
from flask import Flask, request, jsonify
from google.cloud import storage
from google.auth import compute_engine
from google.auth import default

# Pastikan nama bucket sudah benar
BUCKET_NAME = "trashvisor-dataset"

app = Flask(__name__)

@app.route("/generate-signed-url", methods=["POST"])
def generate_signed_url():
    """
    Menghasilkan URL yang ditandatangani untuk mengunggah file ke Google Cloud Storage.
    """
    data = request.get_json()
    file_name = data.get("file_name")
    user_id = data.get("user_id")

    if not file_name or not user_id:
        return jsonify({"error": "file_name dan user_id diperlukan"}), 400

    # Membuat path blob dengan user_id sebagai folder
    blob_path = f"{user_id}/{file_name}"

    try:
        # Gunakan kredensial default dari lingkungan. Ini adalah pendekatan yang paling andal.
        credentials, project = default()
        storage_client = storage.Client(credentials=credentials, project=project)
        
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_path)

        # Menghasilkan URL yang ditandatangani
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=15),  # URL berlaku selama 15 menit
            method="PUT",
            content_type="image/jpeg"
        )

        return jsonify({"signed_url": url})
    except Exception as e:
        # Menangani kesalahan dan mengembalikannya sebagai respons JSON
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
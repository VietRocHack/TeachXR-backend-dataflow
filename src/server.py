from flask import Flask, request, jsonify, make_response, send_file
from io import BytesIO
from flask_cors import CORS
from flask_socketio import SocketIO
from services.ocrservice import OCRService
from services.databaseservice import DatabaseService
from dotenv import load_dotenv
from bson import Binary
import os, base64
import json


load_dotenv()

IS_PROD = os.getenv("IS_PROD") == "True" # Set to True when deploying to production
print(f"Running in production: {IS_PROD}")

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_ERROR = 500

ocr_service = OCRService()
database_service = DatabaseService(is_prod=IS_PROD)

@app.route('/')
def home():
    return "Welcome to the OCR Server!"

@app.route("/ocr", methods=["POST"])
def image_ocr():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), HTTP_BAD_REQUEST

    file = request.files['image']
    text = ""

    try:
        text = ocr_service.extract_text_from_filestorage(file)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_ERROR
    
    # Reset the file pointer to the beginning of the file, 
    # as reading the file for text extraction moves the pointer to the end of the file
    file.seek(0)

    try:
        database_service.add_to_database("vision_data", text, Binary(file.read()))
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_ERROR
    
    socketio.emit("newData", text)
    
    return text, HTTP_OK

@app.route("/get_latest", methods=["GET"])
def get_latest():
    try:
        latest_text = database_service.get_latest_from_database("vision_data")
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_ERROR
    image_bytesio = BytesIO(latest_text['image'])
    image_bytesio.seek(0)
    response = make_response(send_file(image_bytesio, download_name="image.png", as_attachment=True))
    extra_data = {
        "text": latest_text['text'],
        "timestamp": str(latest_text['timestamp'])
    }
    response.headers['X-Extra-Data'] = base64.b64encode(json.dumps(extra_data).encode()).decode()
    return response, HTTP_OK

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=not IS_PROD)
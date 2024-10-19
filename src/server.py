from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from services.ocrservice import OCRService
from services.databaseservice import DatabaseService
from dotenv import load_dotenv
from bson import Binary
import os


load_dotenv()

IS_PROD = bool(os.getenv("IS_PROD")) # Set to True when deploying to production

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

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
    
    socketio.emit("new_document", "OK")
    
    return text, HTTP_OK

@app.route("/get_latest", methods=["GET"])
def get_latest():
    try:
        latest_text = database_service.get_latest_from_database("vision_data")
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_ERROR
    
    return latest_text, HTTP_OK

if __name__ == '__main__':
    # app.run(port=5000, debug=not IS_PROD)
    socketio.run(app, port=5000, debug=not IS_PROD)
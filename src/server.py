from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
from services.ocrservice import OCRService
from services.databaseservice import DatabaseService
from dotenv import load_dotenv
from bson import Binary


load_dotenv()

app = Flask(__name__)
CORS(app)

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_ERROR = 500

ocr_service = OCRService()
database_service = DatabaseService()

@app.route('/')
def home():
    return "Welcome to the OCR Server!"

@app.route("/ocr", methods=["POST"])
def image_ocr():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

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
        text = database_service.add_to_database("vision_data", text, Binary(file.read()))
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_ERROR
    
    return "Image and text added to database", HTTP_OK
    


if __name__ == '__main__':
    app.run(debug=True)
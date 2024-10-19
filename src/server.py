from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
from services.ocrservice import OCRService

app = Flask(__name__)
CORS(app)

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_ERROR = 500

ocr_service = OCRService()

@app.route('/')
def home():
    return "Welcome to the OCR Server!"

@app.route("/ocr", methods=["POST"])
def image_ocr():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    try:
        text = ocr_service.extract_text_from_filestorage(file)
        return jsonify({"text": text}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_ERROR

if __name__ == '__main__':
    app.run(debug=True)
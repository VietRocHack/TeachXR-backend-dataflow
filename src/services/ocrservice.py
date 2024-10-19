# import easyocr
from google.cloud import vision
import io
from werkzeug.datastructures import FileStorage

class OCRService:
    def __init__(self):
        # print(os.getcwd())
        # if os.path.exists('./keys/calhacks-2024-vietrochack.json'):
        #     print("exists")
        # else:
        #     print("path not exists")
        self.client = vision.ImageAnnotatorClient()
        # self.reader = easyocr.Reader(['en'])

    def extract_text(self, image_path):
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description
        # results = self.reader.readtext(image_path)
        # # print(results)
        # return " ".join([result[1] for result in results])

    def extract_text_from_filestorage(self, file_storage: FileStorage):
        content = file_storage.read()
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description
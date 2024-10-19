from services.ocrservice import OCRService
from dotenv import load_dotenv

load_dotenv()

ocrservice = OCRService()

result = ocrservice.extract_text("./assets/images/blurred-image-test.png")
print(result)
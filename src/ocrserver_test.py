from services.ocrservice import OCRService
from dotenv import load_dotenv

load_dotenv()

ocrservice = OCRService()

result = ocrservice.extract_text("./assets/images/hbrbook1-test.jpg")
print(result)
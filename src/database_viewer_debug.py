from services.databaseservice import DatabaseService
from dotenv import load_dotenv
from bson import Binary

load_dotenv()

databaseservice = DatabaseService()

latest_row = databaseservice.get_latest_from_database("vision_data")
print(latest_row['text'])
# get the image field from latest row and save it to ./output/images/latest_image.jpg, creating the file if necessary
with open('./output/images/latest_image.png', 'wb') as f:
    f.write(latest_row['image'])
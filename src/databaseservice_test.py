from services.databaseservice import DatabaseService
from dotenv import load_dotenv
from bson import Binary

load_dotenv()

# Open the file in binary mode
with open('./assets/images/hbrbook1-test.jpg', 'rb') as f:
    binary_data = Binary(f.read())

databaseservice = DatabaseService()

if databaseservice.database_count("test_collection") == 0:
    databaseservice.add_index("test_collection", "timestamp", True)

databaseservice.add_to_database("test_collection", "test_string", binary_data)

print("All rows in database:")
all_rows = databaseservice.get_from_database("test_collection", ["timestamp", "_id"], 10)
for row in all_rows:
    print(row)

print("Latest row in database:")
latest_row = databaseservice.get_latest_from_database("test_collection", ["timestamp", "_id"])
print(latest_row)
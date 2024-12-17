import os

BASE_URL = "https://restful-booker.herokuapp.com/"
USER = os.environ.get("API_USERNAME", "admin")
PASSWORD = os.environ.get("API_PASSWORD", "password123")
TESTDATA_FILE = "resources/testdata.json"

import dotenv
import os

dotenv.load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

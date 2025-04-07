import os

from dotenv import load_dotenv

load_dotenv()
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
SOLAR_API_KEY = os.getenv("SOLAR_API_KEY")

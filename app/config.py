import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firebase configuration
FIREBASE_URL = os.getenv("FIREBASE_URL")
if not FIREBASE_URL:
    raise ValueError("FIREBASE_URL environment variable is not set. This is required for Firebase operations.")

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
if not FIREBASE_API_KEY:
    raise ValueError("FIREBASE_API_KEY environment variable is not set. This is required for Firebase operations.")

# JWT settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set. This is required for secure token generation.")

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60 * 24  # 24 hours
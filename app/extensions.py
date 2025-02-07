import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

load_dotenv()


bcrypt = Bcrypt()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise ValueError("No encryption key set for the application")

CIPHER = Fernet(ENCRYPTION_KEY.encode())

HMAC_SECRET_KEY = os.getenv("HMAC_SECRET_KEY")
HMAC_KEY = bytes.fromhex(HMAC_SECRET_KEY)

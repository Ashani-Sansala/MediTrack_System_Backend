# firebase_config.py
import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use environment variables for database connection
CERT = os.getenv('CERT')
BUCKET = os.getenv('BUCKET')

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(CERT)
        firebase_admin.initialize_app(cred, {
            'storageBucket': BUCKET
        })

def get_storage_bucket():
    initialize_firebase()  # Ensure Firebase is initialized
    return storage.bucket()

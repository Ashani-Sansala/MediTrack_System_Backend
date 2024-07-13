import firebase_admin
from firebase_admin import credentials, storage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use environment variables for Firebase credentials and storage bucket name
CERT = os.getenv('CERT')  # Path to the Firebase service account key file
BUCKET = os.getenv('BUCKET')  # Name of the Firebase Storage bucket

def initialize_firebase():

    # Initialize Firebase Admin SDK if not already initialized.
    if not firebase_admin._apps:
        cred = credentials.Certificate(CERT)  # Load Firebase credentials from the provided path
        firebase_admin.initialize_app(cred, {
            'storageBucket': BUCKET  # Specify the Firebase Storage bucket to use
        })

def get_storage_bucket():

    # Retrieve the Firebase Storage bucket object.
    initialize_firebase()  # Ensure Firebase Admin SDK is initialized
    return storage.bucket()  # Return the Firebase Storage bucket

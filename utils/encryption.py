import base64
import bcrypt
import os
from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import unpad
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variable for the secret key
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY or len(SECRET_KEY) not in [16, 24, 32]:
    raise ValueError("SECRET_KEY must be set and be either 16, 24, or 32 bytes long")

def verify_password(stored_password: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

def decrypt(cipher_text, iv_hex):
    # Convert the IV from hexadecimal to bytes
    iv = bytes.fromhex(iv_hex)

    # Decode the base64 encoded ciphertext
    cipher_text_bytes = base64.b64decode(cipher_text)

    # Create the AES cipher object with the given key and IV
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    decrypted_bytes = cipher.decrypt(cipher_text_bytes)

    # Unpad the decrypted bytes to get the original plaintext
    decrypted_text = unpad(decrypted_bytes, AES.block_size)

    # Decode the bytes to a string
    return decrypted_text.decode('utf-8')

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()
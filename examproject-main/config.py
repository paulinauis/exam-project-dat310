import os
import secrets

def generate_secret_key():
    return secrets.token_urlsafe(32)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or generate_secret_key()
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or '/examproject/data/database.db'


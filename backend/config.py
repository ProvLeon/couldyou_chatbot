import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = ENV == 'development'
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/couldyou'
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

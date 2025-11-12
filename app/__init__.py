"""
Alliance Management System - Flask Application
Initialize Flask app with environment variables
"""
from flask import Flask  
from dotenv import load_dotenv 
import os  

# Load environment variables from .env file
load_dotenv() 

# Environment variables
APP_NAME = os.getenv("APP_NAME", "Alliance Management System") 
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")  
DEBUG = os.getenv("DEBUG", "False").lower() == "true"  
HOST = os.getenv("HOST", "0.0.0.0") 
PORT = int(os.getenv("PORT", 5000))  
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")  

# Create Flask app
app = Flask(__name__)  

# Configure Flask app
app.config['SECRET_KEY'] = SECRET_KEY  
app.config['DEBUG'] = DEBUG  

from app import routes 

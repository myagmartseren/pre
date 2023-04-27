import os

# Flask app configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:password@localhost/pre'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Example app-specific configuration variables
    EXAMPLE_CONFIG_VAR = os.environ.get('EXAMPLE_CONFIG_VAR') or 'example_value'
import os

class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///banking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    INTEREST_RATE = 0.05  # 5% annual interest rate

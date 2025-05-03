import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://rihab:123@user-db:5432/userServiceDb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   

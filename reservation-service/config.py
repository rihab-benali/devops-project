import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://rihab:123@db:5432/reservationServiceDb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
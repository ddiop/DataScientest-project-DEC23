""" Data warehouse """

import os
from database.models import Weather, DailyWeather, AirPollution, City, AustralianMeteorologyWeather

from sqlalchemy import (create_engine, ForeignKey, Column, Integer, String,
                        Float, Date, Time, DateTime, func)
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
from dotenv import load_dotenv
import os
from pymongo import MongoClient
# Load environment variables from .env
load_dotenv()

class PostgresManager:
    """ Postgres Manager class """
    def __init__(self):
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.host = os.getenv('PG_HOST', 'localhost')
        self.port = os.getenv('PG_PORT', '54995')
        self.dbname = os.getenv('DB_NAME')

        self.engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        )
        self.session = sessionmaker(bind=self.engine)()

        # Tester la connexion
        try:
            with self.engine.connect() as connection:
                print("Connexion réussie")
                result = connection.execute("SELECT version();")
                for row in result:
                    print(f"PostgreSQL version: {row[0]}")
        except Exception as e:
            print(f"Erreur de connexion : {e}")

    def add_record(self, record):
        """ Add a record to a table """
        self.session.add(record)
        self.session.commit()

    def fetch_record(self, model, query):
        """ Fetch a record from a table """
        return self.session.query(model).filter_by(**query).first()

    def fetch_all_records(self, model):
        """ Fetch all records from a table """
        return self.session.query(model).all()

    def delete_record(self, record):
        """ Delete a record from the database """
        self.session.delete(record)
        self.session.commit()

    def fetch_city_record_by_coord(self, lat, lon):
        """ Fetch the nearest record from table City based on latitude and longitude """
        return (self.session.query(City)
                .order_by(func.abs(City.latitude - lat), func.abs(City.longitude - lon))
                .first())


if __name__ == "__main__":
    db = PostgresManager()

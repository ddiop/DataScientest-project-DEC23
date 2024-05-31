""" Datawarehouse """

import os

from sqlalchemy import (create_engine, ForeignKey, Column, Integer, String,
                        Float, Date, Time, DateTime, func)
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


class Weather(Base):
    """ Weather table """
    __tablename__ = 'Weather'

    id = Column(Integer, primary_key=True)
    Date = Column(DateTime)
    Temp = Column(Float)
    Rainfall = Column(Float)
    Sunrise = Column(Time)
    Sunset = Column(Time)
    WindGustDir = Column(String)
    WindGustSpeed = Column(Float)
    Cloudiness = Column(Integer)
    Humidity = Column(Integer)
    Pressure = Column(Float)
    City_id = Column(Integer, ForeignKey('City.id'))


    def __repr__(self):
        return (f"<Weather(Date={self.Date},"
                f"Temp={self.Temp},"
                f"Rainfall={self.Rainfall},"
                f"Sunrise={self.Sunrise},"
                f"Sunset={self.Sunset},"
                f"WindGustDir={self.WindGustDir},"
                f"WindGustSpeed={self.WindGustSpeed},"
                f"Cloudiness={self.Cloudiness},"
                f"Humidity={self.Humidity},"
                f"Pressure={self.Pressure},"
                f"City_id={self.City_id})>")


class DailyWeather(Base):
    """ Daily Weather table """
    __tablename__ = 'DailyWeather'

    id = Column(Integer, primary_key=True)
    Date = Column(DateTime)
    MinTemp = Column(Float)
    MaxTemp = Column(Float)
    Rainfall = Column(Float)
    WindGustDir = Column(String)
    WindGustSpeed = Column(Float)
    Cloudiness = Column(Integer)
    Humidity = Column(Integer)
    Pressure = Column(Float)
    City_id = Column(Integer, ForeignKey('City.id'))

    def __repr__(self):
        return (f"<DailyWeather(Date={self.Date},"
                f"MinTemp={self.MinTemp},"
                f"MaxTemp={self.MaxTemp},"
                f"Rainfall={self.Rainfall},"
                f"WindGustDir={self.WindGustDir},"
                f"WindGustSpeed={self.WindGustSpeed},"
                f"Cloudiness={self.Cloudiness},"
                f"Humidity={self.Humidity},"
                f"Pressure={self.Pressure},"
                f"City_id={self.City_id})>")


class AirPollution(Base):
    """ Air Pollution table"""
    __tablename__ = 'AirPollution'

    id = Column(Integer, primary_key=True)
    Date = Column(DateTime)
    AirQualityIndex = Column(Integer)
    COConcentration = Column(Float)
    NOConcentration = Column(Float)
    NO2Concentration = Column(Float)
    O3Concentration = Column(Float)
    SO2Concentration = Column(Float)
    PM25Concentration = Column(Float)
    PM10Concentration = Column(Float)
    NH3Concentration = Column(Float)
    City_id = Column(Integer, ForeignKey('City.id'))

    def __repr__(self):
        return (f"<AirPollution(Date={self.Date},"
                f"AirQualityIndex={self.AirQualityIndex},"
                f"COConcentration={self.COConcentration},"
                f"NOConcentration={self.NOConcentration},"
                f"NO2Concentration={self.NO2Concentration},"
                f"O3Concentration={self.O3Concentration},"
                f"SO2Concentration={self.SO2Concentration},"
                f"PM25Concentration={self.PM25Concentration},"
                f"PM10Concentration={self.PM10Concentration},"
                f"NH3Concentration={self.NH3Concentration},"
                f"City_id={self.City_id})>")


class AustralianMeteorologyWeather(Base):
    """ Australian Meteorology Weather table """
    __tablename__ = 'AustralianMeteorologyWeather'

    id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Location = Column(String)
    MinTemp = Column(Float)
    MaxTemp = Column(Float)
    Rainfall = Column(Float)
    Evaporation = Column(Float)
    Sunshine = Column(Float)
    WindGustDir = Column(String)
    WindGustSpeed = Column(Float)
    Temp9am = Column(Float)
    Humidity9am = Column(Float)
    Cloud9am = Column(Float)
    WindDir9am = Column(String)
    WindSpeed9am = Column(Float)
    Pressure9am = Column(Float)
    Temp3pm = Column(Float)
    Humidity3pm = Column(Float)
    Cloud3pm = Column(Float)
    WindDir3pm = Column(String)
    WindSpeed3pm = Column(Float)
    Pressure3pm = Column(Float)

    def __repr__(self):
        return (f"<AustralianMeteorologyWeather(Date={self.Date},"
                f"Location={self.Location},"
                f"MinTemp={self.MinTemp},"
                f"MaxTemp={self.MaxTemp},"
                f"Rainfall={self.Rainfall},"
                f"Evaporation={self.Evaporation},"
                f"Sunshine={self.Sunshine},"
                f"WindGustDir={self.WindGustDir},"
                f"WindGustSpeed={self.WindGustSpeed},"
                f"Temp9am={self.Temp9am},"
                f"Humidity9am={self.Humidity9am},"
                f"Cloud9am={self.Cloud9am},"
                f"WindDir9am={self.WindDir9am},"
                f"WindSpeed9am={self.WindSpeed9am},"
                f"Pressure9am={self.Pressure9am},"
                f"Temp3pm={self.Temp3pm},"
                f"Humidity3pm={self.Humidity3pm},"
                f"Cloud3pm={self.Cloud3pm},"
                f"WindDir3pm={self.WindDir3pm},"
                f"WindSpeed3pm={self.WindSpeed3pm},"
                f"Pressure3pm={self.Pressure3pm})>")


class City(Base):
    """ City table """
    __tablename__ = 'City'

    id = Column(Integer, primary_key=True)
    Name = Column(String)
    Country = Column(String)
    Latitude = Column(Float)
    Longitude = Column(Float)

    def __repr__(self):
        return (f"<City(Name={self.Name},"
                f"Country={self.Country},"
                f"Latitude={self.Latitude},"
                f"Longitude={self.Longitude})>")


class PostgreSQLManager:
    """ PostgreSQL Manager class """
    def __init__(self):
        self.user = os.getenv('PG_USER')
        self.password = os.getenv('PG_PASSWORD')
        self.host = os.getenv('PG_HOST', 'localhost')
        self.port = os.getenv('PG_PORT', '5432')
        self.dbname = os.getenv('POSTGRES_DB')

        self.engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        )
        self.session = sessionmaker(bind=self.engine)()

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
                .order_by(func.abs(City.Latitude - lat), func.abs(City.Longitude - lon))
                .first())


if __name__ == "__main__":
    db = PostgreSQLManager()

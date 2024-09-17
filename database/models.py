import os

from sqlalchemy import (create_engine, ForeignKey, Column, Integer, String,
                        Float, Date, Time, DateTime, func)
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
from dotenv import load_dotenv

load_dotenv()

class Weather(Base):
    """ Weather table """
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, unique=True)
    temp = Column(Float)
    sunrise = Column(Time)
    sunset = Column(Time)
    wind_dir = Column(String)
    wind_speed = Column(Float)
    cloud = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return (f"<Weather(Date={self.date},"
                f"Temp={self.temp},"
                f"Rainfall={self.rainfall},"
                f"Sunrise={self.sunrise},"
                f"Sunset={self.sunset},"
                f"WindGustDir={self.wind_dir},"
                f"WindGustSpeed={self.wind_speed},"
                f"Cloud={self.cloud},"
                f"Humidity={self.humidity},"
                f"Pressure={self.pressure},"
                f"City_id={self.city_id})>")


class DailyWeather(Base):
    """ Daily Weather table """
    __tablename__ = 'daily_weather'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    min_temp = Column(Float)
    max_temp = Column(Float)
    rainfall = Column(Float)
    evaporation = Column(Float)
    sunshine = Column(Float)
    wind_gust_dir = Column(String)
    wind_gust_speed = Column(Float)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return (f"<DailyWeather(Date={self.date},"
                f"MinTemp={self.min_temp},"
                f"MaxTemp={self.max_temp},"
                f"Rainfall={self.rainfall},"
                f"WindGustDir={self.wind_gust_dir},"
                f"WindGustSpeed={self.wind_gust_speed},"
                f"City_id={self.city_id})>")


class AirPollution(Base):
    """ Air Pollution table"""
    __tablename__ = 'air_pollution'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, unique=True)
    air_quality_index = Column(Integer)
    co_concentration = Column(Float)
    no_concentration = Column(Float)
    no2_concentration = Column(Float)
    o3_concentration = Column(Float)
    so2_concentration = Column(Float)
    pm25_concentration = Column(Float)
    pm10_concentration = Column(Float)
    nh3_concentration = Column(Float)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return (f"<AirPollution(Date={self.date},"
                f"AirQualityIndex={self.air_quality_index},"
                f"COConcentration={self.co_concentration},"
                f"NOConcentration={self.no_concentration},"
                f"NO2Concentration={self.no2_concentration},"
                f"O3Concentration={self.o3_concentration},"
                f"SO2Concentration={self.so2_concentration},"
                f"PM25Concentration={self.pm25_concentration},"
                f"PM10Concentration={self.pm10_concentration},"
                f"NH3Concentration={self.nh3_concentration},"
                f"City_id={self.city_id})>")


class AustralianMeteorologyWeather(Base):
    """ Australian Meteorology Weather view """
    __tablename__ = 'australian_meteorology_weather'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    min_temp = Column(Float)
    max_temp = Column(Float)
    rainfall = Column(Float)
    evaporation = Column(Float)
    sunshine = Column(Float)
    wind_gust_dir = Column(String)
    wind_gust_speed = Column(Float)
    temp_9am = Column(Float)
    humidity_9am = Column(Float)
    cloud_9am = Column(Float)
    wind_dir_9am = Column(String)
    wind_speed_9am = Column(Float)
    pressure_9am = Column(Float)
    temp_3pm = Column(Float)
    humidity_3pm = Column(Float)
    cloud_3pm = Column(Float)
    wind_dir_3pm = Column(String)
    wind_speed_3pm = Column(Float)
    pressure_3pm = Column(Float)

    def __repr__(self):
        return (f"<AustralianMeteorologyWeather(Date={self.date},"
                f"Location={self.location},"
                f"MinTemp={self.min_temp},"
                f"MaxTemp={self.max_temp},"
                f"Rainfall={self.rainfall},"
                f"Evaporation={self.evaporation},"
                f"Sunshine={self.sunshine},"
                f"WindGustDir={self.wind_gust_dir},"
                f"WindGustSpeed={self.wind_gust_speed},"
                f"Temp9am={self.temp_9am},"
                f"Humidity9am={self.humidity_9am},"
                f"Cloud9am={self.cloud_9am},"
                f"WindDir9am={self.wind_dir_9am},"
                f"WindSpeed9am={self.wind_speed_9am},"
                f"Pressure9am={self.pressure_9am},"
                f"Temp3pm={self.temp_3pm},"
                f"Humidity3pm={self.humidity_3pm},"
                f"Cloud3pm={self.cloud_3pm},"
                f"WindDir3pm={self.wind_dir_3pm},"
                f"WindSpeed3pm={self.wind_speed_3pm},"
                f"Pressure3pm={self.pressure_3pm})>")


class City(Base):
    """ City table """
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String)
    latitude = Column(Float, nullable=False, unique=True)
    longitude = Column(Float, nullable=False, unique=True)

    def __repr__(self):
        return (f"<City(Name={self.name},"
                f"Country={self.country},"
                f"Latitude={self.latitude},"
                f"Longitude={self.longitude})>")

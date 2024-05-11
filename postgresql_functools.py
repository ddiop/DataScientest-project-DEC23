import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

Base = declarative_base()


class OpenWeather(Base):
    __tablename__ = 'OpenWeather'

    id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Location = Column(String)
    MinTemp = Column(Float)
    MaxTemp = Column(Float)
    Rainfall = Column(Float)
    Sunrise = Column(Time)
    Sunset = Column(Time)
    WindGustDir = Column(String)
    WindGustSpeed = Column(Float)
    Cloudiness = Column(Integer)
    Humidity = Column(Integer)
    Pressure = Column(Float)

    def __repr__(self):
        return f"OpenWeather(id={self.id}, \
                             Date={self.Date}, \
                             Location='{self.Location}', \
                             MinTemp={self.MinTemp}, \
                             MaxTemp={self.MaxTemp}, \
                             Rainfall={self.Rainfall}, \
                             Sunrise='{self.Sunrise}', \
                             Sunset='{self.Sunset}', \
                             WindGustDir='{self.WindGustDir}', \
                             WindGustSpeed={self.WindGustSpeed}, \
                             Cloudiness={self.Cloudiness}, \
                             Humidity={self.Humidity}, \
                             Pressure={self.Pressure})"


class AirPollution(Base):
    __tablename__ = 'AirPollution'

    id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Location = Column(String)
    AirQualityIndex = Column(Integer)
    COConcentration = Column(Float)
    NOConcentration = Column(Float)
    NO2Concentration = Column(Float)
    O3Concentration = Column(Float)
    SO2Concentration = Column(Float)
    PM25Concentration = Column(Float)
    PM10Concentration = Column(Float)
    NH3Concentration = Column(Float)

    def __repr__(self):
        return f"AirPollution(id={self.id}, \
                              Date={self.Date}, \
                              AirQualityIndex='{self.AirQualityIndex}', \
                              COConcentration={self.COConcentration}, \
                              NOConcentration={self.NOConcentration}, \
                              NO2Concentration={self.NO2Concentration}, \
                              O3Concentration='{self.O3Concentration}', \
                              SO2Concentration='{self.SO2Concentration}', \
                              PM25Concentration='{self.PM25Concentration}', \
                              PM10Concentration={self.PM10Concentration}, \
                              NH3Concentration={self.NH3Concentration})"


class PostgreSQLManager:
    def __init__(self):
        self.dbname = os.getenv('POSTGRES_DB_NAME')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')

        # Connection URL
        self.database_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        self.engine = create_engine(self.database_url, echo=True)

        # Create all tables in the database
        Base.metadata.create_all(self.engine)

        # Create a configured "Session" class
        self.Session = sessionmaker(bind=self.engine)

    def add_record(self, record):
        """Generic method to add a record to the database."""
        session = self.Session()
        session.add(record)
        session.commit()
        session.close()

    def get_record(self, model, **filters):
        """Generic method to retrieve records from the database."""
        session = self.Session()
        record = session.query(model).filter_by(**filters).first()
        session.close()
        return record


if __name__ == "__main__":
    db_manager = PostgreSQLManager()

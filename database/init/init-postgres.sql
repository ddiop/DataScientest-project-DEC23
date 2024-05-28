CREATE USER openuser WITH ENCRYPTED PASSWORD 'openpassword';
GRANT ALL PRIVILEGES ON DATABASE opendb TO openuser;

\connect opendb;

CREATE TABLE "City" (
    id SERIAL PRIMARY KEY,
    "Name" VARCHAR(255) NOT NULL,
    "Country" VARCHAR(255) NOT NULL,
    "Latitude" FLOAT NOT NULL,
    "Longitude" FLOAT NOT NULL
);

CREATE TABLE "Weather" (
    id SERIAL PRIMARY KEY,
    "Date" TIMESTAMP,
    "Temp" FLOAT,
    "Rainfall" FLOAT,
    "Sunrise" TIME,
    "Sunset" TIME,
    "WindGustDir" VARCHAR(255),
    "WindGustSpeed" FLOAT,
    "Cloudiness" INTEGER,
    "Humidity" INTEGER,
    "Pressure" FLOAT,
    "City_id" INTEGER,
    FOREIGN KEY ("City_id") REFERENCES "City"(id)
);

CREATE TABLE "DailyWeather" (
    id SERIAL PRIMARY KEY,
    "Date" TIMESTAMP,
    "MinTemp" FLOAT,
    "MaxTemp" FLOAT,
    "Rainfall" FLOAT,
    "WindGustDir" VARCHAR(255),
    "WindGustSpeed" FLOAT,
    "Cloudiness" INTEGER,
    "Humidity" INTEGER,
    "Pressure" FLOAT,
    "City_id" INTEGER,
    FOREIGN KEY ("City_id") REFERENCES "City"(id)
);

CREATE TABLE "AirPollution" (
    id SERIAL PRIMARY KEY,
    "Date" TIMESTAMP,
    "AirQualityIndex" INTEGER,
    "COConcentration" FLOAT,
    "NOConcentration" FLOAT,
    "NO2Concentration" FLOAT,
    "O3Concentration" FLOAT,
    "SO2Concentration" FLOAT,
    "PM25Concentration" FLOAT,
    "PM10Concentration" FLOAT,
    "NH3Concentration" FLOAT,
    "City_id" INTEGER,
    FOREIGN KEY ("City_id") REFERENCES "City"(id)
);

CREATE TABLE "AustralianMeteorologyWeather" (
    id SERIAL PRIMARY KEY,
    "Date" DATE,
    "Location" VARCHAR(255),
    "MinTemp" FLOAT,
    "MaxTemp" FLOAT,
    "Rainfall" FLOAT,
    "Evaporation" FLOAT,
    "Sunshine" FLOAT,
    "WindGustDir" VARCHAR(255),
    "WindGustSpeed" FLOAT,
    "Temp9am" FLOAT,
    "Humidity9am" FLOAT,
    "Cloud9am" FLOAT,
    "WindDir9am" VARCHAR(255),
    "WindSpeed9am" FLOAT,
    "Pressure9am" FLOAT,
    "Temp3pm" FLOAT,
    "Humidity3pm" FLOAT,
    "Cloud3pm" FLOAT,
    "WindDir3pm" VARCHAR(255),
    "WindSpeed3pm" FLOAT,
    "Pressure3pm" FLOAT
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO openuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO openuser;
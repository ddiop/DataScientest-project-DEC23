CREATE USER ${PG_USER} WITH ENCRYPTED PASSWORD '${PG_PASSWORD}';
GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${PG_USER};

\connect ${POSTGRES_DB};

CREATE TABLE city (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL
);

CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    temp FLOAT,
    rainfall FLOAT,
    sunrise TIME,
    sunset TIME,
    wind_gust_dir VARCHAR(255),
    wind_gust_speed FLOAT,
    cloudiness INTEGER,
    humidity INTEGER,
    pressure FLOAT,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES city(id)
);

CREATE TABLE daily_weather (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    min_temp FLOAT,
    max_temp FLOAT,
    rainfall FLOAT,
    wind_gust_dir VARCHAR(255),
    wind_gust_speed FLOAT,
    cloudiness INTEGER,
    humidity INTEGER,
    pressure FLOAT,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES city(id)
);

CREATE TABLE air_pollution (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    air_quality_index INTEGER,
    co_concentration FLOAT,
    no_concentration FLOAT,
    no2_concentration FLOAT,
    o3_concentration FLOAT,
    so2_concentration FLOAT,
    pm25_concentration FLOAT,
    pm10_concentration FLOAT,
    nh3_concentration FLOAT,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES city(id)
);

CREATE TABLE australian_meteorology_weather (
    id SERIAL PRIMARY KEY,
    date DATE,
    location VARCHAR(255),
    min_temp FLOAT,
    max_temp FLOAT,
    rainfall FLOAT,
    evaporation FLOAT,
    sunshine FLOAT,
    wind_gust_dir VARCHAR(255),
    wind_gust_speed FLOAT,
    temp_9am FLOAT,
    humidity_9am FLOAT,
    cloud_9am FLOAT,
    wind_dir_9am VARCHAR(255),
    wind_speed_9am FLOAT,
    pressure_9am FLOAT,
    temp_3pm FLOAT,
    humidity_3pm FLOAT,
    cloud_3pm FLOAT,
    wind_dir_3pm VARCHAR(255),
    wind_speed_3pm FLOAT,
    pressure_3pm FLOAT
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${PG_USER};
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${PG_USER};
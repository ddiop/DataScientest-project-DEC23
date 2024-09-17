#!/bin/bash
set -e

# Trouver la racine du projet en remontant jusqu'à trouver le fichier .env
DIR="."
if [ ! -f "$DIR/.env" ]; then
  echo "Erreur : Le fichier .env n'a pas été trouvé dans le répertoire . ."
  exit 1
fi

echo "Fichier .env trouvé à : $DIR/.env"

# Charger les variables d'environnement depuis le fichier .env à la racine
export $(grep -v '^#' $DIR/.env | xargs)
echo "Variables d'environnement chargées :"
echo "DB_NAME=$DB_NAME"
echo "POSTGRES_USER=$POSTGRES_USER"
echo "POSTGRES_DB=$POSTGRES_DB"

# Créer la base de données en utilisant la variable DB_NAME
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE DATABASE $DB_NAME;
EOSQL

echo "Database $DB_NAME created and migrations applied successfully."


# Connexion à la base de données et exécution des commandes SQL
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" <<-EOSQL
    CREATE TABLE IF NOT EXISTS city (
        id SERIAL PRIMARY KEY,
        name      VARCHAR(255) NOT NULL,
        country   VARCHAR(255),
        latitude  FLOAT NOT NULL,
        longitude FLOAT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS weather (
        id SERIAL PRIMARY KEY,
        date TIMESTAMP NOT NULL,
        temp FLOAT,
        sunrise TIME,
        sunset TIME,
        wind_dir VARCHAR(255),
        wind_speed FLOAT,
        cloud    FLOAT,
        humidity FLOAT,
        pressure FLOAT,
        city_id INTEGER NOT NULL,
        FOREIGN KEY (city_id) REFERENCES city(id)
    );

    CREATE TABLE IF NOT EXISTS daily_weather (
        id SERIAL PRIMARY KEY,
        date TIMESTAMP NOT NULL,
        min_temp FLOAT,
        max_temp FLOAT,
        rainfall FLOAT,
        evaporation FLOAT,
        sunshine FLOAT,
        wind_gust_dir VARCHAR(255),
        wind_gust_speed FLOAT,
        city_id INTEGER NOT NULL,
        FOREIGN KEY (city_id) REFERENCES city(id)
    );

    CREATE TABLE IF NOT EXISTS air_pollution (
        id SERIAL PRIMARY KEY,
        date TIMESTAMP NOT NULL,
        air_quality_index INTEGER,
        co_concentration FLOAT,
        no_concentration FLOAT,
        no2_concentration FLOAT,
        o3_concentration FLOAT,
        so2_concentration FLOAT,
        pm25_concentration FLOAT,
        pm10_concentration FLOAT,
        nh3_concentration FLOAT,
        city_id INTEGER NOT NULL,
        FOREIGN KEY (city_id) REFERENCES city(id)
    );
EOSQL

# Vérifier si la vue existe, et la créer si ce n'est pas le cas
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" <<-EOSQL
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_views WHERE viewname = 'australian_meteorology_weather') THEN
      CREATE VIEW australian_meteorology_weather AS
        SELECT
            dw.id,
            EXTRACT(YEAR FROM dw.date) || '-' || EXTRACT(MONTH FROM dw.date) || '-' || EXTRACT(DAY FROM dw.date) AS date,
            c.name AS location,
            dw.min_temp,
            dw.max_temp,
            dw.rainfall,
            dw.evaporation,
            dw.sunshine,
            dw.wind_gust_dir,
            dw.wind_gust_speed,
            w9.temp AS temp_9am,
            w9.humidity AS humidity_9am,
            w9.cloud AS cloud_9am,
            w9.wind_dir AS wind_dir_9am,
            w9.wind_speed AS wind_speed_9am,
            w9.pressure AS pressure_9am,
            w3.temp AS temp_3pm,
            w3.humidity AS humidity_3pm,
            w3.cloud AS cloud_3pm,
            w3.wind_dir AS wind_dir_3pm,
            w3.wind_speed AS wind_speed_3pm,
            w3.pressure AS pressure_3pm
        FROM
            daily_weather dw
        JOIN
            city c ON dw.city_id = c.id
        LEFT JOIN
            weather w9 ON dw.city_id = w9.city_id
                              AND EXTRACT(HOUR FROM w9.date) = 9
                              AND EXTRACT(YEAR FROM dw.date) = EXTRACT(YEAR FROM w9.date)
                              AND EXTRACT(MONTH FROM dw.date) = EXTRACT(MONTH FROM w9.date)
                              AND EXTRACT(DAY FROM dw.date) = EXTRACT(DAY FROM w9.date)
        LEFT JOIN
            weather w3 ON dw.city_id = w3.city_id
                              AND EXTRACT(HOUR FROM w3.date) = 15
                              AND EXTRACT(YEAR FROM dw.date) = EXTRACT(YEAR FROM w3.date)
                              AND EXTRACT(MONTH FROM dw.date) = EXTRACT(MONTH FROM w3.date)
                              AND EXTRACT(DAY FROM dw.date) = EXTRACT(DAY FROM w3.date)
        ORDER BY
            location, date;
   END IF;
END \$\$;
EOSQL

echo "Tables and view created successfully."
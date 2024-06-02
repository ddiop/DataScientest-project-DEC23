import os

from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, AirPollution
from utils.csv_functools import load_from_csv
from utils.json_functools import load_from_json


def load_air_pollution():
    mongo_manager = MongoDBManager()
    [mongo_manager.insert_document('air_pollution', air_pollution)
     for air_pollution in load_from_json(os.path.join('dataJson', 'airPollutionInfo.json'))]

    postgre_manager = PostgreSQLManager()
    [postgre_manager.add_record(AirPollution(**air_pollution))
     for air_pollution in load_from_csv(os.path.join('dataCsv', 'airPollutionInfo.csv'))]

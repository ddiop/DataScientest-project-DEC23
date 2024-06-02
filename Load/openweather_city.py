import os

from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, City
from utils.csv_functools import load_from_csv
from utils.json_functools import load_from_json


def load_city():
    mongo_manager = MongoDBManager()
    [mongo_manager.insert_document('city', city)
     for city in load_from_json(os.path.join('dataJson', 'cityInfo.json'))]

    postgre_manager = PostgreSQLManager()
    [postgre_manager.add_record(City(**city))
     for city in load_from_csv(os.path.join('dataCsv', 'cityInfo.csv'))]

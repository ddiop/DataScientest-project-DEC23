from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd
from database.postgresql_functools import PostgresManager


if __name__ == '__main__':
    load_dotenv()
    postgres = PostgresManager()
    root_path = Path().resolve().parent

    df = pd.read_sql_table('australian_meteorology_weather', postgres.engine) \
        .drop(columns=['id']) \
        .to_csv(os.path.join(root_path, 'data', 'csv', 'weather_study.csv'), index=False)

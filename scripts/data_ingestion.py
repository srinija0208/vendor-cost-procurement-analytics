# script to save csv files into database with their filename as tablename

import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Anchor all paths to the project root (one level above /scripts), 
# regardless of where this script is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "inventory.db")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "ingestion_db.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine(f"sqlite:///{DB_PATH}")


def ingest_db(file_path, table_name, engine):
    first_chunk = True
    for chunk in pd.read_csv(file_path, chunksize=50000):
        chunk.to_sql(
            table_name,
            con=engine,
            if_exists="replace" if first_chunk else "append",
            index=False
        )
        first_chunk = False


def load_raw_data():
    start = time.time()
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(DATA_DIR, file)
            logging.info(f"Ingesting {file} into database...")
            ingest_db(file_path, file[:-4], engine)
            logging.info(f"{file} loaded successfully.")
    end = time.time()
    total_time = (end - start) / 60
    logging.info("******** Ingestion Complete ********")
    logging.info(f"Total Time Taken: {total_time:.2f} minutes")


if __name__ == "__main__":
    load_raw_data()
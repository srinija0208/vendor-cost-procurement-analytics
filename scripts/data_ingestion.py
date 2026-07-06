# Use this script to save csv files into database with their filename as tablename

import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine("sqlite:///inventory.db")


def ingest_db(file_path, table_name, engine):
    """
    Read CSV in chunks and ingest into SQLite database.
    """

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
    """
    Load all CSV files from the data folder into SQLite.
    """

    start = time.time()

    for file in os.listdir("data"):

        if file.endswith(".csv"):

            file_path = os.path.join("data", file)

            logging.info(f"Ingesting {file} into database...")

            ingest_db(file_path, file[:-4], engine)

            logging.info(f"{file} loaded successfully.")

    end = time.time()

    total_time = (end - start) / 60

    logging.info("******** Ingestion Complete ********")
    logging.info(f"Total Time Taken: {total_time:.2f} minutes")


if __name__ == "__main__":
    load_raw_data()
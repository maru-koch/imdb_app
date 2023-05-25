from collections.abc import Callable, Iterable, Mapping
from typing import Any
import psycopg2
import threading
from dataclasses import dataclass
from decouple import config

class ImDBScheduler(threading.Thread):
    def __init__(self, **kwargs) -> None:
        super(PostgresDbWorker, self).__init__(**kwargs)

@dataclass
class PostgresDbWorker():

    conn = psycopg2.connect(

        database=config('POSTGRES_DB'), 
        user=config('POSTGRES_USER'), 
        password=config('POSTGRES_PASSWORD'), 
        host=config("HOST"))
    
    cur = conn.cursor()
    
    def create_table(self):
        """ creates a db table if not exists """

        query = """CREATE TABLE IF NOT EXITS movies (
            id PRIMARY KEY AUTOINCREMENT,
            imdb_id VAR(20),
            title VAR(100)
        )"""
        self.execute_query(query)

    def save_data(self, imdb_id:str, movie_title:str ):
        """ commits data to the database """
        query = f""" INSERT INTO movies (imdb_id, movie_title) VALUES ({imdb_id}, {movie_title})"""
        self.execute_query(query)

    def execute_query(self, query:str):
        """ executes a given query parameter """
        return self.cur.execute(query)
    
    def close_connection(self):
        """ closes the database connection """
        self.cur.close()
        self.conn.close()
from collections.abc import Callable, Iterable, Mapping
from typing import Any
import psycopg2
import threading
from dataclasses import dataclass
from decouple import config

class PostgreDBScheduler(threading.Thread):
    """
    :insert_data: inserts data into the movies table in the database
    """
    def __init__(self, data_queue, **kwargs) -> None:
        self.queue = data_queue
        super(PostgreDBScheduler, self).__init__(**kwargs)
        self.start()
        self.pgworker = PostgresDbWorker()
        self.pgworker.create_table()
        

    def run(self):
        self.insert_data()

    def insert_data(self)->None:
        """ 
        Retrieves the queued records to be inserted into the 
        database 
        """
        while True:
            record = self.queue.get()
            print("RECORDS:", record)
            if record == None:
                break
            self.pgworker.save_data(*record)

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

        query = """CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            imdb_id VARCHAR(40) NOT NULL,
            title VARCHAR(100) NOT NULL
        )"""

        print('Table successfully created')
        self.cur.execute(query)
        self.conn.commit()

    def save_data(self, imdb_id:str, movie_title:str ):
        """ commits data to the database """

        query = f" INSERT INTO movies (imdb_id, title) VALUES (%s, %s);"
        self.cur.execute(query, (imdb_id, movie_title))
        self.conn.commit()

    def retrieve_data(self):
        """ Removes records from the database """

        query ="""SELECT * FROM public.movies ORDER BY id ASC"""
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
    
    
    def table_exists(self):
        exists = False
        try:
            self.cur.execute("select exists(select imdb_id title from movies where relname=imdb)")
            exists = self.cur.fetchone()[0]
            self.cur.close()
        except psycopg2.Error as error:
            print(error)
        return exists
    
    def close_connection(self):
        """ closes the database connection """
        self.cur.close()
        self.conn.close()


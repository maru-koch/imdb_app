from bs4 import BeautifulSoup as Bs
import psycopg2
import requests
import bs4

from dataclasses import dataclass
from typing import Optional

@dataclass
class IMDB:

    conn:psycopg2.connect
    cur:None
    url:str

    def fetch_webpage(self):
        """ get the webpage of the specified url and extract the relevant value from the html elements """
        response = requests.get(self.url)
        soup = Bs(response.text, 'html.parser')
        titles = soup.select('div.title')
        print("content", response.json())

    def extract(self):
        """"""

    def save_data(self, tableName:str, **kwargs:dict):
        """ commits data to the database """
        query = f""" INSERT INTO {tableName.upper()} ({kwargs.keys()}) VALUES ({kwargs.values()})"""
        self.execute_query(query)

    def execute_query(self, query:str):
        """ executes a given query parameter """
        return self.cur.execute(query)
    
    def close(self):
        """ closes the database """
        self.cur.close()
        self.conn.close()
    
if __name__=="__main__":

    from decouple import config

    database = config('POSTGRES_DB')
    user = config('POSTGRES_USER')
    password = config('POSTGRES_PASSWORD')
    host = config("HOST")

    conn = psycopg2.connect(database=database, user=user, password=password, host=host)
    cur = conn.cursor()

    url = "https://query.wikidata.org/"

    url = "https://w.wiki/6kYf"

    imdb = IMDB(conn, cur, url)
    imdb.fetch_webpage()
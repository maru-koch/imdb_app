from bs4 import BeautifulSoup as Bs
import psycopg2
import requests

from dataclasses import dataclass
from typing import Optional

@dataclass
class IMDB:

    conn:psycopg2.connect
    cur:psycopg2.cursor
    url:str

    def connect(self):
        """ connects to the database """
        pass

  

    def fetch_webpage(self):
        """ get the webpage of the specified url and extract the relevant value from the html elements """
        response = requests.get(self.url)
        soup = Bs(response.text, 'html.parse')
        titles = soup.select('div.title')
        print("content", response.content)

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

    database = config('POSTGRE_DB')
    user = config('POSTGRE_USER')
    password = config('POSTGRE_PASSWORD')
    host = "0.0.0.0"

    conn = psycopg2.connect(database=database, user=user, password=password, host=host)
    cur = conn.cursor()
    url = " https://query.wikidata.org/"

    imdb = IMDB(conn, cur, url)
    imdb.fetch_webpage()
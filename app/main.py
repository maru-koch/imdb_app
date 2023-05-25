from bs4 import BeautifulSoup as Bs
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
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

    def fetch_wikidata(self, query:str)->dict:

        """ gets the data from wikidata.org based on the query supplied """

        sparql = SPARQLWrapper(self.url)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

    def convert_to_pandas_df(self, results:dict) -> pd.DataFrame:

        """ converts the results obtained from wikidata to pandas dataframe """

        results_df = pd.io.json._normalize(results['results']['bindings'])
        pandas_df = results_df[['item.value', 'itemLabel.value']]
        return pandas_df
    
    def extract_fields(self, results):
        """"""
        item, itemLabel = data['head']['vars']
        print(item, itemLabel)
        print(data['results'])

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

    url = "https://query.wikidata.org/sparql"

    query= """
            SELECT DISTINCT ?item ?itemLabel WHERE {
            ?item wdt:P31 wd:Q11424.
            ?item wdt:P577 ?pubdate.
            FILTER((?pubdate >= "2013-01-01T00:00:00Z"^^xsd:dateTime) && (?pubdate <= "2023-12-31T00:00:00Z"^^xsd:dateTime))
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            """
    imdb = IMDB(conn, cur, url)
    data = imdb.fetch_wikidata(query=query)
    item, itemLabel = data['head']['vars']
    print(item, itemLabel)
    results = data['results']['bindings']
    data = results[0]
import threading
from dataclasses import dataclass
from multiprocessing import Pool, cpu_count
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from queue import Queue

@dataclass
class WikiDataWorker:

    url:str
    query:str 
    queue:Queue
        
    def get_data(self):
        """ 
        fetches the raw data from wikidata.org, extracts the 
        values of the items and itemLabels and put those in the queue 
        """

        results = self.fetch_wikidata(self.url, self.query)
        data = results['results']['bindings']

        for record in self.extract_fields(data):
            self.queue.put(record)

        self.queue.put(None)

    def fetch_wikidata(self, url:str, query:str)->dict:
        sparql = SPARQLWrapper(url)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

    
    def extract_fields(self, rows:list) -> tuple([str, str]):
        """ Extracts the imdb_id and movie title from each row in the table list """
        
        for row in rows:
            imdb_id = row['item']['value'].split("/")[-1]
            title = row['itemLabel']['value']
            if imdb_id != title:
                yield (imdb_id, title)


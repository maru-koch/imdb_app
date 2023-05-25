from bs4 import BeautifulSoup as Bs

import pandas as pd
import psycopg2
import requests
import bs4
from dataclasses import dataclass
from typing import Optional

@dataclass
class IMDB:

  
    
if __name__=="__main__":

    from decouple import config
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
    
    
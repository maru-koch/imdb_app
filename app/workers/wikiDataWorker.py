import threading
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

class WikiDataWorker(threading.Thread):
    
    def __init(self, url, query_string, **kwargs):
        super(WikiDataWorker, self).__init__(**kwargs)
        self.start()
        self._url = url
        self._query = query_string

    def run(self):
        self.fetch_wikidata(self._query)

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
        item, itemLabel = results['head']['vars']
        print(item, itemLabel)
        print(results['results']['binding'])
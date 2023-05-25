from queue import Queue
from workers.wikiDataWorker import WikiDataWorker
from workers.postgreDbWorker import PostgreDBScheduler

def main(url, query):

    data_queue = Queue()
    num_of_workers = 4

    wikiWorker = WikiDataWorker(url, query, data_queue)
    wikiWorker.get_data()
   
    for _ in range(num_of_workers):
        postgre_scheduler = PostgreDBScheduler(data_queue)
        postgre_scheduler.join()
        
if __name__=="__main__":

    url = "https://query.wikidata.org/sparql"

    query= """
            SELECT DISTINCT ?item ?itemLabel WHERE {
            ?item wdt:P31 wd:Q11424.
            ?item wdt:P577 ?pubdate.
            FILTER((?pubdate >= "2013-01-01T00:00:00Z"^^xsd:dateTime) && (?pubdate <= "2023-12-31T00:00:00Z"^^xsd:dateTime))
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            """
    main(url, query)
    
    
   

 
    
    
import LabEntryScraper
#import os, threading, Queue
import os

# Opens multiple threads to scrape data from each html page
def run():
#    q = Queue.Queue()

#    maxThreads = 150
#    for i in range(maxThreads):
#        t = threading.Thread(target=LabEntryScraper.scrape, args=(q,))
#        t.daemon = True
#        t.start()

    for index, i in enumerate(os.listdir("Data_From_Labs_HTML")):
        #q.put(i.split(".")[0])
        LabEntryScraper.scrape(i.split(".")[0])

#    q.join()


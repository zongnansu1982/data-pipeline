import LabEntryScraper
import os, threading, Queue


def run():
    q = Queue.Queue()

    maxThreads = 150
    for i in range(maxThreads):
        t = threading.Thread(target=LabEntryScraper.scrape, args=(q,))
        t.daemon = True
        t.start()

    for index, i in enumerate(os.listdir("Data From Labs HTML")):
        q.put(i.split(".")[0])

    q.join()


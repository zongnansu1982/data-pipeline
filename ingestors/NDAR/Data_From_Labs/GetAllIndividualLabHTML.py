#!/usr/bin/python3.4
import requests, bs4, time, os
from multiprocessing import Pool

totalEntries = 0
#q = Queue.Queue()

def clean(txt):
    txt = txt.replace('"', "'")
    escape = txt.find("\\")
    while not escape == -1:
        txt = txt[:escape] + txt[escape+2:]
        escape = txt.find("\\")

    return txt


def writeHTML(item):
        try:
            # Every home page starts with this text followed by the page's id number
            noIdPage = "https://ndar.nih.gov/edit_collection.html?id="
            entry = requests.get(noIdPage + item)
            directory = "Data_From_Labs_HTML"
            if not os.path.exists(directory):
                os.makedirs(directory)
            f = open(directory + "/Entry" + item + ".html", "wb")

            for line in entry:
                f.write(line)

            f.close()
            global totalEntries
            totalEntries -= 1
            print("Finished writing Entry " + str(item) + ".HTML, " + str(totalEntries) + " entries left.")

        except Exception as e:
            print(item + " failed!\n" + type(e))

def run():
    print("Writing all HTML files")
    page = open("DataFromLabs.html", "r").read()

    soup = bs4.BeautifulSoup(page, "html.parser")

    # List of homepages
    homepages = []

    # Puts the html for each entry number into a list
    pageIDs = soup.find_all('span', {"class" : "model-id"})


#    maxThreads = 150

#    for i in range(maxThreads):
#        t = threading.Thread(target=writeHTML)
#        t.daemon = True
#        t.start()

    global totalEntries
    totalEntries = len(pageIDs)


    elems = []
    for index in range(totalEntries):
        elems.append(pageIDs[index].text)
        # writeHTML(pageIDs[index].text)

    pool = Pool(processes=8)
    pool.map(writeHTML, elems)


#!/usr/bin/python3
import requests, bs4, time, LabEntryScraper, dryscrape


def clean(txt):
    txt = txt.replace('"', "'")
    escape = txt.find("\\")
    while not escape == -1:
        txt = txt[:escape] + txt[escape+2:]
        escape = txt.find("\\")

    return txt





print "Getting webpage from file..."
page = open("DataFromPapers.html", "r").read()

print "Generating soup..."
soup = bs4.BeautifulSoup(page, "html.parser")


print "Initializing scraper..."


# List of homepages
homepages = []

# Every home page starts with this text followed by the page's id number
noIdPage = "https://ndar.nih.gov/study.html?id="

# Puts the html for each entry number into a list
pageIDs = soup.find_all('span', {"class" : "model-id"})
session = dryscrape.Session()

for index in range(len(pageIDs)):
    if pageIDs[index].text == "304":
        print "Getting file: Entry", pageIDs[index].text
        entry = requests.get(noIdPage + pageIDs[index].text)
        session.visit(noIdPage + pageIDs[index].text)
        response = session.body()


        print "Writing HTML file"
        f = open("Data From Papers HTML/Entry" + pageIDs[index].text + ".html", "w")

        for line in response:
            f.write(line)

        f.close()
        print "Finished writing Entry" + pageIDs[index].text + ".HTML"
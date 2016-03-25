#!/usr/bin/python3
import requests, bs4, time, os


def clean(txt):
    txt = txt.replace('"', "'")
    escape = txt.find("\\")
    while not escape == -1:
        txt = txt[:escape] + txt[escape+2:]
        escape = txt.find("\\")

    return txt

def run():
    print("Getting all HTML files ...")
    page = open("DataFromPapers.html", "r").read()

    soup = bs4.BeautifulSoup(page, "html.parser")

    # List of homepages
    homepages = []

    # Every home page starts with this text followed by the page's id number
    noIdPage = "https://ndar.nih.gov/study.html?id="

    # Puts the html for each entry number into a list
    pageIDs = soup.find_all('span', {"class" : "model-id"})
    totalEntries = len(pageIDs)

    for index in range(len(pageIDs)):
        entry = requests.get(noIdPage + pageIDs[index].text)
        directory = "Data_From_Papers_HTML"
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(directory + "/Entry" + pageIDs[index].text + ".html", "w")

        for line in entry:
            f.write(line)

        f.close()
        totalEntries -= 1
        print("Finished writing Entry" + pageIDs[index].text + ".HTML, " +  totalEntries + " entries left")

    print("Done.")

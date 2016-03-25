import requests
from datetime import date


# This function gets the Data From Labs page from NDAR and saves its html file
def run():
    page = requests.get('https://ndar.nih.gov/data_from_labs.html')

    f = open("DataFromLabs.html", "wb")

    for line in page:
        f.write(line)

    s = "\n<!-- Updated on " + str(date.today()) + " -->"
    f.write(s.encode('utf-8'))

    f.close()
    print("DataFromLabs.html written!")

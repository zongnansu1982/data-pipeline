import requests
from datetime import date


# This function gets the Data From Labs page from NDAR and saves its html file
def run():
    page = requests.get('https://ndar.nih.gov/data_from_labs.html')

    f = open("DataFromLabs.html", "w")

    for line in page:
        f.write(line)

    f.write("\n<!-- Updated on " + str(date.today()) + " -->")

    f.close()
    print "DataFromLabs.html written!"

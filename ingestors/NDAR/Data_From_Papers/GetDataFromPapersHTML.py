import requests

def run():
    print("Getting DataFromPapers.html ...")
    page = requests.get('https://ndar.nih.gov/data_from_papers.html')

    f = open("DataFromPapers.html", "w")

    for line in page:
        f.write(line)

    f.close()
    print("Done.")

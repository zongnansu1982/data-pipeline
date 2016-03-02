import requests

page = requests.get('https://ndar.nih.gov/data_from_papers.html')

f = open("DataFromPapers.html", "w")

for line in page:
    f.write(line)

f.write("\n<!-- Updated on " + str(date.today()) + " -->")

f.close()
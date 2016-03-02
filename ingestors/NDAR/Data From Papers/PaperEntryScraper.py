import requests, bs4, time, pprint, json, string
import SeleniumTypesScraper, Queue, threading, os

totalEntries = 0

def cleanDict(d):
    for elm in d.keys():
        if len(d[elm]) == 0:
            del d[elm]

def scrape(queue):
    while True:
        filename = queue.get()
        try:
            #print "Getting webpage from file..."
            f = "Data From Papers HTML/" + filename + ".html"
            page = open(f, "r").read()

            #print "Generating soup..."
            soup = bs4.BeautifulSoup(page, "html.parser")
            entryDict = {}

            leftTable = soup.find('div', {'class' : 'study-summary-wrapper study-left-wrapper'})
            entryDict["Investigators"] = leftTable.find_next('tr').extract().find_next('td').find_next('td').text.encode('utf-8').strip()
            entryDict["Abstract"] = leftTable.find_next('tr').extract().find_next('td').find_next('td').text.encode('utf-8').strip()

            #TODO: Get link, but need login info
            resultList = []
            try:
                resultTD = leftTable.find_next('tr').extract().find_next('td').find_next('td')
                while True:
                    resultLink = str(resultTD.find_next('div').extract().text.strip())
                    resultList.append(resultLink)
            except:
                pass

            entryDict["Results"] = resultList
            entryDict["Documents"] = leftTable.find_next('tr').extract().find_next('td').find_next('td').text.encode('utf-8').strip()
            entryDict["DOI"] = leftTable.find_next('tr').extract().find_next('td').find_next('td').text.encode('utf-8').strip()
            entryDict["Data Use"] = leftTable.find_next('tr').extract().find_next('td').find_next('td').text.encode('utf-8').strip()

            cleanDict(entryDict)

            rightTable = soup.find('div', {'class' : 'study-summary-wrapper study-right-wrapper'})

            cohort = rightTable.find_next('tr').extract().find_next('td').find_next('td').find_next('div')
            cohorts = {}
            while cohort is not None:
                cohortDict = {}



                cohortTitle = str(cohort.find_next('label').extract().text).strip(), "(" , str(cohort.find_next('label').text).strip() , ")"

                cohortAge = str(cohort.find_next('div', {'class' : 'cohort-info'}).extract().text).split('\n')
                for index in range(len(cohortAge)):
                    cohortAge[index] = cohortAge[index].strip()
                cohortAge = string.join(cohortAge[2:-1])
                cohortDict["Age"] = cohortAge

                cohortDict["Gender"] = str(cohort.find_next('div', {'class' : 'cohort-info'}).extract().text).split(':')[1].strip()

                cohorts[string.join(cohortTitle)] = cohortDict

                cohort = cohort.find_next('div')

            cleanDict(cohorts)
            entryDict["Cohorts"] = cohorts

            measuresTable = soup.find('table', {'class' : 'standard-table measure-table'})
            measure = measuresTable.find_next('tr').find_next_sibling('tr')
            measures = []
            while measure is not None:
                m = {}
                m["Data Structure"] = str(measure.find_next('a').text.strip())
                link = str(measure.find_next('a')['href'])
                link1 = link.split(";")[0]
                link2 = link.split("?")[1]

                m["URL"] = "https://ndar.nih.gov" + link1 + "?" + link2
                m["Status"] = str(measure.find_next('td', {'class' : 'radio-table'}).text.strip())

                elements = measure.find_next('div', {'class' : 'elements'}).find_all('tr')
                elementList = []
                for e in elements:
                    dataElement = e.find_next('td').extract().text.strip()
                    order = e.find_next('td').extract().text.strip()
                    elementList.append((str(dataElement), str(order)))
                m["Elements"] = elementList
                measure = measure.find_next_sibling('tr')
                cleanDict(m)
                measures.append(m)


            entryDict["Measures"] = measures




            # Gets the id number of the entry
            typeDict = SeleniumTypesScraper.scrape(filename[5:])

            if len(typeDict) > 0:
                entryDict["Types"] = typeDict

            jFile = json.dumps(entryDict, sort_keys=True, indent=4, separators=(',',':'))
            file = open("Data From Papers JSON/" + filename + ".json", 'w')

            for line in jFile:
                file.write(line)

            file.close()
            global totalEntries
            totalEntries -= 1
            print "Finished writing" , filename, ", ", totalEntries, " files left"
            queue.task_done()
        except Exception as e:
            totalEntries -= 1
            print filename, " failed!\n", e

def run():
    q = Queue.Queue()

    maxThreads = 10
    for i in range(maxThreads):
        t = threading.Thread(target=scrape, args=(q,))
        t.daemon = True
        t.start()
    global totalEntries
    totalEntries = len(os.listdir("Data From Papers HTML"))
    for index, i in enumerate(os.listdir("Data From Papers HTML")):
        if i.split(".")[0] == "Entry289":
            q.put(i.split(".")[0])

    q.join()



run()

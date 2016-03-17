import requests, bs4, time, pprint, json, string
import SeleniumTypesScraper, Queue, threading, os

totalEntries = 0

def cleanDict(d):
    for elm in d.keys():
        if len(d[elm]) == 0:
            del d[elm]

def getNextChunk(table):
    return table.find_next('tr').extract().find_next('td').find_next('td').text.encode('utf-8').strip()

def scrape(queue):
    while True:
        filename = queue.get()
        try:
            #print "Getting webpage from file..."
            f = "Data_From_Papers_HTML/" + filename + ".html"
            page = open(f, "r").read()

            #print "Generating soup..."
            soup = bs4.BeautifulSoup(page, "html.parser")
            entryDict = {}
            entryDict["Title"] = soup.find('div', {'class':'id-wrapper'}).find_next('label').text
            leftTable = soup.find('div', {'class' : 'study-summary-wrapper study-left-wrapper'})
            entryDict["Investigators"] = getNextChunk(leftTable)
            entryDict["Abstract"] = getNextChunk(leftTable)

            #TODO: Get link, but need login info
            resultList = []
            try:
                resultTD = leftTable.find_next('tr').extract().find_next('td').find_next('td')
                while True:
                    titleDict = {}
                    urlDict = {}
                    resultDict = {}
                    resultDict["URL"] = str(resultTD.find_next('div').find_next('a')['href'])
                    resultDict["Title"] = str(resultTD.find_next('div').extract().text.strip())



                    resultList.append(resultDict)

            except:
                pass

            entryDict["Results"] = resultList
            entryDict["Documents"] = getNextChunk(leftTable)
            entryDict["DOI"] = getNextChunk(leftTable)
            entryDict["Data Use"] = getNextChunk(leftTable)

            cleanDict(entryDict)

            rightTable = soup.find('div', {'class' : 'study-summary-wrapper study-right-wrapper'})

            cohort = rightTable.find_next('tr').extract().find_next('td').find_next('td').find_next('div')
            cohorts = []
            while cohort is not None:
                cohortDict = {}



                cohortTitle = str(cohort.find_next('label').extract().text).strip(), "(" , str(cohort.find_next('label').text).strip() , ")"

                cohortAge = str(cohort.find_next('div', {'class' : 'cohort-info'}).extract().text).split('\n')
                for index in range(len(cohortAge)):
                    cohortAge[index] = cohortAge[index].strip()
                cohortAge = string.join(cohortAge[2:-1])
                cohortDict["Age"] = cohortAge

                cohortDict["Gender"] = str(cohort.find_next('div', {'class' : 'cohort-info'}).extract().text).split(':')[1].strip()
                cohortDict["Type"] = string.join(cohortTitle)
                cohorts.append(cohortDict)

                cohort = cohort.find_next('div')


            entryDict["Cohorts"] = cohorts

            measuresTable = soup.find('table', {'class' : 'standard-table measure-table'})
            measures = measuresTable.find_next('tr').find_next_siblings('tr')
            measuresList = []
            for measure in measures:
                m = {}
                m["Data Structure"] = str(measure.find_next('a').text.strip())
                link = str(measure.find_next('a')['href'])
                link1 = link.split(";")[0]
                link2 = link.split("?")[1]
                m["URL"] = "https://ndar.nih.gov" + link1 + "?" + link2
                m["Status"] = str(measure.find_next('td', {'class' : 'radio-table'}).text.strip())

                # elements div
                elements = measure.find_next('a').find_next_sibling('div')
                if elements is not None:

                    elementList = []

                    for elem in elements.find_all('tr'):

                        dataElement = elem.find_next('td').extract().text.strip()
                        #print dataElement
                        order = elem.find_next('td').extract().text.strip()
                        #print order
                        elementList.append((str(dataElement), str(order)))
                    m["Elements"] = elementList
                cleanDict(m)
                measuresList.append(m)

            entryDict["Measures"] = measuresList

            # Gets the id number of the entry
            try:
                typeDict = SeleniumTypesScraper.scrape(filename[5:])
            except AttributeError:
                pass


            if len(typeDict) > 0:
                entryDict["Types"] = typeDict

            entryDict['ResourceURL'] = "https://ndar.nih.gov/study.html?id=" + filter(str.isdigit, filename)
            entryDict['identifier'] = filter(str.isdigit, filename)
            entryDict['identifierScheme'] = "An identifier for these studies is the number given to it on the NDAR" \
                                            + " website.  For example, the entry with identifier '1' would represent" \
                                            + " the data found at 'https://ndar.nih.gov/study.html?id=1'"

            jFile = json.dumps(entryDict, sort_keys=True, indent=4, separators=(',',':'))
            directory = "Data_From_Papers_JSON"
            if not os.path.exists(directory):
                os.makedirs(directory)
            file = open(directory + "/" + filename + ".json", 'w')

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
    print "Getting all JSON files ..."
    q = Queue.Queue()

    maxThreads = 10
    for i in range(maxThreads):
        t = threading.Thread(target=scrape, args=(q,))
        t.daemon = True
        t.start()
    global totalEntries
    directory = "Data_From_Papers_HTML"
    totalEntries = len(os.listdir(directory))
    for index, i in enumerate(os.listdir(directory)):
        q.put(i.split(".")[0])

    q.join()

    print "Done."

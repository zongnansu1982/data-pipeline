#!/usr/bin/python3
import TableSearches
import bs4
import json
import os

# Gets the next section of information based on this page's structure
# i.e. Collection Title, Investigators, etc.
def getNext(start):
    return start.find_next_sibling('tr').extract().find_next('td').find_next('td').text.strip().encode('utf-8')

# Gets all of the info from a table inside a span, like the Funding Sources table
# or the grant information table



def scrape(queue):
    while True:
        filename = queue.get()
        try:
            #print "Getting webpage from file..."
            f = "Data From Labs HTML/" + filename + ".html"
            page = open(f, "r").read()

            #print "Generating soup..."
            soup = bs4.BeautifulSoup(page, "html.parser")



            #print "Initializing scraper..."
            tab1 = soup.find('div', {'id' : 'tab-1'})
            table = tab1.find('table', {'class' : 'summaryTable'})

            # Get <tr> that holds the title
            start = table.find('td', {'class' : 'labelColumn'}).parent


            title = start.find_next('td').find_next('td').text.strip().encode('utf-8')
            investigators = getNext(start)
            description = getNext(start)
            dataSource = getNext(start)
            collectionPhase = getNext(start)
            collectionState = getNext(start)



            fundingSourcesTable = table.find_next_sibling('span').extract()
            if fundingSourcesTable.find_next('tr', {'class' : 'tableHeader'}) is not None:
                fundingSourcesTable.find_next('tr', {'class' : 'tableHeader'}).find_next('th').find_next('th').find_next('th').extract()


            suppDocsTable = table.find_next_sibling('span').extract()


            grantTable = table.find_next_sibling('span').extract()


            clinicalTrialsTable = table.find_next_sibling('span').extract()


            experimentsTable = soup.find('tbody', {'id' : 'experiment-table_data'})


            tab3 = soup.find('div', {'id' : 'tab-3'})
            sharedDataTable = tab3.find_next('table')


            publicationTable = soup.find('thead', {'id' : 'publication-table_head'})


            relevantPubTable = soup.find('thead', {'id' : 'relevant-publication-table_head'})



            # Slightly different than other tables because it uses values instead of text
            dataExpectedTable = soup.find('tbody', {'id' : 'data-expected-table_data'})
            info = []
            if not dataExpectedTable is None:

                row = dataExpectedTable.find_next('tr')

                # Returns if the table does not have any info
                if not row is None:
                     # Gets each column of data
                    while not row is None:
                        col = row.find_next('td').extract()
                        rowInfo = []
                        rowInfo.append(str(col.text.strip()))
                        col = row.find_next('td')
                        if col is None:
                            break

                        for i in range(5):
                            if not col.find_next('input') is None:
                                try:
                                    rowInfo.append(str(col.find_next('input')['value']))
                                except:
                                    print "Caught missing value in Data Expected for ", filename
                                    rowInfo.append("0")
                                col = col.find_next_sibling('td')

                        rowDict = {}

                        if col is not None:
                            rowInfo.append(str(col.text))
                            rowDict["Data Expected"] = rowInfo[0]
                            rowDict["Targeted Enrollment"] = rowInfo[1]
                            rowDict["Initial Submission"] = rowInfo[2]
                            rowDict["Subjects Submitted"] = rowInfo[3]
                            rowDict["Initial Share"] = rowInfo[4]
                            rowDict["Subjects Shared"] = rowInfo[5]
                            rowDict["Status"] = rowInfo[6]
                        else:
                            print "Col was None for " , filename ," with rowInfo " , rowInfo
                            rowDict["No records found."] = ""



                        info.append(rowDict)
                        row = row.find_next_sibling('tr')




            studiesTable = soup.find('div', {'id' : 'tab-7'}).find_next('table')

            pageDict = {}
            pageDict["Title"] = str(title)
            pageDict["Investigators"] = str(investigators)
            pageDict["Description"] = str(description)
            pageDict["Data Source"] = str(dataSource)
            pageDict["Collection Phase"] = str(collectionPhase)
            pageDict["Collection State"] = str(collectionState)

            FS = TableSearches.getBWTableInfo(fundingSourcesTable)

            SD = TableSearches.getTableInfo(suppDocsTable)

            GT = TableSearches.getGTTableInfo(grantTable)

            CT = TableSearches.getBWTableInfo(clinicalTrialsTable)

            ET = TableSearches.getETTableInfo(experimentsTable)

            SHD = TableSearches.getSHDTableInfo(sharedDataTable)

            PT = TableSearches.getRPTableInfo(publicationTable)

            RP = TableSearches.getRPTableInfo(relevantPubTable)

            ST = TableSearches.getBWTableInfo(studiesTable)

            if len(FS) > 0:
                pageDict["Funding Sources"] = FS
            if len(SD) > 0:
                pageDict["Supporting Documentation"] = SD
            if len(GT) > 0:
                pageDict["Grant Information"] = GT
            if len(CT) > 0:
                pageDict["Clinical Trials"] = CT
            if len(ET) > 0:
                pageDict["Experiments"] = ET
            if len(SHD) > 0:
                pageDict["Shared Data"] = SHD
            if len(PT) > 0:
                pageDict["Publications"] = PT
            if len(RP) > 0:
                pageDict["Relevant Publications"] = RP
            if len(info) > 0:
                pageDict["Data Expected"] = info
            if len(ST) > 0:
                pageDict["Associated Studies"] = ST

            pageDict['ResourceURL'] = "https://ndar.nih.gov/edit_collection.html?id=" + filename[-1:]

            final = {}
            final['Entry'] = pageDict
            jFile = json.dumps(final, sort_keys=True, indent=4, separators=(',', ':'))

            directory = "Data From Labs JSON"
            if not os.path.exists(directory):
                os.makedirs(directory)

            file = open(directory + "/" + filename + ".json", 'w')
            for line in jFile:
                file.write(line)

            file.close()
            print "Finished writing", filename
            queue.task_done()
        except Exception as e:
            print filename, " failed!\n", type(e)

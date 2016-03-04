def getBWTableInfo(table):
    info = []
    if table is None:
        return info

    headers = []
    h = table.find('tr', {'class' : "tableHeader"})
    if h is None:

        return info
    h = h.find_next('th')
    while h is not None:
        headers.append(str(h.text))
        h = h.find_next('th')


    row = table.find_next('tr')

    # Returns if the table does not have any info
    if row == None:
        return info
    else:
        row = row.find_next('tr')


    # Gets each column of data
    while not row == None:
        col = row.find_next('td')
        rowInfo = {}
        count = 0
        while not col == None:
            try:
                rowInfo[headers[count]] = str(col.text.encode('utf-8').strip())
            except:
               pass

            col = col.find_next_sibling('td')
            count += 1

        info.append(rowInfo)
        row = row.find_next_sibling('tr')

    return info

def getSHDTableInfo(table):
    info = []
    if table is None:
        return info

    headers = ["Title", "Type", "Number of Subjects"]



    row = table.find_next('tr')

    # Returns if the table does not have any info
    if row == None:
        return info
    else:
        row = row.find_next('tr')


    # Gets each column of data
    while not row == None:
        col = row.find_next('td')
        rowInfo = {}
        count = 0
        while not col == None:
            try:
                rowInfo[headers[count]] = str(col.text.encode('utf-8').strip())
            except:
               pass


            col = col.find_next_sibling('td')
            count += 1

        info.append(rowInfo)
        row = row.find_next_sibling('tr')

    return info


def getETTableInfo(table):
    info = []
    if table is None:
        return info

    headers = ["ID", "Name", "Created Date", "Status", "Type"]



    row = table.find_next('tr')

    # Returns if the table does not have any info
    if row == None:
        return info


    # Gets each column of data
    while not row == None:
        col = row.find_next('td')
        rowInfo = {}
        count = 0
        while not col == None:
            try:
                rowInfo[headers[count]] = str(col.text.encode('utf-8').strip())
            except:
               pass

            if count == 0:
                    rowInfo["URL"] = "https://ndar.nih.gov" + str(col.find_next('a')['href'])
            col = col.find_next_sibling('td')
            count += 1

        info.append(rowInfo)
        row = row.find_next_sibling('tr')

    return info

def getGTTableInfo(table):
    info = []
    if table is None:
        return info

    headers = ["Project Number", "Project Title", "Start Date", "End Date", "Organization"]



    row = table.find_next('tr')

    # Returns if the table does not have any info
    if row == None:
        return info
    else:
        row = row.find_next('tr')


    # Gets each column of data
    while not row == None:
        col = row.find_next('td')
        rowInfo = {}
        count = 0
        rowInfo["URL"] = str(col.find_next('a')['href'])
        while not col == None:
            try:
                rowInfo[headers[count]] = str(col.text.encode('utf-8').strip())
            except:
               pass


            col = col.find_next_sibling('td')
            count += 1

        info.append(rowInfo)
        row = row.find_next_sibling('tr')

    return info


def getRPTableInfo(table):
    info = []
    if table is None:
        return info

    headers = ["PubMed ID", "Study", "Title", "Journal", "Authors", "Date"]



    row = table.find_next('tr')

    # Returns if the table does not have any info
    if row == None:
        return info
    else:
        row = row.find_next('tr')


    # Gets each column of data
    while not row == None:
        col = row.find_next('td')
        rowInfo = {}
        count = 0
        while not col == None:
            try:
                rowInfo[headers[count]] = str(col.text.encode('utf-8').strip())
            except:
               pass

            if count == 2:
                    rowInfo["URL"] = str(col.find_next('a')['href'])

            col = col.find_next_sibling('td')
            count += 1

        info.append(rowInfo)
        row = row.find_next_sibling('tr')

    return info

# Gets all of the info from a table inside a span, like the Funding Sources table
# or the grant information table
def getTableInfo(table):
    info = []
    if table is None:
        return info

    row = table.find_next('tr')

    # Returns if the table does not have any info
    if row == None:
        return info
    else:
        row = row.find_next('tr')


    # Gets each column of data
    while not row == None:
        col = row.find_next('td')
        rowInfo = []
        count = 0
        while not col == None:
            rowInfo.append(str(col.text.encode('utf-8').strip()))
            col = col.find_next_sibling('td')
            count += 1

        info.append(rowInfo)
        row = row.find_next_sibling('tr')

    return info
from selenium import webdriver





# gets all checked values from a category and adds them to a dictionary
def getChecked(td):

    checkboxDivs = td.find_elements_by_xpath(".//input[contains(@type, 'checkbox')]/../..")
    checkDict = {}
    for index, element in enumerate(checkboxDivs):
        if element.find_element_by_xpath(".//input").get_attribute("checked") == "true":
            title = str(element.find_element_by_xpath(".//span[contains(@class, 'tree-row-label')]")
                        .get_attribute("innerHTML"))
            parentID = str(element.find_element_by_xpath(".//p[contains(@class, 'tree-row-parent-id invisible')]")
                           .get_attribute("innerHTML"))
            checkDict[title] = parentID
    return checkDict



# Compiles a dictionary of all expanded categories and their ids
def findExpanded(td):
    rowDiv = td.find_elements_by_xpath(".//img[contains(@src, 'images/collapse.gif')]/../..")
    tableDict = {}
    for element in rowDiv:
        #print element.get_attribute("innerHTML")
        title = element.find_element_by_xpath(".//span[contains(@class, 'tree-row-label')]").get_attribute("innerHTML")
        #print title
        categoryID = element.find_element_by_xpath(".//p").get_attribute("innerHTML")
        #print categoryID
        tableDict[categoryID] = title
    return tableDict


def scrape(idNumber):
    dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
     "(KHTML, like Gecko) Chrome/15.0.87")

    path_to_phantomjs = 'C:/Users/Ted/node_modules/phantomjs/lib/phantom/bin/phantomjs'
    driver = webdriver.PhantomJS(executable_path = path_to_phantomjs, desired_capabilities = dcap)
    studyType = None
    try:

        driver.get("https://ndar.nih.gov/study.html?id=" + idNumber)

        elem = driver.find_element_by_css_selector(".type-radio.ignore-dirty")
        if elem.find_element_by_tag_name("input").get_attribute("checked") is None:
            studyType = "Controlled Study"
            elem = driver.find_element_by_css_selector(".Controlled.type-panel")
        else:
            studyType = "Observational Study"
            elem = driver.find_element_by_css_selector(".Observational.type-panel")
    except:
        print "Couldn't find study type."
        return -1



    typeDict = {}
    tds = elem.find_elements_by_xpath(".//td")
    for element in tds:
        #checkDict[control] = genomicsID
        checkDict = getChecked(element)
        expandedDict = findExpanded(element)
        tdDict = {}

        for category in expandedDict.keys():
            # loop through id numbers, match with a parent from expandeddict
            catList = []
            for checked in checkDict.keys():
                if checkDict[checked] == category:
                    catList.append(checked)
            #print "Checkdict [check]", checkDict[checked]

            tdDict[str(expandedDict[category])] = catList
    # want arms/comparison: [ genomics: [control, study cohort]]
        typeDict[str(element.find_element_by_xpath(".//label").get_attribute("innerHTML"))] = tdDict

    for elm in typeDict.keys():
        if len(typeDict[elm]) == 0:
            del typeDict[elm]
    return typeDict




    driver.close()

scrape("289")
import requests, json, xml.etree.ElementTree as ET, threading

xmlPage = open('DataStructures.xml', 'r')

tree = ET.parse(xmlPage)
root = tree.getroot()


def writeJson(name):
        print name
        datastructure = requests.get('https://ndar.nih.gov/api/datadictionary/v2/datastructure/' + name).text

        f = open("Data Dictionary JSON/" + name + ".json", 'w')

        f.write(json.dumps(json.loads(datastructure), indent=4))
        f.close()




for index, child in enumerate(root):
    writeJson(child[0].text)
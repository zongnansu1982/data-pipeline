import requests, json, xml.etree.ElementTree as ET, threading, Queue


xmlPage = open('DataStructures.xml', 'r')

tree = ET.parse(xmlPage)
root = tree.getroot()
totalFiles = len(root)


# Recursively removes any empty elements or lists from the structure dictionary
def clean(structure):
    for key in structure.keys():
        if structure[key] is None:
            del structure[key]
        elif type(structure[key]) is list:
            if len(structure[key]) == 0:
                del structure[key]
            else:
                for elem in structure[key]:
                    if type(elem) is dict:
                        clean(elem)

def writeJson():
    while True:
        item = q.get()
        try:
            page = requests.get('https://ndar.nih.gov/api/datadictionary/v2/datastructure/' + item)
            datastructure = page.text
            loaded = json.loads(datastructure)

            # Remove blank elements
            clean(loaded)

            f = open("Data Dictionary JSON/" + item + ".json", 'w')
            f.write(json.dumps(loaded, indent=4))
            f.close()
            global totalFiles
            totalFiles -= 1
            print "Finished writing ", item, ",", totalFiles, "files remain."



            q.task_done()
        except Exception as e:
            print item, " failed!\n", type(e)
            totalFiles -= 1


q = Queue.Queue()

maxThreads = 150
for i in range(maxThreads):
    t = threading.Thread(target=writeJson)
    t.daemon = True
    t.start()

for index, child in enumerate(root):
    q.put(child[0].text)

q.join()
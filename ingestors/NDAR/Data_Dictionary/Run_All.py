import requests, json, threading, Queue, os, ast, time


# Recursively removes any empty elements or lists from the structure dictionary
def clean(structure):
    for key in structure.keys():
        # Check if element is None
        if structure[key] is None:
            del structure[key]

        # Check if element is empty list
        elif type(structure[key]) is list:
            if len(structure[key]) == 0:
                del structure[key]
            else:
                for elem in structure[key]:
                    # If element is a dict, recurse
                    if type(elem) is dict:
                        clean(elem)

# Generates JSON files
def writeJson():
    while True:
        item = q.get()
        try:
            # Loads the entry
            p = requests.get('https://ndar.nih.gov/api/datadictionary/v2/datastructure/' + item)
            datastructure = p.text
            loaded = json.loads(datastructure)

            for elem in loaded['dataElements']:
                if loaded['publishDate'] is not None:
                    elem['publishDate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(loaded['publishDate']) / 1000))



            # Remove blank elements
            clean(loaded)

            # Creates new directory if it does not exist
            directory = "Data_Dictionary_JSON"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Writes to directory
            f = open(directory + "/" + item + ".json", 'w')
            f.write(json.dumps(loaded, indent=4))
            f.close()

            # Adjusts the total number of remaining files
            global totalFiles
            totalFiles -= 1

            print "Finished writing ", item, ",", totalFiles, "files remain."

            # Adjusts the queue
            q.task_done()

        except Exception as e:
            print item, " failed!\n", type(e)
            totalFiles -= 1

# Lists all entries
page = requests.get('https://ndar.nih.gov/api/datadictionary/v2/datastructure/')

# Gets the shortName id of each entry
elements = page.text.split('"shortName":"')

shortNames = []
for elem in elements:
    shortNames.append(str(elem.split('"')[0]))
del shortNames[0]




totalFiles = len(shortNames)

q = Queue.Queue()

# Multithreading logic
maxThreads = 150
for i in range(maxThreads):
    t = threading.Thread(target=writeJson)
    t.daemon = True
    t.start()

# Adds all entries to the queue to be converted to JSON files
for index, name in enumerate(shortNames):
    if index < 5:
        q.put(name)

q.join()


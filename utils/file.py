import json

def readFile(filePath, encoding="cp936"):
    try:
        with open(filePath, mode='r', encoding=encoding) as f:
            datas = f.readlines()
            return datas
    except:
        return []

def deleteFile(filePath):
    import os
    if os.path.isfile(filePath):
        os.remove(filePath)
        return True
    return False

def readJsonStrings(filePath, encoding="cp936"):
    import json
    try:
        with open(filePath, mode='r', encoding=encoding) as f:
            datas = f.readlines()
            dataSet = []
            for item in datas:
                try:
                    dataSet.append(json.loads(item))
                except:
                    return False
            return dataSet
    except:
        return dict()

def readJsonFile(filePath, encoding="cp936"):
    try:
        with open(filePath, mode='r', encoding=encoding) as f:
            return json.load(f)
    except:
        return {}
    
def writeJsonFile(filePath, content, encoding="cp936"):
    jsonObject = json.dumps(content, indent=4)
    with open(filePath, mode='w', encoding=encoding) as f:
        f.write(jsonObject)

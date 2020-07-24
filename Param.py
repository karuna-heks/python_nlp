import json

class Param:
    
    def __init__(self, path=None):
        if path==None:
            f = open('param.json', 'r')
        else:
            f = open(path, 'r')
        self.json_param = f.read()
        f.close()
    
    def readString(self):
        return self.json_param

    def readName(self):
        return json.loads(self.json_param).get('name')

    def readLanguage(self):
        return json.loads(self.json_param).get('language')
    
    def readStemType(self):
        return json.loads(self.json_param).get('stemType')
    
    def readStopWordsType(self):
        return json.loads(self.json_param).get('stopWordsType')
    
    def readMetric(self):
        return json.loads(self.json_param).get('metric')
    
    def readDBCorpusPath(self):
        return json.loads(self.json_param).get('dbCorpusPath')
    
    def readDocCorpusPath(self):
        return json.loads(self.json_param).get('docCorpusPath')
    
    def saveDictionary(self):
        return json.loads(self.json_param).get('saveDictionary')
        
    def getTrainPercentage(self):
        return json.loads(self.json_param).get('trainPercentage')
    
    def getPathToDBForReport(self):
        return json.loads(self.json_param).get('pathToDBForReport')
        
if __name__ == '__main__':
    p = Param()
    print(p.readString())
    print(p.readName())
    print(p.readDBCorpusPath())
    print(p.saveDictionary())
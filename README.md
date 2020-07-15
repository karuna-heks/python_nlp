# python_nlp


### To get started:
**Install:**
```
$ pip install --upgrate tensorflow
$ pip install --upgrade scikit-learn
$ pip install --upgrade matplotlib
$ pip install numpy scipy
$ pip install keras
$ pip install --user -U nltk
```
**Сonfigure model parameters**
in *param.json*:
```
    "name": "testCorpus",
    "language": "eng",
    "source": "myCorpusSmall",
    "stemType": "stemming",
    "stopWordsType": "none",
    "metric": "tf",
    "dbCorpusPath": "/mnt/hgfs/vmware D/dataBase/myCorpus.db",
    "docCorpusPath": "/mnt/hgfs/vmware D/topicsSmall",
    "trainPercentage": 70,
    "saveDictionary": false
```
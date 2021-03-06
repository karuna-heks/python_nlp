# python_nlp


### Начало работы:
**Установить модули:**
```
$ pip install --upgrate tensorflow
$ pip install --upgrade scikit-learn
$ pip install --upgrade matplotlib
$ pip install numpy scipy
$ pip install keras
$ pip install --user -U nltk
$ pip install pymystem3
$ pip install corus
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('brown')
wget https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz
$ pip install navec
wget https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar
wget https://storage.yandexcloud.net/natasha-navec/packs/navec_news_v1_1B_250K_300d_100q.tar
```

**Настроить параметры модели**
в файле *param.json*:
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

### **Описание параметров:**
**"name": "testCorpus"**
Имя может быть произвольное, желательно, чтобы соответствовало конкретному корпусу данных.

**"language": "eng"**
Язык может быть: *"eng", "rus", "mul"*.
*mul* - применяется, когда есть необходимость учитывать разные слова. Например, текст корпуса -- русский, но важно учитывать различные специальные термины.
От выбора языка зависит набор парсеров, стеммеров и тд. Они для каждого свои и у каждого разная скорость работы.

**"source": "topics"**
Источник данных для корпуса. Доступны варианты: *"file", "brown"*.
*file* -- данные будут браться из папки, в которой хранятся все тексты. В исходной папке должны храниться тексты, разбитые по различным папкам, каждая папка -- отдельная категория текстов.
*brown* -- корпус данных из nltk. Содержит 500 больших текстов, на английском, разбитых на категории.

**"stemType": "lemma"**
Вид операции стемминга. Доступны варианты: *"lemma", "stemming", "none"*.
*lemma* -- приведение слова к его основе с помощью сложных алгоритмов и словаря слов. Долгий метод, но работает эффективно. Для русского языка используется стеммер mystem от яндекса, для англ языка стеммер из библиотеки NLTK.
*stemming* -- усечение окончаний слов с помощью стемминга портера для англ. языка и snowball стеммера для русского языка, высокая скорость работы.
*none* - отсуствие стемминга. слова остаются в той форме, в которой были изначально

**"stopWordsType": "default"**
Вид операции отсечения стоп-слов. На данный момент доступны только варианты: *"default"* и *"none"*
*default* -- удаление стоп-слов согласно словарю стоп-слов из библиотеки NLTK, как для английского, так и для русского текстов.
*none* -- не удалять стоп-слова

**"metric": "tfidf"**
Выбор метрики для формирования векторов. Доступны варианты: *"tf"* и *"tfidf"*
*tf* -- вектор строится на основе частоты появления слова в тексте.
*tfidf* -- вектор строится на основе величины TF-IDF. Подробнее: https://ru.wikipedia.org/wiki/TF-IDF
Также, если параметр *"maxFeatures"* не равняется *"none"*, то выбор метрики влияет на критерий, по которым будут удаляться лишние признаки из векторов данных. При выборе tfidf будут отсекаться признаки с наименьшим показателем TF-IDF по всему корпусу текстов, а при выборе tf будут отсекаться только признаки, которые имеют наименьшую частоту встречаемости во всех текстах.

**"maxFeatures": 1000**
Максимальное число признаков для нейросетевого анализа. Доступны варианты в диапазоне *1-10000* либо *"none"*.
Из всех слов формируется набор признаков из которого и будет формироваться выходной вектор для обучения. При слишком большом количестве признаков может не хватить оперативной памяти для обработки всех текстов, а, также скорость обучения будет очень низкой из-за большого количества параметров. При слишком низком количестве признаков высока вероятность потери ключевых признаков для выполнения корректной операции обучения сети.
Если выбран параметр *"none"*, то число признаков останется без изменений и будет зависеть от размера корпуса.

**"dbCorpusPath": "/mnt/myCorpus.db"**
Путь к базе данных, хранящей все результаты выполнения операции классификации.

**"docCorpusPath": "/mnt/hgfs/vmware D/topics"**
Путь к папке, содержащей тексты для анализа. (Актуально только в случае выбора параметра *"file"* при выборе источника данных (*"source"*)

**"trainPercentage": 70**
Количество (в процентах) тренировочных данных из всего размера корпуса. Диапазон от 1 до 100. значение 70 означает, что 70% данных будет в обучающей выборке, а 30% - в тестовой.

**"saveDictionary": true**
Флаг для выполнения операции сохранения словаря. Если стоит *true*, то в базе данных будет сохранён весь набор признаков. Может занимать достаточно долгое время.

**"pathToDBForReport": "/mnt/dataBase/dataBase.db"**
Путь к базе данных из которой будут браться готовые данные для тематического анализа. В этой БД уже должны быть полностью сформированные векторы к каждому тексту. Работает только в с файлами *main_nn_analysis.py* и *demo_classification.ipynp*



### Запуск классификатора:
Для полного анализа корпуса, необходимо запустить файл *main.py* или *demo_full_analysis.ipynb*
Для нейросетевого анализа корпуса на основе только входных векторов (которые должны быть заранее сформированны и находиться в базе данных), необходимо запустить файл *main_nn_analysis.py* или *demo_classification.ipynb*

**Для начала работы могут понадобиться файлы с корпусом текстов и файл базы данных**
Архивы с файлам корпусов данных можно найти тут:
[20 news groups corpus](https://drive.google.com/file/d/1RkS4Ote-M4jw5GbHaKIrL2Il0LjAmo5w/view?usp=sharing)
[myCorpus](https://drive.google.com/file/d/1iZW8ixQlmBo1ULw8P5r0zncwqaaZ3wUp/view?usp=sharing)

Пустой файл базы данных с готовыми таблицами можно найти тут:
[myDataBase.db](https://drive.google.com/open?id=1TA1QWPc4ppmW-EmjgSDwuVhByfNcueUN)
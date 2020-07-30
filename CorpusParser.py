"""
v0.19.3
CorpusParser - файл, содержащий методы и классы для парсинга 
исходных текстов:
    1. Разбивка текста на отдельные токены (слова)
    2. Удаление общеупотребительных-слов
    3. Выполнение операции стемминга/лемматизации
Обработка рассчитана на тексты, написанные кириллицей и/или латиницей

Параметры, которые используются классом CorpusParser задаются при
инициализации класса

#!!! - перенести глобальные переменные класса внутрь конструктора
#!!! - реализовать:
- список стоп-слов лучше конвертировать во множество. т.к. поиск по множеству
будет происходить быстрее поиска по списку
- метод report() с выводом полного текстового отчета
- поддержка русского, английского и рус/англ (mul, multilanguage) языков
- проверить разные способы лемматизации для англ языка. Выбрать один из них
или добавить несколько:
    - wordnet lemmatizer (сейчас)
    - spaCy
    - TextBlob
    - Pattern Lemmatizer
    - Stanford CoreNLP
    - Gensim
    (подробнее тут: 
        https://webdevblog.ru/podhody-lemmatizacii-s-primerami-v-python/)
- возможность удаления слов со слишком низкой частотой
"""
import re
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from pymystem3 import Mystem
import sys


class CorpusParser:
    
    _tempWordList = None # весь текст в виде списка слов
    _stopList = [] # список общеупотребительных слов
    _stopListEng = []
    _stopListRus = []
    
    _porter = None # NLTK porter Stemmer
    _lemma = None # NLTK lemmatizer
    _snowball = None # NLTK SnowballStemmer
    _mystem = None # mystem lemmatizer
    
    #@ params
    _language = None
    _stemType = None
    _stopWordsType = None
    
    def __init__(self, language: str = 'eng', stemType: str = 'stemming',
                 stopWordsType: str = 'default'):
        """
        В конструкторе класса выполняется определение дальнейших параметров,
        которые будут использоваться при выполнении обработки текстов
        Parameters
        ----------
        language : str, optional
            Язык корпуса данных. Может принимать значения "eng", "rus", "mul". 
             "mul" - мультиязычный (англ и рус). Каждый вариант, 
             в первую очередь, влияет на то, какие слова будут 
             игнорироваться фильтром. The default is 'eng'.
             #!!! - пока работает только англ и рус по-отдельности
        stemType : str, optional
            Тип операции приведения слова к своей основе. Доступны 2 варианта
            "lemma" - лемматизация, "stemming" - стемминг. алгоритмы 
            различаются между собой как по скорости работы, так и по 
            качеству приведения к основе. The default is 'stemming'.
        stopWordsType : str, optional
            выбор способа отсечения стоп-слов. The default is 'default'.
            #!!! - пока работает только отсечение заранее определённого списка
            слов
        Returns
        -------
        None.
        """
        if (language == 'russian' or language == 'rus'):
            self._language = 'rus'
        elif (language == 'english' or language == 'eng'):
            self._language = 'eng'
        elif (language == 'multilanguage' or language == 'mul'):
            sys.exit("Error: multilanguage is not available")
            #!!! использование одновременно двух языков пока недоступно
            self._language = 'mul' 
            
        if (stemType == 'stemmer' or stemType == 'stem' or 
            stemType == 'stemming'):
            self._stemType = 'stem'
            if self._language == 'rus':
                self._snowball = SnowballStemmer('russian')
            elif self._language == 'eng':
                self._porter = PorterStemmer()
            elif self._language == 'mul':
                self._snowball = SnowballStemmer('russian')
                self._porter = PorterStemmer()
                
        elif (stemType == 'lemmatization' or stemType == 'lemmatizing' or 
            stemType == 'lemma'):
            self._stemType = 'lemma'
            if self._language == 'rus':
                self._mystem = Mystem()
            elif self._language == 'eng':
                self._lemma = WordNetLemmatizer()
            elif self._language == 'mul':
                self._lemma = WordNetLemmatizer()
            self._mystem = Mystem()
                
        elif (stemType == 'none' or stemType == 'no' or stemType == 'not' or
              stemType == 'n'):
            self._stemType = 'none'
        else:
            self._stemType = 'none'
            
        if (stopWordsType == 'default'):
            self._stopWordsType = 'default'
            #!!! продумать логику использования параметра стопВордс
            self._initStopWords()
        

    def parsing(self, text:str):
        """
        public parsing(self, text):
        Метод получает на вход исходный необработанный текст и возвращает
        текст, прошедший все выбранные этапы фильтрации. Во многом итоговый
        результат будет зависеть от того, какие параметры были заданы в
        конструкторе класса
        Parameters
        ----------
        text : str
            исходный текст.
        Returns
        -------
        str
            итоговый текст.
        """
        # получаем текст
        # отправляем в токенайзер
        # получаем список
        # удаляем общеупотребительные слова из списка
        # отправляем список в стеммер/лемматизатор
        # возвращаем текст
        
        self._tempWordList = self._tokenizer(text)
        # <- токенайзер делит текст на токены и приводит к нижнему регистру
        
        # -> удаление стоп-слов
        if (self._stopWordsType == 'default'):
            #!!! продумать логику использования параметра стопВордс
            self._tempWordList = self._deleteStopWords(self._tempWordList)
        
        # -> выделение основы слова
        if (self._stemType != 'none'):
            tempList = []
            for w in self._tempWordList:
                tempList.append(self._stemmer(w))
            self._tempWordList = tempList
        return " ".join(self._tempWordList)
        
        
    # @private methods
    
    def _stemmer(self, word:str):
        """
        private _stemmer(self, word):
        В зависимости от выбранного метода стемминга, выполняется определённая
        операция. Метод определяется в конструкторе
        Parameters
        ----------
        word : str
            Исходное слово.
        Returns
        -------
        str. Слово после стемминга
        """
        #!!! добавить мультиязычность (пока только англ и рус по-отдельности)
        if (self._language == 'eng'):
            if (self._stemType == 'lemma'):
                word = self._lemma.lemmatize(word, self._getWordnetPos(word))
            elif (self._stemType == 'stem'):
                word = self._porter.stem(word)
                
        elif (self._language == 'rus'):
            if (self._stemType == 'lemma'):
                word = self._mystem.lemmatize(word)[0]
            elif (self._stemType == 'stem'):
                word = self._snowball.stem(word)
        
        return word

    
    def _getWordnetPos(self, word:str):
        """
        private _getWordnetPos(self, word):
        Метод определяет POS-тег для входящего слова. Это должно улучшить
        процесс лемматизации Wordnet стеммером
        Parameters
        ----------
        word : str
            Слово, для которого будет определяться POS-тег.
        Returns
        -------
        TYPE: str
            POS-тег.
        """
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)
        
        
    def _tokenizer(self, text:str):
        """
        private _tokenizer(self, text):
        метод приводит весь текст к нижнему регистру, затем выполняется 
        замена последовательности небуквенных символов (в зависимости
        от выбранного языка) на одиночные пробелы. по пробелам происходит
        разделение текста на список слов
        Parameters
        ----------
        text : str
            Исходный текст.
        Returns
        -------
        TYPE
            список слов в тексте.
        """
        text = text.lower()
        if self._language == 'eng':
            text = re.sub(r"[^a-z]+", " ", text)
        elif self._language == 'rus':
            text = re.sub(r"[^а-яё]+", " ", text)
        elif self._language == 'mul':
            text = re.sub(r"[^a-zа-яё]+", " ", text)
        else:
            sys.exit("Error: unknown language")
        # <- перевод в нижний регистр и замена небуквенных символов пробелами
        #!!! продумать, что делать с цифрами. нужны ли они, или 
        # их нужно как другой мусор удалять
        # подсказка по регулярным выражениям:
        # \b\W+\b|\b\W+$ - последовательности между словами (англ) и цифрами
        # \b[\W0-9]+\b|\b\W+$ - последовательности между словами  (англ)
        # [^a-zа-яA-ZА-ЯёЁ]+ - последовательности между словами русс и англ (любых)
        # [^a-zа-яё]+ - последовательности между словами русс и англ (нижн)
        # [^a-zа-яA-ZА-ЯёЁ0-9]+ - посл. межд. словами и цифрами любыми
        # [^a-z]+ - последовательности между словами (англ)
        return text.split(" ")

    
    def _deleteStopWords(self, wordList):
        """
        private _deleteStopWords(self, wordList):
        метод получает список со всеми словами в тексте и удаляет лишние
        слова, согласно правилам, которые задаются в конструкторе класса
        Parameters
        ----------
        wordList : TYPE
            Исходный список.
        Returns
        -------
        wordList : TYPE
            Отформатированный список.
        """
        newWordList = []
        for word in wordList:
            if word not in self._stopList:
                newWordList.append(word)
        return newWordList
               
            
    def _initStopWords(self):
        """
        private _initStopWords(self):
        Метод формирует список со стоп-словами, для дальнейшего удаления
        их из списка слов в методе _deleteStopWords
        Returns None.
        """
        stopListTrash = ['', ' ', '\n']
        self._stopList.extend(stopListTrash)
        if (self._language == 'eng' or self._language == 'mul'):
            self._stopList.extend(stopwords.words('english'))
        if (self._language == 'rus' or self._language == 'mul'):
            self._stopList.extend(stopwords.words('russian'))
                              

if __name__ == '__main__':
    cp = CorpusParser(language = 'rus', stemType = 'lemma',
                 stopWordsType = 'default')
    testText1 = """The colour designations for these iron plates are as follows: \
    It is useful to note the colour assignment \
    of these iron plates is consistent with the heavier bumper plates \
    The Christian beliefs of Catholicism are found in the Nicene Creed. 
    The Catholic Church teaches that it is the One, Holy, Catholic and 
    Apostolic church founded by Jesus Christ in his Great Commission,
    [9][10][note 1] that its bishops are the successors of Christ's 
    apostles, and that the pope is the successor to Saint Peter upon 
    whom primacy was conferred by Jesus Christ.[13] It maintains that 
    it practises the original Christian faith, reserving infallibility, 
    passed down by sacred tradition.[14] The Latin Church, the 
    twenty-three Eastern Catholic Churches, and institutes such 
    as mendicant orders, enclosed monastic orders and third orders 
    reflect a variety of theological and spiritual emphases in 
    the church.[15][16] In the UK, BMX was a craze which took 
    off in the early 1980s, specifically 1982/3, when it became 
    the "must have" bicycle for children and teenagers. Previously 
    a small niche area, BMX exploded at this time into the dominant 
    bicycle for the younger rider, with older teenagers and even adults"""
    testText2 = """
    Медве́жьи[1] (лат. Ursidae) — семейство млекопитающих отряда хищных. 
    Отличаются от других представителей псообразных более коренастым 
    телосложением. Медведи всеядны, хорошо лазают и плавают, быстро 
    бегают, могут стоять и проходить короткие расстояния на задних 
    лапах. Имеют короткий хвост, длинную и густую шерсть, а также 
    отличное обоняние. Охотятся вечером или на рассвете.

    Обычно остерегаются человека, но могут быть опасными в тех местах, 
    где они привыкли к людям, особенно белый медведь и медведь гризли. 
    Мало восприимчивы к пчелиным укусам из-за своей густой шерсти, 
    чувствительны для медведей укусы пчёл в нос[2]. В природе естественных 
    врагов почти не имеют (на юге Дальнего Востока России и в Маньчжурии на 
    них могут нападать взрослые тигры).
    """
    text = testText2
    text = cp.parsing(text)
    print(text)
    
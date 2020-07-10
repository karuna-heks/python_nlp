import nltk
import os
from pymystem3 import Mystem
import re
import sys
from nltk.stem import PorterStemmer
import json


import numpy as np
from numpy import linalg as la

a = [1, 3, 23, 42, 23, 32, 1, 2, 23, 23, 342]
print(a)
b = np.array(a)
print(b)
c = la.norm(b)
print(c)
d = b/c
print(d)

a
npArray = np.array(a)
npArray = npArray/la.norm(npArray)

f = list(npArray)
print(f)


d_json = json.dumps(npArray)
print(d_json)

npArray2 = json.loads(d_json)
print(npArray2)




#text = "Backgammon is one, of the oldest known board games. Its history can be traced back nearly 5,000 years to archeological discoveries in the Middle East. It is a two player game where each player has fifteen checkers which move between twenty-four points according to the roll of two dice."

# print("test String 1")
# print("test String 3")
# # sys.exit("fafs")
# print("test String 2")

# text2 = "Пишем тут какой-нибудь текст. Посмотрим, как НЛТК с ним справится"
# text3 = """The colour designations for these iron plates are as follows: \
#     1 kg is green, 1.5 kg is yellow, 2 kg is blue, 2.5 kg is red, \
#     5 kg and 0.5 kg are white. It is useful to note the colour assignment \
#     of these iron plates is consistent with the heavier bumper plates \
#     (i.e. 1 kg and 10 kg are green, 1.5 kg and 15 kg are yellow, etc.).\
#         Вот это поворот, конечно, в возникшей крайней ситуации... \
#         Что же теперь поделать, если 13 лет не могу справиться \
#         с последовательностями слов :4 вот это это что это субститьюшн \
#         авы у ук ну ты это что это 33 43 а: авот? ав в Ашот в Ашон!Кек."""
    
    
# # f = open(r'/mnt/hgfs/vmware D/testRussian/output_file.txt', 'r')
# # text = f.read()
# # f.close()

# text = text3
# print("1\n\n")
# print(text)

# text = text.lower()
# print("2\n\n")
# print(text)

# text = re.sub(r"[^a-zа-яA-ZА-ЯёЁ]+", " ", text)
# # \b\W+\b|\b\W+$ - последовательности между словами (англ) и цифрами
# # \b[\W0-9]+\b|\b\W+$ - последовательности между словами  (англ)
# # [^a-zа-яA-ZА-ЯёЁ]+ - последовательности между словами русс и англ (любых)
# # [^a-zа-яA-ZА-ЯёЁ0-9]+ - посл. межд. словами и цифрами любыми
# # [^a-z]+ - последовательности между словами (англ)
# print("3\n\n")
# print(text)

# textList = text.split(" ")
# print("5\n\n")
# print(textList)

# removeList = ['for' , 'is', 'kg', 'are', 'это', 'у']

# for word in removeList:
#     for i in range(textList.count(word)):
#         textList.remove(word)
# print("6\n\n")
# print(textList)

# ps = PorterStemmer()
# list2 = []
# for w in textList:
#     list2.append(ps.stem(w))
# print(list2)

#sentences = nltk.sent_tokenize(text)
# words = nltk.word_tokenize(text, language = 'russian')

# print(words)
# print()

# # os.system(r'./mystem')

# # cmd = "mystem -l"
# # subprocess.Popen(cmd, shell = True)

# mystem = Mystem()
# lemmas = mystem.lemmatize(text)
# print(''.join(lemmas))


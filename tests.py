import nltk
import os
from pymystem3 import Mystem
import re
import sys


#text = "Backgammon is one, of the oldest known board games. Its history can be traced back nearly 5,000 years to archeological discoveries in the Middle East. It is a two player game where each player has fifteen checkers which move between twenty-four points according to the roll of two dice."

print("test String 1")
print("test String 3")
sys.exit("fafs")
print("test String 2")

text2 = "Пишем тут какой-нибудь текст. Посмотрим, как НЛТК с ним справится"
f = open(r'/mnt/hgfs/vmware D/testRussian/output_file.txt', 'r')
text = f.read()
f.close()


text = text.lower()
text = re.sub(r"[^\w]", " ", text)
text = re.sub(r"\s+", " ", text)

#sentences = nltk.sent_tokenize(text)
words = nltk.word_tokenize(text, language = 'russian')

print(words)
print()

# os.system(r'./mystem')

# cmd = "mystem -l"
# subprocess.Popen(cmd, shell = True)

mystem = Mystem()
lemmas = mystem.lemmatize(text)
print(''.join(lemmas))
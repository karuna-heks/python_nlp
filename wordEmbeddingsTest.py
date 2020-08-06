from navec import Navec
from numpy import linalg as ln
import numpy as np

path = 'navec_news_v1_1B_250K_300d_100q.tar'
navec = Navec.load(path)

# print(navec['король'])

king = navec['король']
queen = navec["королева"]
man = navec['мужчина']
woman = navec['женщина']

queen_estimate = king - man + woman
print(ln.norm(navec['стол'] - navec['стул']))
print(ln.norm(navec['стул'] - navec['чехословакия']))
print(ln.norm(navec['диктатор'] - navec['булочка']))
print(ln.norm(navec['лабрадор'] - navec['овчарка']))
print(ln.norm(navec['народ'] - navec['люди']))
print(ln.norm(navec['шторы'] - navec['тюль']), end = "\n\n")

path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
navec = Navec.load(path)

# print(navec['король'])

king = navec['король']
queen = navec["королева"]
man = navec['мужчина']
woman = navec['женщина']

queen_estimate = king - man + woman
print(ln.norm(navec['стол'] - navec['стул']))
print(ln.norm(navec['стул'] - navec['чехословакия']))
print(ln.norm(navec['диктатор'] - navec['булочка']))
print(ln.norm(navec['лабрадор'] - navec['овчарка']))
print(ln.norm(navec['народ'] - navec['люди']))
print(ln.norm(navec['шторы'] - navec['тюль']), end = "\n\n")
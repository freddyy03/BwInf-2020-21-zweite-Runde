import time
start_time = time.time()

"""Eingabe"""
file = open('BspEingabe1.txt')
numFruits = int(file.readline())  # Anzahl der verfügbaren Obstsorten
# print(numFruits)
fav = file.readline().split()  # Donalds Wunschsorten ('Favoriten')
# print(fav)
N = int(file.readline())  # Anzahl N der beobachteten Obstspieße
# print(N)
# in je zwei Zeilen hintereinander eine Beobachtung; in der ersten Zeile die Menge der Schüsselnummern, aus denen die in
# der zweiten Zeile angegebenen Obstsorten stammen ('bowls and fruits')
bowls = []
fruits = []
for i in range(N):
    bowls.append(file.readline().split())
    fruits.append(file.readline().split())
# print(bowls)
# print(fruits)

"""Variablen"""
# erstellt dictionary mit Anfangsbuchstabe als key und Obstsorte als value ('a' für 'abbreviations')
# ändert Obstsorten von fav und baf zu den Anfangsbuchstaben der Obstsorten
a = {}

for i in range(len(fav)):
    a[fav[i][0]] = fav[i]
    fav[i] = fav[i][0]

for i in range(len(fruits)):
    for j in range(len(fruits[i])):
        a[fruits[i][j][0]] = fruits[i][j]
        fruits[i][j] = fruits[i][j][0]

a = dict(sorted(a.items()))
# print(a)

# dictionary, das jeder Schüssel eine Obstsorte zuordnen soll
result = {}

for i in range(1, numFruits+1):
    result[str(i)] = []
# print(result)

# gleich aufgebauter dictionary wie 'result'
# values geben an, ob der Key (Schüssel) in den Beobachtungen ('observation') vorkommt
# 1 an der Stelle i bedeutet, dass die Schüssel in der i-ten Beobachtung vorkommt
# 0 an der Stelle i bedeutet, dass die Schüssel in der i-ten Beobachtung nicht vorkommt
observation = {}

for i in range(1, numFruits+1):
    observation[str(i)] = []

for x in observation:
    for y in bowls:
        if x in y:
            observation[x].append(1)
        else:
            observation[x].append(0)
# print(observation)

# Liste mit dem boolean-Wert, ob die Obstsorte schon einer Schüssel zugeordnet wurde
checked = [False] * numFruits

"""Programm"""
for i in fruits:
    # iteriert durch die Beobachtungen der Obstsorten
    for j in i:
        # iteriert durch die Obstsorten
        if not checked[ord(j) - ord('A')]:
            # prüft, ob eine Obstsorte schon einer Schüssel zugeordnet wurde
            temp = []
            for k in fruits:
                # erstellt eine Liste mit der Beobachtung der Obstsorte
                if j in k:
                    temp.append(1)
                else:
                    temp.append(0)
            for l in observation:
                # vergleicht die Liste mit der Beobachtung der Obstsorte mit der Beobachtung der Schüssel und ordnet
                # ggf. zu
                if observation[l] == temp:
                    result[l].append(j)
                    checked[ord(j) - ord('A')] = True

# nicht zugeordnete Schüsseln werden mit nicht geprüften Obstsorten verglichen und ggf. zugeordnet
left = []

for i in range(len(checked)):
    if not checked[i]:
        left.append(chr(ord('A') + i))

for x in result:
    if result[x] == []:
        result[x].extend(left)

"""Ausgabe"""
# print(fav)
# print(bowls)
# print(fruits)
# print(result)

r = []  # speichert alle richtigen Obstsorten
w = []  # speichert alle falschen Obstsorten, die in einer Schüssel mit möglichen richtigen Obstsorten enthalten sind
for i in result:
    x = result[i]
    b1 = False
    b2 = False
    temp1 = []
    temp2 = []
    for y in x:
        if y in fav:
            b1 = True
            if i not in temp1:
                temp1.append(i)
        else:
            b2 = True
            if y not in w:
                temp2.append(y)
    r.extend(temp1)
    if b1 and b2:
        w.extend(temp2)

for i in range(len(w)):
    w[i] = a[w[i]]

if w == []:
    print('Donald soll sich aus den Schüsseln ', end='')
    print(', '.join(r), end='')
    print(' bedienen, um eine seiner Lieblingssorten zu ziehen.')
else:
    print('Das Ergebnis ist nicht eindeutig, da unter den potenziellen Schüsseln auch die Sorten ', end='')
    print(', '.join(w), end='')
    print(' vorkommen.')

print("--- %s seconds ---" % (time.time() - start_time))

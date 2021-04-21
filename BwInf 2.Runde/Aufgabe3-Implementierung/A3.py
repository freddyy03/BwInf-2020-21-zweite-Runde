import time
start_time = time.time()

"""Eingabe"""
file = open('BspEingabe4.txt')
firstLine = file.readline().split()
c = int(firstLine[0])  # Umfang des Sees ('circumference')
N = int(firstLine[1])  # Anzahl der Häuser
# print(c, N)
a = [int(x) for x in file.readline().split()]  # Adressen der Häuser ('address')
# print(a)


"""Teil 1"""
# bestimmt die Distanz von einer Adresse zur Eisbude
def dist(x, e, c):
    if x == e:
        return 0
    elif abs(x-e) > c//2:
        return abs(c-abs(x-e))-1
    else:
        return abs(x-e)-1


# fügt in der Liste v an jeder Position des Sees die Häuser ein, die für eine Eisbude an dieser Position
# stimmen würden
def countV(x, c, v, d):
    if x-d < 0:  # distance überlappt links von 0
        for i in range(x+d+1):
            # v[i] += 1
            v[i].append(x)
        for i in range(-(d-x), 0):
            # v[i] += 1
            v[i].append(x)
    elif x+d >= c:  # distance überlappt rechts von 0
        for i in range(x-d, len(v)):
            # v[i] += 1
            v[i].append(x)
        for i in range(d-(c-1-x)):
            # v[i] += 1
            v[i].append(x)
    else:  # distance überlappt gar nicht
        for i in range(x-d, x+d+1):
            # v[i] += 1
            v[i].append(x)


result = [] # speichert alle votes, also alle Listen v
for x in range(0, N-1):
    i = a[x]
    for y in range(x+1, N):
        j = a[y]
        for k in range(0, c):
            if (k == i) or (k == j):  # es können keine zwei oder drei Eisbuden am gleichen Ort sein
                continue
            v = [[] for x in range(c)]  # speichert die Stimmen für jede Position am See
            # i = 7
            # j = 37
            # k = 27
            for x in a:
                d = min(dist(x, i, c), dist(x, j, c), dist(x, k, c))
                countV(x, c, v, d)
            v[i] = []
            v[j] = []
            v[k] = []
            v.append(i)
            v.append(j)
            v.append(k)
            result.append(v)
            # break
        # break
    # break


"""Teil 2"""
# überflüssig, ich dachte wenn man gleich zur größten Stimme springt bekommt man eindeutige Lösungen
# es hat sich jedoch herausgestellt, dass es immer noch falsche Lösungen in der Ausgabe gab
# es können lediglich die falschen Lösungen damit minimiert werden
# die Funktion isValid(v) (s. unten) prüft mit Brute-Force, ob unter den minimierten Lösungen richtige dabei sind
def moveToFirst(v, largest):
    temp = []
    for i in range(len(v)):
        if len(v[i]) == largest:
            temp.append(v[i])
    for i in range(len(temp)):
        if temp[i][0] not in temp[i-1]:
            start = i
            break
    if temp != []:
        start = v.index(temp[i])
    else:
        return v
    new = v[start:]
    new.extend(v[:start])
    return new


# berechnet die unterschiedlichen Stimmen zu den Stimmen von den bereits bestimmten Eisbuden in e
def isDifferent(l1, l2, largest):
    counter = 0
    for x in l1:
        if x in l2:
            counter += 1
    if counter <= len(l1)-largest:
        return True
    return False


# berechnet (fast immer) die größtmöglichste Anzahl an Stimmen für drei Eisbuden eines Gegenvorschlags
def maxV(v):
    v = v[:-3]
    temp = []
    # streicht alle mehrfach vorkommenden Stimmen
    for i in range(len(v)):
        if v[i] != v[i-1] and v[i] != []:
            temp.append(v[i])
    v = temp
    e = [] # hier sollen die drei größten Stimmen gespeichert werden
    total = 0 # die Anzahl der unterscheidbaren Elemente von den Stimmen (maximale Stimmen)
    largest = max([len(x) for x in v]) # größte Länge von den Stimmen
    while len(e) != 3:
        #v = moveToFirst(v, largest)  # nicht in der Doku beschrieben, da unnötig
        for i in range(len(v)):
            if len(e) == 3:
                break
            elif len(v[i]) < largest:
                continue
            else:
                bool = True
                for x in e:
                    if not isDifferent(v[i], x, largest):
                        bool = False
                if bool:
                    e.append(v[i])
                    total += largest
        largest -= 1
    return [total, e, v]


# mit Brute-Force werden die wenigen verbliebenen Lösungen auf Richtigkeit überprüft
def isValid(v):
    for i in range(len(v)-2):
        for j in range(i+1, len(v)-1):
            for k in range(j+1, len(v)):
                counter = 0
                for x in v[i]:
                    if x in v[j]:
                        counter += 1
                    if x in v[k]:
                        counter += 1
                for y in v[j]:
                    if y in v[k] and y not in v[i]:
                        counter += 1
                # nun werden alle unterschiedlichen Elemente ausgegeben
                if len(v[i]) + len(v[j]) + len(v[k]) - counter > N//2:
                    return False
    return True


#result = sorted(result, key=lambda x: max([len(y) for y in x[:-3]]))

"""Ausgabe"""
bool = True
for i in range(len(result)):
    v = result[i]
    # print(v)
    x = maxV(v)
    # print(x[0],x[1], x[2])
    if x[0] <= N//2:
        if isValid(x[2]):
            print(sorted([v[-3], v[-2], v[-1]]))
            bool = False
if bool:
    print('Keine Lösung')

print("--- %s seconds ---" % (time.time() - start_time))

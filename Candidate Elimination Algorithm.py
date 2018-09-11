import csv

with open("Dataset.csv", "r") as f:
    reader = csv.reader(f)
    arr = list(reader)

GS = []
SS = []
values = []
t1 = []
t2 = []
for i in range(0, arr[0].__len__() - 1):
    t1.append(0)
    t2.append("?")
    values.append([])
SS.append(t1)
GS.append(t2)


def initialize():
    for i in arr:
        ptr = 0
        for j in i[0:i.__len__() - 1]:
            if j not in values[ptr]:
                values[ptr].append(j)
            ptr += 1


def unique(x):
    y = []
    for i in x:
        if i in y:
            pass
        else:
            y.append(i)
    return y


def isConsistent(x, y):
    for i in range(0, x.__len__() - 1):
        if x[i] != y[i] and x[i] != "?" and y[i] != "?":
            return False
    return True


def getQues(x):
    c = 0
    for i in x:
        if i == "?":
            c += 1
    return c


def generalization(x, s):
    ret = []
    for i in range(0, 2 ** s.__len__()):
        temp = s.copy()
        for j in range(0, s.__len__()):
            if i & (1 << j):
                if temp[j] == 0:
                    temp[j] = x[j]
                else:
                    temp[j] = "?"
        if isConsistent(x, temp):
            ret.append(temp)
    SS.remove(s)
    ret = unique(ret)
    min = x.__len__() - 1
    newS = []
    for i in ret:
        if getQues(i) < min:
            min = getQues(i)
    for i in ret:
        if getQues(i) == min:
            newS.append(i)
    return newS


def specialization(x, g):
    ret = [g]
    newG = []
    flag = 0
    while flag == 0:
        i = ret[0]
        for j in range(0, i.__len__()):
            for k in values[j]:
                temp = i.copy()
                temp[j] = k
                if not isConsistent(temp, x):
                    tf = 0
                    for m in arr:
                        if m[-1].upper() == "YES":
                            if not isConsistent(m, temp):
                                tf = 1
                        else:
                            if isConsistent(m, temp):
                                tf = 1
                    if tf == 0:
                        newG.append(temp)
                        flag = 1
                    else:
                        ret.append(temp)
                else:
                    ret.append(temp)
        ret.remove(i)
    return newG


initialize()
for i in arr:
    if i[-1].upper() == "YES":
        for j in GS:
            if not isConsistent(i, j):
                GS.remove(j)
        for j in SS:
            if not isConsistent(i, j):
                SS = SS + generalization(i, j)
    else:
        for j in SS:
            if isConsistent(i, j):
                SS.remove(j)
        for j in GS:
            if isConsistent(i, j):
                GS = GS + specialization(i, j)
                GS.remove(j)
print(SS)
print(GS)


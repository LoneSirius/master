#   compare sorting algorithms
#
#   By Angus Lin
#   2022.01.21
#   
#   
import logging
import random
import datetime
re_count = 0

#   base version of quick sort
def quick_re0(data, s = None,e = None):
    global re_count
    re_count += 1
    s = 0 if s == None else s
    e = len(data) - 1 if e == None else e
    if e > s:
        i = s
        j = s + 1
        while (j <= e):
            if data[j] < data[s]:
                i += 1
                data[i], data[j] = data[j], data[i]
            j += 1
        data[i], data[s] = data[s], data[i]
        quick_re0(data, s, i - 1)
        quick_re0(data, i + 1, e)
    return data

#   enhanced version of quick sort
def quick_re(data, s = None,e = None):
    global re_count
    re_count += 1
    s = 0 if s == None else s
    e = len(data) - 1 if e == None else e
    if e > s:
        i = s
        j = s + 1
        while (j <= e):
            if data[j] < data[s]:
                i += 1
                data[i], data[j] = data[j], data[i]
            j += 1
        if i != s:
            data[i], data[s] = data[s], data[i]
            quick_re(data, s, i - 1)
        quick_re(data, i + 1, e)
    return data

#   Quick Sort - non recursive version
def quick_nonre(data):
    stack = []
    stack.append([0,len(data)-1])
    while len(stack) > 0:
        s, e = stack.pop()
        if e > s:
            i = s
            j = s + 1
            while (j <= e):
                if data[j] < data[s]:
                    i += 1
                    data[i], data[j] = data[j], data[i]
                j += 1
            if i != s:
                data[i], data[s] = data[s], data[i]
                stack.append([s, i - 1])
            stack.append([i + 1, e])
    return data

#   selection sort
def selection(data):
    i = 0
    while i < len(data):
        v = i
        j = i + 1
        while j < len(data):
            if data[v] > data[j]:
                v = j
            j += 1
        data[i], data[v] = data[v], data[i]
        i += 1
    return data

#   bubble sort
def bubble(data):
    k = 0
    while k < len(data):
        i = 1
        while i < len(data) - k:
            if data[i - 1] > data[i]:
                data[i - 1], data[i] = data[i], data[i - 1]
            i += 1
        k += 1
    return data

#   check if the elements in data are in order.
def verify(data):
    i = 0
    while i < len(data) - 1:
        if data[i] > data[i + 1]:
            print(f'Error : {i} {data[i]} {data[i+1]}')
        i += 1

if __name__ == "__main__":
    #logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    # alglist = [[re_qs, 'Recursive quick sort'],
    #            [nonre_qs, 'Non-recursive quick sort'],
    #            [ss, 'Selection sort'],
    #            [bs, 'Bubble sort'] ]
    # alglist = [[quick_nonre1, 'Recursive quick sort V1'],
    #             [quick_nonre2, 'Recursive quick sort V1']]
    # #                [quick_re2, 'Recursive quick sort V2']]
    alglist = [[quick_re0, 'Recursive quick sort v0'],
                [quick_re, 'Recursive quick sort'],
                [quick_nonre, 'Non-recursive quick sort'],
                [selection, 'Selection sort'],
                [bubble, 'Bubble sort']]

    srcdata = []
    datalen = 10000
    i = 0
    while i < datalen:
        srcdata.append(random.randint(1,1000000))
        i += 1
    #print(srcdata)
    for alg, msg in alglist:
        re_count = 0
        t1 = datetime.datetime.now()
        res = alg(srcdata.copy())
        t2 = datetime.datetime.now()
        verify(res)
        print(f"time = {t2 - t1} / Recursive call = {re_count} / {msg}")
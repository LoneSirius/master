#   compare sorting algorithms
#
#   By Angus Lin
#   2022.01.21
#
#   Remark :
#   2022.01.21  create first version quick sort, selection sort and bubble sort.
#
#
import logging
import random
import datetime
import math
re_count = 0

#   merge sort


def merge_re(data, s=None, e=None):
    global re_count
    re_count += 1
    s = 0 if s == None else s
    e = len(data) - 1 if e == None else e

    #   if length of data less than 2, swap and return
    if (e - s + 1) <= 2:
        if data[s] > data[e]:
            data[s], data[e] = data[e], data[s]
        return data[s:e + 1]
    else:
        m = (e - s + 1) // 2 + s
        ld = merge_re(data, s, m)
        rd = merge_re(data, m + 1, e)

        # merge back the two segments
        l, r = 0, 0
        res = []
        while l < len(ld) and r < len(rd):
            if ld[l] < rd[r]:
                res.append(ld[l])
                l += 1
            else:
                res.append(rd[r])
                r += 1
        if l >= len(ld):
            res = res + rd[r:]
        elif r >= len(rd):
            res = res + ld[l:]

        return res

#   merge sort version 1


def merge_re1(data, s=None, e=None):
    global re_count
    re_count += 1
    s = 0 if s == None else s
    e = len(data) - 1 if e == None else e

    #   if length of data less than 2, swap and return
    if (e - s + 1) < 2:
        return data[s:e + 1]
    else:
        m = math.floor((e - s + 1) / 2) + s
        ld = merge_re(data, s, m)
        rd = merge_re(data, m + 1, e)

        # merge back the two segments
        l, r = 0, 0
        res = []
        while l < len(ld) and r < len(rd):
            if ld[l] < rd[r]:
                res.append(ld[l])
                l += 1
            else:
                res.append(rd[r])
                r += 1
        if l >= len(ld):
            res = res + rd[r:]
        elif r >= len(rd):
            res = res + ld[l:]

        return res

#   Non-recursive merge sort (bottom up)


def merge_nonre(data):
    e = len(data)
    step = 1

    while step < e:
        l = 0
        while (l < e):
            r = min(l + step, e - 1)
            re = min(r + step - 1, e - 1)
            #   merge left and right
            ld = data[l:r].copy()
            rd = data[r:re + 1].copy()
            i, lp, rp = l, 0, 0
            while lp < len(ld) and rp < len(rd):
                if ld[lp] < rd[rp]:
                    data[i] = ld[lp]
                    lp += 1
                else:
                    data[i] = rd[rp]
                    rp += 1
                i += 1

            while rp < len(rd):
                data[i] = rd[rp]
                rp += 1
                i += 1
            while lp < len(ld):
                data[i] = ld[lp]
                lp += 1
                i += 1
            l += step * 2
        step *= 2
    return data

#   base version of quick sort


def quick_re0(data, s=None, e=None):
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


def quick_re(data, s=None, e=None):
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
    stack.append([0, len(data)-1])
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


def test():
    # alglist = [[quick_re0, 'Recursive quick sort v0'],
    #            [quick_re, 'Recursive quick sort'],
    #            [quick_nonre, 'Non-recursive quick sort'],
    #            [selection, 'Selection sort'],
    #            [bubble, 'Bubble sort']]
    alglist = [[quick_re0, 'Recursive quick sort v0'],
               [quick_re, 'Recursive quick sort'],
               [quick_nonre, 'Non-recursive quick sort'],
               [merge_re, 'Recursive Merge sort'],
               [merge_re1, 'Recursive Merge sort version 1'],
               [merge_nonre, 'Non-recursive merge sort (bottom up)']]

    srcdata = []
    datalen = 1000000
    i = 0
    while i < datalen:
        srcdata.append(random.randint(1, 100000))
        i += 1
    for alg, msg in alglist:
        re_count = 0
        t1 = datetime.datetime.now()
        res = alg(srcdata.copy())
        t2 = datetime.datetime.now()
        verify(res)
        print(f"time = {t2 - t1} / Recursive call = {re_count} / {msg}")


if __name__ == "__main__":
    #logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    test()
    #print(merge_nonre([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))

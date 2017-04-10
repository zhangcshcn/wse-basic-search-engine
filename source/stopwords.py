#!/usr/bin/python
# -*- coding: utf-8 -*-
# from __future__ import print_function
import sys
import os
import re
import lxml
import numpy as np
# from bs4 import BeautifulSoup as BS


def stopwords(path):
    if not os.path.isdir(path):
        print("No directory named %s" % os.path.abspath(path))
        return
    env = os.getcwd()
    fList = os.listdir(path)
    words = {}
    for fname in fList:
        fp = open(path + '/' + fname)
        for w in re.findall('[0-9a-zA-Z]+', fp.read()):
            if w.lower() not in words:
                words[w.lower()] = 1
            else:
                words[w.lower()] += 1
        fp.close()
    wordtag = np.array(words.keys())
    wordlabel = {x: word for x, word in enumerate(wordtag)}
    vals = np.array(words.values())
    idx = np.argsort(vals)[::-1]
    vals[::-1].sort()
    vallog = np.log10(vals)
    ranklog = np.log10(np.arange(len(vallog)) + 1)
    maxval, minval = vallog[0], vallog[-1]
    maxrank, minrank = ranklog[0], ranklog[-1]
    a = (maxval - minval) / (maxrank - minrank)
    b = maxrank - a * maxval
    diff = vallog - a * ranklog - b
    pivot = np.argmax(diff)

    '''fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(np.arange(pivot) + 1, vals[:pivot],
              label="Stop Words", marker="x", color='red')
    ax.loglog(np.arange(pivot, len(vals)) + 1, vals[pivot:],
              label="Non-Stop Words", marker='o', color='blue')
    ax.set_title("Word Frequency Distribution",fontsize=25)
    ax.set_xlabel('rank', fontsize=15)
    ax.set_ylabel('occurence', fontsize=20)
    leg = ax.legend(loc='upper right', fancybox=True)
    leg.get_frame().set_alpha(0.7)
    plt.savefig('stopword.png')'''
    return wordtag[idx[:pivot]]


if __name__ == "__main__":
    print (stopwords(sys.argv[1]))

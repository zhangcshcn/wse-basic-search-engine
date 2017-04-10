#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jcc
from lucene import \
    QueryParser, IndexSearcher, StandardAnalyzer, SimpleFSDirectory, File, \
    VERSION, initVM, Version, getVMEnv, Term
import numpy as np
import re
import os

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


def run(searcher, analyzer, command):
    # print "Searching for:", command
    query = QueryParser(Version.LUCENE_CURRENT, "contents",
                        analyzer).parse(command)
    scoreDocs = searcher.search(query, 10).scoreDocs
    # print "%s total matching documents." % len(scoreDocs)
    rankedfiles = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        # print 'path:', doc.get("path"), 'name:', doc.get("name")
        rankedfiles.append(int(doc.get("name")))
    return rankedfiles


def SearchFiles(command):
    STORE_DIR = "lucene/index"
    getVMEnv().attachCurrentThread()
    # print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    rankedfiles = run(searcher, analyzer, command)
    searcher.close()
    return rankedfiles


def queryenhancement(query, swords, k, fList, path, TotalN):
    if not os.path.isdir(path):
        print("No directory named %s" % os.path.abspath(path))
        return
    if len(fList) == 0:
        return ""
    wordcount = {}
    N = len(fList)
    # def length of docs
    doclen = np.zeros(N)
    # def docs query
    docquery = np.zeros(N)
    # proximity to query word
    proxword = {}
    # tokenize query
    queryword = re.findall('[0-9a-zA-Z]+', query)
    for i in range(N):
        fname = fList[i]
        fp = open(path + "/" + str(fname))
        # tokenize doc
        docword = [s.lower() for s in re.findall("[0-9a-zA-Z]+", fp.read())]
        # length of docs
        doclen[i] = len(docword)                                # l(D)
        # store the location of query words
        queryloc = []
        for j in range(len(docword)):
            # occurence of words
            if docword[j] not in wordcount:
                wordcount[docword[j]] = np.zeros(N)
                wordcount[docword[j]][i] = 1
            else:
                wordcount[docword[j]][i] += 1
            # record token location
            if docword[j].lower() in queryword:
                docquery[i] += 1                                # m(Q,D)
                queryloc.append(j)
        proxanc = [filter(lambda y: y < 6 and y > 0, range(x - 5, x + 6))
                   for x in queryloc]
        for ancL in proxanc:
            for anc in ancL:
                if docword[anc] not in proxword:
                    proxword[docword[anc]] = np.zeros(N)
                    proxword[docword[anc]][i] = 1
                else:
                    proxword[docword[anc]][i] += 1
        fp.close()
    # exclude stopwords and query words
    for w in wordcount.keys():
        if w in queryword or w in swords:
            wordcount.pop(w)                                    # c(W,D)
    for w in proxword.keys():
        if w in queryword or w in swords:
            proxword.pop(w)
    # align proximity measurement and word frequency
    for w in wordcount.keys():
        if w not in proxword:
            proxword[w] = np.zeros(N)                           # f(W,Q,D)
    rwordocc = {w: np.sum(wordcount[w] != 0) for w in wordcount}  # z(W,Q)

    STORE_DIR = "lucene/index"
    getVMEnv().attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR))
    ireader = IndexSearcher(directory, True)
    docfreq = {w: ireader.docFreq(Term("contents", w.lower()))
               for w in wordcount}                              # g(W)
    ireader.close()
    # label the words
    wordtag = np.array(wordcount.keys())
    wordlabel = {x: word for x, word in enumerate(wordtag)}

    score1 = np.zeros([len(wordcount), N])
    score2 = np.zeros([len(wordcount), N])
    y = np.zeros(len(wordcount))
    for i in range(len(wordcount)):
        w = wordlabel[i]
        score1[i] = proxword[w]
        score2[i] = wordcount[w]
        y[i] = np.max([0, (rwordocc[w] * 1. / N - 2. * docfreq[w] / TotalN)])
    score1 *= 1. / docquery
    score2 *= 1. / doclen
    score1 = np.sqrt(score1)
    score2 = np.sqrt(score2)
    vals = np.sum(score1 + (y * score2.T).T, axis=1)
    idx = np.argsort(vals)[::-1]
    print vals[idx[:100]]
    print docquery
    ret = ""
    count = 0
    for i in range(len(idx)):
        # if wordtag[idx[i]] not in query and wordtag[idx[i]] not in swords:
        ret += " " + wordtag[idx[i]]
        count += 1
        if count < k:
            continue
        else:
            break
    # print ret
    return ret


if __name__ == '__main__':
    queryenhancement("trump", set(), 2, [10, 20, 12, 30], "../index")

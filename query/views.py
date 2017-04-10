# Create your views here.
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import Docs, IndexedUrl, StopWords

import os
import sys

cwd = os.getcwd()
os.chdir("source")
sys.path.append(os.getcwd())
os.chdir("../lucene")
sys.path.append(os.getcwd())
os.chdir(cwd)

from Build import BuildSearchEngine
from SearchFiles import SearchFiles, queryenhancement
from stopwords import stopwords

swords = set()


def index(request):
    global swords
    if len(swords) == 0:
        swords = set(stopwords("cache"))
        swords.add("rlq")
        swords.add("u")
        swords.add("wp")
        print "stopwords fixed!"
    inCache = IndexedUrl.objects.all()
    return render(request, 'query/index.html', {'inCache': inCache})


def newIndex(request):
    return render(request, 'query/crawl.html')


def what(request):
    return render(request, 'query/queryenhancement.html')


def crawl(request):
    inCache = IndexedUrl.objects.all()
    start = request.POST['start']
    number = int(request.POST['number'])
    domain = request.POST['domain']
    global swords
    try:
        fHash = BuildSearchEngine(start, number, domain)
        for q in IndexedUrl.objects.all():
            q.delete()
        for q in Docs.objects.all():
            q.delete()
        '''for q in StopWords.objects.all():
            q.delete()'''

        log = IndexedUrl.objects.create(
            start=start, number=number, domain=domain, timestamp=timezone.now())
        log.save()
        for num in fHash:
            url, title = fHash[num]
            doc = Docs.objects.create(num=num, url=url, title=title)
            doc.save()
        swords = set(stopwords("cache"))
        '''for w in stopwords("cache"):
            word = StopWords.objects.create(word=w)
            word.save()'''
        # print fHash
        return render(request, 'query/results.html', {'start': start, 'number': num + 1, 'domain': domain})
    except:
        return render(request, 'query/error.html', {'inCache': inCache})


def fix(request):
    global swords
    print "start fixing"
    swords = set(stopwords("cache"))
    swords.add("rlq")
    swords.add("u")
    swords.add("wp")
    fp = open("stopwords.txt", "w")
    fp.write("<table>\n<tr>\n")
    i = 0
    for w in swords:
        fp.write(" <td> %s </td> " % w)
        i += 1
        if (i % 8 == 0):
            fp.write("</tr>\n<tr>")

    fp.write("</tr>\n</table>")
    fp.close()
    return HttpResponse("StopWords fixed!")


def search(request):
    global swords
    if len(swords) == 0:
        swords = set(stopwords("cache"))
        swords.add("rlq")
        swords.add("u")
        swords.add("WP")
        print "stopwords fixed!"
    inCache = IndexedUrl.objects.all()
    backupnumDocs = 0
    backup = []
    qaug = ""
    try:
    # if True:
        q = request.GET.get('q', None)
        try:
            k = int(request.GET.get('k', None))
        except:
            k = 0
        print "searching ", q, ", ", k
        rankedfiles = SearchFiles(q)
        if k != 0:
            for docID in rankedfiles:
                backup.append(Docs.objects.get(num=int(docID)))
            backupnumDocs = len(backup)
            qaug = queryenhancement(
                q, swords, k, rankedfiles, "cache", inCache[0].number)
            # print qaug
            rankedfiles = SearchFiles(q + qaug)
        url_title = []
        for docID in rankedfiles:
            url_title.append(Docs.objects.get(num=int(docID)))
        numDocs = len(url_title)
        return render(request, 'query/present.html',
                      {'docs': url_title, 'q': q, 'qaug': qaug, 'numDocs': numDocs,
                       'inCache': inCache, 'backup': backup, 'backupnumDocs': backupnumDocs})
    except:
       return render(request, 'query/error.html', {'inCache': inCache})

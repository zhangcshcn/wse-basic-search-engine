# Create your views here.
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .forms import Keywords
from .models import Docs, IndexedUrl

import os, sys
cwd = os.getcwd()
os.chdir("source")
sys.path.append(os.getcwd())
os.chdir("../lucene")
sys.path.append(os.getcwd())
os.chdir(cwd)

from Build import BuildSearchEngine
from SearchFiles import SearchFiles

fHash = {}

def index(request):
    inCache = IndexedUrl.objects.all()
    return render(request, 'query/index.html',{'inCache':inCache})
    
def crawl(request):
    inCache = IndexedUrl.objects.all()
    start = request.POST['start']
    number = int(request.POST['number'])
    domain = request.POST['domain']
    
    try:
        fHash = BuildSearchEngine(start,number,domain)
        for q in IndexedUrl.objects.all():
            q.delete()
        for q in Docs.objects.all():
            q.delete()
            
        log = IndexedUrl.objects.create(start=start,number=number,domain=domain,timestamp=timezone.now())
        log.save()
        for num in fHash:
            url,title = fHash[num]
            doc = Docs.objects.create(num=num,url=url,title=title)
            doc.save()
        
        # print fHash
        return render(request, 'query/results.html', {'start': start,'number': num+1,'domain':domain})
    except:
        return render(request, 'query/error.html',{'inCache':inCache})
        
    
def search(request):
    inCache = IndexedUrl.objects.all()
    try:
        q = request.GET.get('q',None)
        print "searching ",q
        rankedfiles = SearchFiles(q)
        print rankedfiles
        url_title = []
        for docID in rankedfiles:
            d = Docs.objects.get(num=int(docID))
            url_title.append(d)
        numDocs = len(url_title)
        # print url_title
        return render(request, 'query/present.html', {'docs': url_title,'q':q,'numDocs':numDocs,'inCache':inCache })
    except:
        return render(request, 'query/error.html',{'inCache':inCache})
    

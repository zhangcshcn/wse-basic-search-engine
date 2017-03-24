from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Docs(models.Model):
    num = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=100, null=True, blank=True) 
    def __str__(self):
        return "%d\t%s: %s"%(self.num,self.url,self.title)
    
@python_2_unicode_compatible      
class IndexedUrl(models.Model):
    start = models.CharField(max_length=200)
    number = models.IntegerField(null=True, blank=True)
    domain = models.CharField(max_length=100)
    timestamp = models.DateTimeField('date crawded')
    def __str__(self):
        return "%s\t%d\t%s"%(self.timestamp,self.number,self.start)

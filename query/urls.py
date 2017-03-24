from django.conf.urls import url

from . import views

app_name = 'query'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^crawl$', views.crawl, name='crawl'),
    url(r'^search$', views.search, name='search'),
]

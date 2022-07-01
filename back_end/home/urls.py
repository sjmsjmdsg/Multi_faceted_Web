from django.urls import path

from home.views import getLatestCve, getHtmlByUrl
# from common.views import getLatestCve

urlpatterns = [
    path('cvelatest', getLatestCve),
    path('gethtml',getHtmlByUrl)
]
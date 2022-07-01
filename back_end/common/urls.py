from django.urls import path

# from common.views import returnClickNums, searchKey,searchOneCve
from common.views import searchKey, searchOneCve, getBarPicData, getNewCve,getMenu, returnClickNums, getCompareData, searchByStr, searchByStr2,searchByStr3, getAspectMultiInfo

urlpatterns = [
    # path('clicknums/', returnClickNums),
    path('search', searchKey),
    path('searchbystr',searchByStr),
    path('searchbystr2', searchByStr3),
    path('cveinfo', searchOneCve),
    path('bardata', getBarPicData),
    path('getnewcve', getNewCve),
    path('getmenu', getMenu),
    path('getclicknum', returnClickNums),
    path('comparedata', getCompareData),
    path('multiinfo', getAspectMultiInfo)
]
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def listorders(request):
    return HttpResponse("下面是系统中所有的订单信息...")

def listorders1(request):
    return HttpResponse("下面是系统中所有的订单信息111...")

from django.urls import path

from search.views import listorders,listorders1

urlpatterns = [
    path('orders/', listorders),

    path('orders1/', listorders1),
]
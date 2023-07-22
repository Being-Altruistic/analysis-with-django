from django.urls import include, path
from .views import (home_view, SaleListView,
                    SaleDetailView)

app_name = 'sales'

urlpatterns =[
    path('', home_view, name='home'),
    path('list/', SaleListView.as_view(), name='list'),
    path('list/<pk>/', SaleDetailView.as_view(), name='detail')
]
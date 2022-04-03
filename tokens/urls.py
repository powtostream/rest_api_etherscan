from django.urls import path

from . import views

app_name = 'tokens'

urlpatterns = [
    path('create/', views.Create.as_view(), name='create'),
    path('list/', views.TokenList.as_view(), name='list'),
    path('total_supply/', views.TotalSupply.as_view(), name='total_supply'),
]

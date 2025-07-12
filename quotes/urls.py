from django.urls import path
from .views.random_quote import random_quote_view, rate_quote_view
from .views.dashboard import dashboard_view

app_name = 'quotes'

urlpatterns = [
    path('', random_quote_view, name='random-quote'),
    path('rate/', rate_quote_view, name='rate-quote'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

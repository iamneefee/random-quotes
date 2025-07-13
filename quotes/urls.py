from django.urls import path
from .views.random_quote import random_quote_view, rate_quote_view
from .views.dashboard import dashboard_view
from .views.add_entry import add_quote_view, add_source_view

app_name = 'quotes'

urlpatterns = [
    path('', random_quote_view, name='random-quote'),
    path('rate/', rate_quote_view, name='rate-quote'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('add/source/', add_source_view, name='add-source'),
    path('add/quote/', add_quote_view, name='add-quote'),
]

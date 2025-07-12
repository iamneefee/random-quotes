from django.urls import path
from quotes import views

app_name = 'quotes'

urlpatterns = [
    path('', views.random_quote, name='random-quote'),
    path('rate/', views.rate_quote, name='rate-quote'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

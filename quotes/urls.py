from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quote_list, name='quote_list'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('tag/<str:tag>/', views.search_quotes_by_tag, name='search_by_tag'),
    path('author/<int:author_id>/', views.quotes_by_author, name='quotes_by_author'), 
]

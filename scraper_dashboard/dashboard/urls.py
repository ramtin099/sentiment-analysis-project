from django.urls import path
from .views import home_view, news_view, dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('news/', news_view, name='news'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

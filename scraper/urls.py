from django.contrib import admin
from django.urls import path
from scraper.views import DashboardPageView,MarketPageView,ListingDetailView,InformationView, UserDashboardView

app_name = 'scraper'

urlpatterns=[
    path('dashboard/', DashboardPageView.as_view(),name='dashboard'),
    path('Market/<str:pk>/',MarketPageView.as_view(),name='market_detail'),
    path('Listing/<int:pk>/',ListingDetailView.as_view(),name='listing_detail'),
    path('information/',InformationView.as_view(),name='information'),
    path('user_dashboard/', UserDashboardView.as_view(), name='user_dashboard' )
]

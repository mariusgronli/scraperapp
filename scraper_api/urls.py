from django.urls import path
from .views import (MarketListView,MarketAdsListView,TotalView,
                    DailyStatisticView,AverageModelView)

app_name = 'scraper_api'

urlpatterns=[
    path('markets/', MarketListView.as_view(),name='markets'),
    path('<str:market>/ads',MarketAdsListView.as_view(),name="ads"),
    path('<str:market>/total',TotalView.as_view(),name="total"),
    path('<str:market>/daily',DailyStatisticView.as_view(),name="daily"),
    path('<str:market>/average',AverageModelView.as_view(),name="average")
]

from django.shortcuts import render
from .serializers import (MarketSerializer,HouseModelSerializer,
                            TotalModelSerializer,DailyStatisticSerializer,
                            AverageModelSerializer)
from scraper.models import (MarketModel,HouseModel,NewTotalModel,DailyStatistic,
                            AverageModel)
from rest_framework import generics
from datetime import date,timedelta


# Create your views here.
class MarketListView(generics.ListAPIView):
    queryset = MarketModel.objects.all()
    serializer_class = MarketSerializer

class MarketAdsListView(generics.ListAPIView):
    #Custom variables
    lookup_url_kwarg = "market"
    #Class variables
    serializer_class = HouseModelSerializer

    def get_queryset(self):
        market = self.kwargs.get(self.lookup_url_kwarg)
        today = date.today()
        allowed = today - timedelta(days=10)
        queryset = HouseModel.objects.filter(date__gte=allowed,date__lte=today,market=market)
        return queryset

class TotalView(generics.RetrieveAPIView):
    #Custom variables
    lookup_url_kwarg = "market"
    #Class variables
    serializer_class = TotalModelSerializer

    def get_object(self):
        market = self.kwargs.get(self.lookup_url_kwarg)
        obj = NewTotalModel.objects.get(market=market)
        return obj

class DailyStatisticView(generics.RetrieveAPIView):
    #Custom variables
    lookup_url_kwarg = "market"
    #Class variables
    serializer_class = DailyStatisticSerializer

    def get_object(self):
        market = self.kwargs.get(self.lookup_url_kwarg).title()
        try:
            obj = DailyStatistic.objects.get(market=market,date=date.today())
        except DailyStatistic.DoesNotExist:
            date_search = date.today() - timedelta(days=1)
            obj = DailyStatistic.objects.get(market=market,date=date_search)
        return obj

class AverageModelView(generics.RetrieveAPIView):
    #Custom variables
    lookup_url_kwarg = "market"
    #Class variables
    serializer_class = AverageModelSerializer

    def get_object(self):
        market = self.kwargs.get(self.lookup_url_kwarg).title()
        obj = AverageModel.objects.get(market=market)
        return obj

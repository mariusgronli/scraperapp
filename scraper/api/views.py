
from rest_framework.generics import get_object_or_404
from .serializers import HouseSerializer,MarketSerializer
from rest_framework.response import Response
from scraper.models import MarketModel,HouseModel,DailyStatistic,AverageModel

################ Market model #####################

from rest_framework import serializers
from scraper.models import (MarketModel,HouseModel,NewTotalModel,DailyStatistic,
                            AverageModel)

class MarketSerializer(serializers.ModelSerializer):

    class Meta:
        model=MarketModel
        fields = "__all__" #We want all the fields.
        #fields = ("field","field")

class HouseModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=HouseModel
        exclude=("id","bilde")

class TotalModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=NewTotalModel
        exclude=("id","total_value","total_sqm")

class DailyStatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model=DailyStatistic
        exclude=("id",)

class AverageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=AverageModel
        exclude=("id",)

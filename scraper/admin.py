from django.contrib import admin
from scraper.models import (MarketModel,HouseModel,TotalModel,AverageModel,
    DailyStatistic,MonthlyStatistic)
# Register your models here.
admin.site.register(MarketModel)
admin.site.register(HouseModel)
admin.site.register(TotalModel)
admin.site.register(AverageModel)
admin.site.register(DailyStatistic)
admin.site.register(MonthlyStatistic)

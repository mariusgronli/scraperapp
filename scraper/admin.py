from django.contrib import admin
from scraper.models import (MarketModel,HouseModel,NewTotalModel,AverageModel,
    DailyStatistic,MonthlyStatistic,PriceModel,DailyScan,ErrorListings,
    ZipCodeModel)
#classes for display
class HouseModelAdmin(admin.ModelAdmin):
    list_display=['id','adress','postnummer','date']

# Register your models here.
admin.site.register(MarketModel)
admin.site.register(HouseModel,HouseModelAdmin)
admin.site.register(NewTotalModel)
admin.site.register(AverageModel)
admin.site.register(DailyStatistic)
admin.site.register(MonthlyStatistic)
admin.site.register(PriceModel)
admin.site.register(DailyScan)
admin.site.register(ErrorListings)
admin.site.register(ZipCodeModel)

from django.db import models
from datetime import datetime
# Create your models here.
class MarketModel(models.Model):
    '''
    Model for markets
    '''
    district = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.district

class HouseModel(models.Model):
    '''
    Model for listings
    '''
    market = models.ForeignKey(MarketModel,related_name='listing',on_delete=models.CASCADE)
    adress = models.CharField(max_length=200)
    postnummer = models.IntegerField(null=True, blank=True)
    prisantydning = models.IntegerField(null=True, blank=True)
    fellesgjeld = models.IntegerField(null=True, blank=True)
    omkostninger = models.IntegerField(null=True, blank=True)
    totalpris = models.IntegerField(null=True, blank=True)
    felleskostnader = models.IntegerField(null=True, blank=True)
    boligtype = models.CharField(max_length=200, null=True, blank=True)
    eieform = models.CharField(max_length=20, null=True, blank=True)
    soverom = models.IntegerField(null=True, blank=True)
    primærrom = models.IntegerField(null=True, blank=True)
    bruksareal = models.IntegerField(null=True, blank=True)
    grunnflate = models.IntegerField(null=True, blank=True)
    etasje = models.IntegerField(null=True, blank=True)
    byggeår = models.IntegerField(null=True, blank=True)
    rom = models.IntegerField(null=True, blank=True)
    tomteareal = models.IntegerField(null=True, blank=True)
    bruttoareal = models.IntegerField(null=True, blank=True)
    areal = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=200)
    bilde = models.URLField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}: {}, annonsert for {}'.format(self.boligtype,self.adress,self.prisantydning)

    class Meta:
      unique_together = ('prisantydning', 'adress')

class TotalModel(models.Model):
    '''
    '''
    market = models.ForeignKey(MarketModel,related_name='total',on_delete=models.CASCADE)
    total_listings = models.IntegerField(null=True, blank=True,default=0)
    total_value = models.IntegerField(null=True, blank=True,default=0)
    total_sqm = models.IntegerField(null=True, blank=True,default=0)

    def __str__(self):
        return 'Total model for {}'.format(self.market)

class AverageModel(models.Model):
    '''
    '''
    market = models.ForeignKey(MarketModel,related_name='average',on_delete=models.CASCADE)
    average_price = models.FloatField(null=True, blank=True)
    average_sqm = models.FloatField(null=True, blank=True)
    average_price_over_sqm = models.FloatField(null=True, blank=True)

    def __str__(self):
        return 'Average statistics for {}'.format(self.market)

class DailyStatistic(models.Model):
    '''
    '''
    market = models.ForeignKey(MarketModel,related_name='daily',on_delete=models.CASCADE)
    listings_value_dd = models.IntegerField(null=True, blank=True,default=0)
    total_listings_dd = models.IntegerField(null=True, blank=True,default=0)
    percent_change_dd = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Daily statistics for {} - {}'.format(self.market,self.date)

class MonthlyStatistic(models.Model):
    '''
    '''
    market = models.ForeignKey(MarketModel,related_name='monthly',on_delete=models.CASCADE)
    listings_value_mm = models.IntegerField(null=True, blank=True)
    highest_listing_mm = models.IntegerField(null=True, blank=True)
    lowest_listing_mm = models.IntegerField(null=True, blank=True)
    total_listings_mm = models.IntegerField(null=True, blank=True)
    percent_change_mm = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Monthly statistics for {} - {}'.format(self.market,self.date)

class PriceModel(models.Model):
    market = models.ForeignKey(MarketModel,related_name='price',on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Average price: {}'.format(self.price)

class DailyScan(models.Model):
    '''
    The model tracks the daily scan from the scraper
    '''
    error_complex = models.IntegerField(null=True, blank=True)
    error_price_sqm = models.IntegerField(null=True, blank=True)
    populated_count = models.IntegerField(null=True, blank=True)
    ads_searched = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Ads searched: {}. at {}}'.format(self.ads_searched,self.date)

class ErrorListings(models.Model):
    '''
    The model stores the information of the ad that was not populated
    '''
    listing = models.URLField(max_length=500)
    error_message = models.CharField(max_length=200, null=True, blank=True)
    date = date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'listing: {}'.format(self.listing)

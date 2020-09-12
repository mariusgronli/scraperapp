from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView,DetailView
from scraper.models import (TotalModel,DailyStatistic,AverageModel,
    MarketModel,HouseModel,ErrorListings,DailyScan)
import datetime
# Create your views here.

class LandingPageView(TemplateView):
    template_name = "scraper/index.html"

class InformationView(TemplateView):
    template_name = "scraper/dashboard/information.html"

class ListingDetailView(DetailView):
    model = HouseModel
    context_object_name = 'listing'
    template_name = "scraper/dashboard/listing_detail.html"

class MarketPageView(DetailView):
    model = MarketModel
    context_object_name = 'market'
    template_name = "scraper/dashboard/market_detail.html"

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super(MarketPageView, self).get_context_data(**kwargs)
        market = get_object_or_404(MarketModel,pk=pk)
        #Get the total values
        total = TotalModel.objects.get(market=market)
        average = AverageModel.objects.get(market=market)
        #Get the dailystats
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        try:
            daily_stat = DailyStatistic.objects.get(market=market,date=today)
        except DailyStatistic.DoesNotExist:
            daily_stat = DailyStatistic.objects.get(market=market,date=yesterday)
        new_percent = daily_stat.percent_change_dd*100
        #Get the listings
        #put in a filter function instead
        all_models= HouseModel.objects.filter(market=market)
        all_models.order_by('-date')
        new_ads= all_models[:10]
        context.update({
            'listings':total.total_listings,
            'value':f"{total.total_value:,}",
            'average_sqm_total':f"{round(average.average_price_over_sqm):,}",
            'new_listings':daily_stat.total_listings_dd,
            'new_value':f"{daily_stat.listings_value_dd:,}",
            'new_percent': round(new_percent),
            'new_ads':new_ads,
            'average_price': f"{round(average.average_price):,}",
            'average_sqm': f"{round(average.average_sqm):,}",
            })
        return context

class DashboardPageView(TemplateView):
    template_name="scraper/dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardPageView, self).get_context_data(**kwargs)
        #Get the dailystats
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        #Variables needed:
        total_value = 0
        total_listings = 0
        total_markets=0
        last_day_added=0
        high_price_sqm_market = ''
        high_price_sqm_value = 0
        low_price_sqm_market = ''
        low_price_sqm_value = 10000000
        today = datetime.date.today()
        #Calculations
        totalmodels = TotalModel.objects.all()
        dailystats = DailyStatistic.objects.filter(date=today)
        averagestats = AverageModel.objects.all()
        total_markets = len(totalmodels)

        for model in totalmodels:
            total_value += model.total_value
            total_listings += model.total_listings

        for daily in dailystats:
            last_day_added += daily.listings_value_dd

        for average in averagestats:
            if average.average_price_over_sqm > high_price_sqm_value:
                high_price_sqm_market = average.market
                high_price_sqm_value = average.average_price_over_sqm
        for average in averagestats:
            if average.average_price_over_sqm < high_price_sqm_value:
                low_price_sqm_market = average.market
                low_price_sqm_value = average.average_price_over_sqm

        high_price_sqm_value = round(high_price_sqm_value)
        low_price_sqm_value = round(low_price_sqm_value)
        #Diagnostics variables
        try:
            daily_scan = DailyScan.objects.get(date=today)
        except DailyScan.DoesNotExist:
            daily_scan = DailyScan.objects.get(date=yesterday)
        not_populated = daily_scan.ads_searched - daily_scan.populated_count

        error_listings = ErrorListings.objects.filter(date=today)
        if len(error_listings)==0:
            error_listings = ErrorListings.objects.filter(date=yesterday)
        error_listings = error_listings[:10]



        context.update({
            'value': f"{total_value:,}",
            'listings': total_listings,
            'markets': total_markets,
            'last_day': f"{last_day_added:,}",
            'high_price_sqm_market': high_price_sqm_market,
            'high_price_sqm_value': f"{high_price_sqm_value:,}",
            'low_price_sqm_market': low_price_sqm_market,
            'low_price_sqm_value': f"{low_price_sqm_value:,}",
            'daily_scan': daily_scan,
            'not_populated': not_populated,
            'error_listings': error_listings,
            })
        return context

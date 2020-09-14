import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate.settings")
django.setup()

#Imports
import requests
from bs4 import BeautifulSoup as BS
from unidecode import unidecode
from datetime import date,timedelta

#Import validators
from scraper.validators import (vali_only_one_price,vali_house_object)
from django.db import IntegrityError
#Import functionality functions
from scraper.scraper_functions import (find_house_information,find_links_to_ads,
soup_object,populate_housemodel,update_total_model,update_average_model,
update_dailystatistic,update_price_model,
update_dailystatistic_price)
#Import diagnostics functions
from scraper.diagnostic_fucntions import populate_dailyscan,populate_errorlistings
#Import models to be populated
from scraper.models import MarketModel,HouseModel,DailyStatistic


############################ Global variables ##############################
# Market
market_1 = 'Horten'
market_1_link = 'https://www.finn.no/realestate/homes/search.html?filters=&location=0.22038&location=1.22038.20131&published=1'
market_2 = 'Tønsberg'
market_2_link ='https://www.finn.no/realestate/homes/search.html?filters=&location=0.22038&location=1.22038.20133&published=1'
market_3 = 'Holmestrand'
market_3_link = 'https://www.finn.no/realestate/homes/search.html?filters=&location=0.22038&location=1.22038.20132&published=1'
market_4 = 'Sandefjord'
market_4_link = 'https://www.finn.no/realestate/homes/search.html?filters=&location=0.22038&location=1.22038.20134&published=1'
#Variables for calculations
today=date.today()
yesterday = today - timedelta(1)

##### ERROR COUNT #######
complex_error = 0
missing_price_sqm_error = 0
populated_count = 0
ads_searched = 0


market_dict={
    market_1:market_1_link,
    market_2:market_2_link,
    market_3:market_3_link,
    market_4:market_4_link,
    }
################################## SCRIPT ####################################
for market,market_link in market_dict.items():
    print('----------------Searching through: {} ------------'.format(market))
    #Link to all the listings published today
    ads = find_links_to_ads(market_link)
    #For diagnostics
    ads_searched += len(ads)
    #Retrive or create the market models
    market_model,created = MarketModel.objects.get_or_create(district=market)
    dailystat,created = DailyStatistic.objects.get_or_create(market=market_model,date=today)

    #Find listings and update, housemodel, totalmodel, averagemodel
    for apartment in ads:
        soup = soup_object(apartment)
        if vali_only_one_price(soup):
            price_info_dict,house_info_dict= find_house_information(soup)
            if vali_house_object(price_info_dict,house_info_dict):
                print('Passed the house validator -- Populating')
                try:
                    listing = populate_housemodel(market_model,house_info_dict,price_info_dict,apartment)
                except IntegrityError:
                    print('Apartment is already in database')
                    break
                total = update_total_model(market_model,listing)
                average = update_average_model(market_model,total)
                update_dailystatistic(dailystat,listing)
                populated_count += 1
            else:
                print('apartment {} is missing price or sqm'.format(apartment))
                missing_price_sqm_error +=1
                populate_errorlistings(apartment,'apartment is missing price or sqm')
        else:
            print('Apartment: {} is an complex with many apartments'.format(apartment))
            complex_error += 1
            populate_errorlistings(apartment,'Apartment is an complex with many apartments')
    #Update the dailyprice for the market being iterated
    update_price_model(market_model,today)
    update_dailystatistic_price(dailystat,market_model,today,yesterday)
    #End iterations through each market




#### Error diagnostics ####
print('Scraper searched through {}.\n Ads that where populated as model instances: {}\n Ads that was missing price or sqm: {} \n Ads that was apartment complexes: {}'.format(ads_searched,populated_count,missing_price_sqm_error,complex_error))
populate_dailyscan(complex_error,missing_price_sqm_error,populated_count,ads_searched)

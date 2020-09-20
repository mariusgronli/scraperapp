#imports
import requests
from bs4 import BeautifulSoup as BS
from unidecode import unidecode
#Import validators
from scraper.validators import(vali_has_numbers,vali_house_info,vali_price_info)
from django.db import IntegrityError
#import models
from scraper.models import HouseModel,TotalModel,AverageModel,DailyStatistic,PriceModel
from datetime import date,timedelta
#Main functions
def soup_object(url):
    '''
    Takes in an url and makes a soup object
    '''
    page = requests.get(url)
    soup = BS(page.content,'html.parser')
    return soup

def find_house_information(soup):
    ''''''
    #Find all the information
    raw_description = soup.find_all('dt')
    raw_value = soup.find_all('dd')
    #Empty lists used for formating
    description = []
    value = []
    price_info_dict={}
    house_info_dict={}
    #Populating the lists with cleaned information
    for x in raw_description:
        description.append(x.get_text())
    for y in raw_value:
        formated_value = y.get_text()
        cleaned_value = unidecode(formated_value)
        if '\n' in cleaned_value:
            cleaned_value = cleaned_value.splitlines()[1].strip()
        if vali_has_numbers(cleaned_value):
            if 'm2' in cleaned_value:
                cleaned_value = cleaned_value.strip('m2')
                cleaned_value = convert_to_int(cleaned_value)
            elif 'm²' in cleaned_value:
                cleaned_value = cleaned_value.strip('m²')
                cleaned_value = convert_to_int(cleaned_value)
            else:
                cleaned_value = convert_to_int(cleaned_value)
        value.append(cleaned_value)
    #Creating empty dict to populate with formatted and clean values
    information = {}
    information['Prisantydning']= find_price(soup)
    information['Adress'],information['Postnummer']=find_adress(soup)
    information['Bilde']=find_picture_url(soup)
    for x,y in zip(description,value):
        information[x]=y
    #Sort information after validators
    for item in information.items():
        if vali_price_info(item[0]):
            price_info_dict[item[0]]=item[1]
        elif vali_house_info(item[0]):
            house_info_dict[item[0]]=item[1]
    return price_info_dict,house_info_dict

def find_picture_url(soup):
    img = soup.find_all('img',class_="img-format__img u-border-radius-8px")[0]
    url = img['srcset'].split(',')[0].split(' ')[0]
    return url

def find_links_to_ads(link):
    cut='page='
    annonser=[]
    if cut in link:
        string_1= link[:link.index(cut)+len(cut)]
        string_2= link[link.index(cut)+len(cut)+1:]

        for x in range(10):
            search = string_1+str(x)+string_2
            soup = soup_object(search)
            all_objects = soup.find_all('a',class_='ads__unit__link')
            all_objects = all_objects[1:]
            if len(all_objects)!= 0:
                for y in all_objects:
                    ad_link = 'http://finn.no'+y['href']
                    annonser.append(ad_link)
            else:
                print('Did not find more ads, search ended at page: {}'.format(x))
                break
    else:
        soup = soup_object(link)
        all_objects = soup.find_all('a',class_='ads__unit__link')
        all_objects = all_objects[1:]
        for y in all_objects:
            ad_link = 'http://finn.no'+y['href']
            annonser.append(ad_link)

    return annonser

#Supporting functions to main functions

def find_adress(soup):
    '''
    Returns the adress of the apartment
    '''
    try:
        adress = soup.find_all('p',class_='u-caption')[0].get_text()
        zip_code = [int(i) for i in adress.split() if i.isdigit()]
        if len(zip_code)==1:
            zip_code = zip_code[0]
        else:
            zip_code = zip_code[1]
    except IndexError:
        adress = 'NA'
        zip_code = 0
    return adress,zip_code

def find_price(soup):
    '''
    Returns the asking price of the apartment
    '''
    all_objects = soup.find_all('span',class_='u-t3')
    price = ''
    for x in all_objects:
        if 'kr' in x.get_text():
            raw_price = x.get_text()
            price = unidecode(raw_price)
    #Removes white space and \n if in the price
    if '\n' in price:
        price = price.splitlines()[1].strip()
    if price == '':
        price = 'Error in find price function'
        return price
    else:
        price = convert_to_int(price)
        return price

def convert_to_int(string):
    try:
        return int(''.join(filter(str.isdigit, string)))
    except ValueError:
        print('Got an value error on string {}'.format(string))
        string = 0
        return string

#Populating functions
def populate_housemodel(market,house_info_dict,price_info_dict,url):
    # Clean the data
    try:
        adress = house_info_dict['Adress']
    except KeyError:
        adress = 'NA'
    try:
        prisantydning = price_info_dict['Prisantydning']
    except KeyError:
        prisantydning = 0
    try:
        fellesgjeld = price_info_dict['Fellesgjeld']
    except KeyError:
        fellesgjeld = 0
    try:
        omkostninger = price_info_dict['Omkostninger']
    except KeyError:
        omkostninger = 0
    try:
        totalpris = price_info_dict['Totalpris']
    except KeyError:
        totalpris = 0
    try:
        felleskostnader = price_info_dict['Felleskost/mnd.']
    except KeyError:
        felleskostnader = 0
    try:
        boligtype = house_info_dict['Boligtype']
    except KeyError:
        boligtype = 'NA'
    try:
        eieform = house_info_dict['Eieform bolig']
    except KeyError:
        eieform = 'NA'
    try:
        bilde = house_info_dict['Bilde']
    except KeyError:
        bilde = 'NA'
    try:
        soverom = house_info_dict['Soverom']
    except KeyError:
        soverom = 0
    try:
        primærrom = house_info_dict['Primærrom']
    except KeyError:
        primærrom = 0
    try:
        bruksareal = house_info_dict['Bruksareal']
    except KeyError:
        bruksareal = 0
    try:
        grunnflate = house_info_dict['Grunnflate']
    except KeyError:
        grunnflate = 0
    try:
        etasje = house_info_dict['Etasje']
    except KeyError:
        etasje = 0
    try:
        byggeår = house_info_dict['Byggeår']
    except KeyError:
        byggeår = 0
    try:
        rom = house_info_dict['Rom']
    except KeyError:
        rom = 0
    try:
        tomteareal = house_info_dict['Tomteareal']
    except KeyError:
        tomteareal = 0
    try:
        bruttoareal = house_info_dict['Bruttoareal']
    except KeyError:
        bruttoareal = 0
    try:
        areal = house_info_dict['Areal']
    except KeyError:
        areal = 0
    try:
        postnummer = house_info_dict['Postnummer']
    except KeyError:
        postnummer = 0

    #Populate an instance of the model
    listing = HouseModel(
        market = market,
        adress = adress,
        postnummer = postnummer,
        prisantydning = prisantydning,
        fellesgjeld = fellesgjeld,
        omkostninger = omkostninger,
        totalpris = totalpris,
        felleskostnader = felleskostnader,
        boligtype = boligtype,
        eieform = eieform,
        soverom = soverom,
        primærrom = primærrom,
        bruksareal = bruksareal,
        grunnflate = grunnflate,
        etasje = etasje,
        byggeår = byggeår,
        rom = rom,
        tomteareal = tomteareal,
        bruttoareal = bruttoareal,
        areal = areal,
        bilde = bilde,
        url = url
        )
    listing.save()
    return listing

def update_total_model(market,listing):
    model, created = TotalModel.objects.get_or_create(market=market)
    model.total_listings+=1
    model.total_value+=listing.prisantydning
    if listing.bruttoareal >=1:
        model.total_sqm += listing.bruttoareal
    else:
        model.total_sqm += listing.areal
    model.save()
    return model

def update_average_model(market,total):
    model, created = AverageModel.objects.get_or_create(market=market)
    model.average_price = total.total_value/total.total_listings
    model.average_sqm = total.total_sqm/total.total_listings
    try:
        model.average_price_over_sqm = total.total_value/total.total_sqm
    except ZeroDivisionError:
        model.average_price_over_sqm = 0
    model.save()
    return model

def update_dailystatistic(daily_obj,listing):
    '''
    daily_obj = ModelObject for DailyStatistic
    yd_stats = ModelObject for DailyStatistic
    listing = ModelObject for HouseModel
    ---------------------------------------------
    Updates an instance of DailyStatistic
    '''
    daily_obj.listings_value_dd+=listing.prisantydning
    daily_obj.total_listings_dd+=1
    daily_obj.save()

def update_price_model(market,today):
    try:
        avg_model = AverageModel.objects.get(market=market)
    except AverageModel.DoesNotExist:
        avg_model = 'NA'

    if avg_model != 'NA':
        model, created = PriceModel.objects.get_or_create(market=market,date=today)
        model.price = avg_model.average_price_over_sqm
        model.save()

def update_dailystatistic_price(daily_obj,market,today,yesterday):
    #Get yesterday price and today price
    try:
        yesterday_price = PriceModel.objects.get(market=market,date=yesterday)
    except PriceModel.DoesNotExist:
        yesterday_price = 'NA'
    try:
        today_price = PriceModel.objects.get(market=market,date=today)
    except PriceModel.DoesNotExist:
        today_price = 'NA'
    #Populate the price change
    if yesterday_price != 'NA' and today_price != 'NA':
        percent_change = (today_price.price-yesterday_price.price)/yesterday_price.price
        daily_obj.percent_change_dd = round(percent_change,4)
        daily_obj.save()
    else:
        daily_obj.percent_change_dd = 0
        daily_obj.save()

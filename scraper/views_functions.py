#imports
from scraper.models import DailyStatistic,ZipCodeModel,MarketModel
from django.core.paginator import Paginator
#############################################################################
################### Functions for search apps ###############################
#############################################################################

def update_mapping_context(self,data,context):
    market = MarketModel.objects.get(district=data['market'])
    #Generating querysets for each type
    queryset_leilighet = ZipCodeModel.objects.filter(
                                            market=market,
                                            housetype='Leilighet',
                                            ).order_by('-database')[0:5]
    queryset_rekkehus = ZipCodeModel.objects.filter(
                                            market=market,
                                            housetype='Rekkehus',
                                            ).order_by('-database')[0:5]
    queryset_enebolig = ZipCodeModel.objects.filter(
                                            market=market,
                                            housetype='Enebolig',
                                            ).order_by('-database')[0:5]
    queryset_tomannsbolig = ZipCodeModel.objects.filter(
                                            market=market,
                                            housetype='Tomannsbolig',
                                            ).order_by('-database')[0:5]
    #Update context:
    context['leilighet']=queryset_leilighet
    context['rekkehus']=queryset_rekkehus
    context['enebolig']=queryset_enebolig
    context['tomannsbolig']=queryset_tomannsbolig


def update_search_context(queryset,context,data):
    #gloval Variables
    price=0
    sqm=0
    price_over_sqm=0
    searched=0
    #return search variables
    context["market"]=data['market']
    context["zipcode"]=data['zipcode']
    context["type"]=data['type']

    #Populate variables
    if len(queryset)>0:
        for ad in queryset:
            price += ad.prisantydning
            sqm += ad.bruttoareal
            searched +=1
        context["price"] = f"{round((price/searched)):,}"
        context["sqm"] = round(sqm/searched)
        context["price_over_sqm"]=f"{round((price/sqm)):,}"
        context["searched"]=searched
        context["search_bol"]=True
        context["quaryset"]=queryset[0:10]

    else:
        context["search_bol"]=False

def update_price_calculator_context(queryset,context,data):
    #Global variables
    price=0
    sqm=0
    price_over_sqm=0
    searched=0
    estimated_price = 0
    context["market"]=data['market']
    context["zipcode"]=data['zipcode']
    context["type"]=data['type']
    context["bruttoareal"]=data['bruttoareal']
    #Populate variables
    if len(queryset)>0:
        for ad in queryset:
            price += ad.prisantydning
            sqm += ad.bruttoareal
            searched +=1
        context["price"] = f"{round((price/searched)):,}"
        context["sqm"] = round(sqm/searched)
        context["price_over_sqm"]=f"{round((price/sqm)):,}"
        context["searched"]=searched
        context["estimated_price"]= f"{round((price/sqm)*data['bruttoareal']):,}"
        context["search_bol"]=True
        context["quaryset"]=queryset[0:10]
    else:
        context["search_bol"]=False

def populate_price_change_graph(market):
    """
    Returns the data and labels for the price graph in market detail.
    Market : MarketModel object
    """
    data = list()
    labels = list()

    queryset = DailyStatistic.objects.filter(market=market).order_by('-date')[:10]

    for stat in queryset:
        try:
            data.append(round(stat.percent_change_dd*100))
            labels.append("{}.{}".format(stat.date.day,stat.date.month))
        except TypeError:
            data.append(0)
            data.append('No data')


    data.reverse()
    labels.reverse()

    return data,labels

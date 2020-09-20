#imports

#############################################################################
################### Functions for search apps ###############################
#############################################################################

def update_search_context(queryset,context,data):
    #gloval Variables
    price=0
    sqm=0
    price_over_sqm=0
    searched=0
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
    else:
        error='Could not find any listings on zipscode {}. Please try another'.format(data['zipcode'])
        context["error"]=error
        context["search_bol"]=False

def update_price_calculator_context(queryset,context,data):
    #Global variables
    price=0
    sqm=0
    price_over_sqm=0
    searched=0
    estimated_price = 0
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
    else:
        if data['zipcode'] is None:
            error='Could not find any listings in {}. Please try another'.format(data['market'])
        else:
            error='Could not find any listings in {} with Zipcode: {}. Please try another'.format(data['market'],data['zipcode'])
        context["error"]=error
        context["search_bol"]=False

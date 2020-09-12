#Imports
import requests
from bs4 import BeautifulSoup as BS
from unidecode import unidecode

def vali_only_one_price(soup_item):
    '''
    Check if its only one or more prices.
    If its two prices it means its apartment complex that is not done yet
    '''
    check = 0
    for item in soup_item.find_all('span',class_='u-t3'):
        if 'kr' in unidecode(item.get_text()):
            check= check + 1
    if check <= 1:
        return True
    else:
        return False

def vali_price_info(item):
    '''
    Checks if an item is inside the price information we are looking for.
    Returns True if is. Else it returns False.
    '''
    price_info = ['Prisantydning','Fellesgjeld','Omkostninger','Totalpris','Felleskost/mnd.']
    if item in price_info:
        return True
    else:
        return False

def vali_house_info(item):
    '''
    checks if an item is inside the house information we are looking for.
    Returns True if it is. Else it returns False
    '''
    house_info = [
        'Adress','Boligtype','Eieform bolig','Soverom','Primærrom','Bruksareal',
        'Grunnflate','Etasje','Byggeår','Rom',
        'Tomteareal','Bruttoareal','Areal','Postnummer','Bilde']
    if item in house_info:
        return True
    else:
        return False

def vali_has_numbers(string):
    '''
    Checks wheter a string contains numbers. Returns True if there is numbers in string, or False otherwise
    '''
    return any(char.isdigit() for char in string)

def vali_house_object(price_info_dict,house_info_dict):
    errors=0
    if type(price_info_dict['Prisantydning']) != int:
        errors+=1
        print('Prisantydning is not int')
    try:
        if house_info_dict['Bruttoareal']==0:
            errors+=1
            print('Bruttoareal = 0')
    except KeyError:
        errors+=1
        print('Bruttoareal does not exist')
    if errors == 0:
        return True
    else:
        return False

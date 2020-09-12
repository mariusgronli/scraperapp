from scraper.models import ErrorListings,DailyScan
from datetime import datetime

def populate_dailyscan(error_complex,error_price,populated,searched):
    scan = DailyScan(
        error_complex = error_complex,
        error_price_sqm = error_price,
        populated_count = populated,
        ads_searched = searched,
        )
    scan.save()

def populate_errorlistings(url,error_message):
    error = ErrorListings(
        listing=url,
        error_message = error_message,
        )
    error.save()

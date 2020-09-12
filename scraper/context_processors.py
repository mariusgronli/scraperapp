from scraper.models import MarketModel

def get_list_of_markets(request):
    all_markets = MarketModel.objects.all()
    return {
        'all_markets':all_markets,
    }

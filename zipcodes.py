import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate.settings")
django.setup()

#Imports
from scraper.models import HouseModel,ZipCodeModel

queryset = HouseModel.objects.all()

for ad in queryset:
    zip,created = ZipCodeModel.objects.get_or_create(
                                        market=ad.market,
                                        housetype=ad.boligtype,
                                        zipcode=ad.postnummer,
                                        )
    if created:
        print('Created: {}'.format(zip))
    else:
        zip.add_entry()
        print('Added entry for {}'.format(zip))
    zip.save()
    print("-------------------------------------")

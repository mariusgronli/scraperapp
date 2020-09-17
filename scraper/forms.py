from django import forms

class PostcodeSearchForm(forms.Form):

    CHOICES_MARKET = (
       ('Horten', 'Horten'),
       ('Sandefjord', 'Sandefjord'),
       ('Holmestrand', 'Holmestrand'),
       ('Tønsberg','Tønsberg'),
    )
    CHOICES_TYPE = (
        ('Enebolig', 'Enebolig'),
        ('Rekkehus', 'Rekkehus'),
        ('Leilighet', 'Leilighet'),
        ('Tomannsbolig','Tomannsbolig'),
        )
    market = forms.ChoiceField(choices=CHOICES_MARKET)
    zipcode = forms.IntegerField(max_value=9999)
    type = forms.ChoiceField(choices=CHOICES_TYPE)

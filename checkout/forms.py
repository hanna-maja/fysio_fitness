from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode',)
    password = forms.CharField(label='Lösenord', widget=forms.PasswordInput(attrs={'placeholder': 'ange lösenord'}))

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'För och efternamn',
            'email': 'Email',
            'phone_number': 'Mobilnummer',
            'postcode': 'Postnummer',
            'town_or_city': 'Postadress',
            'street_address1': 'Gata och nummer',
            'street_address2': 'c/o',
            'password':'Lösenord',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

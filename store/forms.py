from django import forms
from localflavor.us.forms import USStateSelect


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('CC', 'Credit Card'),
    ('IN', 'Invoice')
)


class CheckOutForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '(123) 456-7890'
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '123 Main St.'
    }))
    suite_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Suite #1'
    }))
    state = forms.CharField(widget=USStateSelect(attrs={
        'class': 'form-control'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control"
    }))
    delivery_date = forms.DateField(widget=forms.SelectDateWidget())
    same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

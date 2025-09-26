from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Product

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','price','image']

        
class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16, min_length=16)
    expiry_month = forms.ChoiceField(label='Expiry Month', choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)])
    expiry_year = forms.ChoiceField(label='Expiry Year', choices=[(str(i), str(i)) for i in range(2025, 2035)])
    cvv = forms.CharField(label='CVV', max_length=3, min_length=3)
    cardholder_name = forms.CharField(label='Cardholder Name', max_length=100)
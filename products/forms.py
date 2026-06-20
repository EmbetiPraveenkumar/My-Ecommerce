from django import forms
from django.forms import ModelForm
from .models import Order
# class CheckoutForm(forms.Form):
#     customer_name = forms.CharField(max_length = 100)
#     phone = forms.CharField(max_length=15)
#     address = forms.CharField(widget=forms.Textarea)
    

from django import forms

class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password'
            }
        )
    )



class OrderForm(ModelForm):

    class Meta:

        model = Order

        fields = [
            'name',
            'phone',
            'address'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your full name'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter delivery address',
                    'rows': 4
                }
            )

        }
        

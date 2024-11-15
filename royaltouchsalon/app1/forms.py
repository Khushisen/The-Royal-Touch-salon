from django import forms
from .models import Contact, Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','message']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'your name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'your email'}),
            'message':forms.Textarea(attrs={'class':'form-control','placeholder':'your message'})

        }
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user_name','phone_number','email','address']
        widgets = {
            'address' : forms.Textarea(attrs={'rows':3}),
        }
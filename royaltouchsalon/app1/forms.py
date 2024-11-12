from django import forms
from .models import Contact

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255)
    postal_code = forms.CharField(max_length=10)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','message']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'your name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'your email'}),
            'message':forms.Textarea(attrs={'class':'form-control','placeholder':'your message'})

        }
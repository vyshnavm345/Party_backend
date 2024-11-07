from django import forms


class UserDeleteForm(forms.Form):
    contact_info = forms.CharField(label="Email or Phone", max_length=100)

# forms.py
from django import forms


class UserDeleteForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)

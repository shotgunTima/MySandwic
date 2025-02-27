
from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from myapp.models import *

class RawmaterialsForm(forms.ModelForm):
    class Meta:
        model = Rawmaterials
        exclude = ['quantity', 'totalamount']

class FinishedgoodsForm(forms.ModelForm):
    class Meta:
        model = Finishedgoods
        exclude = ['quantity', 'totalamount']

class UnitsForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = '__all__'

from django import forms
from .models import Ingredients


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['productid', 'rawmaterialid', 'quantity']

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        if product_id:
            self.fields['productid'].initial = product_id
            self.fields['productid'].widget.attrs['readonly'] = True

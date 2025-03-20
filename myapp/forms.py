
from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from myapp.models import *

class RawmaterialsForm(forms.ModelForm):
    totalamount = forms.DecimalField(label="Общая сумма", initial=0)
    quantity = forms.IntegerField(label="Количество", initial=0)
    class Meta:
        model = Rawmaterials
        fields = ['name', 'quantity', 'totalamount', 'unitid']
        labels = {
            'name': 'Название сырья',
            'quantity': 'Количество',
            'totalamount': 'Общая сумма',
            'unitid': 'Единица измерения'
        }

class FinishedgoodsForm(forms.ModelForm):
    class Meta:
        model = Finishedgoods
        exclude = ['quantity', 'totalamount']
        fields = ['name', 'unitid']
        labels = {
            'name': 'Название',
            'unitid': 'Единица измерения',
        }

class UnitsForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = '__all__'
        labels = {
            'unitname': 'Название единицы измерения',
        }

from django import forms
from .models import Ingredients


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['productid', 'rawmaterialid', 'quantity']
        labels = {
            'productid': 'Продукт',
            'rawmaterialid': 'Сырьё',
            'quantity': 'Количество',
        }

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)
        if product_id:
            self.fields['productid'].initial = product_id
            self.fields['productid'].widget.attrs['readonly'] = True




from .models import Rawmaterialpurchases, Rawmaterials, Employees, Budget
from django import forms
from django.utils.timezone import now

class RawMaterialPurchaseForm(forms.ModelForm):
    totalamount = forms.DecimalField(initial=0, label="Общая сумма")
    quantity = forms.IntegerField(initial=0, label="Количество")
    purchasedate = forms.DateField(
        initial=now,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата закупки"  # Добавлен label
    )

    class Meta:
        model = Rawmaterialpurchases
        fields = ['rawmaterialid', 'quantity', 'totalamount', 'purchasedate', 'employeeid']
        labels = {
            'rawmaterialid': 'Сырьё',
            'employeeid': 'Сотрудник'
        }
        widgets = {
            'purchasedate': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import Employees

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['fullname', 'salary', 'address', 'phone']
        labels = {
            'fullname': 'ФИО сотрудника',
            'salary': 'Зарплата',
            'address': 'Адрес',
            'phone': 'Номер телефона',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom widget attributes for form fields
        self.fields['fullname'].widget.attrs.update({'class': 'form-control'})
        self.fields['salary'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['positionid'].widget.attrs.update({'class': 'form-control'})

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['totalamount']

    widgets = {
        'totalamount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    }

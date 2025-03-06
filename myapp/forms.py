
from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from myapp.models import *

class RawmaterialsForm(forms.ModelForm):
    class Meta:
        model = Rawmaterials
        exclude = ['quantity', 'totalamount']
        fields = ['name', 'unitid']
        labels = {
            'name': 'Название',
            'unitid': 'Единица измерения',
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



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Rawmaterialpurchases, Rawmaterials, Employees, Budget
from django import forms


class RawmaterialPurchaseForm(forms.ModelForm):
    class Meta:
        model = Rawmaterialpurchases
        fields = ['rawmaterialid', 'quantity', 'totalamount', 'purchasedate', 'employeeid']
        labels = {

            'rawmaterialid': 'Сырьё',
            'quantity': 'Количество',
            'totalamount': 'Общая сумма',
            'purchasedate': 'Дата закупки',
            'employeeid': 'Сотрудник'
        }
        widgets = {
            'purchasedate': forms.DateInput(attrs={'type': 'date'}),
        }


def purchase_raw_material(request):
    if request.method == "POST":
        form = RawmaterialPurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            raw_material = purchase.rawmaterialid
            budget = Budget.objects.first()  # Предполагаем, что бюджет один

            # Расчет стоимости
            purchase.totalamount = purchase.quantity * raw_material.unit_price

            if budget.totalamount < purchase.totalamount:
                messages.error(request, "Недостаточно средств в бюджете для этой закупки!")
            else:
                # Обновляем бюджет
                budget.totalamount -= purchase.totalamount
                budget.save()

                # Обновляем данные сырья
                raw_material.quantity += purchase.quantity
                raw_material.totalamount += purchase.totalamount
                raw_material.save()

                # Сохраняем закупку
                purchase.save()
                messages.success(request, "Закупка успешно добавлена!")
                return redirect('raw_materials_list')
    else:
        form = RawmaterialPurchaseForm()

    return render(request, 'myapp/purchase_form.html', {'form': form})

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
        fields = ['totalamount']  # Только поле totalamount

    widgets = {
        'totalamount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    }

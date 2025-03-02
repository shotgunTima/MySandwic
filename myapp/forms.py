from django import forms
from myapp.models import Rawmaterials, Finishedgoods, Units, Ingredients
from django.core.exceptions import ValidationError


# Форма для сырья
class RawmaterialsForm(forms.ModelForm):
    class Meta:
        model = Rawmaterials
        exclude = ['totalamount']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Расчет общей суммы
        if instance.unit_price and instance.quantity:
            instance.totalamount = instance.unit_price * instance.quantity
        if commit:
            instance.save()
        return instance


# Форма для готовой продукции
class FinishedgoodsForm(forms.ModelForm):
    class Meta:
        model = Finishedgoods
        exclude = ['totalamount']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Расчет общей суммы
        if instance.unit_price and instance.quantity:
            instance.totalamount = instance.unit_price * instance.quantity
        if commit:
            instance.save()
        return instance


# Форма для единиц измерения
class UnitsForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = '__all__'

# Форма для ингредиентов
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
        # Вы можете также добавить custom validation для quantity, если нужно
        self.fields['quantity'].widget.attrs.update({'min': 1})

    # Пример валидации для quantity (можно изменить по необходимости)
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise ValidationError("Количество должно быть больше 0.")
        return quantity

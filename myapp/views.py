from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from myapp.models import *
from myapp.forms import *
import datetime

def home_page(request):
    return render(request, 'myapp/mainPage.html')




def raw_materials_list(request):
    rawmaterials = Rawmaterials.objects.all()
    return render(request, 'myapp/rawmaterials_list.html', {'rawmaterials': rawmaterials})


def raw_material_create(request):
    if request.method == "POST":
        form = RawmaterialsForm(request.POST)
        if form.is_valid():
            rawmaterial = form.save(commit=False)
            rawmaterial.quantity = 0  # Устанавливаем начальное количество
            rawmaterial.totalamount = 0  # Устанавливаем начальную сумму
            form.save()
            return redirect('myapp:rawmaterials_list')  # Перенаправление на список сырья
    else:
        form = RawmaterialsForm()

    return render(request, 'myapp/rawmaterial_form.html', {'form': form})


def raw_material_update(request, pk):
    rawmaterial = get_object_or_404(Rawmaterials, pk=pk)
    if request.method == "POST":
        form = RawmaterialsForm(request.POST, instance=rawmaterial)
        if form.is_valid():
            form.save()
            return redirect('myapp:rawmaterials_list')
    else:
        form = RawmaterialsForm(instance=rawmaterial)
    return render(request, 'myapp/rawmaterial_form.html', {'form': form})


def raw_material_delete(request, pk):
    rawmaterial = get_object_or_404(Rawmaterials, pk=pk)
    if request.method == "POST":
        rawmaterial.delete()
        return redirect('rawmaterials_list')
    return render(request, 'myapp/rawmaterial_confirm_delete.html', {'rawmaterial': rawmaterial})



def finished_goods_list(request):
    finishedgoods = Finishedgoods.objects.all()
    return render(request, 'myapp/finishedgoods_list.html', {'finishedgoods': finishedgoods})


def finished_goods_create(request):
    if request.method == "POST":
        form = FinishedgoodsForm(request.POST)
        if form.is_valid():
            good = form.save(commit=False)
            good.quantity = 0
            good.totalamount = 0
            good.save()
            return redirect('myapp:finishedgoods_list')
    else:
        form = FinishedgoodsForm()
    return render(request, 'myapp/finishedgoods_form.html', {'form': form})


def finished_goods_update(request, pk):
    finishedgood = get_object_or_404(Finishedgoods, pk=pk)
    if request.method == "POST":
        form = FinishedgoodsForm(request.POST, instance=finishedgood)
        if form.is_valid():
            form.save()
            return redirect('myapp:finishedgoods_list')
    else:
        form = FinishedgoodsForm(instance=finishedgood)
    return render(request, 'myapp/finishedgoods_form.html', {'form': form})


def finished_goods_delete(request, pk):
    finishedgood = get_object_or_404(Finishedgoods, pk=pk)
    if request.method == "POST":
        finishedgood.delete()
        return redirect('myapp:finishedgoods_list')
    return render(request, 'myapp/finishedgoods_confirm_delete.html', {'finishedgood': finishedgood})


def unit_list(request):
    units = Units.objects.all()
    return render(request, 'myapp/units_list.html', {'units': units})

def unit_create(request):
    if request.method == "POST":
        form = UnitsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:units_list')
    else:
        form = UnitsForm()
    return render(request, 'myapp/unit_form.html', {'form': form})


def unit_update(request, pk):
    unit = get_object_or_404(Units, pk=pk)
    if request.method == "POST":
        form = UnitsForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('myapp:units_list')
    else:
        form = UnitsForm(instance=unit)
    return render(request, 'myapp/unit_form.html', {'form': form})


def unit_delete(request, pk):
    unit = get_object_or_404(Units, pk=pk)
    if request.method == "POST":
        unit.delete()
        return redirect('myapp:units_list')
    return render(request, 'myapp/unit_confirm_delete.html', {'unit': unit})


def ingredient_list(request):
    ingredients = Ingredients.objects.all()
    return render(request, 'myapp/ingredients_list.html', {'ingredients': ingredients})


from django.core.exceptions import ValidationError


def ingredient_create(request, product_id):
    product = get_object_or_404(Finishedgoods, pk=product_id)

    if request.method == "POST":
        form = IngredientsForm(request.POST, product_id=product_id)

        if form.is_valid():
            raw_material = form.cleaned_data['rawmaterialid']

            # Проверка на существование ингредиента
            if Ingredients.objects.filter(productid=product, rawmaterialid=raw_material).exists():
                messages.error(request, 'Этот ингредиент уже добавлен для данного продукта.')
            else:
                form.save()
                return redirect('myapp:product_ingredients', product_id=product_id)
        else:
            # Добавьте отладочный вывод ошибок формы
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме. Возможно этот ингредиент уже существует')

    else:
        form = IngredientsForm(product_id=product_id)

    return render(request, 'myapp/ingredient_form.html', {'form': form, 'product': product})


def ingredient_update(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    product = ingredient.productid  # Получаем связанный продукт
    product_id = product.productid

    if request.method == "POST":
        form = IngredientsForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('myapp:product_ingredients', product_id=product_id)
    else:
        form = IngredientsForm(instance=ingredient)

    return render(request, 'myapp/ingredient_form.html', {'form': form, 'product': product})



def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    product = ingredient.productid  # Получаем связанный продукт
    product_id = product.productid
    if request.method == "POST":
        ingredient.delete()
        return redirect('myapp:product_ingredients', product_id=product_id)
    return render(request, 'myapp/ingredient_confirm_delete.html', {'ingredient': ingredient})


def product_ingredients(request, product_id):
    product = get_object_or_404(Finishedgoods, pk=product_id)
    ingredients = Ingredients.objects.filter(productid=product)
    return render(request, 'myapp/product_ingredients.html', {'product': product, 'ingredients': ingredients})

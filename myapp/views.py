from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from myapp.models import *
from myapp.forms import *

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
            rawmaterial.quantity = 0
            rawmaterial.totalamount = 0
            if rawmaterial.unit_price is None:
                rawmaterial.unit_price = 0
            rawmaterial.save()
            return redirect('rawmaterials_list')
    else:
        form = RawmaterialsForm()
    return render(request, 'myapp/rawmaterial_form.html', {'form': form})

def raw_material_update(request, pk):
    rawmaterial = get_object_or_404(Rawmaterials, pk=pk)
    if request.method == "POST":
        form = RawmaterialsForm(request.POST, instance=rawmaterial)
        if form.is_valid():
            form.save()
            return redirect('rawmaterials_list')
    else:
        form = RawmaterialsForm(instance=rawmaterial)
    return render(request, 'myapp/rawmaterial_form.html', {'form': form, 'rawmaterial': rawmaterial})  # <-- Добавляем rawmaterial

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
            if good.unit_price is None:
                good.unit_price = 0
            good.save()
            return redirect('finishedgoods_list')
    else:
        form = FinishedgoodsForm()
    return render(request, 'myapp/finishedgoods_form.html', {'form': form})


def finished_goods_update(request, pk):
    finishedgood = get_object_or_404(Finishedgoods, pk=pk)
    if request.method == "POST":
        form = FinishedgoodsForm(request.POST, instance=finishedgood)
        if form.is_valid():
            form.save()
            return redirect('finishedgoods_list')
    else:
        form = FinishedgoodsForm(instance=finishedgood)
    return render(request, 'myapp/finishedgoods_form.html', {'form': form})

def finished_goods_delete(request, pk):
    finishedgood = get_object_or_404(Finishedgoods, pk=pk)
    if request.method == "POST":
        finishedgood.delete()
        return redirect('finishedgoods_list')
    return render(request, 'myapp/finishedgoods_confirm_delete.html', {'finishedgood': finishedgood})

def unit_list(request):
    units = Units.objects.all()
    return render(request, 'myapp/units_list.html', {'units': units})

def unit_create(request):
    if request.method == "POST":
        form = UnitsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('units_list')
    else:
        form = UnitsForm()
    return render(request, 'myapp/unit_form.html', {'form': form})

def unit_update(request, pk):
    unit = get_object_or_404(Units, pk=pk)
    if request.method == "POST":
        form = UnitsForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('units_list')
    else:
        form = UnitsForm(instance=unit)
    return render(request, 'myapp/unit_form.html', {'form': form})

def unit_delete(request, pk):
    unit = get_object_or_404(Units, pk=pk)
    if request.method == "POST":
        unit.delete()
        return redirect('units_list')
    return render(request, 'myapp/unit_confirm_delete.html', {'unit': unit})

from itertools import groupby
from django.shortcuts import render
from .models import Ingredients

from django.shortcuts import render
from itertools import groupby
from .models import Ingredients, Finishedgoods


def ingredient_list(request):
    selected_product_id = request.GET.get("product")

    ingredients = Ingredients.objects.select_related("productid", "rawmaterialid").order_by("productid")

    if selected_product_id:
        ingredients = ingredients.filter(productid=selected_product_id)

    grouped_ingredients = {}
    for product, items in groupby(ingredients, key=lambda x: x.productid):
        grouped_ingredients[product] = list(items)

    products = Finishedgoods.objects.all()

    return render(request, 'myapp/ingredients_list.html', {
        'grouped_ingredients': grouped_ingredients,
        'products': products,
        'selected_product': selected_product_id
    })


from django.urls import reverse
from django.shortcuts import redirect

def ingredient_create(request, product_id):
    product = get_object_or_404(Finishedgoods, pk=product_id)

    if request.method == "POST":
        form = IngredientsForm(request.POST, product_id=product_id)
        if form.is_valid():
            raw_material = form.cleaned_data['rawmaterialid']
            raw_material.product_id = product_id

            if Ingredients.objects.filter(productid=product, rawmaterialid=raw_material).exists():
                messages.error(request, 'Ingredients with this Productid and Rawmaterialid already exists.')
            else:
                form.save()
                return redirect(f"{reverse('ingredients_list')}?product={product_id}")

        else:
            messages.error(request, 'В форме есть ошибки, исправь.')

    else:
        form = IngredientsForm(product_id=product_id)

    return render(request, 'myapp/ingredient_form.html', {'form': form, 'product': product})

def ingredient_update(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    product_id = ingredient.productid.productid

    if request.method == "POST":
        form = IngredientsForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('ingredients_list')}?product={product_id}")  # ✅ Перенаправляем с product_id
    else:
        form = IngredientsForm(instance=ingredient)

    return render(request, 'myapp/ingredient_form.html', {'form': form, 'product': ingredient.productid})

def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredients, pk=pk)
    product_id = ingredient.productid.productid

    if request.method == "POST":
        ingredient.delete()
        return redirect(f"{reverse('ingredients_list')}?product={product_id}")  # ✅ Перенаправляем с product_id
    return render(request, 'myapp/ingredient_confirm_delete.html', {'ingredient': ingredient})

def product_ingredients(request, product_id):
    product = get_object_or_404(Finishedgoods, pk=product_id)
    ingredients = Ingredients.objects.filter(productid=product)
    return render(request, 'myapp/product_ingredients.html', {'product': product, 'ingredients': ingredients})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Rawmaterialpurchases, Rawmaterials, Budget
from .forms import RawmaterialPurchaseForm

def purchase_raw_material(request):
    budget = get_object_or_404(Budget, pk=1)  # Assuming there is only one budget

    if request.method == 'POST':
        form = RawmaterialPurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            raw_material = purchase.rawmaterialid

            # Calculate total cost of the purchase
            purchase.totalamount = purchase.quantity * raw_material.unit_price

            if budget.totalamount < purchase.totalamount:
                messages.error(request, "Недостаточно средств в бюджете для этой закупки!")
            else:
                # Update the budget
                budget.totalamount -= purchase.totalamount
                budget.save()

                # Update raw material quantity and total cost
                raw_material.quantity += purchase.quantity
                raw_material.totalamount += purchase.totalamount
                raw_material.save()

                # Save the purchase
                purchase.save()
                messages.success(request, "Закупка успешно добавлена!")
                return redirect('rawmaterials_list')
    else:
        form = RawmaterialPurchaseForm()

    return render(request, 'myapp/purchase_form.html', {'form': form, 'budget': budget})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Employees, Positions, Budget, Rawmaterials, Rawmaterialpurchases
from .forms import EmployeeForm, RawmaterialPurchaseForm
from django.db import transaction
from django.contrib import messages


def employee_list(request):
    employees = Employees.objects.all()
    return render(request, 'myapp/employee_list.html', {'employees': employees})


def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'myapp/employee_form.html', {'form': form})


def employee_update(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'myapp/employee_form.html', {'form': form})


def employee_delete(request, pk):
    employee = get_object_or_404(Employees, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect('employee_list')
    return render(request, 'myapp/employee_confirm_delete.html', {'employee': employee})


def budget_edit(request):
    try:
        # Попытаться получить существующий бюджет, или создать новый
        budget = Budget.objects.first()  # Получаем первый бюджет в базе
        if not budget:
            # Если бюджета нет, создаем новый
            budget = Budget.objects.create(totalamount=0)
    except Budget.DoesNotExist:
        # Если нет записи о бюджете, создаем новую
        budget = Budget.objects.create(totalamount=0)

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_edit')  # Перенаправление на страницу редактирования
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'myapp/budget_form.html', {'form': form})

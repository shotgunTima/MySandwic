
from django.db import models


class Budget(models.Model):
    budgetid = models.AutoField(db_column='BudgetID', primary_key=True)
    totalamount = models.FloatField(db_column='TotalAmount')

    class Meta:
        db_table = 'Budget'


class Employees(models.Model):
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)
    fullname = models.CharField(db_column='FullName', max_length=100)
    positionid = models.ForeignKey('Positions', on_delete=models.CASCADE, db_column='PositionID')  # Каскадное удаление
    salary = models.FloatField(db_column='Salary')
    address = models.CharField(db_column='Address', max_length=200, blank=True, null=True)
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Employees'

    def __str__(self):
        return self.fullname


class Finishedgoods(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    unitid = models.ForeignKey('Units', on_delete=models.CASCADE, db_column='UnitID')  # Каскадное удаление
    unit_price = models.FloatField(db_column='UnitPrice')
    quantity = models.FloatField(db_column='Quantity')
    totalamount = models.FloatField(db_column='TotalAmount')

    class Meta:
        db_table = 'FinishedGoods'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    ingredientid = models.AutoField(db_column='IngredientID', primary_key=True)
    productid = models.ForeignKey(Finishedgoods, on_delete=models.CASCADE, db_column='ProductID')
    rawmaterialid = models.ForeignKey('Rawmaterials', on_delete=models.CASCADE, db_column='RawMaterialID')
    quantity = models.FloatField(db_column='Quantity')

    class Meta:
        db_table = 'Ingredients'
        unique_together = ('productid', 'rawmaterialid')

    def __str__(self):
        return f"{self.rawmaterialid.name} для {self.productid.name}"


class Positions(models.Model):
    positionid = models.AutoField(db_column='PositionID', primary_key=True)
    positionname = models.CharField(db_column='PositionName', max_length=50)

    class Meta:
        db_table = 'Positions'

    def __str__(self):
        return self.positionname


class Productproduction(models.Model):
    productionid = models.AutoField(db_column='ProductionID', primary_key=True)
    productid = models.ForeignKey(Finishedgoods, on_delete=models.CASCADE, db_column='ProductID')
    quantity = models.FloatField(db_column='Quantity')
    productiondate = models.DateField(db_column='ProductionDate')
    employeeid = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='EmployeeID')

    class Meta:
        db_table = 'ProductProduction'


class Productsales(models.Model):
    saleid = models.AutoField(db_column='SaleID', primary_key=True)
    productid = models.ForeignKey(Finishedgoods, on_delete=models.CASCADE, db_column='ProductID')
    quantity = models.FloatField(db_column='Quantity')
    totalamount = models.FloatField(db_column='TotalAmount')
    saledate = models.DateField(db_column='SaleDate')
    employeeid = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='EmployeeID')

    class Meta:
        db_table = 'ProductSales'


class Rawmaterialpurchases(models.Model):
    purchaseid = models.AutoField(db_column='PurchaseID', primary_key=True)
    rawmaterialid = models.ForeignKey('Rawmaterials', on_delete=models.CASCADE, db_column='RawMaterialID')
    quantity = models.FloatField(db_column='Quantity')
    totalamount = models.FloatField(db_column='TotalAmount')
    purchasedate = models.DateField(db_column='PurchaseDate')
    employeeid = models.ForeignKey(Employees, on_delete=models.CASCADE, db_column='EmployeeID')

    class Meta:
        db_table = 'RawMaterialPurchases'



class Rawmaterials(models.Model):
    rawmaterialid = models.AutoField(db_column='RawMaterialID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    unitid = models.ForeignKey('Units', on_delete=models.CASCADE, db_column='UnitID')
    unit_price = models.FloatField(db_column='UnitPrice')
    quantity = models.FloatField(db_column='Quantity')
    totalamount = models.FloatField(db_column='TotalAmount')

    class Meta:
        db_table = 'RawMaterials'

    def __str__(self):
        return self.name


class Units(models.Model):
    unitid = models.AutoField(db_column='UnitID', primary_key=True)
    unitname = models.CharField(db_column='UnitName', max_length=50)

    class Meta:
        db_table = 'Units'

    def __str__(self):
        return self.unitname

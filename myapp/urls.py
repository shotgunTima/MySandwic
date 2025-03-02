
from django.urls import path, include
from myapp.views import *

app_name = 'myapp'

urlpatterns = [

    path('', home_page, name='home'),


    # Raw Materials
    path('rawmaterials/', raw_materials_list, name='rawmaterials_list'),
    path('rawmaterials/create/', raw_material_create, name='raw_material_create'),
    path('rawmaterials/<int:pk>/edit/', raw_material_update, name='raw_material_update'),
    path('rawmaterials/<int:pk>/delete/', raw_material_delete, name='raw_material_delete'),

    # Finished Goods
    path('finishedgoods/', finished_goods_list, name='finishedgoods_list'),
    path('finishedgoods/create/', finished_goods_create, name='finished_goods_create'),
    path('finishedgoods/<int:pk>/edit/', finished_goods_update, name='finished_goods_update'),
    path('finishedgoods/<int:pk>/delete/', finished_goods_delete, name='finished_goods_delete'),

    # Units
    path('units/', unit_list, name='units_list'),
    path('units/create/', unit_create, name='unit_create'),
    path('units/<int:pk>/edit/', unit_update, name='unit_update'),
    path('units/<int:pk>/delete/', unit_delete, name='unit_delete'),

    path('ingredients/', ingredient_list, name='ingredients_list'),
    path('ingredient/create/<int:product_id>/', ingredient_create, name='ingredient_create'),
    path('ingredients/<int:pk>/update/', ingredient_update, name='ingredient_update'),
    path('ingredients/<int:pk>/delete/', ingredient_delete, name='ingredient_delete'),
    path('product/<int:product_id>/ingredients/', product_ingredients, name='product_ingredients'),
]
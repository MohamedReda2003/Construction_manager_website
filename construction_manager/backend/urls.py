from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('materials/', views.materials, name='materials'),
    path('inventory/', views.inventory, name='inventory'),
    path('movement/', views.movement, name='movement'),
    path('api/add_construction_site/', views.add_construction_site, name='add_construction_site'),
    path('api/delete_construction_site/<int:site_id>/', views.delete_construction_site, name='delete_construction_site'),
    path('api/add_material/', views.add_material, name='add_material'),
    path('api/get_materials_for_site/<int:site_id>/', views.get_materials_for_site, name='get_materials_for_site'),
    path('api/get_material_quantity/<int:site_id>/<int:material_id>/', views.get_material_quantity, name='get_material_quantity'),
    path('api/move_material/', views.move_material, name='move_material'),
    path('api/delete_material/<int:material_id>/', views.delete_material, name='delete_material'),
]

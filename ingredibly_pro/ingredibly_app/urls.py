from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('fill_product_table/',views.fill_product_table,name="fill_product_table"),
    path('scan_product/',views.scan_product,name="scan_product"),
    path('fill_ingredient_table/',views.fill_ingredient_table,name="fill_ingredient_table"),
    path('similar_pro/<str:ing>',views.similar_pro,name="similar_pro"),
    path('disimilar_pro/<str:ing>',views.disimilar_pro,name="disimilar_pro"),
    path('',views.home,name="home"),
    path('description/<str:ing>',views.description,name="description"),
]
from django.urls import path # type: ignore
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('menu', views.better_list, name='better_list'),
    path('basic_list/<int:pk>/', views.basic_list, name ='basic_list'),
    path('add_menu', views.add_menu, name='add_menu'),
    path('view_detail/<int:pk>/', views.view_detail, name='view_detail'),
    path('delete_dish/<int:pk>/', views.delete_dish, name='delete_dish'),
    path('update_dish/<int:pk>/', views.update_dish, name='update_dish'),
]
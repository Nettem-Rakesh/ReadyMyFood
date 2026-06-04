from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='hotel-home'),
    path('menu/', views.menu_view, name='menu'),
    path('order/', views.order_view, name='order'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('update_cart/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
]

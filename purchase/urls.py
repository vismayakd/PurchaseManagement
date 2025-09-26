from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('admin_dashboard/', views.admin_dashboard,name='admin_dashboard'),
    path('logout/', views.user_logout,name='logout'),
    path('add_product/', views.add_product,name='add_product'),
    path('user_register/', views.user_register,name='user_register'),
    path('user_dashboard/', views.user_dashboard,name='user_dashboard'),
    path('add_to_cart/<int:id>', views.add_to_cart,name='add_to_cart'),
    path('cart/', views.view_cart,name='cart'),
    path('user_orders/', views.user_orders,name='user_orders'),
    path('delete_item/<int:id>', views.delete_item,name='delete_item'),
    path('place_order/', views.place_order,name='place_order'),
    path('make_payment/<int:order_id>', views.make_payment,name='make_payment'),
    path('admin_orders/', views.admin_orders,name='admin_orders'),
    path("update_order_status/<int:order_id>/<str:action>/", views.update_order_status, name="update_order_status")


]
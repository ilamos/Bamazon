from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>', views.product_by_id, name='product_by_id'),
    path('add_cart/<int:product_id>', views.add_to_cart, name="add_to_cart"),
    path('remove_cart/<int:item_id>', views.remove_cart, name="remove_from_cart"),
    path('register', views.register_req, name="register"),
    path('login', views.login_req, name="login"),
    path('logout', views.logout_req, name="logout"),
    path('search', views.search_req, name="search"),
    path('cart', views.cart, name="cart")
]
from django.urls import path
from . import views


urlpatterns = [
    path('',views.store,name='index'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('updateitem/',views.updateItem,name='updateitem'),
    path('products/<str:category>/',views.productCategory,name='productCategory'),
    path('deleteitem/',views.deleteItem,name='deleteitem'),
    path('login/',views.loginView,name="login"),
    path('register/',views.registerView,name="register"),
    path('logout/',views.logout_view,name="logout"),
]
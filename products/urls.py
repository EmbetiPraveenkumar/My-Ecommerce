from . import views
from django.urls import path

urlpatterns = [
    path('',views.product_list,name ='product_list'),
    path('<int:id>',views.product_details,name='product_details'),
    path('cart/add/<int:id>',views.add_to_cart,name = 'add_to_cart'),
    path('cart/',views.cart_view,name='cart_view'),
    path('cart/increment/<int:id>',views.cart_increment,name='product_increment'),
    path('cart/decrement/<int:id>',views.cart_decrement,name='product_decrement'),
    path('clearcart',views.clear_cart,name='clear_cart'),
    path('register/',views.register,name ='register'),
    path('login/',views.login_view,name ='login_view'),
    path('logout/',views.logout_view,name ='logout_view'),
    path('checkout',views.checkout,name='checkout'),
    path('myorder',views.myorder,name='myorder'),
    path('orderdetails/<int:id>',views.orderdetails,name='orderdetails'),
    path('user',views.usr,name='usr'),
    path('wishlist/<int:id>',views.wishlist,name='wishlist'),
    path('payment_success',views.payment_success,name='payment_success'),
    path('wishlist_view',views.wishlist_view,name = 'wishlist_view')
]
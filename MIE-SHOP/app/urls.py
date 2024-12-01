from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('cart',views.cart_page,name='cart'),
    path('remove_cart/<str:cid>',views.remove_cart,name='remove_cart'),
    path('collections',views.collections,name='collections'),
    path('collections/<str:name>',views.collectionsview,name='collections'),
    path('collections/<str:cname>/<str:pname>',views.productview,name='productview'),
    path('addtocart',views.addto_cart,name='addtocart'),
    path('fav',views.fav_page,name='fav'),
    path('addtofav',views.addto_fav,name='addtofav'),
    path('rmfav/<str:fid>',views.rmfav,name='rmfav')
]

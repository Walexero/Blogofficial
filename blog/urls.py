from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.blog, name = 'blog'),
    path('home/', views.home, name = 'home'),
    path('search/', views.search, name = 'search'),
    path('post/<slug:slug_id>', views.postdetails, name = 'post'),
    path('shop/', views.shop, name = 'shop'),
    path('addtocart/<str:id>', views.addtocart, name='addtocart'),
    path('buy/<slug:slug_id>', views.buy, name = 'buy'),
    path('createpost/', views.createpost, name= 'createpost'),
    path('register/', views.register, name= 'register'),
    path('myadmin/', views.myadmin, name= 'myadmin'),
    path('userprofile/', views.userprofile, name= 'userprofile'),
    path('userpostview/<slug:slug_id>', views.userpostview, name= 'userpostview'),
    path('userpostedit/<str:postid>', views.userpostedit, name= 'userpostedit'),
    path('userpostdelete/<str:title>', views.userpostdelete, name= 'userpostdelete'),
    path('delpost/<str:title>', views.delpost, name= 'delpost'), 
]
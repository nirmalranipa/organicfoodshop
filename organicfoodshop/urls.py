"""organicfoodshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header = "Oganic Food Shop"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indexView,name='index'),
    path('about/',views.about,name='about'),
    path('blog_details/',views.blogdetails,name='blog_details'),
    path('blog/',views.blog,name='blog'),
    path('cart /',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login,name='login'), 
    path('myaccount/',views.myaccount,name='myaccount'),
    path('productdetails/',views.productdetails,name='productdetails'),
    path('register/',views.register,name='register'),
    path('shop/',views.shop,name='shop'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.myaccount,name='myaccount'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('plus/<int:id>',views.plus,name='plus'),
    path('minus/<int:id>',views.minus,name='minus'),
    path('myorder/',views.myorder,name='myorder'),
    path('response/',views.response,name='response'),
    path('payment/',views.payment,name='payment'),


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

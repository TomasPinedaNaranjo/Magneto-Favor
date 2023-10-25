"""
URL configuration for MagnetoFavor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from ofertas import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('crear_ofertas/', views.crear_ofertas, name='crear_ofertas'),
    path('ofertas/<int:offer_id>/calificar/', views.rate_offer, name='calificar_oferta'),
    path('ofertas/<int:offer_id>/ver_rating/', views.view_ratings, name='view_rating'),
    path('ver_oferta/<int:oferta_id>/', views.ver_oferta, name='ver_oferta'),
]
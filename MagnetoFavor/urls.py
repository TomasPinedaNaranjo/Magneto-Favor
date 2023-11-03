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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('crear_ofertas/', views.crear_ofertas, name='crear_ofertas'),
    path('mapa/', views.mapa, name='crear_ofertas'),
    path('eliminar_oferta/<int:oferta_id>/', views.eliminar_oferta, name='eliminar_oferta'),
    path('editar_oferta/<int:oferta_id>/', views.editar_oferta, name='editar_oferta'),
    path('aceptar_oferta/<int:oferta_id>/', views.aceptar_oferta, name='accept_offer'),
    path('ofertas_en_curso/', views.ofertas_en_curso, name='ofertas_en_curso'),
    path('cancelar_oferta/<int:oferta_id>/', views.cancelar_oferta, name='cancelar_oferta'),
    #calificar
    path('ofertas/<int:offer_id>/calificar/', views.rate_offer, name='calificar_oferta'),
    path('ofertas/<int:offer_id>/view_rating/', views.view_ratings, name='view_rating'),
    #perfil-olvideContraseña
    path('edit_user/', views.edit_user, name='edit_user'),
    path('change_password/', views.change_password, name='change_password'),
    #modify password
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"), name="reset_password"),
    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="password/change_password.html"), name="password_reset_confirm"),
    path("reset_password_complete/",auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_done.html"), name="password_reset_complete"), 
    
]
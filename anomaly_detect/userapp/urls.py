from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True,template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('result/<int:id>/', views.result, name='result'),
    path('download/<int:id>/', views.dwn_final, name='dwn_fin'),
    path('download/<int:id>/', views.dwn_out, name='dwn_out'),
    path('total_result/', views.total_result, name='total_result'),
    path('detail/<int:id>/', views.detail, name='detail'),
]

from django.urls import path
from spoc.views import index
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.index, name='spoc-index'),
	path('signup/', views.signup, name='spoc-signup'),
	path('login/', auth_views.LoginView.as_view(template_name='spoc/login.html'), name='spoc-login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='spoc/logout.html'), name='spoc-logout'),
]
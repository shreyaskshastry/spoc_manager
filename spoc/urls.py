from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('view/', views.view, name='spoc-view'),
	path('login_redirect', views.login_redirect, name='redirect'),
	path('edit/<int:pk>', views.edit, name='spoc-edit'),
	path('view/<int:id>', views.delete, name='spoc-delete'),
	path('signup/', views.signup, name='spoc-signup'),
	path('', auth_views.LoginView.as_view(template_name='spoc/login.html'), name='spoc-login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='spoc/logout.html'), name='spoc-logout'),
	path('entry/', views.make_entry, name='spoc-entry'),
	path('view/upload/', views.upload, name='spoc-upload'),
	path('view/download/', views.download, name='spoc-download'),
	path('adminview/', views.approve, name='admin-view'),
	path('confirm/<int:id>/', views.confirm_delete, name='confirm'),
	path('reject/<int:id>/', views.confirm_reject, name='reject'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
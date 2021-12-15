from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('view/', views.view, name='spoc-view'),
	path('view/edit/', views.edit, name='spoc-edit'),
	path('view/delete/', views.delete, name='spoc-delete'),
	path('signup/', views.signup, name='spoc-signup'),
	path('', auth_views.LoginView.as_view(template_name='spoc/login.html'), name='spoc-login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='spoc/logout.html'), name='spoc-logout'),
	path('entry/', views.make_entry, name='spoc-entry'),
	path('view/upload/', views.upload, name='spoc-upload'),
	path('view/download/', views.download, name='spoc-download'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
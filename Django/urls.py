from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from worker import views
from worker.views import RegistrationForm, AuthorizationForm, logout_site, home, userlist, photo
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/<int:pk>/', views.profile, name = 'profile'),
    path('my_profile/', views.my_profile, name = 'my_profile'),
    path('registration/', views.RegistrationForm, name='registration'),
    path('authorization/', views.AuthorizationForm, name='authorization'),
    path('all_profiles/', views.userlist, name='all_profiles'),
    path('logout/', views.logout_site, name='logout'),
    path('photo/', views.photo, name='photo'),
    path('', views.home, name='base'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

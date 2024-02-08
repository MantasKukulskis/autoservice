from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, user_login, change_password, user_logout, user_register


urlpatterns = [
    path("admin/", admin.site.urls),
    path("service/", include("service.urls")),
    path("", home, name="home"),
    path('login/', user_login, name='login'),
    path('change-password/', change_password, name='change-password'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

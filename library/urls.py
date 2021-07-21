from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


# including the urlpatterns 
urlpatterns = [
    path('',include('store.urls')),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('authentication/',include('django.contrib.auth.urls')),
    path('',include('authentication.urls')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

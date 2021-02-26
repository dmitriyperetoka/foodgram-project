from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('personal/', include('users.urls')),
    path('personal/purchases/', include('purchases.urls')),
    path('', RedirectView.as_view(url='/recipes/'), name='main_page')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

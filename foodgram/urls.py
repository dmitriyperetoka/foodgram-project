from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls')),
    path('purchases/', include('purchases.urls')),
    path('', RedirectView.as_view(url='/recipes/'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)

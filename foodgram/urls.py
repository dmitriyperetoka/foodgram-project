from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('personal/auth/', include('django.contrib.auth.urls')),
    path('personal/', include('users.urls', namespace='users')),
    path('recipes/', include('recipes.urls', namespace='recipes')),
    path('about/', include('about.urls', namespace='about')),
    path('api/', include('api.urls', namespace='api')),
    path('', RedirectView.as_view(url='/recipes/'), name='main_page'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

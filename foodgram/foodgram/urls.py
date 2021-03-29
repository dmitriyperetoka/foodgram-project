from django.conf import settings
from django.conf.urls import (  # noqa
    handler400, handler403, handler404, handler500
)
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

handler400 = 'foodgram.views.bad_request'  # noqa
handler403 = 'foodgram.views.permission_denied'  # noqa
handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa

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

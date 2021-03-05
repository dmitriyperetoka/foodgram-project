from django.conf import settings
from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'about'

urlpatterns = [
    path('project', views.AboutProjectView.as_view(), name='project'),
    path('tech', views.AboutTechView.as_view(), name='tech'),
    path('author', RedirectView.as_view(url=settings.AUTHOR_PAGE_URL), name='author'),
]

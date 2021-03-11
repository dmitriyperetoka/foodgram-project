from django.views.generic.base import TemplateView


class AboutProjectView(TemplateView):
    template_name = 'about/project.html'


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

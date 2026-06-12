from django.urls import path
from django.views.generic import TemplateView
from .views import ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name='general/acerca_de.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='general/contacto.html'), name='contact'),
]
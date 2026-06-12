from django.urls import path
from django.views.generic import TemplateView
from .views import ArticleListView, RegisterView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name='general/acerca_de.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='general/contacto.html'), name='contact'),

    path('registro/', RegisterView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
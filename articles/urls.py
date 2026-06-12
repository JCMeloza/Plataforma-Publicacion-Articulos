from django.urls import path
from django.views.generic import TemplateView
from .views import AdminDashboardView, ArticleListView, ChangeUserRoleView, RegisterView, CustomLoginView, CustomLogoutView, WorkDashboardView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name='general/acerca_de.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='general/contacto.html'), name='contact'),

    path('registro/', RegisterView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('admin-dashboard/', AdminDashboardView.as_view(template_name='articles/admin_dashboard.html'), name='admin_dashboard'),
    path('dashboard/admin/change-role/<int:user_id>/', ChangeUserRoleView.as_view(), name='change_role'),
    path('dashboard/workspace/', WorkDashboardView.as_view(), name='work_dashboard'),
]
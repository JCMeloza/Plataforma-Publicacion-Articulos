from django.urls import path
from django.views.generic import TemplateView
from .views import AdminDashboardView, ApproveArticleView, ArticleDetailView, ArticleListView, ArticleUpdateView, CategoryCreateView, ChangeUserRoleView, RegisterView, CustomLoginView, CustomLogoutView, RejectArticleView, ReviewCreateView, SendToReviewView, TagCreateView, WorkDashboardView

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

    path('dashboard/workspace/create/reviews/', ReviewCreateView.as_view(), name ='review_create'),
    path('dashboard/admin/category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('dashboard/admin/tag/create/', TagCreateView.as_view(), name='tag_create'),
    
    path('dashboard/workspace/send-to-review/<int:article_id>/', SendToReviewView.as_view(), name='send_to_review'),
    path('dashboard/workspace/aprove/<int:article_id>/', ApproveArticleView.as_view(), name='approve_article'),
    path('dashboard/workspace/reject/<int:article_id>/', RejectArticleView.as_view(), name='reject_article'),

    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
]

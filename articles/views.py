from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from .models import Article
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, ChangeRoleForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth import get_user_model
User = get_user_model()
class ArticleListView(ListView):
    model = Article
    template_name = 'articles/home.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status='published').select_related('autor', 'category').order_by('-created_at')

# Vista para registro de usuarios
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registro.html'
    succes_url = reverse_lazy('login')
    def get_success_url(self):
        return reverse('login')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse('admin_dashboard')
        
        return reverse('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'articles/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_articles']= Article.objects.count()
        context['published_articles'] = Article.objects.filter(status = 'published').count()
        context['draft_articles'] = Article.objects.filter(status = 'draft').count()
        context['recent_articles'] = Article.objects.select_related('autor', 'category').order_by('-created_at')[:5]
        context ['user_list'] = User.objects.filter(is_superuser=False).order_by('username')
        return context
    
class ChangeUserRoleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def post(self, request, user_id):
        user_to_edit = get_object_or_404(User, id=user_id)
        form = ChangeRoleForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
        return redirect('admin_dashboard')
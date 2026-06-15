from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView
from .models import Article, Category, Tag
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CategoryCreateForm, CustomUserCreationForm, ChangeRoleForm, ReviewCreateForm, TagCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
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
        
        if user.role in ['reviewer', 'editor']:
            return reverse('work_dashboard')
        
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
        context ['users_list'] = User.objects.filter(is_superuser=False).order_by('username')
        return context
    
class ChangeUserRoleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    
    def post(self, request, user_id):
        user_to_edit = get_object_or_404(User, id=user_id)
        form = ChangeRoleForm(request.POST, instance=user_to_edit)
        #if form.is_valid():
        #    form.save()
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                f"¡Rol de @{user_to_edit.username} actualizado con éxito a '{user_to_edit.get_role_display()}'!"
            )
        else:
            messages.error(request, "Hubo un problema al intentar cambiar el rol.")
        return redirect('admin_dashboard')
    
class WorkDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'articles/work_dashboard.html'
    context_object_name = 'articles'

    # Regla de seguridad: Solo entran revisores o editores
    def test_func(self):
        return self.request.user.role in ['reviewer', 'editor']

    def get_queryset(self):
        user = self.request.user
        # Si es Revisor: ve solo SUS artículos (tanto borradores como publicados)
        if user.role == 'reviewer':
            return Article.objects.filter(autor=user).order_by('-created_at')
        
        # Si es Editor: ve los artículos de TODOS que estén esperando aprobación
        # (Ajusta 'draft' por 'pending' si creaste ese estado en tus choices)
        if user.role == 'editor':
            return Article.objects.filter(status='pending').select_related('autor').order_by('-created_at')
        
        return Article.objects.none()

class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    template_name = 'articles/review_create.html'
    model = Article
    form_class = ReviewCreateForm
    success_url = reverse_lazy('work_dashboard')

    def test_func(self):
        return self.request.user.role == 'reviewer'
    
    def form_valid(self, form):

        form.instance.autor = self.request.user
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Articulo creado correctamente.",
        )
        return super(ReviewCreateView, self).form_valid(form)


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    
    template_name = 'articles/admin_manage_taxonomies.html'
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self,form):
        messages.success(self.request, f"Categoría '{form.instance.name}' creada con éxito.")
        return super().form_valid(form)


class TagCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    
    template_name = 'articles/admin_manage_taxonomies.html'
    model = Tag
    form_class = TagCreateForm
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self,form):
        messages.success(self.request, f"Etiqueta '{form.instance.name}' creada con éxito.")
        return super().form_valid(form)

class SendToReviewView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        article = get_object_or_404(Article, id = self.kwargs['article_id'])
        return self.request.user == article.autor
    
    def post(self, request, article_id):

        #busca del artículo por su ID
        article = get_object_or_404(Article, id=article_id)

        if article.status in ['draft', 'pending']:
            article.status = 'pending'
            article.save()

            messages.success(
                request, 
                f"🚀 ¡El artículo '{article.title}' ha sido enviado a revisión correctamente!"
            )
        else:
            messages.error(request, "Este artículo no se puede enviar a revisión en su estado actual.")
            
        # Redirigimos de vuelta al escritorio de trabajo
        return redirect('work_dashboard')


class ApproveArticleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'editor'
    
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)

        if article.status == 'pending':
            article.status = 'published'
            article.save()
            messages.success(request, f"🟢 El artículo '{article.title}' ha sido PUBLICADO en la web.")
        else:
            messages.error(request, "Este artículo no está pendiente de revisión.")
            
        return redirect('work_dashboard')  

class RejectArticleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'editor'
    
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)

        if article.status == 'pending':
            article.status = 'rejected'
            article.save()
            messages.success(request, f"🔴 El artículo '{article.title}' ha sido RECHAZADO Y devuelto al autor.")
        else:
            messages.error(request, "Este artículo no está pendiente de revisión.")
            
        return redirect('work_dashboard')  
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'articles/review_create.html'
    form_class = ReviewCreateForm
    success_url = reverse_lazy('work_dashboard')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.autor
    
    def from_valid(self, form):
        if form.instance.status == 'rejected':
            form.instance.status = 'draft'

        messages.success(self.request, "¡Artículo actualizado correctamente!")
        return super().form_valid(form)


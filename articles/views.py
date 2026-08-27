from ast import If
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView
from .models import Article, Category, Like, Tag, ContactMessage
from django.contrib.auth.views import LoginView, LogoutView
from .forms import ArticleForm, CategoryCreateForm, CommentForm, CustomUserCreationForm, ChangeRoleForm, ReviewCreateForm, TagCreateForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
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
        context['published_count'] = Article.objects.filter(status = 'published').count()
        context['draft_count'] = Article.objects.filter(status = 'draft').count()
        context['recent_articles'] = Article.objects.select_related('autor', 'category').order_by('-created_at')[:5]
        context ['users_list'] = User.objects.filter(is_superuser=False).order_by('username')
        context['contact_messages'] = ContactMessage.objects.order_by('-created_at')
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

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    template_name = 'articles/article_form.html'
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('work_dashboard')

    def test_func(self):
        return self.request.user.role == 'reviewer'
    
    def form_valid(self, form):

        form.instance.autor = self.request.user
        form.instance.slug = slugify(form.instance.title)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Articulo creado correctamente.",
        )
        return super(ArticleCreateView, self).form_valid(form)


# Backward compatibility alias (deprecated: use ArticleCreateView)
ReviewCreateView = ArticleCreateView


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


# Stub for ReviewFormView (Foundation PR1 — full GET/POST flow implemented in PR2)
class ReviewFormView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Handle GET (show form) and POST (create Review + update status) for approve/reject.
    Full implementation in Phase 2; stub ensures URL routing exists in PR1."""
    def test_func(self):
        return self.request.user.role == 'editor'

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.status != 'pending':
            messages.error(request, "Este artículo no está pendiente de revisión")
            return redirect('work_dashboard')
        # Placeholder: redirect until full form flow is implemented in PR2
        messages.error(request, "Flujo de revisión en construcción")
        return redirect('work_dashboard')

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.status != 'pending':
            messages.error(request, "Este artículo no está pendiente de revisión")
            return redirect('work_dashboard')
        messages.error(request, "Flujo de revisión en construcción")
        return redirect('work_dashboard')  
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        context['total_likes'] = self.object.likes.count()
        if self.request.user.is_authenticated:
            context['user_has_liked'] = self.object.likes.filter(user=self.request.user).exists()
        else:
            context['user_has_liked'] = False
            
        return context

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'articles/article_form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('work_dashboard')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.autor
    
    def form_valid(self, form):
        if form.instance.status == 'rejected' or form.instance.status == 'published':
            form.instance.status = 'draft'

        messages.success(self.request, "¡Artículo actualizado correctamente!")
        return super().form_valid(form)

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            messages.success(request, "Comentario agregado con éxito.")
        else:
            messages.error(request, "Hubo un error al agregar tu comentario. Por favor, inténtalo de nuevo.")
        
        return redirect('article_detail', pk=article.id)

class LikeArticleView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id= article_id)
        liked_article = Like.objects.filter(article=article, user=request.user)

        if liked_article.exists():
            liked_article.delete()
            messages.success(request, f"Has retirado tu 'Me gusta' del artículo '{article.title}'.")
        else:
            Like.objects.create(article=article, user=request.user)
            messages.success(request, f"Has dado 'Me gusta' al artículo '{article.title}'.")
        return redirect('article_detail', pk=article.id)
        
class ProfileView(LoginRequiredMixin, View):
    template_name = 'articles/profile.html'

    def get(self, request):
        form = UserProfileForm(instance = request.user)
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form = UserProfileForm(request.POST,request.FILES, instance= request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"¡Tu perfil se ha actualizado correctamente")
            return redirect('profile')        
        
        messages.error(request, "Por favor, corrige los errores del formulario.")
        return render(request, self.template_name, {'form': form})
    
class ProfileListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name ='articles/profile_list.html'
    model = User
    context_object_name='users'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['reviewer', 'editor', 'reader']

    def get_queryset(self):
        return User.objects.all().filter(is_superuser=False).exclude(id=self.request.user.id).order_by('username')  
    
class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'articles/profile_detail.html'
    context_object_name = 'profile_user'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['reviewer', 'editor', 'reader']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authored_articles_count'] = self.object.articles.count()
        context['commented_articles_count'] = self.object.comment_set.count()
        context['total_likes_count'] = Like.objects.filter(article__autor=self.object).count()
        return context

class ContactView(View):
    template_name = 'general/contacto.html'

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            context['users'] = User.objects.exclude(id=request.user.id).order_by('username')
            to_user_id = request.GET.get('to')
            if to_user_id:
                context['selected_user'] = get_object_or_404(User, id=to_user_id)
            
            # Capturar asunto si viene por parámetro (ej. responder mensaje)
            asunto = request.GET.get('asunto')
            if asunto:
                context['selected_asunto'] = asunto
        return render(request, self.template_name, context)

    def post(self, request):
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        remitente = None
        destinatario = None
        
        if request.user.is_authenticated:
            remitente = request.user
            nombre = request.user.username
            email = request.user.email
            destinatario_id = request.POST.get('destinatario')
            if destinatario_id:
                destinatario = get_object_or_404(User, id=destinatario_id)

        ContactMessage.objects.create(
            remitente=remitente,
            destinatario=destinatario,
            nombre=nombre,
            email=email,
            asunto=asunto,
            mensaje=mensaje
        )

        messages.success(request, "¡Tu mensaje ha sido enviado con éxito!")
        return redirect('contact')

class InboxView(LoginRequiredMixin, ListView):
    template_name = 'articles/inbox.html'
    context_object_name = 'messages_list'
    model = ContactMessage

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ContactMessage.objects.filter(
                Q(destinatario=self.request.user) | Q(destinatario__isnull=True)
            ).order_by('-created_at')
        return ContactMessage.objects.filter(destinatario=self.request.user).order_by('-created_at')

class MessageDetailView(LoginRequiredMixin, DetailView):
    template_name = 'articles/message_detail.html'
    context_object_name = 'msg'
    model = ContactMessage

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ContactMessage.objects.filter(
                Q(destinatario=self.request.user) | Q(destinatario__isnull=True)
            )
        return ContactMessage.objects.filter(destinatario=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj
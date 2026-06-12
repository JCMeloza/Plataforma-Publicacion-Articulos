from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Article
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/home.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status='published').select_related('autor', 'category').order_by('-created_at')

# Vista para registro de usuarios
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registro.html'
    succes_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
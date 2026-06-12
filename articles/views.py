from django.views.generic import ListView
from .models import Article
# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/home.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status='published').select_related('autor', 'category').order_by('-created_at')

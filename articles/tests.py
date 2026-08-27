from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from articles.forms import ArticleForm
from articles.views import ArticleCreateView, ArticleUpdateView
from articles.models import Article, Category

User = get_user_model()


class ArticleFormRenameTests(TestCase):
    """TDD RED: Rename ReviewCreateForm → ArticleForm verification."""

    def test_article_form_importable(self):
        self.assertIsNotNone(ArticleForm)

    def test_article_form_creates_article(self):
        """ArticleForm should be a ModelForm for Article with expected fields."""
        self.assertEqual(ArticleForm.Meta.model, Article)
        self.assertEqual(
            ArticleForm.Meta.fields,
            ['title', 'content', 'image', 'category', 'tags'],
        )

    def test_article_create_view_importable(self):
        self.assertIsNotNone(ArticleCreateView)

    def test_article_create_view_uses_article_form(self):
        self.assertEqual(ArticleCreateView.form_class, ArticleForm)

    def test_article_update_view_uses_article_form(self):
        self.assertEqual(ArticleUpdateView.form_class, ArticleForm)

    def test_article_create_view_template(self):
        self.assertEqual(ArticleCreateView.template_name, "articles/article_form.html")

    def test_article_update_view_template(self):
        self.assertEqual(ArticleUpdateView.template_name, "articles/article_form.html")


class ArticleCreateUrlTests(TestCase):
    """Verify new article_create URL and that old review_create no longer primary."""

    def setUp(self):
        self.reviewer = User.objects.create_user(
            username="reviewer1", password="pass1234", role="reviewer"
        )
        self.category = Category.objects.create(name="Tech", slug="tech")

    def test_article_create_url_resolves(self):
        url = reverse("article_create")
        self.assertEqual(url, "/dashboard/workspace/create/reviews/")
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "article_create")

    def test_article_create_get_as_reviewer(self):
        self.client.login(username="reviewer1", password="pass1234")
        response = self.client.get(reverse("article_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/article_form.html")

    def test_article_create_post_creates_article(self):
        self.client.login(username="reviewer1", password="pass1234")
        response = self.client.post(
            reverse("article_create"),
            data={
                "title": "Nuevo Artículo de Prueba",
                "content": "Contenido de prueba",
                "category": self.category.id,
                "tags": [],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(title="Nuevo Artículo de Prueba").exists())
        article = Article.objects.get(title="Nuevo Artículo de Prueba")
        self.assertEqual(article.autor, self.reviewer)
        self.assertEqual(article.status, "draft")

    def test_review_create_old_url_not_resolvable(self):
        """Old URL name review_create should not resolve (renamed)."""
        from django.urls import NoReverseMatch

        with self.assertRaises(NoReverseMatch):
            reverse("review_create")

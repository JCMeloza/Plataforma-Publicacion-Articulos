from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from articles.forms import ArticleForm, ReviewForm
from articles.views import ArticleCreateView, ArticleUpdateView, ReviewFormView
from articles.models import Article, Category
from editorial.models import Review

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


# ── Phase 2: ReviewFormView Core Flow (Strict TDD RED) ──────────────
class ReviewFormViewTests(TestCase):
    """TDD RED: ReviewFormView approve/reject flow, permissions, atomicity."""

    def setUp(self):
        self.editor = User.objects.create_user(username="editor1", password="pass1234", role="editor")
        self.reviewer = User.objects.create_user(username="reviewer1", password="pass1234", role="reviewer")
        self.reader = User.objects.create_user(username="reader1", password="pass1234", role="reader")
        self.author = User.objects.create_user(username="author1", password="pass1234", role="reviewer")
        self.category = Category.objects.create(name="Tech2", slug="tech2")
        self.article_pending = Article.objects.create(
            title="Pending Article", slug="pending-article", content="Contenido pendiente",
            category=self.category, autor=self.author, status="pending",
        )
        self.article_published = Article.objects.create(
            title="Published Article", slug="published-article", content="Contenido publicado",
            category=self.category, autor=self.author, status="published",
        )
        self.article_draft = Article.objects.create(
            title="Draft Article", slug="draft-article", content="Contenido borrador",
            category=self.category, autor=self.author, status="draft",
        )
        self.article_rejected = Article.objects.create(
            title="Rejected Article", slug="rejected-article", content="Contenido rechazado",
            category=self.category, autor=self.author, status="rejected",
        )

    # ── Permissions (test_func: only editors) ────────────────────────
    def test_editor_can_access_approve_get(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.get(reverse("review_approve", args=[self.article_pending.id]))
        self.assertEqual(response.status_code, 200)

    def test_reviewer_cannot_approve_get_403(self):
        self.client.login(username="reviewer1", password="pass1234")
        response = self.client.get(reverse("review_approve", args=[self.article_pending.id]))
        self.assertEqual(response.status_code, 403)

    def test_reader_cannot_approve_get_403(self):
        self.client.login(username="reader1", password="pass1234")
        response = self.client.get(reverse("review_approve", args=[self.article_pending.id]))
        self.assertEqual(response.status_code, 403)

    def test_reviewer_cannot_reject_get_403(self):
        self.client.login(username="reviewer1", password="pass1234")
        response = self.client.get(reverse("review_reject", args=[self.article_pending.id]))
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_redirects_to_login(self):
        response = self.client.get(reverse("review_approve", args=[self.article_pending.id]))
        # LoginRequiredMixin → 302 to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_editor_can_access_approve_post_overall_allowed(self):
        self.client.login(username="editor1", password="pass1234")
        # POST with valid data should not be 403 (permission passes, then redirects)
        response = self.client.post(
            reverse("review_approve", args=[self.article_pending.id]),
            data={"comments": "Excelente artículo", "feedback": "Bien"},
        )
        self.assertNotEqual(response.status_code, 403)

    # ── Approve GET ──────────────────────────────────────────────────
    def test_approve_get_renders_form_with_decision_approve(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.get(reverse("review_approve", args=[self.article_pending.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/review_form.html")
        self.assertEqual(response.context["decision"], "approve")
        self.assertEqual(response.context["article"], self.article_pending)
        self.assertIsInstance(response.context["form"], ReviewForm)
        self.assertEqual(response.context["form"].decision, "approve")
        self.assertEqual(response.context["form"].instance.decision, "approve")

    def test_reject_get_renders_form_with_decision_reject(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.get(reverse("review_reject", args=[self.article_pending.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/review_form.html")
        self.assertEqual(response.context["decision"], "reject")
        self.assertEqual(response.context["form"].decision, "reject")

    # ── Approve POST happy path ──────────────────────────────────────
    def test_approve_post_creates_review_and_publishes_atomically(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_approve", args=[self.article_pending.id]),
            data={"comments": "Excelente artículo, bien estructurado", "feedback": "Considerar añadir más ejemplos en la sección 3"},
        )
        self.assertRedirects(response, reverse("work_dashboard"))
        self.assertTrue(Review.objects.filter(article=self.article_pending, decision="approve").exists())
        review = Review.objects.get(article=self.article_pending, decision="approve")
        self.assertEqual(review.reviewer, self.editor)
        self.assertEqual(review.comments, "Excelente artículo, bien estructurado")
        self.assertEqual(review.feedback, "Considerar añadir más ejemplos en la sección 3")
        self.article_pending.refresh_from_db()
        self.assertEqual(self.article_pending.status, "published")

    def test_approve_post_with_only_comments_no_feedback(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_approve", args=[self.article_pending.id]),
            data={"comments": "Aprobado", "feedback": ""},
        )
        self.assertRedirects(response, reverse("work_dashboard"))
        review = Review.objects.get(article=self.article_pending)
        self.assertEqual(review.decision, "approve")
        self.assertEqual(review.feedback, "")
        self.article_pending.refresh_from_db()
        self.assertEqual(self.article_pending.status, "published")

    # ── Reject POST happy path ───────────────────────────────────────
    def test_reject_post_creates_review_and_rejects_atomically(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_reject", args=[self.article_pending.id]),
            data={"comments": "Falta profundidad en el análisis", "feedback": "Revisar la metodología y ampliar la bibliografía"},
        )
        self.assertRedirects(response, reverse("work_dashboard"))
        review = Review.objects.get(article=self.article_pending, decision="reject")
        self.assertEqual(review.reviewer, self.editor)
        self.assertEqual(review.comments, "Falta profundidad en el análisis")
        self.assertEqual(review.feedback, "Revisar la metodología y ampliar la bibliografía")
        self.article_pending.refresh_from_db()
        self.assertEqual(self.article_pending.status, "rejected")

    def test_reject_post_with_only_comments_no_feedback(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_reject", args=[self.article_pending.id]),
            data={"comments": "No cumple criterios", "feedback": ""},
        )
        self.assertRedirects(response, reverse("work_dashboard"))
        review = Review.objects.get(article=self.article_pending)
        self.assertEqual(review.decision, "reject")
        self.assertEqual(review.feedback, "")
        self.article_pending.refresh_from_db()
        self.assertEqual(self.article_pending.status, "rejected")

    # ── Validation errors ────────────────────────────────────────────
    def test_approve_post_empty_comments_shows_form_error_no_review_no_status_change(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_approve", args=[self.article_pending.id]),
            data={"comments": "", "feedback": "algo"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/review_form.html")
        self.assertIn("comments", response.context["form"].errors)
        self.assertFalse(Review.objects.filter(article=self.article_pending).exists())
        self.article_pending.refresh_from_db()
        self.assertEqual(self.article_pending.status, "pending")

    def test_reject_post_empty_comments_shows_form_error_no_review_no_status_change(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_reject", args=[self.article_pending.id]),
            data={"comments": "", "feedback": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("comments", response.context["form"].errors)
        self.assertFalse(Review.objects.filter(article=self.article_pending).exists())
        self.article_pending.refresh_from_db()
        self.assertEqual(self.article_pending.status, "pending")

    def test_approve_post_whitespace_comments_fails(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_approve", args=[self.article_pending.id]),
            data={"comments": "   ", "feedback": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("comments", response.context["form"].errors)
        self.assertFalse(Review.objects.filter(article=self.article_pending).exists())

    # ── Non-pending article ──────────────────────────────────────────
    def test_approve_get_non_pending_redirects_with_error_no_review(self):
        self.client.login(username="editor1", password="pass1234")
        for article in [self.article_published, self.article_draft, self.article_rejected]:
            response = self.client.get(reverse("review_approve", args=[article.id]))
            self.assertRedirects(response, reverse("work_dashboard"))
            self.assertFalse(Review.objects.filter(article=article).exists())
            # status unchanged
            article.refresh_from_db()
            self.assertIn(article.status, ["published", "draft", "rejected"])

    def test_reject_get_non_pending_redirects_with_error_no_review(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.get(reverse("review_reject", args=[self.article_draft.id]))
        self.assertRedirects(response, reverse("work_dashboard"))
        self.assertFalse(Review.objects.filter(article=self.article_draft).exists())

    def test_approve_post_non_pending_redirects_with_error_no_review(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_approve", args=[self.article_published.id]),
            data={"comments": "Intento aprobar publicado", "feedback": ""},
        )
        self.assertRedirects(response, reverse("work_dashboard"))
        self.assertFalse(Review.objects.filter(article=self.article_published).exists())
        self.article_published.refresh_from_db()
        self.assertEqual(self.article_published.status, "published")

    def test_reject_post_non_pending_redirects_with_error_no_review(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.post(
            reverse("review_reject", args=[self.article_draft.id]),
            data={"comments": "Intento rechazar borrador", "feedback": ""},
        )
        self.assertRedirects(response, reverse("work_dashboard"))
        self.assertFalse(Review.objects.filter(article=self.article_draft).exists())
        self.article_draft.refresh_from_db()
        self.assertEqual(self.article_draft.status, "draft")

    # ── Permissions on POST ──────────────────────────────────────────
    def test_non_editor_cannot_approve_post_403_no_review(self):
        self.client.login(username="reviewer1", password="pass1234")
        response = self.client.post(
            reverse("review_approve", args=[self.article_pending.id]),
            data={"comments": "Intento", "feedback": ""},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Review.objects.filter(article=self.article_pending).exists())
        self.article_pending.refresh_from_db()
        self.assertEqual(self.article_pending.status, "pending")

    def test_non_editor_cannot_reject_post_403_no_review(self):
        self.client.login(username="reviewer1", password="pass1234")
        response = self.client.post(
            reverse("review_reject", args=[self.article_pending.id]),
            data={"comments": "Intento", "feedback": ""},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Review.objects.filter(article=self.article_pending).exists())

    # ── Work dashboard editor buttons link to review flow ────────────
    def test_work_dashboard_editor_shows_links_to_review_flow(self):
        self.client.login(username="editor1", password="pass1234")
        response = self.client.get(reverse("work_dashboard"))
        self.assertEqual(response.status_code, 200)
        approve_url = reverse("review_approve", args=[self.article_pending.id])
        reject_url = reverse("review_reject", args=[self.article_pending.id])
        self.assertContains(response, approve_url)
        self.assertContains(response, reject_url)
        # Old direct POST endpoints should NOT appear as primary editor action (no approve_article/reject_article forms for this article)
        # Ensure the new GET links exist (Aprobar/Rechazar text)
        self.assertContains(response, "Aprobar")
        self.assertContains(response, "Rechazar")


# ── Phase 3: Review History Display + Resubmission (Strict TDD RED) ──
class ReviewHistoryVisibilityTests(TestCase):
    """TDD RED: review history visibility per review-history-display spec."""

    def setUp(self):
        self.author = User.objects.create_user(username="hist_author", password="pass1234", role="reviewer")
        self.editor = User.objects.create_user(username="hist_editor", password="pass1234", role="editor")
        self.other_reviewer = User.objects.create_user(username="hist_other", password="pass1234", role="reviewer")
        self.reader = User.objects.create_user(username="hist_reader", password="pass1234", role="reader")
        self.editor2 = User.objects.create_user(username="hist_editor2", password="pass1234", role="editor")
        self.category = Category.objects.create(name="HistCat", slug="histcat")
        self.article_rejected = Article.objects.create(
            title="Rejected with Review", slug="rejected-with-review", content="Contenido",
            category=self.category, autor=self.author, status="rejected",
        )
        self.review1 = Review.objects.create(
            article=self.article_rejected, reviewer=self.editor,
            decision="reject", comments="Falta profundidad en el análisis",
            feedback="Ampliar bibliografía",
        )
        self.article_published = Article.objects.create(
            title="Published with Review", slug="published-with-review", content="Contenido pub",
            category=self.category, autor=self.author, status="published",
        )
        self.review_pub = Review.objects.create(
            article=self.article_published, reviewer=self.editor,
            decision="approve", comments="Excelente artículo, bien estructurado",
            feedback="Considerar añadir más ejemplos",
        )
        self.article_draft = Article.objects.create(
            title="Draft no reviews", slug="draft-no-reviews", content="borrador",
            category=self.category, autor=self.author, status="draft",
        )
        self.article_multi = Article.objects.create(
            title="Multi Review", slug="multi-review", content="multi",
            category=self.category, autor=self.author, status="published",
        )
        # create 3 reviews with distinct timestamps via manual creation order
        self.r1 = Review.objects.create(article=self.article_multi, reviewer=self.editor, decision="reject", comments="Coment 1", feedback="Feed 1")
        self.r2 = Review.objects.create(article=self.article_multi, reviewer=self.editor2, decision="reject", comments="Coment 2", feedback="Feed 2")
        self.r3 = Review.objects.create(article=self.article_multi, reviewer=self.editor, decision="approve", comments="Coment 3", feedback="Feed 3")

    def test_author_sees_history_with_feedback_and_details(self):
        self.client.login(username="hist_author", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_rejected.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Historial de revisiones")
        self.assertContains(response, self.editor.username)
        self.assertContains(response, "Rechazado")
        self.assertContains(response, "Falta profundidad en el análisis")
        self.assertContains(response, "Ampliar bibliografía")
        # timestamp present (created_at rendered)
        self.assertContains(response, str(self.review1.created_at.year))

    def test_author_sees_published_approval_history(self):
        self.client.login(username="hist_author", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_published.id]))
        self.assertContains(response, "Historial de revisiones")
        self.assertContains(response, "Aprobado")
        self.assertContains(response, "Excelente artículo, bien estructurado")

    def test_editor_sees_all_fields_including_comments(self):
        self.client.login(username="hist_editor", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_rejected.id]))
        self.assertContains(response, "Historial de revisiones")
        self.assertContains(response, "Falta profundidad en el análisis")
        self.assertContains(response, "Ampliar bibliografía")
        self.assertContains(response, self.editor.username)

    def test_editor_sees_history_even_if_not_reviewer(self):
        self.client.login(username="hist_editor2", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_rejected.id]))
        self.assertContains(response, "Historial de revisiones")
        self.assertContains(response, self.editor.username)

    def test_other_reviewer_cannot_see_history(self):
        self.client.login(username="hist_other", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_rejected.id]))
        self.assertNotContains(response, "Historial de revisiones")
        self.assertNotContains(response, "Falta profundidad en el análisis")

    def test_reader_cannot_see_history(self):
        self.client.login(username="hist_reader", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_rejected.id]))
        self.assertNotContains(response, "Historial de revisiones")

    def test_anonymous_cannot_see_history(self):
        response = self.client.get(reverse("article_detail", args=[self.article_rejected.id]))
        self.assertNotContains(response, "Historial de revisiones")
        self.assertNotContains(response, "Ampliar bibliografía")

    def test_draft_with_no_reviews_shows_no_history_or_empty_message(self):
        self.client.login(username="hist_author", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_draft.id]))
        # should not crash, and should not show reviewer data
        self.assertEqual(response.status_code, 200)
        # either hidden or shows "Sin revisiones" — we assert no reviewer name leaked
        self.assertNotContains(response, "Falta profundidad")

    def test_multiple_reviews_displayed_chronologically(self):
        self.client.login(username="hist_author", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_multi.id]))
        self.assertContains(response, "Historial de revisiones")
        self.assertContains(response, "Coment 1")
        self.assertContains(response, "Coment 2")
        self.assertContains(response, "Coment 3")
        content = response.content.decode()
        # chronological order: 1 before 2 before 3
        self.assertTrue(content.index("Coment 1") < content.index("Coment 2") < content.index("Coment 3"))

    def test_non_author_non_editor_does_not_see_feedback(self):
        self.client.login(username="hist_other", password="pass1234")
        response = self.client.get(reverse("article_detail", args=[self.article_multi.id]))
        self.assertNotContains(response, "Coment 1")
        self.assertNotContains(response, "Feed 1")


class ReviewResubmissionTests(TestCase):
    """TDD RED: resubmission cycle — rejected → edit → send_to_review → new review."""

    def setUp(self):
        self.author = User.objects.create_user(username="res_author", password="pass1234", role="reviewer")
        self.editor = User.objects.create_user(username="res_editor", password="pass1234", role="editor")
        self.category = Category.objects.create(name="ResCat", slug="rescat")
        self.article = Article.objects.create(
            title="Resub Article", slug="resub-article", content="Original",
            category=self.category, autor=self.author, status="pending",
        )

    def test_rejected_then_resubmitted_can_be_reviewed_again_and_accumulates_history(self):
        # Step 1: editor rejects pending → rejected + Review1
        self.client.login(username="res_editor", password="pass1234")
        resp = self.client.post(reverse("review_reject", args=[self.article.id]), data={"comments": "Mal", "feedback": "Mejorar"})
        self.assertRedirects(resp, reverse("work_dashboard"))
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "rejected")
        self.assertEqual(Review.objects.filter(article=self.article).count(), 1)
        self.client.logout()

        # Step 2: author edits rejected article → status reset to draft via ArticleUpdateView
        self.client.login(username="res_author", password="pass1234")
        edit_url = reverse("article_edit", args=[self.article.id])
        resp = self.client.post(edit_url, data={
            "title": "Resub Article v2",
            "content": "Contenido mejorado",
            "category": self.category.id,
            "tags": [],
        })
        self.assertEqual(resp.status_code, 302)
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "draft")
        self.assertEqual(self.article.title, "Resub Article v2")

        # Step 3: author sends to review → pending, reviews preserved
        resp = self.client.post(reverse("send_to_review", args=[self.article.id]))
        self.assertRedirects(resp, reverse("work_dashboard"))
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "pending")
        self.assertEqual(Review.objects.filter(article=self.article).count(), 1)
        self.client.logout()

        # Step 4: editor approves resubmitted article → second Review
        self.client.login(username="res_editor", password="pass1234")
        resp = self.client.post(reverse("review_approve", args=[self.article.id]), data={"comments": "Ahora bien", "feedback": ""})
        self.assertRedirects(resp, reverse("work_dashboard"))
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "published")
        self.assertEqual(Review.objects.filter(article=self.article).count(), 2)
        reviews = list(Review.objects.filter(article=self.article).order_by("created_at"))
        self.assertEqual(reviews[0].decision, "reject")
        self.assertEqual(reviews[1].decision, "approve")

    def test_send_to_review_preserves_existing_reviews(self):
        # create rejected article with review already
        self.article.status = "rejected"
        self.article.save()
        Review.objects.create(article=self.article, reviewer=self.editor, decision="reject", comments="c", feedback="f")
        self.client.login(username="res_author", password="pass1234")
        # edit to draft first (simulating author fix) then send
        self.client.post(reverse("article_edit", args=[self.article.id]), data={
            "title": self.article.title, "content": "edit", "category": self.category.id, "tags": []
        })
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "draft")
        before = Review.objects.filter(article=self.article).count()
        self.client.post(reverse("send_to_review", args=[self.article.id]))
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "pending")
        self.assertEqual(Review.objects.filter(article=self.article).count(), before)


class MultipleReviewRoundsTests(TestCase):
    """TDD RED: 3 cycles (reject, reject, approve) → 3 Review records."""

    def setUp(self):
        self.author = User.objects.create_user(username="multi_author", password="pass1234", role="reviewer")
        self.editor = User.objects.create_user(username="multi_editor", password="pass1234", role="editor")
        self.category = Category.objects.create(name="MultiCat2", slug="multicat2")
        self.article = Article.objects.create(
            title="Three Cycles", slug="three-cycles", content="v1",
            category=self.category, autor=self.author, status="pending",
        )

    def test_three_review_cycles_accumulate_and_display(self):
        # Cycle 1: reject
        self.client.login(username="multi_editor", password="pass1234")
        self.client.post(reverse("review_reject", args=[self.article.id]), data={"comments": "C1", "feedback": "F1"})
        self.client.logout()
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "rejected")
        # resubmit 1: edit + send
        self.client.login(username="multi_author", password="pass1234")
        self.client.post(reverse("article_edit", args=[self.article.id]), data={"title": "Three Cycles", "content": "v2", "category": self.category.id, "tags": []})
        self.client.post(reverse("send_to_review", args=[self.article.id]))
        self.client.logout()
        # Cycle 2: reject again
        self.client.login(username="multi_editor", password="pass1234")
        self.client.post(reverse("review_reject", args=[self.article.id]), data={"comments": "C2", "feedback": "F2"})
        self.client.logout()
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "rejected")
        # resubmit 2
        self.client.login(username="multi_author", password="pass1234")
        self.client.post(reverse("article_edit", args=[self.article.id]), data={"title": "Three Cycles", "content": "v3", "category": self.category.id, "tags": []})
        self.client.post(reverse("send_to_review", args=[self.article.id]))
        self.client.logout()
        # Cycle 3: approve
        self.client.login(username="multi_editor", password="pass1234")
        self.client.post(reverse("review_approve", args=[self.article.id]), data={"comments": "C3", "feedback": ""})
        self.client.logout()
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "published")
        self.assertEqual(Review.objects.filter(article=self.article).count(), 3)
        reviews = list(Review.objects.filter(article=self.article).order_by("created_at"))
        self.assertEqual([r.decision for r in reviews], ["reject", "reject", "approve"])
        self.assertEqual([r.comments for r in reviews], ["C1", "C2", "C3"])
        # also verify history visible to author chronologically
        self.client.login(username="multi_author", password="pass1234")
        resp = self.client.get(reverse("article_detail", args=[self.article.id]))
        content = resp.content.decode()
        self.assertContains(resp, "Historial de revisiones")
        self.assertTrue(content.index("C1") < content.index("C2") < content.index("C3"))

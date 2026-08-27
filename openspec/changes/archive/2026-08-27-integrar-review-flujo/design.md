# Design: Integrar modelo Review en flujo editorial

## Technical Approach

Implement editorial review flow by converting `ApproveArticleView`/`RejectArticleView` from direct POST handlers to form-based views that create `Review` records atomically with status changes. Use a **dedicated review form page** (not modal/HTMX) for the simplest reliable UX — editor clicks action button → navigates to review form → submits → returns to dashboard. Add review history display on article detail. Rename misnamed `ReviewCreateView`/`ReviewCreateForm`/`review_create.html` to `ArticleCreateView`/`ArticleForm`/`article_form.html`.

## Architecture Decisions

### Decision: Review Capture UX — Dedicated Page vs Modal

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Bootstrap modal + HTMX | Complex; requires django-htmx, partial templates, JS handling | Rejected — proposal flagged as risk |
| Dedicated review form page (GET/POST) | Simple, reliable, follows existing Django patterns | **Chosen** — editor clicks button → `/review/<id>/approve/` shows form → POST creates Review + updates status |

**Rationale**: Proposal explicitly flags modal/HTMX complexity as Medium risk with mitigation "start with simple POST form". Dedicated page uses existing patterns (same as ArticleCreateView), zero new dependencies, trivial to test.

### Decision: Atomic Review + Status Update

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Two separate saves | Risk of inconsistency if second save fails | Rejected |
| `transaction.atomic()` block | Guarantees both Review creation and Article.save() succeed or fail together | **Chosen** |

**Rationale**: Specs require atomicity. Django's `transaction.atomic()` is the standard pattern.

### Decision: Review Model Changes

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Add `reviewer_role` check field | Redundant — `reviewer` FK + view permission check sufficient | Rejected |
| Make `comments` optional | Specs require comments for both approve/reject | Rejected |
| Keep model as-is | Fields match specs exactly: `decision`, `comments` (required), `feedback` (optional), `reviewer`, `article`, `created_at` | **Chosen** |

**Rationale**: Model already has correct structure. `comments` is required (no `blank=True`), `feedback` is optional (`blank=True`). View-level permission check (`test_func` for editor role) handles authorization.

## Data Flow

```
Editor Dashboard (work_dashboard.html)
    │
    ├─→ GET /review/<id>/approve/  →  ReviewFormView (decision='approve' pre-filled)
    │       │
    │       └─→ POST /review/<id>/approve/  →  transaction.atomic():
    │               Review.objects.create(decision='approve', ...)
    │               article.status = 'published'; article.save()
    │               → redirect to work_dashboard
    │
    └─→ GET /review/<id>/reject/  →  ReviewFormView (decision='reject' pre-filled)
            │
            └─→ POST /review/<id>/reject/  →  transaction.atomic():
                    Review.objects.create(decision='reject', ...)
                    article.status = 'rejected'; article.save()
                    → redirect to work_dashboard

Article Detail (article_detail.html)
    │
    └─→ Render "Historial de revisiones" section
            article.reviews.all().order_by('created_at')
            → shows reviewer, decision, comments, feedback, timestamp
            → visible to author + editors only
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `articles/forms.py` | Modify | Add `ReviewForm`; rename `ReviewCreateForm` → `ArticleForm` |
| `articles/views.py` | Modify | Replace `ApproveArticleView`/`RejectArticleView` with `ReviewFormView`; rename `ReviewCreateView` → `ArticleCreateView`; update `ArticleUpdateView` to use `ArticleForm` |
| `articles/urls.py` | Modify | New URLs for review form; rename `review_create` → `article_create`; update imports |
| `articles/templates/articles/work_dashboard.html` | Modify | Editor action buttons link to review form URLs (GET) instead of direct POST |
| `articles/templates/articles/article_detail.html` | Modify | Add "Historial de revisiones" section using `article.reviews.all` |
| `articles/templates/articles/review_create.html` | Rename → `article_form.html` | Template renamed; used by `ArticleCreateView`/`ArticleUpdateView` |
| `articles/templates/articles/review_form.html` | Create | New template for review form (approve/reject) |

## Interfaces / Contracts

### ReviewForm (articles/forms.py)

```python
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comments', 'feedback']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comentarios internos (requerido)...'}),
            'feedback': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Sugerencias para el autor (opcional)...'}),
        }
        labels = {
            'comments': 'Comentarios internos *',
            'feedback': 'Sugerencias para el autor',
        }

    def __init__(self, *args, **kwargs):
        self.decision = kwargs.pop('decision', None)
        super().__init__(*args, **kwargs)
        if self.decision:
            self.instance.decision = self.decision
```

### ReviewFormView (articles/views.py)

```python
class ReviewFormView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Handle GET (show form) and POST (create Review + update status) for approve/reject."""
    
    def test_func(self):
        return self.request.user.role == 'editor'
    
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.status != 'pending':
            messages.error(request, "Este artículo no está pendiente de revisión")
            return redirect('work_dashboard')
        
        decision = 'approve' if 'approve' in request.path else 'reject'
        form = ReviewForm(decision=decision)
        return render(request, 'articles/review_form.html', {
            'form': form, 'article': article, 'decision': decision
        })
    
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.status != 'pending':
            messages.error(request, "Este artículo no está pendiente de revisión")
            return redirect('work_dashboard')
        
        decision = 'approve' if 'approve' in request.path else 'reject'
        form = ReviewForm(request.POST, decision=decision)
        
        if form.is_valid():
            with transaction.atomic():
                review = form.save(commit=False)
                review.article = article
                review.reviewer = request.user
                review.decision = decision
                review.save()
                
                article.status = 'published' if decision == 'approve' else 'rejected'
                article.save()
            
            messages.success(request, f"Artículo {'aprobado' if decision == 'approve' else 'rechazado'} correctamente")
            return redirect('work_dashboard')
        
        return render(request, 'articles/review_form.html', {
            'form': form, 'article': article, 'decision': decision
        })
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `ReviewForm` validation: comments required, feedback optional, decision pre-filled | `TestCase` in `editorial/tests.py` — instantiate form with various inputs |
| Unit | `ReviewFormView.test_func` allows editors, denies reviewers/readers | `TestCase` — create users with different roles, call view, assert 403/200 |
| Integration | Approve flow: GET shows form, POST creates Review + publishes article atomically | `TestCase` in `articles/tests.py` — login editor, GET `/review/<id>/approve/`, POST valid data, assert Review exists, article.status='published' |
| Integration | Reject flow: GET shows form, POST creates Review + rejects article atomically | Same pattern with reject URL |
| Integration | Validation error: empty comments → form error, no Review created, status unchanged | POST empty comments, assert form errors, assert no Review, article.status='pending' |
| Integration | Non-pending article: approve/reject shows error, no Review created | Set article.status='published', attempt approve, assert error message |
| Integration | Review history display: author sees feedback, editors see all fields | `TestCase` — create article with reviews, login as author/editor, GET article_detail, assert template context contains reviews |
| Integration | Resubmission: rejected → author edits → send_to_review → status=pending → new review cycle | `TestCase` — full cycle test per spec scenario |
| Integration | Rename: `article_create` URL works, `ArticleCreateView`/`ArticleForm`/`article_form.html` used | `TestCase` — login reviewer, GET/POST article_create, assert Article created |

## Threat Matrix

N/A — no routing, shell, subprocess, VCS/PR automation, executable-file classification, or process-integration boundary.

## Migration / Rollout

No migration required. Review model unchanged. New Review records created going forward. Rollback: revert code changes only (views, forms, urls, templates); existing Review records remain harmless.

## Open Questions

- [ ] None — all design decisions resolved concretely above.

(End of file - total ~780 words)
# Proposal: Integrar modelo Review en flujo editorial

## Intent

The `Review` model exists but is never used. Editor approvals/rejections only flip `Article.status` without recording who decided, what comments were made, or what feedback was given. This change makes the Review model the **source of truth** for editorial decisions — every status change to `published` or `rejected` creates a `Review` record with the editor, decision, comments, and feedback. Authors gain visibility into review history and feedback on rejected articles.

## Scope

### In Scope
- New `ReviewForm` in `articles/forms.py` for editor input (decision, comments, feedback)
- Modify `ApproveArticleView`/`RejectArticleView` to handle GET (show modal) + POST (create Review + update status)
- Update `work_dashboard.html`: replace direct approve/reject buttons with modal-triggering buttons
- Add review history section to `article_detail.html` showing all reviews for the article
- Rename misnamed `ReviewCreateView` → `ArticleCreateView` and `ReviewCreateForm` → `ArticleForm`
- Ensure resubmission (author edits rejected article → sends to review) starts a new review cycle

### Out of Scope
- Reviewer role workflow changes (reviewers currently create articles, not reviews)
- Email/notification system for review events
- Review assignment (editor picks article from dashboard — unchanged)
- Analytics/reporting on review metrics
- Migration of historical status changes to Review records (no-op; only future changes)

## Capabilities

### New Capabilities
- `editorial-review`: Editor submits structured review (decision + comments + feedback) that creates Review record and updates Article.status atomically
- `review-history-display`: Author and editors can view chronological review history on article detail page

### Modified Capabilities
- `article-workflow`: Status transitions (pending→published, pending→rejected) now require Review creation; status alone no longer sufficient for audit trail

## Approach

**Inline Review Creation in Approve/Reject Views** (from exploration).

1. **New `ReviewForm`**: Fields — `decision` (hidden, pre-filled by view), `comments` (required), `feedback` (optional, shown to author on rejection).
2. **Views**: `ApproveArticleView` and `RejectArticleView` become `FormView`-style: GET renders modal via HTMX/fragment; POST validates form, creates `Review(reviewer=request.user, article=article, decision=..., comments=..., feedback=...)`, updates `article.status`, redirects to dashboard.
3. **Template**: `work_dashboard.html` — each editor row gets a button opening a modal with the review form (HTMX `hx-get` to view, `hx-post` to same URL). No full page reload.
4. **Article Detail**: New section "Historial de revisiones" listing `article.reviews.all` with reviewer, decision, comments, feedback, timestamp.
5. **Renames**: `ReviewCreateView` → `ArticleCreateView`, `ReviewCreateForm` → `ArticleForm`, URL `review_create` → `article_create`, template `review_create.html` → `article_form.html`.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `articles/forms.py` | New | Add `ReviewForm`; rename `ReviewCreateForm` → `ArticleForm` |
| `articles/views.py` | Modified | `ApproveArticleView`, `RejectArticleView` become form-handling views; rename `ReviewCreateView` → `ArticleCreateView` |
| `articles/urls.py` | Modified | Update URL names for renamed views |
| `articles/templates/articles/work_dashboard.html` | Modified | Editor actions use modal with review form |
| `articles/templates/articles/article_detail.html` | Modified | Add review history section |
| `articles/templates/articles/review_create.html` | Renamed | → `article_form.html` (used by ArticleCreateView/ArticleUpdateView) |
| `editorial/models.py` | None | Model unchanged; may add helper property later |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Modal/HTMX complexity blocks editors | Medium | Start with simple POST form (full page); enhance to modal in follow-up |
| Renaming breaks existing templates/URLs | Low | Grep all references; update atomically in same commit |
| Feedback field confusion (editor vs author view) | Low | Clear label: "Comentarios internos" (comments) vs "Sugerencias para el autor" (feedback); only feedback shown to author |
| Resubmission creates duplicate reviews | Low | Each editor action creates one Review; model supports multiple via FK |

## Rollback Plan

1. Revert `articles/forms.py`, `articles/views.py`, `articles/urls.py` to pre-change state
2. Revert template changes (`work_dashboard.html`, `article_detail.html`, rename `article_form.html` back to `review_create.html`)
3. No DB migration needed (Review model unchanged; new records simply stop being created)
4. Existing Review records remain in DB (harmless)

## Dependencies

- Django HTMX (django-htmx) if modal approach used; otherwise standard Django forms
- No new packages required for base implementation

## Success Criteria

- [ ] Editor clicks "Aprobar" → modal opens → fills comments/feedback → submits → Review created with `decision='approve'` + `article.status='published'`
- [ ] Editor clicks "Rechazar" → modal opens → fills comments/feedback → submits → Review created with `decision='reject'` + `article.status='rejected'`
- [ ] Author views rejected article → sees "Historial de revisiones" with editor feedback
- [ ] Author edits rejected article → "Enviar a revisión" → new review cycle starts (new Review on next editor action)
- [ ] All existing tests pass; new tests cover Review creation on approve/reject
- [ ] Renamed views/URLs work without 404s
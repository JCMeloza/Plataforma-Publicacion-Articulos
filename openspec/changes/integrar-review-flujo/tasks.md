# Tasks: Integrar Review en Flujo Editorial

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 420-480 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 (Foundation) → PR 2 (Core Flow) → PR 3 (History Display) |
| Delivery strategy | auto-chain |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: stacked-to-main
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Forms, URLs, rename foundation | PR 1 | `python manage.py test articles.tests.ReviewFormTests editorial.tests.ReviewFormTests` | N/A (unit tests only) | Revert forms.py, urls.py, template rename |
| 2 | ReviewFormView approve/reject flow | PR 2 | `python manage.py test articles.tests.ReviewFlowTests` | `python manage.py runserver` + editor login → approve/reject pending article | Revert views.py, work_dashboard.html |
| 3 | Review history display + resubmission | PR 3 | `python manage.py test articles.tests.ReviewHistoryTests editorial.tests.ReviewHistoryTests` | `python manage.py runserver` + author/editor login → article detail | Revert article_detail.html, review_form.html |

## Phase 1: Foundation (Forms, URLs, Rename)

- [x] 1.1 Create `ReviewForm` in `articles/forms.py` with `comments` (required), `feedback` (optional), `decision` pre-fill via `__init__`
- [x] 1.2 Write RED tests for `ReviewForm` validation in `editorial/tests.py`: comments required, feedback optional, decision pre-filled
- [x] 1.3 Run tests → GREEN: implement `ReviewForm` to pass validation tests
- [x] 1.4 Rename `ReviewCreateForm` → `ArticleForm` in `articles/forms.py`; update imports
- [x] 1.5 Write RED tests for rename verification in `articles/tests.py`: `article_create` URL works, `ArticleCreateView`/`ArticleForm` used
- [x] 1.6 Run tests → GREEN: update `ArticleCreateView` (rename from `ReviewCreateView`), `ArticleUpdateView` to use `ArticleForm`
- [x] 1.7 Update `articles/urls.py`: add `review_approve`/`review_reject` URLs; rename `review_create` → `article_create`
- [x] 1.8 Rename template `articles/templates/articles/review_create.html` → `article_form.html`
- [x] 1.9 Update `ArticleCreateView.template_name` and `ArticleUpdateView.template_name` to `articles/article_form.html`

## Phase 2: Core Implementation (ReviewFormView Flow)

- [x] 2.1 Write RED tests for `ReviewFormView.test_func` in `articles/tests.py`: editors allowed (200), reviewers/readers denied (403)
- [x] 2.2 Run tests → GREEN: create `ReviewFormView` in `articles/views.py` with `LoginRequiredMixin`, `UserPassesTestMixin`, `test_func` checking `role == 'editor'`
- [x] 2.3 Write RED tests for approve GET: shows form with decision='approve' pre-filled
- [x] 2.4 Run tests → GREEN: implement `ReviewFormView.get()` with non-pending check, render `review_form.html`
- [x] 2.5 Write RED tests for approve POST: valid data → creates Review + publishes article atomically, redirects to dashboard
- [x] 2.6 Run tests → GREEN: implement `ReviewFormView.post()` with `transaction.atomic()`, Review creation, status update
- [x] 2.7 Write RED tests for reject GET/POST: symmetric to approve with decision='reject', status='rejected'
- [x] 2.8 Run tests → GREEN: ensure reject path works identically
- [x] 2.9 Write RED tests for validation error: empty comments → form error, no Review created, status unchanged
- [x] 2.10 Run tests → GREEN: form validation naturally handles this
- [x] 2.11 Write RED tests for non-pending article: approve/reject shows error, redirects, no Review created
- [x] 2.12 Run tests → GREEN: non-pending check in both GET/POST returns error message
- [x] 2.13 Create `articles/templates/articles/review_form.html` template with form, decision context, cancel link
- [x] 2.14 Update `articles/templates/articles/work_dashboard.html`: editor "Aprobar"/"Rechazar" buttons link to `review_approve`/`review_reject` URLs (GET) instead of direct POST forms

## Phase 3: Integration (Review History Display)

- [ ] 3.1 Write RED tests for review history visibility in `articles/tests.py`: author sees feedback, editors see all fields, non-author non-editor sees nothing
- [ ] 3.2 Run tests → GREEN: add "Historial de revisiones" section to `articles/templates/articles/article_detail.html` using `article.reviews.all|dictsort:"created_at"`
- [ ] 3.2.1 Template shows: reviewer name, decision badge (Aprobado/Rechazado), comments, feedback, timestamp
- [ ] 3.2.2 Visibility: show section only if `user == article.autor` or `user.role == 'editor'` and `article.reviews.exists`
- [ ] 3.3 Write RED tests for resubmission cycle in `articles/tests.py`: rejected → author edits → send_to_review → status=pending → new review cycle creates second Review
- [ ] 3.4 Run tests → GREEN: verify `SendToReviewView` already handles this (status reset to pending, reviews preserved)
- [ ] 3.5 Write RED tests for multiple review rounds: 3 cycles (reject, reject, approve) → 3 Review records queryable
- [ ] 3.6 Run tests → GREEN: confirm chronological display works

## Phase 4: Cleanup & Verification

- [ ] 4.1 Remove old `ApproveArticleView` and `RejectArticleView` from `articles/views.py`
- [ ] 4.2 Remove old `approve_article` and `reject_article` URL patterns from `articles/urls.py` (replaced by review_approve/review_reject)
- [ ] 4.3 Run full test suite: `python manage.py test articles editorial`
- [ ] 4.4 Verify all spec scenarios pass manually via `python manage.py runserver`
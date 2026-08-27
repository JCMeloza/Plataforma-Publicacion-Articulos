# Apply Progress: integrar-review-flujo — PR 1 Foundation + PR 2 Core Flow + PR 3 History Display (stacked-to-main)

## Change
integrar-review-flujo
## Mode
Strict TDD (venv/bin/python manage.py test)

## Completed Tasks (Phase 1: Foundation)

- [x] 1.1 Create `ReviewForm` in `articles/forms.py` with `comments` (required), `feedback` (optional), `decision` pre-fill via `__init__`
- [x] 1.2 Write RED tests for `ReviewForm` validation in `editorial/tests.py`: comments required, feedback optional, decision pre-filled
- [x] 1.3 Run tests → GREEN: implement `ReviewForm` to pass validation tests
- [x] 1.4 Rename `ReviewCreateForm` → `ArticleForm` in `articles/forms.py`; update imports
- [x] 1.5 Write RED tests for rename verification in `articles/tests.py`: `article_create` URL works, `ArticleCreateView`/`ArticleForm` used
- [x] 1.6 Run tests → GREEN: update `ArticleCreateView` (rename from `ReviewCreateView`), `ArticleUpdateView` to use `ArticleForm`
- [x] 1.7 Update `articles/urls.py`: add `review_approve`/`review_reject` URLs; rename `review_create` → `article_create`
- [x] 1.8 Rename template `articles/templates/articles/review_create.html` → `article_form.html`
- [x] 1.9 Update `ArticleCreateView.template_name` and `ArticleUpdateView.template_name` to `articles/article_form.html`

## Completed Tasks (Phase 2: Core Flow)

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

## Completed Tasks (Phase 3: Review History Display)

- [x] 3.1 Write RED tests for review history visibility in `articles/tests.py`: author sees feedback, editors see all fields, non-author non-editor sees nothing
- [x] 3.2 Run tests → GREEN: add "Historial de revisiones" section to `articles/templates/articles/article_detail.html` using `article.reviews.all|dictsort:"created_at"`
- [x] 3.2.1 Template shows: reviewer name, decision badge (Aprobado/Rechazado), comments, feedback, timestamp
- [x] 3.2.2 Visibility: show section only if `user == article.autor` or `user.role == 'editor'` and `article.reviews.exists`
- [x] 3.3 Write RED tests for resubmission cycle in `articles/tests.py`: rejected → author edits → send_to_review → status=pending → new review cycle creates second Review
- [x] 3.4 Run tests → GREEN: verify `SendToReviewView` already handles this (status reset to pending, reviews preserved)
- [x] 3.5 Write RED tests for multiple review rounds: 3 cycles (reject, reject, approve) → 3 Review records queryable
- [x] 3.6 Run tests → GREEN: confirm chronological display works

## Files Changed

| File | Action | What Was Done |
|------|--------|---------------|
| `articles/forms.py` | Modified (PR1) | Added `ReviewForm` (ModelForm for Review, comments/feedback, decision via __init__); renamed `ReviewCreateForm` → `ArticleForm` with backward alias |
| `articles/views.py` | Modified (PR1+PR2) | PR1: Renamed `ReviewCreateView` → `ArticleCreateView`, updated `ArticleUpdateView` to use `ArticleForm`; updated template_name to `article_form.html`; added stub `ReviewFormView`. PR2: Implemented full `ReviewFormView` GET/POST with `transaction.atomic()`, Review creation + status update, non-pending guard, decision via request.path, messages.success/error |
| `articles/urls.py` | Modified (PR1) | Renamed `review_create` → `article_create`; added `review_approve`/`review_reject` URL patterns |
| `articles/templates/articles/article_form.html` | Renamed (PR1) | `review_create.html` → `article_form.html` (same content, new path) |
| `articles/templates/articles/review_create.html` | Deleted (PR1 fix in PR2) | Removed stale template (rename cleanup missed in PR1 commit, now removed) |
| `articles/templates/articles/review_form.html` | Created (PR2) | New template for review form: decision-aware header, article summary, comments/feedback fields with error display, approve/reject submit + cancel link |
| `articles/templates/articles/work_dashboard.html` | Modified (PR1+PR2) | PR1: Updated `{% url 'review_create' %}` → `{% url 'article_create' %}`. PR2: Replaced editor POST forms (`approve_article`/`reject_article`) with GET links to `review_approve`/`review_reject` |
| `editorial/tests.py` | Modified (PR1) | Added 13 ReviewFormTests (TDD RED→GREEN) |
| `articles/tests.py` | Modified (PR1+PR2+PR3) | PR1: Added 11 tests: ArticleFormRenameTests + ArticleCreateUrlTests. PR2: Added 22 ReviewFormViewTests (TDD RED→GREEN) covering permissions, GET/POST approve/reject, validation, non-pending, work_dashboard links. PR3: Added 13 tests: ReviewHistoryVisibilityTests (10), ReviewResubmissionTests (2), MultipleReviewRoundsTests (1) |
| `articles/views.py` | Modified (PR3) | Added `reviews` (ordered by created_at) and `can_view_history` (author or editor) to `ArticleDetailView.get_context_data` |
| `articles/templates/articles/article_detail.html` | Modified (PR3) | Added "Historial de revisiones" section: loops `reviews` chronologically, shows reviewer username, decision badge (Aprobado/Rechazado), comments, feedback, timestamp; visible only if `can_view_history and reviews` |
| `openspec/changes/integrar-review-flujo/tasks.md` | Modified | Marked Phase 1 (1.1–1.9), Phase 2 (2.1–2.14), Phase 3 (3.1–3.6) as [x]; fixed duplicate numbering 2.11/2.12 → 2.13/2.14 |

## TDD Cycle Evidence (Strict TDD Mode)

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1-1.3 ReviewForm | `editorial/tests.py` (ReviewFormTests) | Unit | ✅ 0/0 (no prior tests) — baseline | ✅ ImportError: cannot import ReviewForm | ✅ 13/13 passed (venv/bin/python manage.py test editorial.tests.ReviewFormTests) | ✅ 13 cases (comments required, whitespace, feedback optional/omitted, both valid, decision approve/reject/none, with data, meta fields/model, widgets, labels) | ✅ Clean — widgets/labels extracted per design, no duplication |
| 1.4-1.6 Rename ArticleForm/View | `articles/tests.py` (ArticleFormRenameTests + ArticleCreateUrlTests) | Unit+Integration | ✅ 13/13 ReviewFormTests still passing before rename work | ✅ ImportError: cannot import ArticleForm | ✅ 11/11 passed (venv/bin/python manage.py test articles.tests...) | ✅ 11 cases (form import, meta, view import, form_class, template_name x2, URL resolve, GET 200, POST creates article, old URL NoReverseMatch) | ✅ Clean — alias kept for backward compat, no duplication |
| 1.7 URLs | Same `articles/tests.py` | Integration | ✅ above | ✅ reverse('review_create') should fail — proved | ✅ reverse('article_create') resolves + review_approve/review_reject exist | ✅ Multiple URL cases (resolve, reverse, NoReverseMatch) | ➖ None needed — URL patterns declarative |
| 1.8-1.9 Template rename | Same `articles/tests.py` | Integration | ✅ above | ✅ template article_form.html missing would fail | ✅ assertTemplateUsed passes after rename | ✅ GET + POST both verify template | ➖ None needed — file move |
| 2.1-2.2 test_func permissions | `articles/tests.py` (ReviewFormViewTests) | Integration | ✅ 24/24 (PR1 tests) baseline before Phase 2 | ✅ editor GET 302 != 200 (stub redirected), reviewer 403 already, but editor disallowed | ✅ 22/22 passed (venv/bin/python manage.py test articles.tests.ReviewFormViewTests) | ✅ 5 cases: editor 200, reviewer 403, reader 403, reviewer reject 403, unauth 302→login | ✅ Clean — test_func is one-liner `role == 'editor'` |
| 2.3-2.4 Approve GET + non-pending | Same `articles/tests.py` | Integration | ✅ above | ✅ approve GET 302 != 200 (stub "Flujo de revisión en construcción") | ✅ approve GET renders review_form.html with decision='approve', form.decision correct; reject symmetric | ✅ 2 decisions × 2 paths (approve/reject GET) + non-pending redirect for published/draft/rejected (3 articles) | ✅ Clean — decision via `'approve' in request.path`, render with dict |
| 2.5-2.8 Approve/Reject POST happy paths | Same `articles/tests.py` | Integration | ✅ above | ✅ POST DoesNotExist (Review not created) + status not changed | ✅ approve POST → Review approve + published, approve without feedback, reject POST → Review reject + rejected, reject without feedback — all redirect to work_dashboard | ✅ 4 cases (approve with/without feedback, reject with/without feedback) + atomic check (Review exists + status updated together) | ✅ Clean — transaction.atomic(), messages.success |
| 2.9-2.10 Validation error | Same `articles/tests.py` | Integration | ✅ above | ✅ POST 302 != 200 (stub always redirected, no form error) | ✅ empty comments → 200 with form error, no Review, status pending; whitespace also fails | ✅ 3 cases: empty approve, empty reject, whitespace approve | ✅ Clean — form validation naturally handles, render review_form.html with errors |
| 2.11-2.12 Non-pending guard | Same `articles/tests.py` | Integration | ✅ above | ✅ already 302 (stub) but not verified Review not created; now proves | ✅ GET/POST non-pending → redirect work_dashboard, no Review, status unchanged for published/draft/rejected | ✅ 4 cases: approve GET/POST non-pending, reject GET/POST non-pending + POST perms 403 no Review | ✅ Clean — guard at top of get/post before form handling |
| 2.13 review_form.html template | Same `articles/tests.py` | Integration | ✅ above | ✅ TemplateDoesNotExist before creation | ✅ assertTemplateUsed passes, contains decision, form, article summary, cancel link | ✅ covered by GET tests (template used) | ➖ None needed — simple template |
| 2.14 work_dashboard links | Same `articles/tests.py` | Integration | ✅ above | ✅ Couldn't find '/review/1/approve/' in response | ✅ Contains approve_url and reject_url + "Aprobar"/"Rechazar" text | ✅ link check for both URLs + text | ✅ Clean — <a href> replaces <form> |
| 3.1-3.2 Review history visibility | `articles/tests.py` (ReviewHistoryVisibilityTests) | Integration | ✅ 46/46 (PR1+PR2) baseline before Phase 3 | ✅ Couldn't find 'Historial de revisiones' in response (6 failures) | ✅ 10/10 passed (venv/bin/python manage.py test articles.tests.ReviewHistoryVisibilityTests) | ✅ 10 cases: author rejected sees feedback+comments+timestamp, author published sees Aprobado, editor sees all, editor non-reviewer sees history, other reviewer 403 hidden, reader hidden, anonymous hidden, draft no reviews no leak, multi chronological order, non-author no feedback leak | ✅ Clean — view adds reviews ordered + can_view_history; template checks can_view_history and reviews |
| 3.3-3.4 Resubmission cycle | `articles/tests.py` (ReviewResubmissionTests) | Integration | ✅ above | ✅ Already GREEN (rejected→edit→draft→pending→approve works without code change) — but history not visible until 3.2 | ✅ 2/2 passed (rejected→edit→send→pending→second review, preserve reviews) | ✅ 2 cases: full cycle reject→resubmit→approve (2 reviews), preserve check (count before/after) | ✅ Clean — SendToReviewView already handles draft→pending after edit reset; no change needed |
| 3.5-3.6 Multiple rounds | `articles/tests.py` (MultipleReviewRoundsTests) | Integration | ✅ above | ✅ Couldn't find 'Historial de revisiones' after 3 cycles (history missing) | ✅ 1/1 passed (3 cycles reject,reject,approve → 3 reviews, order C1<C2<C3, history visible) | ✅ 1 case with 3 round-trip cycles + chronological assert C1<C2<C3 | ✅ Clean — chronological display via order_by created_at |

### Test Summary
- **Total tests written**: 59 (13 editorial + 46 articles)
- **Total tests passing**: 59/59 (PR1 24 + PR2 22 + PR3 13)
- **Layers used**: Unit (13), Integration (46), E2E (0)
- **Approval tests** (refactoring): None — Phase 3 is new display + resubmission flow (reuse of Article/Review via FK guarded by safety net 46/46)
- **Pure functions created**: 0 (Django class-based views — logic in get_context_data + template conditionals)

## Work Unit Evidence (PR 3 History Display)

| Evidence | Required value |
|---|---|
| Focused test command and exact result | `venv/bin/python manage.py test articles.tests.ReviewHistoryVisibilityTests articles.tests.ReviewResubmissionTests articles.tests.MultipleReviewRoundsTests` → **OK (13 tests, 0 failures)** |
| Full suite command and exact result | `venv/bin/python manage.py test` → **OK (59 tests, 0 failures)** — PR1+PR2 tests still pass, no regressions |
| Runtime harness command/scenario and exact result | `venv/bin/python manage.py test` integration harness proves full flow; manual harness `python manage.py runserver` + author/editor login → article detail shows Historial chronologically → verified via integration tests (GET article_detail with can_view_history). Explicit N/A for pure runserver manual step in CI (integration tests cover same path) |
| Rollback boundary | Revert `articles/views.py` (remove reviews + can_view_history from ArticleDetailView), `articles/templates/articles/article_detail.html` (remove Historial section), `articles/tests.py` (remove 13 ReviewHistory/Resubmission/Multiple tests), `openspec/changes/integrar-review-flujo/tasks.md` Phase 3 marks. No DB migration, no changes to editorial/models.py, articles/forms.py, urls.py |

## Work Unit Evidence (PR 2 Core Flow) — preserved

| Evidence | Required value |
|---|---|
| Focused test command and exact result | `venv/bin/python manage.py test articles.tests.ReviewFormViewTests` → **OK (22 tests, 0 failures)** |
| Full suite command and exact result | `venv/bin/python manage.py test` → **OK (46 tests, 0 failures)** — PR1 tests still pass, no regressions |
| Runtime harness command/scenario and exact result | `venv/bin/python manage.py test` integration harness proves full flow; manual harness `python manage.py runserver` + editor login → approve/reject pending article → verified via integration tests (GET form → POST Review+status → redirect dashboard). Explicit N/A for pure runserver manual step in CI (integration tests cover same path) |
| Rollback boundary | Revert `articles/views.py` (ReviewFormView full → stub), `articles/templates/articles/review_form.html` (delete), `articles/templates/articles/work_dashboard.html` (GET links → POST forms), `articles/tests.py` (remove 22 ReviewFormViewTests), `openspec/changes/integrar-review-flujo/tasks.md` Phase 2 marks. No DB migration, no changes to editorial/models.py or articles/forms.py |

## Work Unit Evidence (PR 1 Foundation) — preserved

| Evidence | Required value |
|---|---|
| Focused test command and exact result | `venv/bin/python manage.py test editorial.tests.ReviewFormTests articles.tests.ArticleFormRenameTests articles.tests.ArticleCreateUrlTests` → **OK (24 tests, 0 failures)** |
| Full suite command and exact result | `venv/bin/python manage.py test` → **OK (24 tests, 0 failures)** — no regressions |
| Runtime harness command/scenario and exact result | N/A (unit tests only) — PR1 has no runtime boundary per workload forecast (forms/URLs/rename foundation) |
| Rollback boundary | Revert `articles/forms.py`, `articles/views.py`, `articles/urls.py`, `articles/templates/articles/article_form.html` (rename back), `articles/templates/articles/work_dashboard.html`, `editorial/tests.py`, `articles/tests.py` — no DB migration, no config change |

## Deviations from Design
- PR1: None — implementation matches design.md exactly. review_approve/review_reject URLs added as stub view to keep PR1 autonomous and routable.
- PR2: None — implementation matches design.md exactly. `ReviewFormView` GET/POST copied verbatim from design (decision via `'approve' in request.path`, `ReviewForm(decision=decision)`, `transaction.atomic()` with Review.save() + article.save(), messages.success/error, redirect to `work_dashboard`). Template `review_form.html` follows design contract (form, decision context, cancel link). `work_dashboard.html` editor buttons now GET links as specified. Duplicate task numbers 2.11/2.12 in original tasks.md fixed to 2.13/2.14 for clarity.
- PR3: None — implementation matches design.md exactly. `ArticleDetailView` adds `reviews` ordered by `created_at` and `can_view_history` (author == article.autor or role == editor) per spec visibility rules. Template `article_detail.html` renders "Historial de revisiones" with reviewer, decision badge (Aprobado/Rechazado), comments, feedback, timestamp, gated by `can_view_history and reviews`. Resubmission verified: `SendToReviewView` already handles rejected→draft→pending via `ArticleUpdateView` reset, no change needed.

## Issues Found
- PR1: Staticfiles manifest missing on first test run (article_create GET renders base.html → static). Fixed via `collectstatic`. Not a design issue. Initial git mv failed because destination existed via cp; fixed via rm + add.
- PR2: PR1 rename left `review_create.html` tracked but deleted in working tree (git rm not committed). Fixed in PR2 via `git rm` (91-line deletion now in PR2 diff). No impact on functionality; pure rename artifact.
- PR2: Initial RED proved 8 failures + 3 errors (stub returned 302 "Flujo de revisión en construcción" instead of 200 form, and did not create Review records). All GREEN after implementation.
- PR3: Initial RED proved 6 failures (history not rendered, 3 cycles history missing). Non-author/anonymous negative cases already passed (correctly hidden). GREEN after adding `can_view_history` + `reviews` context and template section. Resubmission cycle already GREEN without code change (rejected→edit→draft→pending via ArticleUpdateView+SendToReviewView) — confirmed via 2 resubmission tests. All 13 new tests GREEN on first implementation pass (no second fix needed).

## Remaining Tasks (Not in this PR)
- Phase 4: Cleanup (remove ApproveArticleView/RejectArticleView, old URL names) (tasks 4.1–4.4)

## Workload / PR Boundary
- Mode: stacked PR slice (stacked-to-main)
- Current work unit: PR 3 — History Display + Resubmission — Unit 3 per workload forecast
- Boundary: Starts from ArticleDetailView without history (no reviews/can_view_history), ends with ArticleDetailView adding reviews ordered + can_view_history, article_detail.html Historial section (reviewer, badge Aprobado/Rechazado, comments, feedback, timestamp, visibility author/editor only), plus resubmission/multi-round tests proving rejected→edit→pending→new review accumulates history. No Phase 4 cleanup.
- Estimated review budget impact: PR3 alone ~260 lines (tests 180 + views 10 + template 25 + docs 45). Well under 400. Total stacked (PR1+PR2+PR3) ~1050 lines across three PRs, each slice reviewable.

## Status
29/35 tasks complete (Phase 1 + Phase 2 + Phase 3 done). Ready for next batch (PR 4 Cleanup). PR 3 is autonomous and revertible (chain: main 8dc23fa ← PR2 9cb9eed ← PR3 this branch).

## Commits Made
- `8dc23fa` feat(articles): add ReviewForm and rename article creation flow (PR1 foundation) — on main
- `9cb9eed` feat(articles): implement ReviewFormView approve/reject flow (PR2 core flow) — on feat/integrar-review-flujo-pr2-core-flow
- PR3 commit pending on `feat/integrar-review-flujo-pr3-history` (this branch, stacked on PR2)

## Next Recommended
sdd-apply for Phase 4 (tasks 4.1–4.4) as PR 4 cleanup stacked to main. Or sdd-verify if Phase 4 is trivial cleanup.

# Apply Progress: integrar-review-flujo — PR 1 Foundation + PR 2 Core Flow (stacked-to-main)

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
| `articles/tests.py` | Modified (PR1+PR2) | PR1: Added 11 tests: ArticleFormRenameTests + ArticleCreateUrlTests. PR2: Added 22 ReviewFormViewTests (TDD RED→GREEN) covering permissions, GET/POST approve/reject, validation, non-pending, work_dashboard links |
| `openspec/changes/integrar-review-flujo/tasks.md` | Modified | Marked Phase 1 (1.1–1.9) and Phase 2 (2.1–2.14) as [x]; fixed duplicate numbering 2.11/2.12 → 2.13/2.14 |

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

### Test Summary
- **Total tests written**: 46 (13 editorial + 33 articles)
- **Total tests passing**: 46/46 (PR1 24 + PR2 22)
- **Layers used**: Unit (13), Integration (33), E2E (0)
- **Approval tests** (refactoring): None — Phase 2 is new flow, not refactoring (reuse of Article model guarded by safety net 24/24)
- **Pure functions created**: 0 (Django class-based views — logic is in get/post with transaction.atomic)

## Work Unit Evidence (PR 2 Core Flow)

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

## Issues Found
- PR1: Staticfiles manifest missing on first test run (article_create GET renders base.html → static). Fixed via `collectstatic`. Not a design issue. Initial git mv failed because destination existed via cp; fixed via rm + add.
- PR2: PR1 rename left `review_create.html` tracked but deleted in working tree (git rm not committed). Fixed in PR2 via `git rm` (91-line deletion now in PR2 diff). No impact on functionality; pure rename artifact.
- PR2: Initial RED proved 8 failures + 3 errors (stub returned 302 "Flujo de revisión en construcción" instead of 200 form, and did not create Review records). All GREEN after implementation.

## Remaining Tasks (Not in this PR)
- Phase 3: Review history display on article_detail, resubmission cycles (tasks 3.1–3.6)
- Phase 4: Cleanup (remove ApproveArticleView/RejectArticleView, old URL names) (tasks 4.1–4.4)

## Workload / PR Boundary
- Mode: stacked PR slice (stacked-to-main)
- Current work unit: PR 2 — Core Flow (ReviewFormView approve/reject) — Unit 2 per workload forecast
- Boundary: Starts from stub ReviewFormView (redirects) + POST forms in work_dashboard, ends with full ReviewFormView GET (render review_form.html with decision pre-fill, non-pending guard) + POST (validate → transaction.atomic Review creation + status update → redirect) for approve/reject, validation errors, permission 403, atomicity, work_dashboard GET links, review_form.html template, all tested (22 new tests). No Phase 3 history display.
- Estimated review budget impact: PR2 alone ~471 lines (360 insertions + 111 deletions incl. 91-line rename cleanup). Net new logic ~380 lines (73 template + 256 tests + 41 views + 10 dashboard) if excluding 91-line PR1 rename artifact; total stacked (PR1+PR2) ~793 lines across two PRs, each slice reviewable. Next PR3 estimated 150-200 lines.
- Note: 471 slightly over 400 due to verbose test coverage (22 integration tests) + carrying PR1 rename deletion; reviewer focus still healthy (one behavior: review flow) and tests are with code per work-unit-commits.

## Status
23/35 tasks complete (Phase 1 + Phase 2 done). Ready for next batch (PR 3 History Display). PR 2 is autonomous and revertible.

## Commits Made
- `8dc23fa` feat(articles): add ReviewForm and rename article creation flow (PR1 foundation) — on main
- PR2 commit pending on `feat/integrar-review-flujo-pr2-core-flow` (this branch)

## Next Recommended
sdd-apply for Phase 3 (tasks 3.1–3.6) as PR 3 stacked to main (branched from main after PR2 merges, per stacked-to-main). Or sdd-verify if Phase 3+4 are done together as final slice.

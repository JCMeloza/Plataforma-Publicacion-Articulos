# Archive Report: integrar-review-flujo

**Change**: `integrar-review-flujo`
**Archived**: 2026-08-27
**Archived to**: `openspec/changes/archive/2026-08-27-integrar-review-flujo/`
**Mode**: hybrid (OpenSpec + Engram)
**Status**: archived — SDD cycle complete

## Final State Authority

This report describes the state AT CLOSE. It outranks intermediate snapshots per the Final-State Authority hierarchy (reviewGate > tasks artifact > explicit final-state facts in orchestrator launch prompt > verify-report / apply-progress).

- **Commit chain (final)**: `main 8dc23fa` (PR1 foundation) <- `9cb9eed` (PR2 core flow, feat/integrar-review-flujo-pr2-core-flow) <- `6fe680d` (PR3 history, feat/integrar-review-flujo-pr3-history) <- `275f616` (PR4 cleanup, feat/integrar-review-flujo-pr4-cleanup, current HEAD, commit message: `refactor(articles): remove legacy Approve/Reject views and URLs (PR4 cleanup)`). All 4 stacked work units implemented, committed, and verified.
- **Stale claim resolved**: `apply-progress.md` line "PR4 commit pending on feat/integrar-review-flujo-pr4-cleanup (this branch, stacked on PR3)" was stale at the time it was written. Per explicit final-state facts in the orchestrator launch prompt (rank 3) and repository evidence (`git log --oneline` shows `275f616` on current branch), the PR4 commit IS done and committed. This report records the final state, citing commit `275f616`. The stale "pending" text is retained only as history in the archived artifact, not as current fact.
- **Verify warnings NOT fixed in later commits**: Per explicit final-state facts, the 2 WARNINGs and 2 SUGGESTIONs noted in `verify-report` at verification time remain as known non-blocking gaps and were NOT fixed in later commits. They are recorded below as-is without silent resolution.

## Verdict

**PASS WITH WARNINGS** — 0 blockers, 0 critical. All 17 requirements and 29 scenarios compliant. Build `manage.py check` clean, tests `venv/bin/python manage.py test` 65/65 OK (exit 0). Safe to archive under strict-vs-OpenSpec policy.

- Per `verify-report` (observation #36, at verification time) verdict is `pass_with_warnings`.
- No CRITICAL issues exist; archive is not blocked. No override needed beyond recording warnings as known gaps.
- Task Completion Gate: 35/35 checkboxes complete in persisted `tasks.md` (0 unchecked). No stale checkboxes; no reconciliation required.

## Native Review Receipt Gate

- `reviewGate` structurally absent in structured status (kill switch off or no review started for this candidate). Per sdd-archive skill: when `reviewGate` absent, archive proceeds under ordinary repository policy without requiring a receipt. No review topics exist to read; no block.

## Specs Synced

Three delta specs from `openspec/changes/integrar-review-flujo/specs/` were synced into the base capability specs under `openspec/specs/` (no prior `openspec/specs/` existed; delta specs treated as full specs per skill rule "If Main Spec Does NOT Exist, copy mechanically").

| Domain | Action | Details |
|--------|--------|---------|
| editorial-review | Created | `openspec/specs/editorial-review/spec.md` — 4 requirements (Editor Approves, Editor Rejects, Review Form Validation, Resubmission Starts New Review Cycle), 12 scenarios. Mechanical copy via `cp` + `diff -r` + `mv`, empty diff verified. |
| review-history-display | Created | `openspec/specs/review-history-display/spec.md` — 4 requirements (Author Views History, Editor Views History, Visibility Rules, Non-Author Non-Editor Cannot Access), 10 scenarios. Mechanical copy, empty diff verified. |
| article-workflow | Created | `openspec/specs/article-workflow/spec.md` — delta with ADDED (2), MODIFIED (2), RENAMED (3), REMOVED (2) requirements, 7 Given/When/Then scenarios plus structural rename/removal checks. Copied as full spec (no prior base), empty diff verified. |

**Source of truth updated**:
- `openspec/specs/editorial-review/spec.md`
- `openspec/specs/review-history-display/spec.md`
- `openspec/specs/article-workflow/spec.md`

### Mechanical Copy Evidence (MANDATORY readback)

All spec copies used native shell `cp` -> temp file -> `diff -r` -> `mv`, never Read->Write. Verbatim `diff -r` output (empty is passing):

```
# editorial-review
diff source vs temp: (empty output)
diff exit 0 - empty diff (pass)
diff -r "openspec/changes/integrar-review-flujo/specs/editorial-review/spec.md" "openspec/specs/editorial-review/spec.md"
(empty - PASS)

# review-history-display
diff source vs temp: (empty output)
diff exit 0 - empty diff (pass)
diff -r "openspec/changes/integrar-review-flujo/specs/review-history-display/spec.md" "openspec/specs/review-history-display/spec.md"
(empty - PASS)

# article-workflow
diff source vs temp: (empty output)
diff exit 0 - empty diff (pass)
diff -r "openspec/changes/integrar-review-flujo/specs/article-workflow/spec.md" "openspec/specs/article-workflow/spec.md"
(empty - PASS)
```

## Archive Move Evidence (MANDATORY readback)

Entire change folder moved mechanically with snapshot + `diff -r` readback. Verbatim output:

```
snapshot_root=/tmp/sdd-archive.qADCSy
cp -R "openspec/changes/integrar-review-flujo" "$snapshot_root/source" -> snapshot cp ok
git mv "openspec/changes/integrar-review-flujo" "openspec/changes/archive/2026-08-27-integrar-review-flujo" -> git mv succeeded
source gone confirmed
diff -r "$snapshot_root/source" "openspec/changes/archive/2026-08-27-integrar-review-flujo"
(empty output)
diff exit 0 - empty diff (pass)
```

`archive-report.md` is additive-only and excluded from the source/destination comparison per the Mechanical Copy Contract (it did not exist in the source snapshot at move time; it was written afterward inside the archived folder). No truncation or alteration detected.

## Archive Contents

| Artifact | Location | Status |
|----------|----------|--------|
| proposal.md | `openspec/changes/archive/2026-08-27-integrar-review-flujo/proposal.md` | ✅  |
| specs/editorial-review/spec.md | archived specs/ | ✅  |
| specs/review-history-display/spec.md | archived specs/ | ✅  |
| specs/article-workflow/spec.md | archived specs/ | ✅  |
| design.md | `.../design.md` | ✅  |
| exploration.md | `.../exploration.md` | ✅  |
| tasks.md | `.../tasks.md` (35/35 ✅) | ✅  |
| apply-progress.md | `.../apply-progress.md` (65 tests, 4 work units) | ✅  |
| verify-report.md | `.../verify-report.md` (PASS WITH WARNINGS, 17/17 req, 29/29 scenarios) | ✅  |
| archive-report.md | `.../archive-report.md` (this file) | ✅  |

Archived `tasks.md` has no unchecked implementation tasks. Active changes directory no longer contains `integrar-review-flujo` (`ls openspec/changes/` shows only `archive/`).

## Verification Summary (at close)

- **Build**: `venv/bin/python manage.py check` — System check identified no issues (0 silenced), exit 0, hash `sha256:1e3e63f221bde88816c4a4ef7367691607b20cc1d194028a02ec9ae0586cf9b1` (per verify-report #36).
- **Tests**: `venv/bin/python manage.py test` — 65 passed / 0 failed / 0 skipped, Ran 65 tests in 110.882s, OK, hash `sha256:f31747f6a196df24b8f8131ac5345ef014886dffe01117b42106caa17b1780ac`. Breakdown: 13 `editorial.tests.ReviewFormTests` (unit) + 52 `articles.tests` (ArticleFormRenameTests 7, ArticleCreateUrlTests 4, ReviewFormViewTests 22, ReviewHistoryVisibilityTests 10, ReviewResubmissionTests 2, MultipleReviewRoundsTests 1, OldReviewViewsRemovedTests 6).
- **Coverage**: Not measured (no coverage tool configured) — not a failure; behavioral coverage via 65 integration/unit tests.
- **Linter/Type checker**: Not configured in capabilities; `manage.py check` clean.
- **Design coherence**: 8/8 decisions followed (dedicated page vs modal, atomic Review+status, model keep-as-is, data flow, 7 file changes, ReviewForm/ReviewFormView/ArticleDetailView contracts).
- **TDD compliance**: 6/6 checks passed per verify-report.

## Known Non-Blocking Gaps (carried from verify-report, not fixed post-verify)

Per verify-report observation #36, at verification time:

**WARNINGs (2) — spec met but test gap noted; they were NOT fixed in later commits per explicit final-state facts:**
1. Non-pending error message string not regression-tested: `ReviewFormView` correctly sets `messages.error(request, "Este artículo no está pendiente de revisión")` for non-pending GET/POST, but tests only assert redirect + no Review creation, not the message content/rendering.
2. `SendToReviewView` rejected -> pending requires two-step flow: `SendToReviewView.post` allows `status in ['draft','pending']` -> pending, while `work_dashboard.html` shows "Enviar a Revisión" for `draft or rejected`. Direct POST for `rejected` without prior edit hits error branch (`Este artículo no se puede enviar...`). Spec scenario resubmission is satisfied via documented path `ArticleUpdateView` (rejected->draft) then `SendToReviewView` (draft->pending); single-click rejected->pending is not supported. Matches editorial-review spec but diverges from article-workflow simplified GIVEN.

**SUGGESTIONs (2) — improvement, not failure; NOT fixed post-verify:**
1. Add explicit `draft -> pending` standalone test for article-workflow ADDED scenario "Author sends draft to review (no Review created)" — currently covered indirectly via resubmission chain; isolated test would make spec explicit.
2. Consider deprecating backward-compat aliases `ReviewCreateForm = ArticleForm` and `ReviewCreateView = ArticleCreateView` if no external code depends on them; schedule removal with deprecation warning.

None block the change; archive is intentional-with-known-gaps (non-critical). No CRITICAL issues.

## Delivery

- **Delivery strategy**: `auto-chain` (stacked-to-main PR chain)
- **PR chain**: `main 8dc23fa` (PR1 foundation) <- `9cb9eed` (PR2 core flow) <- `6fe680d` (PR3 history display) <- `275f616` (PR4 cleanup, current branch `feat/integrar-review-flujo-pr4-cleanup`)
- **Chain strategy**: stacked-to-main, each slice independently reviewable (PR4 ~75 lines well under 400-line budget; total ~1125 lines across 4 PRs, each slice 60 min review).
- **Local-only**: PR chain is local; NOT pushed (per apply-progress learned: user decision).
- **Work units**: PR1 Foundation (forms, URLs, rename), PR2 Core Flow (ReviewFormView approve/reject), PR3 History Display (Historial + resubmission), PR4 Cleanup (remove legacy Approve/Reject views/URLs, 6 OldReviewViewsRemovedTests).

## Traceability — Engram Observation IDs

Hybrid store: all artifacts persist in Engram for recovery. The following observations were read as source for this report (proving retrieval via `mem_get_observation`; previews alone were not used):

| Artifact | Engram topic_key | Observation ID | sync_id | State |
|----------|-----------------|----------------|---------|-------|
| proposal | sdd/integrar-review-flujo/proposal | #30 | obs-4b06637887744b56 | active |
| spec (3 domains concatenated) | sdd/integrar-review-flujo/spec | #31 | obs-0ec46770a0936222 | active |
| design | sdd/integrar-review-flujo/design | #33 | obs-18c4badc91e1d458 | active |
| tasks | sdd/integrar-review-flujo/tasks | #34 | obs-6fe18bf851e673f9 | active |
| apply-progress | sdd/integrar-review-flujo/apply-progress | #35 | obs-3af94cb609a3eaf6 | active |
| verify-report | sdd/integrar-review-flujo/verify-report | #36 | obs-98282136a24c8398 | active |
| archive-report | sdd/integrar-review-flujo/archive-report | (this save) | — | — |

No review topics (`sdd/{change}/review/{transaction,ledger,receipt,gate-context}`) were read — `reviewGate` absent, so no review ever happened for this candidate.

- **Engram project**: `plataforma-publicacion-articulos` (normalized, detected from git remote)
- **Scope**: project
- **Type**: architecture
- **capture_prompt**: false (automated SDD artifact)

## Files Changed (final implementation coverage)

| File | Action | Scope |
|------|--------|-------|
| articles/forms.py | Modified PR1 | Added ReviewForm (ModelForm, comments required, feedback optional, decision via __init__), renamed ReviewCreateForm -> ArticleForm with alias |
| articles/views.py | Modified PR1+PR2+PR3+PR4 | PR1: Renamed ReviewCreateView -> ArticleCreateView, updated ArticleUpdateView to ArticleForm, stub ReviewFormView. PR2: Full ReviewFormView GET/POST with transaction.atomic(). PR3: ArticleDetailView adds reviews + can_view_history. PR4: Removed ApproveArticleView/RejectArticleView + cleanup imports (31 lines) |
| articles/urls.py | Modified PR1+PR4 | PR1: Renamed review_create -> article_create, added review_approve/review_reject. PR4: Removed approve_article/reject_article patterns + stale imports |
| articles/templates/articles/article_form.html | Renamed PR1 | review_create.html -> article_form.html |
| articles/templates/articles/review_form.html | Created PR2 | Dedicated review form page (decision-aware header, article summary, comments/feedback fields, cancel link) |
| articles/templates/articles/work_dashboard.html | Modified PR1+PR2 | PR1: url review_create -> article_create. PR2: Replaced POST forms with GET links to review_approve/review_reject |
| articles/templates/articles/article_detail.html | Modified PR3 | Added Historial de revisiones section chronological, gated can_view_history and reviews |
| editorial/tests.py | Modified PR1 | Added 13 ReviewFormTests |
| articles/tests.py | Modified PR1+PR2+PR3+PR4 | PR1: 11 tests (ArticleFormRenameTests + ArticleCreateUrlTests). PR2: 22 ReviewFormViewTests. PR3: 13 tests (ReviewHistoryVisibilityTests 10, ReviewResubmissionTests 2, MultipleReviewRoundsTests 1). PR4: 6 OldReviewViewsRemovedTests |
| openspec/specs/editorial-review/spec.md | Created (archived via sync) | Source of truth synced |
| openspec/specs/review-history-display/spec.md | Created (archived via sync) | Source of truth synced |
| openspec/specs/article-workflow/spec.md | Created (archived via sync) | Source of truth synced |

## SDD Cycle Complete

The change has been fully planned (proposal, 3 specs with 17 requirements / 29 scenarios, design with 3 ADRs and atomic data flow), implemented via strict TDD across 4 stacked PRs (35/35 tasks, 65 tests), verified (PASS WITH WARNINGS, 0 blockers, build clean), and archived. The main specs now reflect the new behavior; the change folder is sealed as audit trail. Ready for the next change.

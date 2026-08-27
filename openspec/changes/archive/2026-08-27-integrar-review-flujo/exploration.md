## Exploration: Integrar modelo Review en flujo editorial

### Current State

The `Review` model exists in `editorial/models.py` with all necessary fields (article FK, reviewer FK, comments, decision, feedback, created_at) but is **never used**. The editorial workflow is handled entirely via `Article.status` field in `articles/views.py`:

- **SendToReviewView** (author): sets `status='pending'`
- **ApproveArticleView** (editor): sets `status='published'` — no review record created
- **RejectArticleView** (editor): sets `status='rejected'` — no review record created
- **WorkDashboardView**: editors see `status='pending'` articles; reviewers see their own articles
- **ReviewCreateView** / **ReviewCreateForm**: misnamed — they create/edit **Articles**, not Reviews
- **ArticleUpdateView** (author): resets `status='draft'` when editing rejected/published articles

No form exists for editors to provide comments/feedback during approval/rejection. Authors cannot see review history or feedback on rejected articles.

### Affected Areas

| File | Why Affected |
|------|--------------|
| `articles/views.py` | `ApproveArticleView`, `RejectArticleView` need to create Review records; possibly new `ReviewCreateView` for editors |
| `articles/forms.py` | Need new `ReviewForm` for editor approval/rejection with comments/decision/feedback |
| `articles/templates/articles/work_dashboard.html` | Editor actions need to show a form/modal for review input instead of direct POST |
| `articles/templates/articles/article_detail.html` | Show review history/feedback to author (especially on rejected articles) |
| `editorial/models.py` | Review model already exists — may need `related_name` or helper methods |
| `articles/urls.py` | New URL for editor review submission if using separate view |

### Approaches

1. **Inline Review Creation in Approve/Reject Views** (Recommended)
   - Modify `ApproveArticleView` and `RejectArticleView` to accept POST with comments/feedback
   - Create `Review` record with `decision='approve'` or `'reject'` + editor as reviewer
   - Update `work_dashboard.html` to show a modal/form for editor input before submit
   - Pros: Minimal new views, keeps workflow in one place, atomic status+review update
   - Cons: Slightly more complex views; need to handle GET (show form) + POST (process)
   - Effort: Medium

2. **Separate ReviewCreateView for Editors**
   - New `EditorReviewCreateView` at `/dashboard/workspace/review/<article_id>/`
   - GET shows form with decision radio (approve/reject), comments, feedback
   - POST creates Review + updates Article.status
   - Pros: Clean separation, reusable, follows Django CBV patterns
   - Cons: Extra view/URL/template; two-step flow for editors (click article → fill review)
   - Effort: Medium-High

3. **Signal-based Review Creation**
   - Use `post_save` signal on Article when status changes to published/rejected
   - Auto-create Review with minimal data (decision inferred from status)
   - Pros: Zero view changes
   - Cons: No editor comments/feedback captured; loses accountability (who approved?); signals are implicit/magic
   - Effort: Low (but incomplete — doesn't solve the core need)

### Recommendation

**Approach 1 (Inline Review Creation)** — Best balance. Editors stay on dashboard, fill a quick modal with comments/feedback, submit → Review created + status updated atomically. Requires:
- New `ReviewForm` in `forms.py` (decision, comments, feedback)
- Update `ApproveArticleView`/`RejectArticleView` to handle GET (render modal form) and POST (validate form, create Review, update status)
- Update `work_dashboard.html` with modal for editor review input
- Add review history display in `article_detail.html` for authors

### Risks

- **Misnamed existing `ReviewCreateView`/`ReviewCreateForm`** — they handle Articles, not Reviews. Must rename to `ArticleCreateView`/`ArticleForm` to avoid confusion.
- **Resubmission flow**: When author edits a rejected article and sends to review again, should a new review cycle start? Yes — new Review record on next editor action.
- **Multiple reviews per article**: Model supports it via FK with `related_name='reviews'`. Each approval/rejection creates a new Review.
- **Feedback visibility**: Should `feedback` field (suggestions for improvement) be shown to author? Yes — on rejected articles, show feedback in article_detail.

### Ready for Proposal

Yes. The exploration clarifies the exact changes needed. The orchestrator should proceed to proposal phase.
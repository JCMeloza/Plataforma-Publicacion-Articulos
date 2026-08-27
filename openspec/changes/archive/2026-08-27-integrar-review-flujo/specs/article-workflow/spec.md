# Article Workflow Specification (Delta)

## Purpose

Defines the modified article workflow where status transitions (pending→published, pending→rejected) now require Review record creation. Also covers the rename of misnamed `ReviewCreateView`/`ReviewCreateForm` to `ArticleCreateView`/`ArticleForm`.

## ADDED Requirements

### Requirement: Status Transitions Require Review Creation

The system MUST require a Review record to be created when an article transitions from 'pending' to 'published' (approval).
The system MUST require a Review record to be created when an article transitions from 'pending' to 'rejected' (rejection).
The system MUST NOT allow direct status changes without Review creation for these transitions.

#### Scenario: Approval now creates Review + updates status atomically

- GIVEN an article with status='pending'
- WHEN an editor approves via the new review flow
- THEN a Review record is created with decision='approve'
- AND article status becomes 'published'
- AND both operations succeed or fail together (atomic)

#### Scenario: Rejection now creates Review + updates status atomically

- GIVEN an article with status='pending'
- WHEN an editor rejects via the new review flow
- THEN a Review record is created with decision='reject'
- AND article status becomes 'rejected'
- AND both operations succeed or fail together (atomic)

---

### Requirement: Send to Review Resets Status to Pending

The system MUST allow authors to send draft or rejected articles to review, setting status='pending'.
The system SHALL preserve existing Review records when resubmitting.

#### Scenario: Author sends draft to review

- GIVEN an article with status='draft'
- AND the current user is the article author
- WHEN the author clicks "Enviar a revisión"
- THEN article status becomes 'pending'
- AND no Review record is created (editor action creates it later)

#### Scenario: Author resubmits rejected article

- GIVEN an article with status='rejected' and existing Review records
- AND the current user is the article author
- WHEN the author clicks "Enviar a revisión"
- THEN article status becomes 'pending'
- AND existing Review records are preserved
- AND next editor action will create a new Review record

---

## MODIFIED Requirements

### Requirement: Article Creation by Reviewers (formerly ReviewCreateView)

The system MUST allow users with 'reviewer' role to create new articles.
The system SHALL use `ArticleCreateView` (renamed from `ReviewCreateView`) with `ArticleForm` (renamed from `ReviewCreateForm`).
The system SHALL set the article autor to the current reviewer user.
The system SHALL generate slug from title automatically.
The system SHALL redirect to work_dashboard on success with success message.
(Previously: Handled by misnamed `ReviewCreateView`/`ReviewCreateForm` creating Articles, not Reviews)

#### Scenario: Reviewer creates new article

- GIVEN a user with role='reviewer'
- WHEN the reviewer accesses the article creation page
- AND fills in title, content, category, tags
- AND submits the form
- THEN an Article is created with autor=reviewer, status='draft'
- AND slug is auto-generated from title
- AND reviewer is redirected to work_dashboard with success message

#### Scenario: Reviewer edits own article (ArticleUpdateView)

- GIVEN an article authored by the current reviewer with status='draft' or 'rejected' or 'published'
- WHEN the reviewer edits the article via ArticleUpdateView
- AND submits changes
- THEN the article is updated
- AND if status was 'rejected' or 'published', it is reset to 'draft'
- AND reviewer is redirected to work_dashboard with success message

---

### Requirement: Editor Dashboard Shows Pending Articles for Review

The system MUST show editors a list of articles with status='pending' on the work dashboard.
The system SHALL provide approve/reject actions that trigger the review modal/flow.
The system SHALL NOT allow direct approve/reject without review input.
(Previously: Direct POST to ApproveArticleView/RejectArticleView without review form)

#### Scenario: Editor sees pending articles with review actions

- GIVEN articles with status='pending' exist
- AND the current user is an editor
- WHEN the editor views the work dashboard
- THEN a list of pending articles is shown with author, title, category
- AND each row has "Aprobar" and "Rechazar" buttons
- AND clicking opens a modal with review form (comments required, feedback optional)

---

## RENAMED Requirements

### Requirement: ReviewCreateView → ArticleCreateView

The view class `ReviewCreateView` is renamed to `ArticleCreateView`.
(Reason: The view creates Articles, not Reviews — the name was misleading)
(Migration: Update URL pattern name from `review_create` to `article_create`; update all template `{% url %}` references; update any reverse() calls in views)

### Requirement: ReviewCreateForm → ArticleForm

The form class `ReviewCreateForm` is renamed to `ArticleForm`.
(Reason: The form creates/edits Articles, not Reviews — the name was misleading)
(Migration: Update imports in views.py; update ArticleUpdateView to use ArticleForm)

### Requirement: review_create.html → article_form.html

The template `articles/review_create.html` is renamed to `articles/article_form.html`.
(Reason: Template is used for article creation and editing, not review creation)
(Migration: Update ArticleCreateView and ArticleUpdateView template_name; update any explicit template references)

---

## REMOVED Requirements

### Requirement: Direct Approve/Reject Without Review Input

Direct status change via POST to ApproveArticleView/RejectArticleView without comments/feedback is removed.
(Reason: All editorial decisions must now create a Review record with accountability and feedback)
(Migration: Views now handle GET (show form) + POST (validate form, create Review, update status))

### Requirement: Article Status as Sole Audit Trail

Using Article.status alone to track editorial decisions is removed.
(Reason: Status doesn't capture who decided, when, comments, or feedback)
(Migration: Review model becomes source of truth; Article.status reflects current state only)
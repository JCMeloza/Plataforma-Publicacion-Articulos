# Editorial Review Specification

## Purpose

Defines the behavior for editors to submit structured reviews (approve/reject with comments and feedback) that create Review records and update Article status atomically.

## Requirements

### Requirement: Editor Approves Article with Review

The system MUST allow an editor to approve a pending article by submitting a review with required comments and optional feedback.

The system SHALL create a Review record with decision='approve', reviewer=current editor, comments, and feedback.
The system SHALL update the Article status from 'pending' to 'published' atomically with Review creation.
The system SHALL redirect the editor to the work dashboard after successful approval.

#### Scenario: Happy path — editor approves with comments and feedback

- GIVEN an article with status='pending'
- AND the current user is an editor
- WHEN the editor opens the approval modal for the article
- AND fills in required comments "Excelente artículo, bien estructurado"
- AND fills in optional feedback "Considerar añadir más ejemplos en la sección 3"
- AND submits the form
- THEN a Review record is created with decision='approve', reviewer=editor, comments="Excelente artículo...", feedback="Considerar añadir..."
- AND the article status is updated to 'published'
- AND the editor is redirected to the work dashboard with success message

#### Scenario: Edge case — editor approves with only required comments (no feedback)

- GIVEN an article with status='pending'
- AND the current user is an editor
- WHEN the editor submits approval with comments="Aprobado" and empty feedback
- THEN a Review record is created with decision='approve', feedback=''
- AND the article status is updated to 'published'

#### Scenario: Error state — non-editor cannot approve

- GIVEN an article with status='pending'
- AND the current user is a reviewer (not editor)
- WHEN the reviewer attempts to access the approval endpoint
- THEN access is denied (403 Forbidden)
- AND no Review record is created
- AND article status remains 'pending'

#### Scenario: Error state — cannot approve non-pending article

- GIVEN an article with status='published'
- AND the current user is an editor
- WHEN the editor attempts to approve the article
- THEN an error message is shown: "Este artículo no está pendiente de revisión"
- AND no Review record is created
- AND article status remains 'published'

---

### Requirement: Editor Rejects Article with Review

The system MUST allow an editor to reject a pending article by submitting a review with required comments and optional feedback for the author.

The system SHALL create a Review record with decision='reject', reviewer=current editor, comments, and feedback.
The system SHALL update the Article status from 'pending' to 'rejected' atomically with Review creation.
The system SHALL redirect the editor to the work dashboard after successful rejection.

#### Scenario: Happy path — editor rejects with comments and author feedback

- GIVEN an article with status='pending'
- AND the current user is an editor
- WHEN the editor opens the rejection modal for the article
- AND fills in required comments "Falta profundidad en el análisis"
- AND fills in optional feedback "Revisar la metodología y ampliar la bibliografía"
- AND submits the form
- THEN a Review record is created with decision='reject', reviewer=editor, comments="Falta profundidad...", feedback="Revisar la metodología..."
- AND the article status is updated to 'rejected'
- AND the editor is redirected to the work dashboard with success message

#### Scenario: Edge case — editor rejects with only required comments (no feedback)

- GIVEN an article with status='pending'
- AND the current user is an editor
- WHEN the editor submits rejection with comments="No cumple criterios" and empty feedback
- THEN a Review record is created with decision='reject', feedback=''
- AND the article status is updated to 'rejected'

#### Scenario: Error state — non-editor cannot reject

- GIVEN an article with status='pending'
- AND the current user is a reviewer (not editor)
- WHEN the reviewer attempts to access the rejection endpoint
- THEN access is denied (403 Forbidden)
- AND no Review record is created
- AND article status remains 'pending'

#### Scenario: Error state — cannot reject non-pending article

- GIVEN an article with status='draft'
- AND the current user is an editor
- WHEN the editor attempts to reject the article
- THEN an error message is shown: "Este artículo no está pendiente de revisión"
- AND no Review record is created
- AND article status remains 'draft'

---

### Requirement: Review Form Validation

The system MUST validate that comments field is required for both approve and reject actions.
The system MUST validate that decision field matches the action (approve/reject).
The system SHOULD allow feedback field to be optional (blank allowed).

#### Scenario: Validation error — empty comments on approve

- GIVEN an editor viewing the approval modal
- WHEN the editor submits with empty comments field
- THEN form validation fails
- AND error message indicates comments are required
- AND no Review record is created
- AND article status unchanged

#### Scenario: Validation error — empty comments on reject

- GIVEN an editor viewing the rejection modal
- WHEN the editor submits with empty comments field
- THEN form validation fails
- AND error message indicates comments are required
- AND no Review record is created
- AND article status unchanged

---

### Requirement: Resubmission Starts New Review Cycle

The system MUST allow an author to edit a rejected article and resubmit it for review.
The system SHALL reset the article status to 'pending' on resubmission.
The system SHALL allow a new review cycle (new Review record) on the next editor action.

#### Scenario: Happy path — author resubmits rejected article

- GIVEN an article with status='rejected' and one existing Review (decision='reject')
- AND the current user is the article author
- WHEN the author edits the article and clicks "Enviar a revisión"
- THEN the article status is updated to 'pending'
- AND the existing Review records are preserved
- WHEN an editor subsequently approves the article
- THEN a NEW Review record is created (second review cycle)
- AND the article status is updated to 'published'

#### Scenario: Multiple review rounds — three cycles

- GIVEN an article rejected twice (two Review records with decision='reject')
- AND the current user is the article author
- WHEN the author resubmits after each rejection
- AND editors reject twice more then finally approve
- THEN total of 3 Review records exist (2 reject, 1 approve)
- AND article status is 'published'
- AND all three reviews are queryable via article.reviews.all()
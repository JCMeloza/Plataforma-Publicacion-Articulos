# Review History Display Specification

## Purpose

Defines the behavior for authors and editors to view chronological review history (decisions, comments, feedback, timestamps) for an article on the article detail page.

## Requirements

### Requirement: Author Views Review History on Article Detail

The system MUST display a "Historial de revisiones" section on the article detail page for the article author.
The system SHALL list all Review records for the article in chronological order (oldest first).
The system SHALL show for each review: reviewer name, decision (approve/reject), comments, feedback, and timestamp.
The system SHALL show feedback field content to the author (suggestions for improvement).

#### Scenario: Happy path — author views rejected article with feedback

- GIVEN an article with status='rejected' and one Review (decision='reject', feedback="Ampliar bibliografía")
- AND the current user is the article author
- WHEN the author views the article detail page
- THEN a "Historial de revisiones" section is visible
- AND the section shows one review entry with:
  - Reviewer name (editor username)
  - Decision badge: "Rechazado"
  - Comments: internal editor comments
  - Feedback: "Ampliar bibliografía" (visible to author)
  - Timestamp of review

#### Scenario: Happy path — author views published article with approval history

- GIVEN an article with status='published' and one Review (decision='approve')
- AND the current user is the article author
- WHEN the author views the article detail page
- THEN "Historial de revisiones" section shows one review entry with:
  - Decision badge: "Aprobado y Publicado"
  - Comments: editor's approval comments
  - Feedback: (empty or editor suggestions if provided)
  - Timestamp

#### Scenario: Edge case — multiple review rounds displayed chronologically

- GIVEN an article with three Review records:
  1. decision='reject', created_at=2026-01-10
  2. decision='reject', created_at=2026-01-15
  3. decision='approve', created_at=2026-01-20
- AND the current user is the article author
- WHEN the author views the article detail page
- THEN "Historial de revisiones" shows three entries in chronological order (1, 2, 3)
- AND each entry shows correct decision, comments, feedback, reviewer, timestamp

#### Scenario: Edge case — no reviews yet (draft article)

- GIVEN an article with status='draft' and zero Review records
- AND the current user is the article author
- WHEN the author views the article detail page
- THEN "Historial de revisiones" section shows "Sin revisiones aún" or is hidden
- AND no error occurs

---

### Requirement: Editor Views Review History on Article Detail

The system MUST display the same "Historial de revisiones" section for editors viewing any article.
The system SHALL show all review data including internal comments (not just feedback).

#### Scenario: Happy path — editor views article with review history

- GIVEN an article with two Review records (one reject, one approve)
- AND the current user is an editor
- WHEN the editor views the article detail page
- THEN "Historial de revisiones" section shows both reviews
- AND internal comments field is visible for each review
- AND feedback field is visible for each review

#### Scenario: Edge case — editor views article they didn't review

- GIVEN an article reviewed by a different editor
- AND the current user is an editor (not the reviewer)
- WHEN the editor views the article detail page
- THEN full review history is visible including other editor's name and comments

---

### Requirement: Review History Visibility Rules

The system MUST show feedback field to authors (suggestions for improvement).
The system MUST show comments field to editors (internal editorial notes).
The system SHOULD show both fields to both roles for transparency.

#### Scenario: Author sees feedback but not necessarily internal comments distinction

- GIVEN a Review with comments="Interno: buen estructura" and feedback="Para el autor: añadir ejemplos"
- AND the current user is the article author
- WHEN the author views the review history
- THEN both comments and feedback are displayed
- AND feedback is clearly labeled as suggestions for the author

#### Scenario: Editor sees all fields clearly labeled

- GIVEN a Review with comments and feedback populated
- AND the current user is an editor
- WHEN the editor views the review history
- THEN comments labeled as "Comentarios internos"
- AND feedback labeled as "Sugerencias para el autor"

---

### Requirement: Non-Author Non-Editor Cannot Access Review History

The system MUST restrict review history visibility to article author and users with editor role.
The system SHALL NOT show review history to other reviewers, readers, or anonymous users.

#### Scenario: Error state — other reviewer cannot see review history

- GIVEN an article authored by User A, reviewed by Editor B
- AND the current user is User C (reviewer role, not author, not editor)
- WHEN User C views the article detail page
- THEN "Historial de revisiones" section is NOT visible
- OR the section is visible but empty/access denied

#### Scenario: Error state — anonymous user cannot see review history

- GIVEN an article with reviews
- AND the current user is not authenticated
- WHEN the anonymous user views the article detail page
- THEN "Historial de revisiones" section is NOT visible
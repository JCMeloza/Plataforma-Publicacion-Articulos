from django.test import TestCase

from articles.forms import ReviewForm


class ReviewFormTests(TestCase):
    """TDD RED: ReviewForm validation (Phase 1 Foundation)."""

    def test_comments_required_validation(self):
        """comments field is required — empty should be invalid"""
        form = ReviewForm(data={"comments": "", "feedback": "algo"})
        self.assertFalse(form.is_valid())
        self.assertIn("comments", form.errors)

    def test_comments_required_whitespace(self):
        """comments with only whitespace should be invalid"""
        form = ReviewForm(data={"comments": "   ", "feedback": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("comments", form.errors)

    def test_feedback_optional(self):
        """feedback field is optional — empty feedback should still be valid"""
        form = ReviewForm(data={"comments": "Bien estructurado", "feedback": ""})
        self.assertTrue(form.is_valid())

    def test_feedback_optional_omitted(self):
        """feedback omitted entirely should still be valid"""
        form = ReviewForm(data={"comments": "Comentario valido"})
        self.assertTrue(form.is_valid())

    def test_valid_with_both_fields(self):
        form = ReviewForm(
            data={
                "comments": "Excelente artículo, bien estructurado",
                "feedback": "Considerar añadir más ejemplos en la sección 3",
            }
        )
        self.assertTrue(form.is_valid())

    def test_decision_prefilled_via_init(self):
        """decision passed via __init__ should be set on instance"""
        form = ReviewForm(decision="approve")
        self.assertEqual(form.decision, "approve")
        self.assertEqual(form.instance.decision, "approve")

    def test_decision_reject_prefilled(self):
        form = ReviewForm(decision="reject")
        self.assertEqual(form.decision, "reject")
        self.assertEqual(form.instance.decision, "reject")

    def test_decision_none_when_not_provided(self):
        form = ReviewForm()
        self.assertIsNone(form.decision)

    def test_decision_prefilled_with_data(self):
        """decision should be set even when form is bound with POST data"""
        form = ReviewForm(data={"comments": "ok", "feedback": ""}, decision="approve")
        self.assertEqual(form.instance.decision, "approve")
        self.assertTrue(form.is_valid())

    def test_meta_fields(self):
        """ReviewForm should expose only comments and feedback"""
        self.assertEqual(ReviewForm.Meta.fields, ["comments", "feedback"])

    def test_meta_model_is_review(self):
        from editorial.models import Review

        self.assertEqual(ReviewForm.Meta.model, Review)

    def test_widgets_configured(self):
        """widgets should have placeholder text per design"""
        form = ReviewForm()
        comments_widget = form.fields["comments"].widget
        feedback_widget = form.fields["feedback"].widget
        self.assertIn("Comentarios internos", comments_widget.attrs.get("placeholder", ""))
        self.assertIn("Sugerencias para el autor", feedback_widget.attrs.get("placeholder", ""))

    def test_labels_configured(self):
        form = ReviewForm()
        self.assertEqual(form.fields["comments"].label, "Comentarios internos *")
        self.assertEqual(form.fields["feedback"].label, "Sugerencias para el autor")

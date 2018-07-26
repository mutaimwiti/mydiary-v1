import unittest
from app.request import validate, ValidationException


class RequiredRuleTestCase(unittest.TestCase):

    def test_required_takes_precedence(self):
        request = {'other_field': 'Some value'}
        rules = {'test_field': 'required|min:20|max:55'}
        with self.assertRaises(ValidationException) as context:
            validate(request, rules)
        # only the required validation rule is checked
        # it does not make sense to run any other rule if the field is not set
        errors = {'errors': {'test_field': ['The test_field field is required.']}}
        self.assertEqual(errors, context.exception.errors)

    def test_required_passes_if_field_is_set(self):
        """
        Passes if field is valid.
        """
        request = {'test_field': 'Some value'}
        rules = {'test_field': 'required'}
        self.assertEqual(validate(request, rules), True)

    def test_required_fails_if_field_is_not_set(self):
        """
        Fails if field is not set.
        """
        request = {'other_field': 'Some value'}
        rules = {'test_field': 'required'}
        with self.assertRaises(ValidationException):
            validate(request, rules)

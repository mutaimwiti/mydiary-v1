import unittest
from app.request import validate, ValidationException, InvalidTypeException


class MinRuleTestCase(unittest.TestCase):

    def test_passes_if_field_is_valid(self):
        """
        Passes if field is valid.
        :return:
        """
        # greater than min
        request = {'test_field': 'Greater than fifteen'}
        rules = {'test_field': 'min:15'}
        self.assertEqual(validate(request, rules), True)
        # equal to min
        request = {'test_field': 'Equal 2 fifteen'}
        rules = {'test_field': 'min:15'}
        self.assertEqual(validate(request, rules), True)

    def test_fails_if_field_length_is_less_than_min(self):
        """
        Fails if field length is less than that specified by argument.
        """
        request = {'test_field': 'Less than 15'}
        rules = {'test_field': 'min:15'}
        with self.assertRaises(ValidationException) as context:
            validate(request, rules)
        self.assertTrue('The test_field field must have a minimum length of 15.' in str(context.exception.errors))

    def test_fails_if_field_is_required_and_is_missing(self):
        """
        Fails when field is missing and it is required in request.
        """
        request = {'other_field': 'Some value'}
        rules = {'test_field': 'required|min:5'}
        with self.assertRaises(ValidationException) as context:
            validate(request, rules)
        self.assertTrue('The test_field field is required.' in str(context.exception.errors))

    def test_fails_if_argument_is_invalid(self):
        """
        Fails if rule argument is invalid.
        """
        request = {'test_field': 'Some value'}
        rules = {'test_field': 'required|min:g'}
        with self.assertRaises(InvalidTypeException) as context:
            validate(request, rules)
        self.assertTrue('"g" is not a valid integer.' in str(context.exception))

    def test_fails_for_invalid_field_type(self):
        request = {'test_field': 1500}
        rules = {'test_field': 'required|min:3'}
        with self.assertRaises(ValidationException) as context:
            validate(request, rules)
        self.assertTrue('The test_field field is of an invalid type.' in str(context.exception.errors))
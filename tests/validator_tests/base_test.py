import unittest
from app.request import validate, InvalidValidatorException, ValidationException


class BaseTestCase(unittest.TestCase):

    def test_invalid_validators_fail(self):
        request = {'test_field': 'Some value'}
        rules = {'test_field': 'gibberish'}
        with self.assertRaises(InvalidValidatorException) as context:
            validate(request, rules)
        self.assertTrue('Rule [gibberish] is an invalid validation rule.' in str(context.exception))

    def test_multiple_rules_work(self):
        request = {'test_field': 'Some value'}
        rules = {'test_field': 'required|min:5|max:10'}
        self.assertTrue(validate(request, rules))

    def test_empty_rule_string_works(self):
        request = {'test_field': 'Some value'}
        rules = {'test_field': ''}
        self.assertTrue(validate(request, rules))

    def test_many_fields_can_be_validated(self):
        # without errors
        request = {'test_field': 'Some value', 'test_field2': 'Some other value'}
        rules = {'test_field': 'required', 'test_field2': 'min:5'}
        self.assertTrue(validate(request, rules))
        # with errors
        request = {'test_field': 'Some value', 'test_field2': 'Some other value'}
        rules = {'test_field': 'max:5', 'test_field2': 'min:20'}
        with self.assertRaises(ValidationException) as context:
            validate(request, rules)
        errors = {
            'errors': {
                'test_field': ['The test_field field must have a maximum length of 5.'],
                'test_field2': ['The test_field2 field must have a minimum length of 20.']
            }
        }
        self.assertEqual(errors, context.exception.errors)

    def test_duplicate_validators_fail(self):
        request = {'test_field': 'Some value'}
        rules = {'test_field': 'required|min:5|min:17'}
        with self.assertRaises(InvalidValidatorException) as context:
            validate(request, rules)
        self.assertTrue("Duplicate validation rules ['min'] are not allowed." in str(context.exception))

    def test_multiple_validator_arguments_fail(self):
        request = {'test_field': 'Some value'}
        rules = {'test_field': 'required|min:5:17'}
        with self.assertRaises(InvalidValidatorException) as context:
            validate(request, rules)
        self.assertTrue('Rule [min:5:17] has so more than one argument.' in str(context.exception))

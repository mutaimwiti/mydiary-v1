import re
from app.models import User


class ValidationException(Exception):
    """
    This is a custom exception thrown when validation
    fails. It contains the errors object to be
    presented to the client.
    """
    def __init__(self, errors):
        self.errors = errors


class InvalidTypeException(Exception):
    """
    This is a custom exception for an invalid type
    resulting from invalid usage by developer.
    It's for debugging.
    """
    def __init__(self, message):
        super(InvalidTypeException, self).__init__(message)


class InvalidValidatorException(Exception):
    """
        This is a custom exception for an invalid validation
        resulting from invalid usage by developer.
        It's for debugging.
        """

    def __init__(self, message):
        super(InvalidValidatorException, self).__init__(message)


class Validator:
    INVALID_TYPE_MSG = 'is of an invalid type.'

    def __init__(self, request, rules):
        self.request = request
        self.validation_rules = rules

    @staticmethod
    def parse_int(value):
        """
        Parses an integer. If a TypeError occurs it throws a
        custom InvalidTypeException.
        :param value:
        :return:
        """
        try:
            int_value = int(value)
            return int_value
        except ValueError:
            raise InvalidTypeException('"' + value + '" is not a valid integer.')

    @staticmethod
    def error(field, message):
        """
        Builds an error message for specified field.
        :param field:
        :param message:
        :return:
        """
        return 'The ' + field + ' field ' + message

    @staticmethod
    def duplicates(rules):
        seen = []
        duplicates = []
        for rule in rules:
            name = rule.split(':').pop(0)
            if name in seen:
                duplicates.append(name)
            else:
                seen.append(name)
        return duplicates

    def min(self, field, length):
        """
        Validates a field for a minimum length.
        :param field:
        :param length:
        :rtype: bool | string
        """
        length = Validator.parse_int(length)
        try:
            if len(self.value(field)) < length:
                return 'must have a minimum length of ' + str(length) + '.'
            else:
                return True
        except TypeError:
            return Validator.INVALID_TYPE_MSG

    def max(self, field, length):
        """
        Validates a field for a minimum length.
        :param field:
        :param length:
        :rtype: bool | string
        """
        length = Validator.parse_int(length)
        try:
            if len(self.value(field)) > length:
                return 'must have a maximum length of ' + str(length) + '.'
            else:
                return True
        except TypeError:
            return Validator.INVALID_TYPE_MSG

    def email(self, field):
        """
        Validates a field against an email regex.
        :param field:
        :rtype bool | string
        """
        # This is a complex regular expression. Credit to http://emailregex.com/
        value = self.value(field)
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value):
            return True
        else:
            return '[' + value + '] is not a valid email address.'

    def fields(self):
        """
        Gets a list of all fields to be validated.
        :rtype: list
        """
        return [field for field in self.validation_rules]

    def value(self, field):
        """
        Gets the value of the specified request field.
        It returns None if it is not set.
        :param field:
        :return:
        """
        if field not in self.request:
            return None
        return self.request[field]

    def rules(self, field):
        """
        Gets all the validation rules for the given field. If there
        are duplicate rules it throws an InvalidValidatorException
        If required rule is set it excludes it. If there
        are no rules it returns an empty list.
        :rtype: list
        """
        rules_string = self.validation_rules[field]
        rules = rules_string.split('|')
        duplicates = Validator.duplicates(rules)
        if len(duplicates) > 0:
            raise InvalidValidatorException('Duplicate validation rules ' + str(duplicates) + ' are not allowed.')
        if 'required' in rules:
            rules.remove('required')
        if len(rules) == 1 and rules[0] == '':
            return []
        return rules

    def is_required(self, field):
        """
        Check if a request field is required.
        :rtype: object
        """
        return 'required' in self.validation_rules[field].split('|')

    def is_set(self, field):
        """
        Check if a request field is set.
        :param field:
        :return:
        """
        return self.value(field) is not None

    def validate(self):
        all_errors = {}  # stores all validation errors found
        for field in self.fields():
            errors = []  # stores validation errors for current field
            if self.is_set(field):
                # current field is set
                # get value of field on request
                for rule in self.rules(field):
                    try:
                        parsed_rule = rule.split(':')
                        validator = getattr(self, parsed_rule.pop(0))
                        # we only expect one argument if any
                        if len(parsed_rule) == 0:
                            # rule has no argument
                            result = validator(field)
                        elif len(parsed_rule) == 1:
                            # rule has an argument
                            result = validator(field, parsed_rule.pop(0))
                        else:
                            # more than one argument was given
                            raise InvalidValidatorException('Rule [' + rule + ']' + ' has so more than one argument.')
                    except AttributeError:
                        raise InvalidValidatorException('Rule [' + rule + ']' + ' is an invalid validation rule.')
                    if result is not True:
                        # the validator did not pass
                        errors.append(Validator.error(field, result))
            else:
                # field is not set
                # the only remaining relevant validation rule is 'required'
                if self.is_required(field):
                    # field is not set but is required
                    # this will be the only error reported for this field
                    errors.append(Validator.error(field, 'is required.'))
            if len(errors) > 0:
                # errors were found for the current field
                all_errors[field] = errors
        if len(all_errors) > 0:
            # an error or errors were found in any of the fields
            raise ValidationException({'errors': all_errors})
        return True


def validate(request, rules):
    return Validator(request, rules).validate()


class Auth:
    __email = None

    def __init__(self):
        pass

    @staticmethod
    def set(email):
        Auth.__email = email

    @staticmethod
    def id():
        return Auth.user().get('id')

    @staticmethod
    def email():
        return Auth.__email

    @staticmethod
    def user():
        return User.get_by_email(Auth.__email)


auth = Auth

from abc import ABC, abstractclassmethod
import re



class AbstractBaseValidator(ABC):

    value_type = str
    
    class ValidationError(Exception):
        def __init__(self, message):
            self.message = message

    class ValueTypeError(Exception):
        def __init__(self, message):
            self.message = message

    @abstractclassmethod
    def validate_type(cls, value):
        if not isinstance(value, cls.value_type):
            raise cls.ValueTypeError(f'Value type must be {cls.value_type}.')

    @abstractclassmethod
    def validate(cls, value):
        cls.validate_type(value)


class AbstractRegExValidator(AbstractBaseValidator, ABC):
    re_pattern = r'.'
    has_to_contain = True
    error_message = 'Pattern validation failed!'

    @abstractclassmethod
    def validate(cls, value):
        super().validate(value)
        if not cls.has_to_contain == bool(re.findall(cls.re_pattern, value)):
            raise cls.ValidationError(cls.error_message)


class NumericValidator(AbstractRegExValidator):
    re_pattern = r'\d'
    error_message = 'Value has to contain a number.'


class SpaceBarValidator(AbstractRegExValidator):
    re_pattern = r'\s'
    has_to_contain = False
    error_message = 'No spacebars allowed.'


class UpperCaseValidator(AbstractRegExValidator):
    re_pattern = r'[A-Z]'
    error_message = 'Has to contain upper case letter.'


class LowerCaseValidator(AbstractRegExValidator):
    re_pattern = r'[a-z]'
    error_message = 'Has to contain lower case letter.'


class SpecialCharacterValidator(AbstractRegExValidator):
    re_pattern = r'[*#+@]'
    error_message = 'Has to contain at least one special character.'


class MinLengthValidator(AbstractBaseValidator):

    min_length = 4

    @classmethod
    def validate(cls, value):
        super().validate(value)
        if not len(value) >= cls.min_length:
            raise cls.ValidationError(f'Length must be at least {cls.min_length}')


class MaxLengthValidator(AbstractBaseValidator):

    max_length = 10

    @classmethod
    def validate(cls, value):
        super().validate(value)
        if not len(value) <= cls.max_length:
            raise cls.ValidationError(f'Length must be not bigger than {cls.max_length}')


class ValidatorsGroup(ABC):

    validators = []

    @abstractclassmethod
    def validate(cls, value):
        errors = []

        for validator in cls.validators:
            try:
                validator.validate(value)
            except AbstractBaseValidator.ValidationError as e:
                errors.append(e.message)

        return errors

    @abstractclassmethod
    def validate_password_list(cls, password_list):

        result = []

        for password in password_list:
            validation_dict = {
                    'password': password,
                    'valid': True,
                }
            
            if cls.validate(password):
                if 'errors' not in validation_dict.keys():
                    validation_dict['errors'] = []
                validation_dict['errors'].append(cls.validate(password))
                validation_dict['valid'] = False
            
            result.append(validation_dict)
            
        return result
            


class PasswordValidatorsGroup(ValidatorsGroup):
    validators = [
        UpperCaseValidator,
        NumericValidator,
        LowerCaseValidator,
        SpecialCharacterValidator,
        MinLengthValidator,
        SpaceBarValidator,
    ]

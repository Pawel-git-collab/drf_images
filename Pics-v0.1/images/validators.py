from django.core.exceptions import ValidationError


def validate_time_to_expired(value):
    if not 300 <= value <= 30000:
        raise ValidationError("Value must be a number between 300 and 30000 seconds")

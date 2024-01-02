from core.models import CurrencyExchangeRate
from django.core.exceptions import ValidationError
from datetime import datetime


def validate_create_currency_request_fields(data):
    if isinstance(data, dict):
        if (
            "source_currency" not in data
            or "target_currency" not in data
            or "effective_date" not in data
            or "exchange_rate" not in data
        ):
            raise ValidationError("Missing one or more required fields in the request.")

    if isinstance(data, list):
        for values in data:
            if (
                "source_currency" not in values
                or "target_currency" not in values
                or "effective_date" not in values
                or "exchange_rate" not in values
            ):
                raise ValidationError(
                    "Missing one or more required fields in the request."
                )


def validate_retrieve_currency_request_fields(data):
    if (
        "source_currency" not in data
        or "target_currency" not in data
        or "effective_date" not in data
    ):
        raise ValidationError("Missing one or more required fields in the request.")


def validate_create_currency_input_values(
    source_currency, target_currency, effective_date, exchange_rate
):
    try:
        validate_source_and_target_currency(source_currency, target_currency)
    except ValidationError as e:
        raise ValidationError(f"Invalid currency input. {str(e)}")
    try:
        validate_effective_date(effective_date)
    except ValidationError as e:
        raise ValidationError(f"Invalid effective date input. {str(e)}")
    try:
        validate_exchange_rate(exchange_rate)
    except ValidationError as e:
        raise ValidationError(f"Invalid exchange rate input. {str(e)}")
    try:
        is_new_currency_exchange_rate(source_currency, target_currency, effective_date)
    except ValidationError as e:
        raise ValidationError(f"Invalid combination {str(e)}")


def validate_retrieve_currency_input_values(
    source_currency,
    target_currency,
    effective_date,
):
    try:
        validate_source_and_target_currency(source_currency, target_currency)
    except ValidationError as e:
        raise ValidationError(f"Invalid currency input. {str(e)}")
    try:
        validate_effective_date(effective_date)
    except ValidationError as e:
        raise ValidationError(f"Invalid effective date input. {str(e)}")


def validate_source_and_target_currency(source_currency, target_currency):
    if not (
        isinstance(source_currency, str)
        and isinstance(target_currency, str)
        and source_currency.isalpha()
        and source_currency.isupper()
        and target_currency.isalpha()
        and target_currency.isupper()
        and len(source_currency) == len(target_currency) == 3
    ):
        raise ValidationError(
            "Source and target currency must be a 3-letter code in capital letters."
        )


def validate_effective_date(effective_date):
    if not isinstance(effective_date, str):
        raise ValidationError("Effective date must be a string")
    try:
        parsed_date = datetime.strptime(effective_date, "%Y-%m-%d")
        current_date = datetime.now().date()

        if parsed_date.date() > current_date:
            raise ValidationError("Effective date cannot be in the future.")
    except ValueError:
        raise ValidationError(
            f"Incorrect date format: ({effective_date}). Use YYYY-MM-DD."
        )


def validate_exchange_rate(exchange_rate):
    if not (isinstance(exchange_rate, (int, float)) and exchange_rate > 0):
        raise ValidationError(
            f"Exchange rate: ({exchange_rate}) must be a non-negative, greater than 0 numeric value."
        )


def is_new_currency_exchange_rate(source_currency, target_currency, effective_date):
    existing_currency_exchanges = CurrencyExchangeRate.objects.filter(
        source_currency=source_currency,
        target_currency=target_currency,
        effective_date=effective_date,
    )
    if existing_currency_exchanges:
        raise ValidationError(
            f"This specific currency exchange rate: ({source_currency} --> {target_currency} in {effective_date}) already exists"
        )

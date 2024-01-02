from django.db.models.query import QuerySet
from api.validations import (
    validate_create_currency_input_values,
    validate_create_currency_request_fields,
    validate_retrieve_currency_input_values,
    validate_retrieve_currency_request_fields,
)
from core.models import CurrencyExchangeRate
from core.representations import (
    direct_currency_convertion_representation,
    triangular_currency_convertion_representation,
)


## GET
def get_currency_exchange_filtered_by_closest_effective_date(
    currency_exchange_rate_instance: QuerySet[CurrencyExchangeRate], effective_date: str
):
    currency_exchange_rate_for_effective_date_qs = (
        currency_exchange_rate_instance.filter(effective_date=effective_date).first()
    )

    if currency_exchange_rate_for_effective_date_qs:
        return currency_exchange_rate_for_effective_date_qs

    currency_exchange_rate_before_effective_date_qs = (
        currency_exchange_rate_instance.filter(effective_date__lte=effective_date)
        .order_by("-effective_date")
        .first()
    )
    if currency_exchange_rate_before_effective_date_qs:
        return currency_exchange_rate_before_effective_date_qs
    return None


def get_and_validate_retrieve_currency_request_fields(data):
    validate_retrieve_currency_request_fields(data)
    (
        source_currency,
        target_currency,
        effective_date,
    ) = get_retrieve_currency_request_values(data)
    validate_retrieve_currency_input_values(
        source_currency, target_currency, effective_date
    )
    return source_currency, target_currency, effective_date


def get_create_currency_request_values(data):
    source_currency = data.get("source_currency")
    target_currency = data.get("target_currency")
    effective_date = data.get("effective_date")
    exchange_rate = data.get("exchange_rate")

    return source_currency, target_currency, effective_date, exchange_rate


def get_retrieve_currency_request_values(data):
    source_currency = data.get("source_currency")
    target_currency = data.get("target_currency")
    effective_date = data.get("effective_date")

    return source_currency, target_currency, effective_date


## CREATE
def validate_and_create_currency_convertion_object(data):
    validate_create_currency_request_fields(data)
    (
        source_currency,
        target_currency,
        effective_date,
        exchange_rate,
    ) = get_create_currency_request_values(data)
    validate_create_currency_input_values(
        source_currency, target_currency, effective_date, exchange_rate
    )
    created_currency = create_currency(
        source_currency, target_currency, effective_date, exchange_rate
    )
    return created_currency


def create_currency(source_currency, target_currency, effective_date, exchange_rate):
    rounded_exchange_rate = round(exchange_rate, 4)
    new_currency_exchange = CurrencyExchangeRate(
        source_currency=source_currency,
        target_currency=target_currency,
        effective_date=effective_date,
        exchange_rate=rounded_exchange_rate,
    )

    new_currency_exchange.save()

    return new_currency_exchange


## RETRIEVE
def retrieve_currency_by_triangular_currency_convertion(
    source_currency, target_currency, effective_date
):
    source_currency_convertions_qs = CurrencyExchangeRate.objects.filter(
        source_currency=source_currency
    )
    target_currency_convertions_qs = CurrencyExchangeRate.objects.filter(
        target_currency=target_currency
    )
    if source_currency_convertions_qs and target_currency_convertions_qs:
        source_to_common_currency_convertions_qs = (
            source_currency_convertions_qs.filter(
                target_currency__in=target_currency_convertions_qs.values(
                    "source_currency"
                )
            )
        )
        common_to_target_currency_convertions_qs = (
            target_currency_convertions_qs.filter(
                source_currency__in=source_currency_convertions_qs.values(
                    "target_currency"
                )
            )
        )
        source_to_common_currency_convertion_filtered_by_closest_effective_date = (
            get_currency_exchange_filtered_by_closest_effective_date(
                source_to_common_currency_convertions_qs,
                effective_date,
            )
        )
        common_to_target_currency_convertions_filtered_by_closest_effective_date = (
            get_currency_exchange_filtered_by_closest_effective_date(
                common_to_target_currency_convertions_qs,
                effective_date,
            )
        )
        if (
            source_to_common_currency_convertion_filtered_by_closest_effective_date
            and common_to_target_currency_convertions_filtered_by_closest_effective_date
        ):
            auxiliar_currency = (
                source_to_common_currency_convertion_filtered_by_closest_effective_date.target_currency
            )
            auxiliar_currency_effective_date = (
                source_to_common_currency_convertion_filtered_by_closest_effective_date.effective_date
            )
            auxiliar_currency_exchange_rate = (
                source_to_common_currency_convertion_filtered_by_closest_effective_date.exchange_rate
            )
            target_currency_effective_date = (
                common_to_target_currency_convertions_filtered_by_closest_effective_date.effective_date
            )
            target_currency_exchange_rate = (
                common_to_target_currency_convertions_filtered_by_closest_effective_date.exchange_rate
            )
            triangular_exchange_rate_convertion = (
                source_to_common_currency_convertion_filtered_by_closest_effective_date.exchange_rate
                * common_to_target_currency_convertions_filtered_by_closest_effective_date.exchange_rate
            )

            return triangular_currency_convertion_representation(
                source_currency,
                auxiliar_currency,
                auxiliar_currency_effective_date,
                auxiliar_currency_exchange_rate,
                target_currency,
                target_currency_effective_date,
                target_currency_exchange_rate,
                triangular_exchange_rate_convertion,
            )

    return None


def retrieve_currency_by_direct_currency_convertion(
    source_currency, target_currency, effective_date
):
    direct_currency_convertions_qs = CurrencyExchangeRate.objects.filter(
        source_currency=source_currency, target_currency=target_currency
    )

    if direct_currency_convertions_qs:
        currency_convertion = get_currency_exchange_filtered_by_closest_effective_date(
            direct_currency_convertions_qs, effective_date
        )

        if currency_convertion:
            return (direct_currency_convertion_representation(currency_convertion),)

        return None

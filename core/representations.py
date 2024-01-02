from core.models import CurrencyExchangeRate


def direct_currency_convertion_representation(
    currency_exchange_rate_instance: CurrencyExchangeRate,
):
    rounded_exchange_rate = round(currency_exchange_rate_instance.exchange_rate, 4)
    return {
        "source_currency": currency_exchange_rate_instance.source_currency,
        "target_currency": currency_exchange_rate_instance.target_currency,
        "effective_date": currency_exchange_rate_instance.effective_date,
        "exchange_rate": rounded_exchange_rate,
    }


def triangular_currency_convertion_representation(
    source_currency,
    target_currency,
    effective_date,
    triangular_exchange_rate_convertion,
):
    rounded_exchange_rate = round(triangular_exchange_rate_convertion, 4)
    return {
        "source_currency": source_currency,
        "target_currency": target_currency,
        "effective_date": effective_date,
        "exchange_rate": rounded_exchange_rate,
    }

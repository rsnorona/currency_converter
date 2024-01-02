from django.core.management.base import BaseCommand

from core.functions import create_currency

currency_convertions = [
    # 2022-01
    ("USD", "EUR", "2022-01-01", 0.88151),
    ("EUR", "MXN", "2022-01-01", 23.2012),
    ("MXN", "COP", "2022-01-01", 198.012),
    ("COP", "JPY", "2022-01-01", 0.02833),
    ("JPY", "GBP", "2022-01-01", 0.00643),
    # 2022-04
    ("USD", "EUR", "2022-04-01", 0.89963),
    ("EUR", "MXN", "2022-04-01", 22.0986),
    ("MXN", "COP", "2022-04-01", 188.509),
    ("COP", "JPY", "2022-04-01", 0.03238),
    ("JPY", "GBP", "2022-04-01", 0.00625),
    # 2022-08
    ("USD", "EUR", "2022-08-01", 0.97785),
    ("EUR", "MXN", "2022-08-01", 20.8018),
    ("MXN", "COP", "2022-08-01", 210.271),
    ("COP", "JPY", "2022-08-01", 0.03097),
    ("JPY", "GBP", "2022-08-01", 0.00616),
    # 2022-12
    ("USD", "EUR", "2022-12-01", 0.96498),
    ("EUR", "MXN", "2022-12-01", 19.9652),
    ("MXN", "COP", "2022-12-01", 249.424),
    ("COP", "JPY", "2022-12-01", 0.02875),
    ("JPY", "GBP", "2022-12-01", 0.00601),
    # 2023-01
    ("USD", "EUR", "2023-01-01", 0.93384),
    ("EUR", "MXN", "2023-01-01", 20.826),
    ("MXN", "COP", "2023-01-01", 248.204),
    ("COP", "JPY", "2023-01-01", 0.02699),
    ("JPY", "GBP", "2023-01-01", 0.0063),
    # 2023-04
    ("USD", "EUR", "2023-04-01", 0.91923),
    ("EUR", "MXN", "2023-04-01", 19.6393),
    ("MXN", "COP", "2023-04-01", 256.755),
    ("COP", "JPY", "2023-04-01", 0.02858),
    ("JPY", "GBP", "2023-04-01", 0.00608),
    # 2023-08
    ("USD", "EUR", "2023-08-01", 0.90777),
    ("EUR", "MXN", "2023-08-01", 18.4204),
    ("MXN", "COP", "2023-08-01", 233.945),
    ("COP", "JPY", "2023-08-01", 0.03625),
    ("JPY", "GBP", "2023-08-01", 0.00548),
    # 2023-12
    ("USD", "EUR", "2023-12-01", 0.9149),
    ("EUR", "MXN", "2023-12-01", 18.9688),
    ("MXN", "COP", "2023-12-01", 230.196),
    ("COP", "JPY", "2023-12-01", 0.03679),
    ("JPY", "GBP", "2023-12-01", 0.00535),
    # 2024-01
    ("USD", "EUR", "2024-01-01", 0.90595),
    ("EUR", "MXN", "2024-01-01", 18.7229),
    ("MXN", "COP", "2024-01-01", 227.906),
    ("COP", "JPY", "2024-01-01", 0.03628),
    ("JPY", "GBP", "2024-01-01", 0.00557),
]


class Command(BaseCommand):
    help = "Creates the default currency convertions in the database."

    def handle(self, *args, **options):
        try:
            for (
                source_currency,
                target_currency,
                effective_date,
                exchange_rate,
            ) in currency_convertions:
                create_currency(
                    source_currency, target_currency, effective_date, exchange_rate
                )
        except:
            pass

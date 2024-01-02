from django.db import models


class CurrencyExchangeRate(models.Model):
    source_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    effective_date = models.DateField()
    exchange_rate = models.FloatField(max_length=10)

    class Meta:
        unique_together = (
            "source_currency",
            "target_currency",
            "effective_date",
        )

    def __str__(self):
        rounded_exchange_rate = round(self.exchange_rate, 2)
        return f"Source: {self.source_currency} Target: {self.target_currency} Exchange rate: {rounded_exchange_rate} Effective date: {self.effective_date}"

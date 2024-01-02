from django.urls import path
from api.core.views import (
    create_currency_convertion,
    retrieve_currency_convertion,
)

urlpatterns = [
    path("currency_converter/create_currency_convertion", create_currency_convertion),
    path(
        "currency_converter/retrieve_currency_convertion", retrieve_currency_convertion
    ),
]

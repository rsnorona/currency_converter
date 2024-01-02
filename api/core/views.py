from django.forms import ValidationError
from rest_framework.decorators import api_view
from django.db import transaction
from django.http import JsonResponse
from core.functions import (
    validate_and_create_currency_convertion_object,
    get_and_validate_retrieve_currency_request_fields,
    retrieve_by_direct_currency_convertion,
    retrieve_by_triangular_currency_convertion,
)
from core.representations import (
    direct_currency_convertion_representation,
)


@api_view(["POST"])
@transaction.atomic()
def create_currency_convertion(request):
    data = request.data

    if isinstance(data, dict):
        try:
            created_currency = validate_and_create_currency_convertion_object(data)
        except ValidationError as ve:
            return JsonResponse({"error": str(ve)})
        return JsonResponse(
            {
                "success": f"New currency was created successfully",
                "data": direct_currency_convertion_representation(created_currency),
            },
            status=200,
        )

    if isinstance(data, list):
        created_currencies_serialized = []
        for values in data:
            try:
                created_currency = validate_and_create_currency_convertion_object(
                    values
                )
            except ValidationError as ve:
                return JsonResponse({"error": str(ve)})

            created_currencies_serialized.append(
                direct_currency_convertion_representation(created_currency)
            )
        return JsonResponse(
            {
                "success": "All the currency convertions were created successfully",
                "data": created_currencies_serialized,
            },
            status=200,
        )


@api_view(["POST"])
def retrieve_currency_convertion(request):
    data = request.data
    (
        source_currency,
        target_currency,
        effective_date,
    ) = get_and_validate_retrieve_currency_request_fields(data)

    direct_convertion_result = retrieve_by_direct_currency_convertion(
        source_currency, target_currency, effective_date
    )
    if direct_convertion_result is not None:
        return JsonResponse(
            {
                "success": "Direct currency convertion found",
                "data": direct_convertion_result,
            },
            status=200,
        )

    triangular_currency_convertion_result = retrieve_by_triangular_currency_convertion(
        source_currency, target_currency, effective_date
    )
    if triangular_currency_convertion_result is not None:
        return JsonResponse(
            {
                "success": "Triangular currency convertion found",
                "data": triangular_currency_convertion_result,
            },
            status=200,
        )

    return JsonResponse(
        {"error": "Couldn't find a currency convertion for the provided input"},
        status=400,
    )

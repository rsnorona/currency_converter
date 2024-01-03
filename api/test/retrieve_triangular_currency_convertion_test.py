from automated_test import automated_test
import os
import dotenv
import json

dotenv.load_dotenv()

expected_response = {
    "success": "Triangular currency convertion found",
    "data": {
        "source_currency": "EUR",
        "auxiliar_currency": "MXN",
        "auxiliar_currency_effective_date": "2023-01-01",
        "auxiliar_currency_exchange_rate": 20.826,
        "target_currency": "COP",
        "target_currency_effective_date": "2023-01-01",
        "target_currency_exchange_rate": 248.204,
        "triangular_exchange_rate_convertion": 5169.0965,
    },
}
expected_response = json.dumps(expected_response, indent=2)

api_url = os.getenv("RETRIEVE_CURRENCY_CONVERTION_API")
data = {
    "source_currency": "EUR",
    "target_currency": "COP",
    "effective_date": "2023-02-28",
}
actual_response = automated_test(api_url, data)

if actual_response:
    if actual_response == expected_response:
        print("Test retrieved the expected information", actual_response)

    else:
        print("Test didn't work as expected")
        print("Expected response: ", expected_response)
        print("Actual response: ", actual_response)

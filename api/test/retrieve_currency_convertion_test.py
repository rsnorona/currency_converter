from automated_test import automated_test
import os
import dotenv

dotenv.load_dotenv()


api_url = os.getenv("RETRIEVE_CURRENCY_CONVERTION_API")
data = {
    "source_currency": "EUR",
    "target_currency": "COP",
    "effective_date": "2023-02-28",
}
automated_test(api_url, data)

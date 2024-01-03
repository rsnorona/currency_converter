# Project Title

Currency converter.

## Project Description

Currency converter is a backend application that provides two api's to our customers, the first one can be used to load currency conversion objects to our database, while the second one can be used to retrieve currency conversion information at any specific effective date.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [API Usage](#api-usage)
  - [Create currency convertion](#create-currency-convertion)
    - [Create currency convertion possible outputs](#create-currency-convertion-possible-outputs)
  - [Retrieve currency convertion](#retrieve-currency-convertion)
    - [Retrieve currency convertion possible outputs](#retrieve-currency-convertion-expected-output)
- [Validation Errors](#validation-errors)
  - [Missing Required Fields](#missing-required-fields)
  - [Invalid Currency Input](#invalid-currency-input)
  - [Invalid Effective Date](#invalid-effective-date)
    - [Date in the future](#date-in-the-future)
    - [Wrong year, mont or day](#wrong-year-month-or-day)
    - [Wrong input type](#wrong-input-type)
  - [Invalid Exchange Rate](#invalid-exchange-rate)
- [Test cases](#test-cases)
- [Automated test case](#automated-test-case)
- [Note](#note)

## Introduction

Currency Conversion is a crucial process that involves converting from one currency (source currency) to another (target currency). The core of this system relies on accurate exchange rates, defined by attributes such as source currency, target currency, effective start date, and exchange rate.

## Prerequisites

Before you begin:
  1. Make sure that [Python](https://www.python.org/) (version 3.10 or higher) is installed.
  2. Make sure that [Git](https://git-scm.com/) is installed.
  3. Make sure that [Google Chrome](https://www.google.com/intl/es_es/chrome/) (version 120.0.6099.109 or higher) is installed.
  4. Download git repository using git SSH (don't forget to add ssh key first)
    - [Repository](https://github.com/rsnorona/currency_converter)

  5. Navigate to application directory
    - ```cd currency_converter```
  6. Install application dependencies and seed the database
    - ```sh scripts/install_and_seed.sh```
  7. Start the application locally
    - ```sh scripts/start.sh```

## API Usage

The application provides two api's:
  1. Create currency convertion.
  2. Retrieve currency convertion.

Both of them accept only POST requests. Each API has it's own input format, field types and URL's.
The detailed information about each API usage is listed bellow.

## Create currency convertion

Once the application is started, this API will be available and ready to use at:

```http://localhost:8888/api/currency_converter/create_currency_convertion```

The expected input in the request body is a JSON array of objects or a single object with the following input types:

  ```json 

  {
    "source_currency": "string: three-capital-letter code that represents a specific source currency",
    "target_currency": "string: three-capital-letter code that represents a specific target currency",
    "effective_date": "string: Date time input in ISO 8601 format: YYYY-MM-DD",
    "exchange_rate": "int | float: Greater than cero"
  }

  ```

  example:


  ```json 

  {
    "source_currency": "USD",
    "target_currency": "EUR",
    "effective_date": "2023-12-18",
    "exchange_rate": 0.9123
  }

  ```

## Create currency convertion posible outputs

The outputs for this API are JsonResponses with either a success message and data or an error with an explanation message depending on the user request input format:

  1. If the user sent a single object with the right input format:

  Example of user's request:

  ```json 

  {
      "source_currency": "COP",
      "target_currency": "MXN",
      "effective_date": "2024-01-02",
      "exchange_rate": 0.0044
  }

  ```

  API output:

  ```json

  {
    "success": "New currency was created successfully",
    "data": {
        "source_currency": "COP",
        "target_currency": "MXN",
        "effective_date": "2024-01-02",
        "exchange_rate": 0.0044
    }
  }

  ```

  2. If the user sent and array of objects with the right input format:

  Example of user's request:

  ```json 

  [
      {
          "source_currency": "USD",
          "target_currency": "EUR",
          "effective_date": "2024-01-02",
          "exchange_rate": 0.9122
      },
      {
          "source_currency": "EUR",
          "target_currency": "MXN",
          "effective_date": "2024-01-02",
          "exchange_rate": 18.5632
      }
  ]

  ```

  API output:

  ```json

  {
      "success": "All the currency convertions were created successfully",
      "data": [
          {
              "source_currency": "USD",
              "target_currency": "EUR",
              "effective_date": "2024-01-02",
              "exchange_rate": 0.9122
          },
          {
              "source_currency": "EUR",
              "target_currency": "MXN",
              "effective_date": "2024-01-02",
              "exchange_rate": 18.5632
          }
      ]
  }

  ```

  3. If the combination of "soruce_currency", "target_currency" and "effective_date" already exists in the database:

  API output:

  ```json

  {
      "error": "[\"Invalid combination ['This specific currency exchange rate: (source_currency --> target_currency in effective_date) already exists']\"]"
  }

  ```

## Retrieve currency convertion

Once the application is started, this API will be available and ready to use at:

```http://localhost:8888/api/currency_converter/retrieve_currency_convertion```

The expected input in the request body is a JSON single object with the following input types:

```json 

{
  "source_currency": "string: three-capital-letter code that represents a specific source currency",
  "target_currency": "string: three-capital-letter code that represents a specific target currency",
  "effective_date": "string: Date time input in ISO 8601 format: YYYY-MM-DD",
}

```

example:


```json 

{
  "source_currency": "USD",
  "target_currency": "EUR",
  "effective_date": "2023-12-18",
}

```

## Retrieve currency convertion posible outputs

  1. If the API found a direct currency convertion:

  Example of user's request:

  ```json 

  {
      "source_currency": "USD",
      "target_currency": "EUR",
      "effective_date": "2022-02-28"
  }

  ```

  API output:

  ```json

  {
      "success": "Direct currency convertion found",
      "data": [
          {
              "source_currency": "USD",
              "target_currency": "EUR",
              "effective_date": "2022-01-01",
              "exchange_rate": 0.8815
          }
      ]
  }

  ```

  2. If the API found a triangular currency convertion:

  Example of user's request:

  ```json 

  {
      "source_currency": "COP",
      "target_currency": "GBP",
      "effective_date": "2022-02-28"
  }

  ```

  API output:

  ```json

  {
      "success": "Triangular currency convertion found",
      "data": {
          "source_currency": "COP",
          "auxiliar_currency": "JPY",
          "auxiliar_currency_effective_date": "2022-01-01",
          "auxiliar_currency_exchange_rate": 0.0283,
          "target_currency": "GBP",
          "target_currency_effective_date": "2022-01-01",
          "target_currency_exchange_rate": 0.0064,
          "triangular_exchange_rate_convertion": 0.0002
      }
  }

  ```

  3. If the API couldn't find a currency convertion:

  Example of user's request:

  ```json 

  {
      "source_currency": "COP",
      "target_currency": "USD",
      "effective_date": "2022-02-28"
  }

  ```

  API output:

  ```json

  {
      "error": "Couldn't find a currency convertion for the provided input"
  }

  ```

## Validation errors

If the user request doesn't have the correct input format or input type the API will return one of the following validation errors depending on the case:

### Missing Required Fields

  ```json

  {
    "error": "['Missing one or more required fields in the request.']"
  }

  ```

### Invalid Currency Input (not capital letter || not 3 letters || not string type)

  ```json

  {
      "error": "[\"Invalid currency input. ['Source and target currency must be a 3-letter code in capital letters.']\"]"
  }

  ```

### Invalid Effective Date

#### Date in the future

  ```json

  {
      "error": "[\"Invalid effective date input. ['Effective date cannot be in the future.']\"]"
  }

  ```

#### Wrong year, month or day

  ```json

  {
      "error": "[\"Invalid effective date input. ['Incorrect date format: (2023-14-02). Use YYYY-MM-DD.']\"]"
  }

  ```

#### Wrong input type

  ```json

  {
      "error": "[\"Invalid effective date input. ['Effective date must be a string']\"]"
  }

  ```

### Invalid Exchange Rate (input type || not possitive)

  ```json

  {
      "error": "[\"Invalid exchange rate input. ['Exchange rate: (asd) must be a non-negative, greater than 0 numeric value.']\"]"
  }

  ```

## Test cases

Please navigate to the TESTCASES.md file for detailed information.

## Automated test case

Specify the license under which your project is distributed. Include a link to the full license text.

## Note

The API's are designed to handle various scenarios, ensuring accurate and reliable currency conversions. Validation functions have been implemented to maintain the API's quality and integrity. Automated tests will cover critical aspects of the API, providing a robust and reliable solution for currency conversion needs.
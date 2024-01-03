# Test Cases for Currency Converter Application

Since the currency converter application provides two API's (one to create currency conversions and one to retrieve currency conversions) the test cases will be separated as for each API.

## Create Currency Convertion API

### Creating a new currency conversion

#### Input

The user creates a POST request to the API and passes the fields in the right format and types.

#### Expected Output

The application should check if the combination between "source_currency", "target_currency" and "effective_date" doesn't already exist in the database: 

- If it doesn't exist the application should return a JsonResponse with status: 200, and an success message detailing the user the information about the new created currency conversion and saves the object in the database.

- If it does exist the application should return a JsonResponse with status: 400, and an error message detailing the user that the specific currency conversion already exists.


## Retrieve Currency Convertion API

### Retrieve currency conversion for a missing effective date

#### Input

The user creates a POST request to the API and passes the fields in the right format and types but there isn't any currency conversion for that specific effective date.

#### Expected Output

The application should check if there are any existing currency conversions from the source currency to the target currency: 

- If it doesn't exist the application should return a JsonResponse with status: 400, and an error message detailing the user that it doesn't exist a currency conversion for the provided input combination.

- If it does exist the application should go back in time and find the closest effective date, then return a JsonResponse with status: 200, and an success message detailing the user the information about the currency conversion that was found.

### Retrieve currency conversion by direct conversion or triangular conversion

#### Input

The user creates a POST request to the API and passes the fields in the right format and types

#### Expected Output

The application should check if there are any existing currency conversions from the source currency to the target currency: 

- If it doesn't exist the application should return a JsonResponse with status: 400, and an error message detailing the user that it doesn't exist a currency conversion for the provided input combination.

- If it does exist the application should: 

    - Check if a direct conversion is available between the source and target currencies, if it does then it should return a JsonResponse with status: 200 and a success message detailing the user the information about the currency conversion that was found.

    - If a direct conversion is not available, the application should check if a triangular conversion is available between the source and target currencies, perform the conversion and return a JsonResponse with status: 200 and a success message detailing the user all the information about the currency conversion including that it was a trinagular conversion.

## Applicable to both API's 

### Missing Required Fields

#### Input

The user creates a POST request to the API and misses one or more expected fields in the body of the request.

#### Expected Output

The application should return a JsonResponse with status: 400, and an error message explaining the user that there are one or more required fields missing in the request.

### Validating Input Types

#### Input

The user creates a POST request to the API and passes a wrong input type or value.

#### Expected Output

The application should return a JsonResponse with status: 400, and an error message explaining the user that one of the inputs has a wrong type and detailed information about the expected input for that field.

### Validating method

#### Input

The user creates a GET/DELETE/PUT/PATCH/HEAD/OPTIONS request to the API.

#### Expected Output

The application should return a JsonResponse with status: 400, and an error message explaining the user that POST method is the only allowed method for this API.
import requests
import json
from datetime import datetime


# The URL to send the POST request to
url = 'http://0.0.0.0:8000/receipts/process/'

# List of retailer entries - You can add/remove entries to this list as per your convenience
entries = [
    {
        "retailer": "Walgreens",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "08:13",
        "total": "2.65",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Dasani", "price": "1.40"}
        ]
    },
    {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "total": "1.25",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        ]
    },
    {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": "35.35",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
        ]
    },
    {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "total": "9.00",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"}
        ]
    }
]

# Set the appropriate headers for JSON data
headers = {'Content-Type': 'application/json'}

# Store the results
results = []

# Loop through each entry
for entry in entries:
    # Converting the Python dictionary to a JSON string
    json_data = json.dumps(entry)

    # Sending the POST request
    response = requests.post(url, data=json_data, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        # Adding PurchaseTime and PurchaseDate to distinguish between each entry
        datetime_str = f"{entry['purchaseDate']} {entry['purchaseTime']}"
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        formatted_datetime = datetime_obj.strftime("%H:%M - %m-%d-%Y")
        results.append({
            "retailer": entry["retailer"],
            "id": response_data.get("id"),
            "formatted_datetime": formatted_datetime
        })
    else:
        print("Request failed for retailer:", entry["retailer"], "with status code:", response.status_code)
        print("Response text:", response.text)

# Printing each ID of the entry that could be used to find the points
for result in results:
    print("Retailer:", result["retailer"], "- Timestamp:", result["formatted_datetime"], "- ID:", result["id"])


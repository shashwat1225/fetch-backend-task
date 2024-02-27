
# Receipt Processor Service

This service is designed to process receipts through a simple web service, assigning unique IDs to each receipt and calculating points based on specific criteria. The application does not require a persistent database, as data is stored in memory. This design choice simplifies the setup and testing process.

## Overview

The Receipt Processor Service provides two main functionalities:

- **Process Receipts:** Allows the submission of receipt details in JSON format and returns a unique ID for each receipt.
- **Get Points:** Using the unique ID returned by the Process Receipts endpoint, this endpoint returns the number of points awarded for the receipt.

The service is built with ease of use in mind, requiring minimal setup to get started.

## API Specification Summary

- **Endpoint to Process Receipts**
  - Path: `/receipts/process`
  - Method: POST
  - Payload: Receipt JSON
  - Response: JSON containing a unique ID for the receipt.

- **Endpoint to Get Points**
  - Path: `/receipts/{id}/points`
  - Method: GET
  - Response: JSON object containing the number of points awarded.

## Setup Instructions

To run the application, follow these steps:

1. **Clone the Repository**
   ```
   git clone https://github.com/shashwat1225/fetch-backend-task
   ```
2. **Install Dependencies**
   Navigate to the cloned repository's directory and run:
   ```
   pip install -r requirements.txt
   ```
3. **Run the Server**
   Start the Django server with the following command:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```

## Using the Service

After starting the server, the service is accessible at `http://0.0.0.0:8000/`.

- **To Process Receipts:**
  Use the `populate.py` script to send POST requests to the server. This script sends predefined receipt entries to the server and prints the retailer name, purchase timestamp, and unique ID for each processed receipt. You can modify the `entries` list in the script to include additional receipts or alter the existing ones.

  Run the script with:
  ```
  python populate.py
  ```

- **To Get Points:**
  Access the points for a specific purchase by navigating to:
  ```
  http://0.0.0.0:8000/receipts/<Unique ID>/points/
  ```
  Replace `<Unique ID>` with the ID returned by the populate.py script.

## URL Paths

The service defines the following URL paths in `urls.py`:

```python
from django.urls import path
from myapp.views import points, process

urlpatterns = [
    path('receipts/<str:id>/points/', points),
    path('receipts/process/', process),
]
```

## Further Instructions

For more detailed information about the API and its specifications, contact: spandey1225@gmail.com

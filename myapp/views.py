import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import math

receipts = {}

@csrf_exempt
def process(request):
    """
    Process a request to either add a receipt (POST method) or return all receipts (GET method).
    For POST requests, the receipt data is expected in JSON format.
    
    Args:
        request: HttpRequest object.

    Returns:
        JsonResponse object containing either the ID of the added receipt or all receipts.
    """
    try:
        if request.method == 'POST':
            # Parse request body as JSON
            data = json.loads(request.body.decode('utf-8'))
            # Generate a unique identifier for the receipt
            id_ = uuid.uuid4()
            global receipts
            # Store the receipt data with UUID as key
            receipts[str(id_)] = data
            return JsonResponse({"id": str(id_)})
        else:
            # Return all receipts for non-POST requests (primarily GET)
            return JsonResponse(receipts, safe=False)
    except json.JSONDecodeError:
        # Return error response for invalid JSON format
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        # Catch-all for any other errors
        return JsonResponse({"error": str(e)}, status=500)

def points(request, id):
    """
    Calculate and return points for a receipt based on its details.
    Points are calculated based on several factors like retailer name, total amount, etc.
    
    Args:
        request: HttpRequest object.
        id: UUID of the receipt as a string.

    Returns:
        JsonResponse object containing the calculated points or an error message.
    """
    try:
        if request.method == 'GET':
            receipt = receipts.get(id, None)
            points = 0
            if receipt:
                # Basic validations and calculations for points based on receipt details
                retailer_name = receipt.get('retailer', '')
                total = float(receipt.get('total', 0))
                purchase_date = receipt.get('purchaseDate', '')
                purchase_time = receipt.get('purchaseTime', '')
                items = receipt.get('items', [])
                
                # Calculate points based on alphanumeric characters in retailer name
                points += sum(c.isalnum() for c in retailer_name)
                # Additional points for totals matching certain criteria
                if total % 1 == 0:
                    points += 50
                if total % 0.25 == 0:
                    points += 25
                # Points based on the number of items
                points += ((len(items) // 2) * 5)
                # Extra points for item descriptions and prices meeting specific conditions
                for item in items:
                    if len(item['shortDescription'].strip()) % 3 == 0:
                        points += math.ceil(float(item['price']) * 0.2)
                # Points for purchase dates and times meeting certain criteria
                if int(purchase_date.split('-')[-1]) % 2 != 0:
                    points += 6
                if purchase_time > '14:00' and purchase_time < '16:00':
                    points += 10
            return JsonResponse({"points": points})
        else:
            # Error response for non-GET requests
            return JsonResponse({"error": "Method not allowed"}, status=405)
    except ValueError:
        # Handle invalid data formats (e.g., conversion failures)
        return JsonResponse({"error": "Invalid data format"}, status=400)
    except KeyError as e:
        # Handle missing keys in the receipt data
        return JsonResponse({"error": f"Missing key: {e}"}, status=400)
    except Exception as e:
        # Catch-all for any other errors
        return JsonResponse({"error": str(e)}, status=500)

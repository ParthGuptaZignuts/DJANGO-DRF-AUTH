from rest_framework import status
from rest_framework.response import Response


def success_response(message="Success", data=None, code=status.HTTP_200_OK):
    """
    Standardized success response.
    """
    response_data = {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
    }
    return Response(response_data, status=code)


def error_response(message="Error", code=status.HTTP_400_BAD_REQUEST, errors=None):
    """
    Standardized error response ensuring errors are returned as strings instead of lists.
    """
    # If errors is a dictionary, convert list values to single string values
    if isinstance(errors, dict):
        errors = {
            key: value[0] if isinstance(value, list) and len(value) == 1 else value
            for key, value in errors.items()
        }

    response_data = {
        "success": False,
        "message": message,
        "errors": errors if errors is not None else {},
    }
    return Response(response_data, status=code)

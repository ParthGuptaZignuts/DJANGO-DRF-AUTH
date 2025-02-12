from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET']) 
def check_server(request):
    """
    A simple view to check if the server is working.
    """
    return Response({"message": "Server is working!"}, status=status.HTTP_200_OK)

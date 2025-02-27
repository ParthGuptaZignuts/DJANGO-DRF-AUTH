from django.core.cache import cache
from rest_framework import permissions
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from common.pagination import Pagination
from common.response import error_response, success_response

from .models import Product
from .serializers import ProductSerializer


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission class to grant access only to superusers.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin


class ProductListView(ListCreateAPIView):
    """
    API view to list and create products.

    - GET: Returns a paginated list of products. Requires authentication.
    - POST: Creates a new product. Requires authentication and admin privileges.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = Pagination

    def get_permissions(self):
        """
        Defines permission requirements for different request methods.
        """
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsAuthenticated(), IsSuperUser()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Retrieves products from cache if available; otherwise, fetches from the database
        and caches the result for 15 minutes.
        """
        cache_key = "products_list"
        cached_products = cache.get(cache_key)

        if cached_products:
            return Product.objects.filter(id__in=cached_products)

        queryset = Product.objects.all()
        cache.set(
            cache_key, list(queryset.values_list("id", flat=True)), timeout=60 * 15
        )

        print(cache.get("products_list"))

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Handles GET requests to fetch the product list.
        """
        try:
            self.check_permissions(request)
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return success_response(
                message="Products fetched successfully", data=serializer.data
            )
        except Exception as e:
            return error_response(message="Error fetching products", errors=str(e))

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new product.
        """
        try:
            self.check_permissions(request)
            response = super().create(request, *args, **kwargs)
            return success_response(
                message="Product created successfully", data=response.data
            )
        except Exception as e:
            return error_response(message="Error creating product", errors=str(e))


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a product.

    - GET: Retrieve product details. Requires authentication.
    - PUT/PATCH: Update a product. Requires authentication and admin privileges.
    - DELETE: Delete a product. Requires authentication and admin privileges.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Defines permission requirements for different request methods.
        """
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperUser()]

    def retrieve(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve product details.
        """
        try:
            product = self.get_object()
            serializer = self.get_serializer(product)
            return success_response(
                message="Product details fetched successfully", data=serializer.data
            )
        except Exception as e:
            return error_response(
                message="Error fetching product details", errors=str(e)
            )

    def update(self, request, *args, **kwargs):
        """
        Handles PUT/PATCH requests to update a product.
        """
        try:
            response = super().update(request, *args, **kwargs)
            return success_response(
                message="Product updated successfully", data=response.data
            )
        except Exception as e:
            return error_response(message="Error updating product", errors=str(e))

    def destroy(self, request, *args, **kwargs):
        """
        Handles DELETE requests to remove a product.
        """
        try:
            response = super().destroy(request, *args, **kwargs)
            return success_response(message="Product deleted successfully", data={})
        except Exception as e:
            return error_response(message="Error deleting product", errors=str(e))

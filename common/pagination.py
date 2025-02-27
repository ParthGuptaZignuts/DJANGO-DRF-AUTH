from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    """
    Custom pagination class for controlling the number of items per page.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

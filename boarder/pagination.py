from rest_framework.pagination import PageNumberPagination


class BoarderListPagination(PageNumberPagination):
    page_size = 10                # number of items per page
    page_size_query_param = None  # disables changing page size via query param

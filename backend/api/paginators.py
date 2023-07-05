from rest_framework.pagination import PageNumberPagination


class LimitPagePagination(PageNumberPagination):
    """Cписок первых шести рецептов"""
    page_size_query_param = 'limit'
    page_size = 6

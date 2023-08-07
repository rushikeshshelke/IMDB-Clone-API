from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 5
    # page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 2
    last_page_strings = 'end'


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5


class WatchListCPPagination(CursorPagination):
    page_size = 10
    ordering = 'created'
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPagination(PageNumberPagination):
    def get_next_link(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
from rest_framework import pagination, response
from collections import OrderedDict

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 9

    def get_paginated_response(self, data, template_name, status):
        result = OrderedDict([
                ('last_page', self.page.paginator.num_pages),
                ('total_results', self.page.paginator.count),
                ('items_on_page', self.page_size),
                ('current', self.page.number),
                ('next', self.page.next_page_number() if self.page.has_next() else None),
                ('previous', self.page.previous_page_number() if self.page.has_previous() else None),
                ('results', data),
                ('ordering', self.request.GET.get("ordering") if self.request.GET.get("ordering") else None),
            ])
        return response.Response(result, status, template_name)
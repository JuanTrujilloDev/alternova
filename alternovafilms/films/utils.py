from rest_framework import pagination, response
from collections import OrderedDict

class StandardResultsSetPagination(pagination.PageNumberPagination):
    """
    Pagination class for the Get List of Films endpoint

    Args:
        pagination (PageNumberPagination): PageNumberPagination from rest_framework

    Returns:
        StandardResultsSetPagination: Pagination class for the Get List of Films endpoint

    attributes:
        page_size (int): Number of items per page
        page_size_query_param (str): Query param to change the number of items per page
        max_page_size (int): Max number of items per page

    """


    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 9

    def get_paginated_response(self, data, template_name, status):
        """
        get paginated response method

        Args:
            data (dict): Results of the query
            template_name (str): Template name
            status (int): Status code

        Returns:
            Response: Response with the pagination data
        """

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
    
class FilteredDataResultsSetPagination(pagination.PageNumberPagination):
    """
    Pagination class for the Get List of Films endpoint

    Args:
        pagination (PageNumberPagination): PageNumberPagination from rest_framework

    Returns:
        StandardResultsSetPagination: Pagination class for the Get List of Films endpoint

    attributes:
        page_size (int): Number of items per page
        page_size_query_param (str): Query param to change the number of items per page
        max_page_size (int): Max number of items per page
    """


    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 9

    def get_paginated_response(self, data, template_name, status):
        
        filtering_data = data.pop("filtering_data", None)

        result = OrderedDict([
                ('last_page', self.page.paginator.num_pages),
                ('total_results', self.page.paginator.count),
                ('items_on_page', self.page_size),
                ('current', self.page.number),
                ('next', self.page.next_page_number() if self.page.has_next() else None),
                ('previous', self.page.previous_page_number() if self.page.has_previous() else None),
                ('results', data),
                ('ordering', self.request.GET.get("ordering") if self.request.GET.get("ordering") else None),
                ('filtering_data', filtering_data),
            ])
        return response.Response(result, status, template_name)
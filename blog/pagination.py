from rest_framework.pagination import LimitOffsetPagination

# Custom pagination class to handle pagination for Blog API with limit and offset.
class BlogPagination(LimitOffsetPagination):
    # Default number of items per page when no 'limit' is specified in the request.
    default_limit = 10

    # Custom method to get the 'limit' from the request query parameters.
    def get_limit(self, request):
        # Retrieve the 'limit' parameter from the request's query parameters.
        limit = request.query_params.get('limit', None)
        # If a 'limit' is provided in the query params, try to convert it to an integer.
        if limit is not None:
            try:
                return int(limit)
            except ValueError:
                # If the value cannot be converted to an integer, return the default limit.
                return self.default_limit
        # If no 'limit' is provided, return the default limit.
        return self.default_limit if limit is None else limit
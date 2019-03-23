"""This module will encode and parse the query string params."""

from urlparse import parse_qs
import re


def parse_query_params(query_string):
    """
        Function to parse the query parameter string.
        """
    # Parse the query param string
    query_params = dict(parse_qs(query_string))
    # Get the value from the list
    query_params = {k:  re.compile("^" + v[0], re.IGNORECASE) for k, v in query_params.items()}
    print(query_params)
    return query_params

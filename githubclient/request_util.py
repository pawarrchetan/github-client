"""
This module represents a service for connection with github.
"""

"""
Retrieves the query paginated result.
It goes from first til last page, when the last page is defined as pages_allowed.
The query will be performed per each page.
The method concatenates the url mask with which page number (page number at the end, and url_mask in front)

:returns the list of information items, each item is in json format
:raises RequestException if the status of the response for one of the pages
        is not ok
"""

def get_per_page(url_mask, number_of_pages):
    results = []
    for page in range(1, number_of_pages + 1):
        url = url_mask + str(page)
        results_per_page = get(url)

        if len(results_per_page) == 0:
            return results
        results.extend(results_per_page)
    return results

"""
Performs get query on specific url and returns json response.

:raises RequestException if returned status is not ok
"""

def get(url):
    import requests
    response = requests.get(url)
    __if_status_is_not_OK_raise_error(url, response)
    return response.json()

def __if_status_is_not_OK_raise_error(url, response):
    from requests import RequestException

    if response.status_code != 200:
        raise RequestException(
            'Failed to query url {} Returned status: {}'.format(url, response.status_code)
        )

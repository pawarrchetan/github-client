class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

import flask

def client(events_url, commits_url, pages_allowed):
    flask_app_mock = flask.Flask(__name__)
    flask_app_mock.config['GITHUB_EVENTS_URL_MASK'] = events_url
    flask_app_mock.config['GITHUB_COMMITS_URL_MASK'] = commits_url
    flask_app_mock.config['PAGES_ALLOWED'] = pages_allowed
    flask_app_mock.config['THREADS_ALLOWED'] = 4
    return flask_app_mock

NUMBER_OF_PAGES_WITH_RETURNED_RESULTS = 2

def create_mock_for_requests(user, repository, events, commits, commit):
    # This method will be used by the mock to replace requests.get
    def __mock_get_queries(*args):
        import re
        url = args[0]
        if not url:
            from requests import RequestException
            raise RequestException("url should not be none!")
        if re.search(user + '/events', url):
            return MockResponse(events['response'], events['status'])

        if re.search(user + '/' + repository +'/commits/[a-zA-Z0-9]+', url):
            return MockResponse(commit['response'], commit['status'])

        if re.search(user + '/' + repository + '/commits/{0}[a-zA-Z0-9]{0}\?', url):
            if re.search('page=[1-' + str(NUMBER_OF_PAGES_WITH_RETURNED_RESULTS) + ']{1}', url):
                return MockResponse(commits['response'], commits['status'])
            return MockResponse([], commits['status'])

        return MockResponse(None, 404)

    return __mock_get_queries
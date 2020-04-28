import datetime

from unittest import mock, TestCase
from config import GITHUB_EVENTS_URL_MASK, GITHUB_COMMITS_URL_MASK
from requests import RequestException

from githubclient import request_util
from githubclient.models import PUSH_EVENT_TYPE
from githubclient.tests.mock import client, create_mock_for_requests
from githubclient.const import DATETIME_FORMAT

class GithubTest(TestCase):

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events=None,
        commits={
            'status': 404,
            'response': None
        },
        commit=None))
    def test_get_per_page_should_raise_error_on_not_OK_response(self, request_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10) \
                .app_context():
            # action
            # assert
            self.assertRaises(
                RequestException,
                request_util.get_per_page,
                'user/repo/commits?page=',
                10
            )

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events=None, commits={
            'status': 200,
            'response': []
        },
        commit=None))
    def test_get_per_page_should_raise_error_on_missing_pages_allowed_value(self, request_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=None) \
                .app_context():
            # action
            # assert
            self.assertRaises(
                Exception,
                request_util.get_per_page,
                owner='user',
                repository_name='name',
                since=datetime.datetime.today().strftime(DATETIME_FORMAT),
                until=(datetime.datetime.today() - datetime.timedelta(days=1)).strftime(DATETIME_FORMAT)
            )

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events=None,
        commits={
            'status': 200,
            'response': []
        }, commit=None))
    def test_get_per_page_raises_error_on_pages_allowed_value_of_wrong_type(self, request_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed='pages') \
                .app_context():
            # action
            # assert
            self.assertRaises(
                Exception,
                request_util.get_per_page,
                owner='user',
                repository_name='name',
                since=datetime.datetime.today().strftime(DATETIME_FORMAT),
                until=(datetime.datetime.today() - datetime.timedelta(days=1)).strftime(DATETIME_FORMAT)
            )

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events=None, commits={
            'status': 200,
            'response': []
        }, commit=None))
    def test_get_per_page_raises_error_on_missing_url_value(self, request_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=None,
                    pages_allowed=10) \
                .app_context():
            # action
            # assert
            self.assertRaises(
                Exception,
                request_util.get_per_page,
                owner='user',
                repository_name='name',
                since=datetime.datetime.today().strftime(DATETIME_FORMAT),
                until=(datetime.datetime.today() - datetime.timedelta(days=1)).strftime(DATETIME_FORMAT)
            )

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={
            'status': 200,
            'response': [{'url': '/commits/skldSD'}]
        },
        commit=None
    ))
    def test_get_per_page_returns_results_if_the_result_from_next_page_is_empty(self, request_mock):
        # arrange
        expected = {
            'status': 200,
            'response': [{'url': '/commits/skldSD'}]
        }
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10) \
                .app_context():
            # action
            results = request_util.get_per_page(
                'user/repo/commits?page=', 10
            )

            # assert
            self.assertEqual(2, len(results))
            self.assertEqual(expected['response'][0]['url'], results[0]['url'])
            self.assertEqual(expected['response'][0]['url'], results[1]['url'])

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={
            'status': 200,
            'response': [{'url': '/commits/skldSD'}]
        },
        commit=None
    ))
    def test_get_per_page_uses_pages_allowed_parameter_as_limit(self, request_mock):
        # arrange
        expected = {
            'status': 200,
            'response': [{'url': '/commits/skldSD'}]
        }
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=1) \
                .app_context():
            # action
            results = request_util.get_per_page(
                '/user/repo/commits?page=',
                1
            )

            # assert
            self.assertEqual(1, len(results))
            self.assertEqual(expected['response'][0]['url'], results[0]['url'])

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200,
                'response': [{
                    'type': PUSH_EVENT_TYPE,
                    'created_at': ''
                }]},
        commits=None,
        commit=None
    ))
    def test_get_all_events_should_return_events_per_page(self, request_mock):
        # arrange
        expected = [{
            'type': PUSH_EVENT_TYPE,
            'created_at': ''
        }]
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=None,
                    pages_allowed=None) \
                .app_context():
            # action
            results = request_util.get(
                'user/events'
            )

            # assert
            self.assertEqual(1, len(results))
            self.assertEqual(expected[0]['type'], results[0]['type'])
            self.assertEqual(expected[0]['created_at'], results[0]['created_at'])

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={'status': 200, 'response': {'this': 'that'}},
        commit=None
    ))
    def test_get_should_return_results_obtained_from_the_url(self, request_mock):
        # arrange
        expected = {'this': 'that'}
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10) \
                .app_context():
            # action
            result = request_util.get('/user/repo/commits?page=1')
            # assert
            self.assertEqual(expected['this'], result['this'])

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events=None,
        commits={'status': 400, 'response': None},
        commit=None
    ))
    def test_get_should_raise_error_on_not_ok_status(self, request_mock):
        # arrange
        expected = {'this': 'that'}
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10) \
                .app_context():
            # action
            # assert
            self.assertRaises(Exception,
                              request_util.get,
                              username='user',
                              page=1
                              )

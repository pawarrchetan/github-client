from unittest import mock, TestCase
from githubclient.models import PUSH_EVENT_TYPE
from githubclient.api import Api
from config import GITHUB_EVENTS_URL_MASK, GITHUB_COMMITS_URL_MASK
from githubclient.const import DATETIME_FORMAT
from .mock import create_mock_for_requests, client
import datetime

class ApiTest(TestCase):

    # -------------------------- tests active -------------------------------------
    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repository',
        events=None,
        commits=None,
        commit=None
    ))
    def test_active_should_raise_error_on_unknown_user(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            # assert
            self.assertRaises(Exception, Api().active, 'unknown')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events=None,
        commits=None,
        commit=None
    ))
    def test_active_should_raise_error_on_invalid_events_url(self, rerquest_mock):
        # arrange
        with client(events_url='invalid blabla',
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            self.assertRaises(Exception, Api().active, 'user')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 500, 'response': None},
        commits=None,
        commit=None
    ))
    def test_active_should_raise_error_on_not_ok_status(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            self.assertRaises(Exception, Api().active, 'user')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': 'type2',
            'created_at': ''
        }, {
            'type': 'type1',
            'created_at': ''
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_raise_error_if_there_are_no_push_events_and_date_is_missing(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            # assert
            self.assertRaises(Exception, Api().active, 'user')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': 'type1',
            'created_at': datetime.datetime.fromtimestamp(1000).strftime(DATETIME_FORMAT)
        }, {
            'type': 'type2',
            'created_at': datetime.datetime.fromtimestamp(10).strftime(DATETIME_FORMAT)
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_false_if_no_push_events_not_within_last_twenty_four_hours(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            result = Api().active('user')
            # assert
            self.assertFalse(result)

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': 'type1',
            'created_at': datetime.datetime.now().strftime(DATETIME_FORMAT)
        }, {
            'type': 'type2',
            'created_at': datetime.datetime.now().strftime(DATETIME_FORMAT)
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_false_if_no_push_events_within_last_twenty_four_hours(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            result = Api().active('user')
            # assert
            self.assertFalse(result)

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': '',
            'created_at': ''
        }, {
            'type': '',
            'created_at': ''
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_raise_error_if_there_are_no_type_and_date(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            # assert
            self.assertRaises(Exception, Api().active, 'user')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': '',
            'created_at': datetime.datetime.now().strftime(DATETIME_FORMAT)
        }, {
            'type': '',
            'created_at': datetime.datetime.now().strftime(DATETIME_FORMAT)
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_false_if_there_are_no_types_and_events_within_last_day(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            result = Api().active('user')
            # assert
            self.assertFalse(result)

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': '',
            'created_at': datetime.datetime.fromtimestamp(10).strftime(DATETIME_FORMAT)
        }, {
            'type': '',
            'created_at': datetime.datetime.fromtimestamp(100).strftime(DATETIME_FORMAT)
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_false_if_there_are_no_types_and_events_not_within_last_day(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            result = Api().active('user')
            # assert
            self.assertFalse(result)

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': PUSH_EVENT_TYPE,
            'created_at': datetime.datetime.fromtimestamp(1000).strftime(DATETIME_FORMAT)
        }, {
            'type': PUSH_EVENT_TYPE,
            'created_at': datetime.datetime.fromtimestamp(10).strftime(DATETIME_FORMAT)
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_false_if_there_are_push_events_not_within_last_twenty_four_hours(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            result = Api().active('user')
            # assert
            self.assertFalse(result)

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': PUSH_EVENT_TYPE,
            'created_at': ''
        }, {
            'type': PUSH_EVENT_TYPE,
            'created_at': ''
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_raise_error_if_there_are_push_events_and_date_is_missing(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            # assert
            self.assertRaises(Exception, Api().active, 'user')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': PUSH_EVENT_TYPE,
            'created_at': datetime.datetime.now().strftime(DATETIME_FORMAT)
        }, {
            'type': PUSH_EVENT_TYPE,
            'created_at': (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime(DATETIME_FORMAT)
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_true_if_there_are_push_events_within_twenty_four_hours(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            result = Api().active('user')
            # assert
            self.assertTrue(result)

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [{
            'type': PUSH_EVENT_TYPE,
            'created_at': datetime.datetime.fromtimestamp(100).strftime(DATETIME_FORMAT)
        }, {
            'type': PUSH_EVENT_TYPE,
            'created_at': (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime(DATETIME_FORMAT)
        }]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_true_if__push_event_within_twenty_four_hours_among_others(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            result = Api().active('user')
            # assert
            self.assertTrue(result)

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo name',
        events={'status': 200, 'response': [
            {
                'type': PUSH_EVENT_TYPE,
                'created_at': datetime.datetime.now().strftime(DATETIME_FORMAT)
            },
            {
                'type': PUSH_EVENT_TYPE,
                'created_at': (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime(DATETIME_FORMAT)
            },
            {
                'type': 'type 1',
                'created_at': (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime(DATETIME_FORMAT)
            },
            {
                'type': 'type 2',
                'created_at': (datetime.datetime.fromtimestamp(100)).strftime(DATETIME_FORMAT)
            },
            {
                'type': PUSH_EVENT_TYPE,
                'created_at': (datetime.datetime.fromtimestamp(100)).strftime(DATETIME_FORMAT)
            }
        ]},
        commits=None,
        commit=None
    ))
    def test_active_should_return_true_if_there_are_push_events_among_other_events(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            result = Api().active('user')
            # assert
            self.assertTrue(result)

    # ------------------------------ tests downwards -------------------------------------
    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits=None,
        commit=None
    ))
    def test_downwards_should_raise_error_on_unknown_repository(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            # assert
            self.assertRaises(Exception, Api().downwards, 'user', 'unknown')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits=None,
        commit=None
    ))
    def test_downwards_should_raise_error_on_unknown_user(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            self.assertRaises(Exception, Api().downwards, 'unknown', 'repo')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits=None,
        commit=None
    ))
    def test_downwards_should_raise_error_on_invalid_commits_url(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url='lalalalala',
                    pages_allowed=10).app_context():
            # action
            self.assertRaises(Exception, Api().downwards, 'user', 'repo')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits=[{'status': 500,
                  'response': None
                  }],
        commit=None
    ))
    def test_downwards_should_raise_error_on_status_not_ok(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            self.assertRaises(Exception, Api().downwards, 'user', 'repo')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={'status': 200,
                 'response': []
                 },
        commit=None
    ))
    def test_downwards_should_return_false_on_empty_commit_list(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            self.assertFalse(Api().downwards('user', 'repo'))

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={'status': 200,
                 'response': [{'url': None}, {}]
                 },
        commit=None
    ))
    def test_downwards_should_raise_error_on_commit_without_url(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            # assert
            self.assertRaises(Exception, Api().downwards, 'user', 'repo')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={'status': 200,
                 'response': [
                     {
                         'url': '/user/repo/commits/sukjd'
                     }
                 ]},
        commit={'status': 200, 'response': {'stats': {}}}
    ))
    def test_downwards_should_raise_error_on_commit_list_with_empty_stats(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            # assert
            self.assertRaises(Exception, Api().downwards, 'user', 'repo')

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={'status': 200,
                 'response': [{'url': '/user/repo/commits/sukjd'}]
                 },
        commit={'status': 200, 'response': {'stats': {'additions': 12, 'deletions': 12}}}
    ))
    def test_downwards_should_return_false_on_equal_number_of_additions_and_deletions(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            self.assertFalse(Api().downwards('user', 'repo'))

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={'status': 200,
                 'response': [{'url': '/user/repo/commits/sukjd'}]
                 },
        commit={'status': 200, 'response': {'stats': {'additions': 2, 'deletions': 12}}}
    ))
    def test_downwards_should_return_true_on_deletions_more_than_additions(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            self.assertTrue(Api().downwards('user', 'repo'))

    @mock.patch('requests.get', side_effect=create_mock_for_requests(
        user='user',
        repository='repo',
        events=None,
        commits={'status': 200,
                 'response': [{'url': '/user/repo/commits/sukjd'}]
                 },
        commit={'status': 200, 'response': {'stats': {'additions': 12, 'deletions': 2}}}
    ))
    def test_downwards_should_return_false_on_additions_more_than_deletions(self, rerquest_mock):
        # arrange
        with client(events_url=GITHUB_EVENTS_URL_MASK,
                    commits_url=GITHUB_COMMITS_URL_MASK,
                    pages_allowed=10).app_context():
            # action
            self.assertFalse(Api().downwards('user', 'repo'))

import unittest
from githubclient.models import PUSH_EVENT_TYPE, Event
from githubclient import json_parser
from githubclient.const import DATETIME_FORMAT

class JsonParserTest(unittest.TestCase):

    def test_event_from_json_should_raise_an_error_on_missing_date_field(self):
        # arrange
        expected = Event(None, PUSH_EVENT_TYPE)
        event = {'type': PUSH_EVENT_TYPE}
        # action
        # assert
        self.assertRaises(Exception, json_parser.event_from_json, event)

    def test_event_from_json_should_return_event_object_with_date_from_json(self):
        # arrange
        import datetime
        expected = Event(datetime.datetime.now(), PUSH_EVENT_TYPE)
        event = {'type': PUSH_EVENT_TYPE, 'created_at': expected.time.strftime(DATETIME_FORMAT)}
        # action
        result = json_parser.event_from_json(event)
        # assert
        self.assertEqual(expected.time.year, result.time.year)
        self.assertEqual(expected.time.month, result.time.month)
        self.assertEqual(expected.time.day, result.time.day)
        self.assertEqual(expected.time.hour, result.time.hour)
        self.assertEqual(expected.time.minute, result.time.minute)
        self.assertEqual(expected.event_type, result.event_type)

    def test_event_from_json_should_return_event_object_with_empty_fields_from_empty_json(self):
        # arrange
        event = {}
        # action
        # assert
        self.assertRaises(Exception, json_parser.event_from_json, event)

    def test_commit_from_json_should_raise_an_exception_on_empty_json(self):
        # arrange
        commit = {}
        # action
        # assert
        self.assertRaises(Exception, json_parser.commit_from_json, commit)

    def test_commit_from_json_should_raise_error_on_missing_deletions_field(self):
        # arrange
        commit = {'stats': {'additions': 12}}
        # action
        # assert
        # assert
        self.assertRaises(Exception, json_parser.commit_from_json, commit)

    def test_commit_from_json_should_raise_error_with_none_stats_field(self):
        # arrange
        commit = {'stats': None}
        # action
        # assert
        self.assertRaises(Exception, json_parser.commit_from_json, commit)

    def test_commit_from_json_should_raise_error_on_missing_additions_field(self):
        # arrange
        commit = {'stats': {'deletions': 12}}
        # action
        # assert
        self.assertRaises(Exception, json_parser.commit_from_json, commit)

    def test_commit_from_json_should_raise_error_on_missing_additions_and_deletions(self):
        # arrange
        commit = {'stats': {'deletions': None, 'additions': None}}
        # action
        # assert
        self.assertRaises(Exception, json_parser.commit_from_json, commit)

    def test_commit_from_json_should_return_commit_object_from_json_with_additions_and_deletions(self):
        # arrange
        commit = {'stats': {'deletions': 12, 'additions': 54}}
        # action
        result = json_parser.commit_from_json(commit)
        # assert
        self.assertEqual(54, result.get_additions())
        self.assertEqual(12, result.get_deletions())

import unittest

from githubclient import util
from githubclient.models import Commit, Event, PUSH_EVENT_TYPE

class ServiceTest(unittest.TestCase):

    def test_deletions_more_than_additions_should_raise_error_or_none(self):
        self.assertRaises(TypeError, util.deletions_more_than_additions, None)

    def test_deletions_more_than_additions_should_return_false_on_empty_list(self):
        self.assertEquals(False, util.deletions_more_than_additions([]))

    def test_deletions_more_than_additions_should_raise_error_on_non_list(self):
        self.assertRaises(TypeError, util.deletions_more_than_additions, 1)

    def test_deletions_more_than_additions_should_raise_error_on_collection_of_unknown_objects(self):
        self.assertRaises(AttributeError, util.deletions_more_than_additions, [1, 2, 3])

    def test_deletions_more_than_additions_should_return_false_on_equal_additions_and_deletions(self):
        self.assertFalse(util.deletions_more_than_additions([
            Commit(2, 6),
            Commit(3, 8),
            Commit(9, 0)
        ]))

    def test_deletions_more_than_additions_should_return_true_if_deletions_more_than_additions(self):
        self.assertFalse(util.deletions_more_than_additions([
            Commit(15, 6),
            Commit(7, 8),
            Commit(9, 1)
        ]))

    def test_deletions_more_than_additions_should_return_true_if_additions_less_than_deletions(self):
        self.assertTrue(util.deletions_more_than_additions([
            Commit(1, 10),
            Commit(2, 9)
        ]))

    def test_user_pushed_within_twenty_four_hours_should_raise_error_on_none(self):
        self.assertRaises(ValueError, util.user_pushed_within_twenty_four_hours, None)

    def test_user_pushed_within_twenty_four_hours_should_raise_error_on_non_list(self):
        self.assertRaises(ValueError, util.user_pushed_within_twenty_four_hours, {})

    def test_user_pushed_within_twenty_four_hours_error_on_collection_of_not_events(self):
        self.assertRaises(ValueError,
                          util.user_pushed_within_twenty_four_hours,
                          [1, 2, 3])

    def test_user_pushed_within_twenty_four_hours_returns_true_on_push_within_day(self):
        import datetime

        self.assertEquals(True, util.user_pushed_within_twenty_four_hours([
            Event(datetime.datetime.now(), PUSH_EVENT_TYPE),
            Event(datetime.datetime.now() - datetime.timedelta(days=2), PUSH_EVENT_TYPE)
        ]))

    def test_user_pushed_within_twenty_four_hours_should_return_false_on_event_of_type_other_than_push(self):
        import datetime

        self.assertEquals(False, util.user_pushed_within_twenty_four_hours([
            Event(datetime.datetime.today(), "other type")
        ]))

    def test_user_pushed_within_twenty_four_hours_should_return_false_when_there_are_no_events_within_a_day(self):
        import datetime

        self.assertEquals(False, util.user_pushed_within_twenty_four_hours([
            Event(datetime.datetime.today() - datetime.timedelta(days=3), PUSH_EVENT_TYPE),
            Event(datetime.datetime.today() - datetime.timedelta(days=4), PUSH_EVENT_TYPE)
        ]))

    def test_user_pushed_within_twenty_four_hours_should_return_false_on_long_ago_dates(self):
        import datetime

        self.assertEquals(False, util.user_pushed_within_twenty_four_hours([
            Event(datetime.datetime.fromtimestamp(1000), PUSH_EVENT_TYPE)
        ]))

    def test_filter_events_by_type_should_return_events_of_given_type(self):
        # arrange
        events = [Event(None, "type1"), Event(None, "type1"), Event(None, "type2"), Event(None, "type3")]

        # action
        results = util.filter_events_by_type(events, "type1")

        # assert
        self.assertEqual(2, len(results))
        self.assertTrue(events[0] in results)
        self.assertTrue(events[1] in results)

    def test_filter_events_by_type_should_return_empty_list_on_empty_list(self):
        # arrange
        events = []

        # action
        results = util.filter_events_by_type(events, "type1")

        # assert
        self.assertTrue(not results)

    def test_filter_events_by_type_should_return_empty_list_on_missing_events_of_given_type(self):
        # arrange
        events = [Event(None, "type1"), Event(None, "type1"), Event(None, "type2"), Event(None, "type3")]

        # action
        results = util.filter_events_by_type(events, "type4")

        # assert
        self.assertTrue(not results)

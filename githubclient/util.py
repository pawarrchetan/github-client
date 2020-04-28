from datetime import datetime
from .models import Event, PUSH_EVENT_TYPE

"""
Returns a boolean value, indicating, whether the user is active or not.
Checks, whether the user has pushed the code in any repository within the 24 hours. 
:raises ValueError
"""

def user_pushed_within_twenty_four_hours(events):
    if events is None or type(events) is not list:
        raise ValueError('events variable should be list!')

    for event in events:
        if not isinstance(event, Event):
            raise ValueError('the object cannot be checked because it is not the instance of the Event class')
        today = datetime.now()

        if event.time \
                and event.time <= today \
                and (today - event.time).days <= 0 \
                and event.event_type == PUSH_EVENT_TYPE:
            return True

    return False

def deletions_more_than_additions(commits):
    from githubclient.models import Commit
    from functools import reduce

    result = reduce(lambda first, second: Commit(first.get_additions() + second.get_additions(),
                                                 first.get_deletions() + second.get_deletions()), commits, Commit(0, 0))
    return result.get_deletions() > result.get_additions()

def filter_events_by_type(events, event_type):
    results = []

    for event in events:
        if event.event_type == event_type:
            results.append(event)
    return results

"""
This methods defines, which number is eligible for the last page value in paginated queries.
The value for last page is taken from configuration, and the maximum value of pages allowed
is defined in github api https://developer.github.com/v3/ and is fixed.

:returns a number, which denotes the minimum possible last page.
"""

def define_last_page():
    from githubclient.const import MAXIMUM_PAGES_ALLOWED_ON_GITHUB, PAGES_ALLOWED
    from flask import current_app

    configured_last_page = int(current_app.config[PAGES_ALLOWED])
    return min(MAXIMUM_PAGES_ALLOWED_ON_GITHUB, configured_last_page)

def create_has_user_pushed_within_twenty_for_hours_per_page(url_mask):
    def has_user_pushed_within_twenty_for_hours_per_page(page):
        from githubclient import json_parser, request_util, models

        event_objects = map(json_parser.event_from_json, request_util.get(url_mask + str(page)))
        push_events = filter_events_by_type(event_objects, models.PUSH_EVENT_TYPE)

        if user_pushed_within_twenty_four_hours(push_events):
            return True
        return False

    return has_user_pushed_within_twenty_for_hours_per_page

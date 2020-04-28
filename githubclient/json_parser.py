from githubclient.const import DATETIME_FORMAT, \
    GITHUB_CREATED_AT_EVENT_FIELD, \
    GITHUB_TYPE_EVENT_FIELD, \
    GITHUB_STATS_COMMIT_FIELD, \
    GITHUB_ADDITIONS_COMMIT_STATS_FIELD, \
    GITHUB_DELETIONS_COMMIT_STATS_FIELD

class JsonParseError(Exception):
    pass

def event_from_json(json):
    import datetime as dt
    from githubclient.models import Event
    date = dt.datetime.strptime(json[GITHUB_CREATED_AT_EVENT_FIELD], DATETIME_FORMAT)
    event_type = json[GITHUB_TYPE_EVENT_FIELD]

    if event_type is None or date is None:
        raise JsonParseError("Cannot parse json {} and get Event object".format(json))

    return Event(date, event_type)

def commit_from_json(json):
    from githubclient.models import Commit

    commit_stats = json[GITHUB_STATS_COMMIT_FIELD]
    additions = commit_stats[GITHUB_ADDITIONS_COMMIT_STATS_FIELD]
    deletions = commit_stats[GITHUB_DELETIONS_COMMIT_STATS_FIELD]

    if additions is None or deletions is None:
        raise JsonParseError("Cannot retrieve stats values from json {}".format(json))

    return Commit(
        additions=additions,
        deletions=deletions
    )

PUSH_EVENT_TYPE = 'PushEvent'

class Event:
    def __init__(self, time, event_type):
        self.time = time
        self.event_type = event_type

class Commit:
    def __init__(self, additions, deletions):
        self.__additions = additions
        self.__deletions = deletions

    def get_additions(self):
        return self.__additions

    def get_deletions(self):
        return self.__deletions

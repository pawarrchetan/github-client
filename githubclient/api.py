class Api:

    def __init__(self):
        from githubclient.pool_holder import PoolHolder
        self.__pool = PoolHolder.instance().get_pool()

    def active(self, username):
        from flask import current_app
        from githubclient.const import GITHUB_EVENTS_URL_MASK

        url = current_app.config[GITHUB_EVENTS_URL_MASK].format(username)

        from githubclient import util
        has_user_pushed = util.create_has_user_pushed_within_twenty_for_hours_per_page(url)

        start_page = 1
        if has_user_pushed(start_page):
            return True

        pages = range(start_page + 1, util.define_last_page() + 1)
        results = self.__pool.map(has_user_pushed, pages)

        from functools import reduce
        return reduce(lambda first, second: first or second, results)

    def downwards(self, owner, repository_name):
        number_of_days_to_get_commits_for = 7

        from flask import current_app
        from datetime import datetime, timedelta
        from githubclient.const import GITHUB_COMMITS_URL_MASK, DATETIME_FORMAT

        until = datetime.today()
        since = until - timedelta(days=number_of_days_to_get_commits_for)

        url = current_app.config[GITHUB_COMMITS_URL_MASK].format(owner,
                                                                 repository_name,
                                                                 since.strftime(DATETIME_FORMAT),
                                                                 until.strftime(DATETIME_FORMAT))

        from githubclient import request_util, util, json_parser

        stats = request_util.get_per_page(url, util.define_last_page())
        urls = map(lambda stat: stat['url'], stats)
        commits = self.__pool.map(lambda commit_url: json_parser.commit_from_json(request_util.get(commit_url)), urls)

        return util.deletions_more_than_additions(commits)

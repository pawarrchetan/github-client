# Example configuration

# This parameters denotes the maximum number of threads in thread pool.py, which
# is used for parallel querying of third-party apis
THREADS_ALLOWED = 3

#this constant denotes the number of pages allowed to retrieve within github api.
#this number is taken from Github API documentation
#see https://developer.github.com/v3/#pagination
PAGES_ALLOWED = 10

#first argument - username
#second argument - page number. Up to 10 pages is supported
GITHUB_EVENTS_URL_MASK = 'https://api.github.com/users/{}/events?page='

#first argument - user, who owns the repository
#second argument - repository name
#third argument - since parameter, date, from which the commits should be retrieved
#fourth argument - until parameter, date, until which the commits should be retrieved
#fifth argument - page parameter, denotes the page number
GITHUB_COMMITS_URL_MASK = 'https://api.github.com/repos/{}/{}/commits?since={}&until={}&page='

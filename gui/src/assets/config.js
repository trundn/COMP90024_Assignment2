const base_url = 'http://localhost:8000/tweets/';
const config = {
    'polygon_url': base_url + 'polygon/{0}/',
    'statistics_url': base_url + 'statistics-in-polygon/{0}/',
    'tweets_per_hour': base_url + 'tweets-per-hour/',
    'language_statistics_url': base_url + 'language-statistics/',
    'get_most_active_users': base_url + 'get-most-active-users/',
    'find_route_url': base_url + 'find-route/?user_key={0}',
    'get_user_info': base_url + 'get-user-info/{0}'
}

export default config
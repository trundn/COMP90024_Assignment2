const base_url = 'http://localhost:8000/tweets/';
const backendUrl = {
    'list_polygon': base_url + 'polygon/',
    'detail_polygon': base_url + 'polygon/{0}/',
    'statistics_in_polygon': base_url + 'statistics-in-polygon/{0}/',
    'statistics_in_particular_polygon': base_url + 'statistics-in-polygon/',
    'tweets_per_hour': base_url + 'tweets-per-hour/',
    'language_statistics': base_url + 'language-statistics/',
    'total_tweets_by_day_and_hour': base_url + 'total-tweets-by-day-and-hour/',
    'tweets_with_emotion_values_and_pro_cnt': base_url + 'tweets-with-emo-values-and-pro-cnt/?limit={0}&skip={1}',
    'get_most_active_users': base_url + 'get-most-active-users/',
    'find_route_url': base_url + 'find-route/?user_key={0}',
    'get_user_info': base_url + 'get-user-info/{0}',
    'tweets_by_categories': base_url + 'tweets-by-categories/',
    'tweets_with_coordinates': base_url + 'tweets-with-coordinates/',
    'movement': base_url + 'movement/?limit={0}',
    'tweets_by_political_parties': base_url + 'tweets-by-political-parties/'
}

export default backendUrl
const base_url = "http://localhost:8000/tweets/";
export default config = {
    "polygon_url": base_url + "polygon/{0}/",
    "statistics_url": base_url + "statistics-in-polygon/{0}/",
    "tweets_per_hour": base_url + "language-statistics/",
    "language_statistics_url": base_url + "language-statistics/"
}

from app import app
from app.navigation_bar.navigation_bar import NavBarModule
from app.twitter_feed.twitter_feed import TwitterFeedModule
from app.tweet_analytics.tweet_analytics import TweetAnalyticsModule
from Crawler.crawler_API_lib import files_from_directory
import dash_html_components as html
import os

USER_DIRECTORY = 'C:/dev/data/twitter_election_integrity/ira_tweets_csv_hashed/ira_tweet_by_userid_parquet/'
user_files = files_from_directory(USER_DIRECTORY)
user_ids = [os.path.basename(user_file).replace('.parquet', '') for user_file in user_files]

nav_bar = NavBarModule(user_directory=USER_DIRECTORY)
twitter_feed_module = TwitterFeedModule(tab='Tweets')
tweet_analytics_module = TweetAnalyticsModule(tab='Analytics')

app.layout = html.Div(
    [
        nav_bar.layout,
        twitter_feed_module.layout,
        tweet_analytics_module.layout,
        html.Div(id='intermediate-value', style={'display': 'none'})
    ]
)

nav_bar.set_callbacks(app)
twitter_feed_module.set_callbacks(app)
tweet_analytics_module.set_callbacks(app)

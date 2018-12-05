from app import app
from app.twitter_feed.twitter_feed import TwitterFeedModule
from app.tweet_analytics.tweet_analytics import TweetAnalyticsModule
from Crawler.crawler_API_lib import files_from_directory
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import os

USER_DIRECTORY = 'C:/dev/data/twitter_election_integrity/ira_tweets_csv_hashed/ira_tweet_by_userid_parquet/'
user_files = files_from_directory(USER_DIRECTORY)
user_ids = [os.path.basename(user_file).replace('.parquet', '') for user_file in user_files]

tab_style = {
    'backgroundColor': 'rgb(0, 0, 0)',
    'color': 'rgb(255, 255, 255)',
    'borderTop': 'rgb(0, 0, 0)',
    'border-bottom': '0px',
    'border-left': '0px',
    'border-right': '0px',
    'border-top': '0px',
    'font-family': 'WTC BLOX',
    'font-size': '12pt'
}
selected_tab_style = {
    'backgroundColor': 'rgb(0, 0, 0)',
    'color': 'rgb(134, 188, 37)',
    'borderTop': 'rgb(0, 0, 0)',
    'border-bottom': '0px',
    'border-left': '0px',
    'border-right': '0px',
    'border-top': '0px',
    'font-family': 'WTC BLOX',
    'font-size': '12pt'
}

header = html.Div([
    html.Div([
        dcc.Tabs(
            id='tabs',
            value='Twitter Feed',
            children=[
                dcc.Tab(
                    label='Twitter Feed',
                    value='Twitter Feed',
                    style=tab_style,
                    selected_style=selected_tab_style
                ),
                dcc.Tab(
                    label='Tweet Analytics',
                    value='Tweet Analytics',
                    style=tab_style,
                    selected_style=selected_tab_style
                ),
            ]
        ),
        dcc.Dropdown(
            id='user-focus-list',
            options=[
                {'label': user_id, 'value': user_id} for user_id in user_ids
            ],
            value=[],
            placeholder='Select Userid...',
            multi=True,
            style={
                'width': '100%',
                'height': '90%',
                'padding': '8px 12px',
                'border-radius': '2px',
                'background':'rgb(83, 86, 90)',
                'color': 'rgb(0, 0, 0)'
            }
        ),
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Set Focus List',
            style={
                'padding': '1%',
                'width': '10%',
                'color': 'rgb(255, 255, 255)',
                'backgroundColor':'rgb(123, 127, 133)',
                'border-radius': '2px',
                'border-color': 'rgb(149, 152, 157)',
                'border-bottom': '2px',
                'border-left': '2px',
                'border-right': '2px',
                'border-top': '2px'
            }
        ),
    ], style={
        'display': 'flex',
        'flex': 'auto',
        'align-items': 'center',
        'color': 'rgb(255, 255, 255)'
    }
    ),
    html.Div([
        html.Label('Limit Tweets', style={'padding': '5%', 'color': 'rgb(255, 255, 255)'}),
        dcc.Dropdown(
            id='max-rows',
            value='ALL',
            options=[
                {'label': 'ALL', 'value': 'ALL'},
                {'label': '50', 'value': 50},
                {'label': '100', 'value': 100},
                {'label': '1000', 'value': 1000}
            ],
            style={'width': '30%'}),
        html.Label('Limit Date Range', style={'padding': '5%', 'color': 'rgb(255, 255, 255)'}),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=datetime(1900, 1, 1),
            max_date_allowed=datetime.now(),
            initial_visible_month=datetime.now(),
            end_date=datetime.now(),
        )
    ], style={'display': 'flex', 'flex': 'auto', 'align-items': 'center',})
], style={'display': 'flex', 'align-items': 'center', 'backgroundColor': 'rgb(0, 0, 0)'})

twitter_feed_module = TwitterFeedModule(user_directory=USER_DIRECTORY, tab='Twitter Feed')
tweet_analytics_module = TweetAnalyticsModule(tab='Tweet Analytics')

app.layout = html.Div(
    [
        header,
        twitter_feed_module.layout,
        tweet_analytics_module.layout,
        html.Div(id='intermediate-value', style={'display': 'none'})
    ]
)

twitter_feed_module.set_callbacks(app)
tweet_analytics_module.set_callbacks(app)

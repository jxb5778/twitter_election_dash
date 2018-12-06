import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from Crawler.crawler_API_lib import files_from_directory
from app.navigation_bar.navigation_css import *
from app.navigation_bar.navigation_bar_lib import *
from app.tweet_analytics.twitter_analytics_lib import *
from datetime import datetime
import json
import os


class NavBarModule(object):
    def __init__(self, user_directory):
        self.USER_DIRECTORY = user_directory
        self.user_files = files_from_directory(self.USER_DIRECTORY)
        self.user_ids = [os.path.basename(user_file).replace('.parquet', '') for user_file in self.user_files]

        self.layout = html.Div([
            html.Div([
                dcc.Tabs(
                    id='tabs',
                    value='Tweets',
                    children=[
                        dcc.Tab(
                            label='Tweets',
                            value='Tweets',
                            style=tab_style,
                            selected_style=selected_tab_style
                        ),
                        dcc.Tab(
                            label='Analytics',
                            value='Analytics',
                            style=tab_style,
                            selected_style=selected_tab_style
                        ),
                    ]
                ),
                dcc.Dropdown(
                    id='user-focus-list',
                    options=[
                        {'label': user_id, 'value': user_id} for user_id in self.user_ids
                    ],
                    value=[],
                    placeholder='Select Userid...',
                    multi=True,
                    style=user_focus_list
                ),
                html.Button(
                    id='submit-button',
                    n_clicks=0,
                    children='Set Focus List',
                    style=submit_button
                ),
            ], style={
                'display': 'flex',
                'flex': 'auto',
                'align-items': 'center',
                'color': 'rgb(255, 255, 255)'
            }
            ),
            html.Div([
                html.Label('Limit Tweets', style=limit_tweets),
                dcc.Dropdown(
                    id='max-rows',
                    value='ALL',
                    options=[
                        {'label': '50', 'value': 50},
                        {'label': '100', 'value': 100},
                        {'label': '1000', 'value': 1000},
                        {'label': 'ALL', 'value': 'ALL'}
                    ],
                    style={'width': '30%', 'font-family': 'WTC BLOX'}),
                html.Label('Limit Date Range', style=limit_date_range),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=datetime(1900, 1, 1),
                    max_date_allowed=datetime.now(),
                    initial_visible_month=datetime.now(),
                    end_date=datetime.now(),
                )
            ], style={'display': 'flex', 'flex': 'auto', 'align-items': 'center'})
        ], style={'display': 'flex', 'align-items': 'center', 'backgroundColor': 'rgb(0, 0, 0)'})
        return

    def set_callbacks(self, app):

        @app.callback(
            Output('intermediate-value', 'children'),
            [Input('submit-button', 'n_clicks')],
            [
                State('user-focus-list', 'value'),
                State('max-rows', 'value'),
                State('date-picker-range', 'start_date'),
                State('date-picker-range', 'end_date')
            ]
        )
        def set_focus_list(n_clicks, user_focus_list, max_rows, start_date, end_date):

            if n_clicks == 0:
                return pd.DataFrame({}).to_json(date_format='iso', orient='split')

            focus_data = Buffer()

            focus_data.value = read_focus_data(user_focus_list, self.USER_DIRECTORY)
            focus_data.value = filter_to_date_range(focus_data.value, start_date, end_date)

            try:
                max_rows_int = int(max_rows)
            except (TypeError, ValueError):
                max_rows_int = len(focus_data.value)

            table_df = focus_data.value.head(max_rows_int)
            word_frequency_df = generate_top_results_dataframe(focus_data.value, count_results=10)
            tweet_frequency_df = generate_tweet_frequency_dataframe(focus_data.value)

            datasets = {
                'table': table_df.to_json(date_format='iso', orient='split'),
                'word_frequency_df': word_frequency_df.to_json(date_format='iso', orient='split'),
                'tweet_frequency_df': tweet_frequency_df.to_json(date_format='iso', orient='split'),
            }

            return json.dumps(datasets)

        return

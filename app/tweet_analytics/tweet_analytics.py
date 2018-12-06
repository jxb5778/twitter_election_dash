from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import json
from app.tweet_analytics.twitter_analytics_lib import *


class TweetAnalyticsModule(object):

    def __init__(self, tab):
        self.id = 'tweet-analytics'
        self.tab = tab
        self.style = {'display': 'none', 'padding': '8px'}

        self.layout = html.Div(
            id=self.id,
            children=[
                    html.Div([dcc.Graph(id='word-frequency')], style={'display': 'inline-block'}),
                    html.Div([dcc.Graph(id='tweet-frequency')], style={'display': 'inline-block'}),
                    dcc.Input(
                        id='tweet-polarity-text',
                        placeholder='Word Polarity History...',
                        value='',
                        type='text',
                        style={'display': 'block', 'width': '30%', 'color': 'rgb(0, 0, 0)'}
                    ),
                    dcc.Graph(id='tweet-polarity', style={'display': 'inline-block'}),
            ], style=self.style
        )

    def set_callbacks(self, app):

        @app.callback(Output(self.id, 'style'), [Input('tabs', 'value')])
        def display_module(tab):
            if tab == self.tab:
                self.style['display'] = 'block'
                return self.style
            self.style['display'] = 'none'
            return self.style

        @app.callback(Output('word-frequency', 'figure'), [Input('intermediate-value', 'children')])
        def update_word_frequency_graph(jsonified_cleaned_data):
            datasets = json.loads(jsonified_cleaned_data)
            try:
                top_results_df = pd.read_json(datasets['word_frequency_df'], orient='split')
            except ValueError:
                return {}

            if top_results_df.empty:
                return {}

            return {
                'data': [
                    {
                        'x': top_results_df['count'],
                        'y': top_results_df['word'],
                        'type': 'bar',
                        'orientation': 'h',
                        'marker': {
                            'color': 'rgb(134, 188, 37)'
                        }
                    }
                ],
                'layout': {
                    'title': 'Most Frequent Words'
                }
            }

        @app.callback(Output('tweet-frequency', 'figure'), [Input('intermediate-value', 'children')])
        def update_tweet_frequencies(jsonified_cleaned_data):
            datasets = json.loads(jsonified_cleaned_data)
            try:
                tweet_frequency_df = pd.read_json(datasets['tweet_frequency_df'], orient='split')
            except ValueError:
                return {}

            if tweet_frequency_df.empty:
                return {}

            return {
                'data': [
                    {
                        'x': tweet_frequency_df['tweet_year'],
                        'y': tweet_frequency_df['tweet_year_freq'],
                        'type': 'bar',
                        'marker': {
                            'color': 'rgb(134, 188, 37)'
                        }
                    }
                ],
                'layout': {
                    'title': 'Tweet Frequency',
                    'xaxis': {
                        'showgrid': False,
                        'nticks': len(tweet_frequency_df['tweet_year']) + 1
                    }
                }
            }

        @app.callback(
            Output('tweet-polarity', 'figure'),
            [Input('intermediate-value', 'children'), Input('tweet-polarity-text', 'value')]
        )
        def update_tweet_polarity_graph(jsonified_cleaned_data, input_text):
            datasets = json.loads(jsonified_cleaned_data)
            try:
                dff = pd.read_json(datasets['table'], orient='split')
            except ValueError:
                return html.Div([])

            if dff.empty:
                return html.Div([])

            tweet_polarity_df = generate_tweet_polarity_dataframe(dff, input_text)

            return {
                'data': [
                    {
                        'x': tweet_polarity_df['tweet_time'],
                        'y': tweet_polarity_df['tweet_polarity_rolling'],
                        'marker': {
                            'color': 'rgb(134, 188, 37)'
                        }
                    }
                ],
                'layout': {
                    'title': 'Polarity of Tweets with "{}"'.format(input_text),
                    'xaxis': {
                        'showgrid': False,
                        'nticks': 10
                    }
                }
            }

        return
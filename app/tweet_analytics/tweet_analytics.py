from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
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

            try:
                dff = pd.read_json(jsonified_cleaned_data, orient='split')
            except ValueError:
                return html.Div([])

            if dff.empty:
                return html.Div([])

            top_results_df = generate_top_results_dataframe(dff, count_results=10)

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

            try:
                dff = pd.read_json(jsonified_cleaned_data, orient='split')
            except ValueError:
                return html.Div([])

            if dff.empty:
                return html.Div([])

            tweet_frequency_df = generate_tweet_frequency_dataframe(dff)

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

        return
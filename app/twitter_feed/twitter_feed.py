from app.twitter_feed.twitter_feed_lib import *
from dash.dependencies import Input, Output
import dash_html_components as html
import pandas as pd
import json


class TwitterFeedModule(object):

    def __init__(self, tab):
        self.id = 'twitter-feed'
        self.tab = tab
        self.style = {'display': 'none'}
        self.layout = html.Div(id=self.id,
            children=[
                html.Table(id='table'),
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

        @app.callback(Output('table', 'children'), [Input('intermediate-value', 'children')])
        def update_table(jsonified_cleaned_data):
            datasets = json.loads(jsonified_cleaned_data)
            try:
                dff = pd.read_json(datasets['table'], orient='split')
            except ValueError:
                return html.Div([])

            if dff.empty:
                return html.Div([])

            table = create_table(dff)

            return table

        return

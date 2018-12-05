from app.twitter_feed.twitter_feed_helper_lib import *
from dash.dependencies import Input, Output, State
import dash_html_components as html
import pandas as pd


class TwitterFeedModule(object):

    def __init__(self, user_directory, tab):
        self.id = 'twitter-feed'
        self.tab = tab
        self.style = {'display': 'none'}

        self.USER_DIRECTORY = user_directory
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

            focus_data.value = focus_data.value.head(max_rows_int)

            return focus_data.value.to_json(date_format='iso', orient='split')

        @app.callback(Output('table', 'children'), [Input('intermediate-value', 'children')])
        def update_table(jsonified_cleaned_data):
            try:
                dff = pd.read_json(jsonified_cleaned_data, orient='split')
            except ValueError:
                return html.Div([])

            if dff.empty:
                return html.Div([])

            table = create_table(dff)

            return table

        return

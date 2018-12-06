from dateutil.parser import parse
from Crawler.buffer import Buffer
import pandas as pd


def read_focus_data(user_focus_list, user_directory):
    reader = Buffer()
    focus_data = Buffer()

    focus_data.value = []

    for user_id in user_focus_list:
        reader.value = pd.read_parquet('{}{}.parquet'.format(user_directory, user_id), engine='pyarrow')
        focus_data.value.append(reader.value)

    focus_data.value = pd.concat(focus_data.value)[['userid', 'tweet_text', 'tweet_time']]

    return focus_data.value


def filter_to_date_range(df, start_date, end_date):

    dff = df.sort_values(by='tweet_time', ascending=False)

    dff['tweet_time_parsed'] = [parse(str(tweet_time)) for tweet_time in dff['tweet_time']]

    if start_date is None:
        start_date_parsed = dff['tweet_time_parsed'].min()
    else:
        start_date_parsed = parse(start_date)

    if end_date is None:
        end_date_parsed = dff['tweet_time_parsed'].max()
    else:
        end_date_parsed = parse(end_date)

    if start_date_parsed > dff['tweet_time_parsed'].max():
        start_date_parsed = dff['tweet_time_parsed'].max()

    if end_date_parsed < start_date_parsed:
        end_date_parsed = start_date_parsed

    dff = dff.query('(tweet_time_parsed >= @start_date_parsed) & (tweet_time_parsed <= @end_date_parsed)')

    return dff.drop(columns=['tweet_time_parsed'])
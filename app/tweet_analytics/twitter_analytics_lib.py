from Elections.election_lib import generate_corpus_for_user, top_results_across_corpus
from dateutil.parser import parse
import pandas as pd


def generate_top_results_dataframe(dff, count_results):
    dff['tweet_time'] = dff['tweet_time'].map(str)
    dictionary, corpus = generate_corpus_for_user(dff)

    words = []
    counts = []

    for word_count in top_results_across_corpus(dictionary, corpus, count_results=count_results):

        words.append(word_count[0])
        counts.append(word_count[1])

    return pd.DataFrame({'word': words, 'count': counts})


def generate_tweet_frequency_dataframe(dff):
    dff['tweet_time'] = dff['tweet_time'].map(str)
    dff['tweet_year'] = dff['tweet_time'].apply(lambda x: parse(x).year)
    dff['tweet_year_freq'] = dff.groupby('tweet_year')['tweet_year'].transform('count')

    return dff[['tweet_year', 'tweet_year_freq']].drop_duplicates().sort_values(by='tweet_year')

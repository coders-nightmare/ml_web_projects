from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extractor = URLExtract()


def fetch_stats(selected_user, df):

    if(selected_user != 'All'):
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)

    # fetchig number of media messages
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetching urls
    urls = []
    for message in df['message']:
        urls.extend(extractor.find_urls(message))
    num_urls = len(urls)
    return num_messages, num_words, num_media, num_urls


def most_busy_users(df):
    x = df['user'].value_counts().head()
    name = x.index
    count = x.values
    # chat percentage per user
    df = round((df['user'].value_counts()/df.shape[0])*100,
               2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return name, count, df


def create_wordcloud(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    wc = WordCloud(background_color='white')
    df_wc = wc.generate(
        df[df['message'] != '<Media omitted>\n']['message'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    # removing media
    nm_df = df[df['message'] != '<Media omitted>\n']
    # removing group notfication
    temp_df = nm_df[nm_df['user'] != 'group_notification']

    # most used words
    words = []
    for message in temp_df['message']:
        words.extend(message.split())
    muw_df = pd.DataFrame(Counter(words).most_common(20))
    return muw_df


def emoji_helper(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    e_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return e_df

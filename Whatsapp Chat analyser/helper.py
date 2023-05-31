from urlextract import URLExtract

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

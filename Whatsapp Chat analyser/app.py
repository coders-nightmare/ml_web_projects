import streamlit as st
import preprocessor as pp
import helper


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # the date we got is in byte now to change in string
    data = bytes_data.decode('utf-8')

    # displaying text
    # st.text(data)

    # preprocessing data
    df = pp.preprocess(data)

    # displaying df
    st.dataframe(df)

    # fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'All')

    # selectbox for user list
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # show analysis
    if st.sidebar.button('Show Analysis'):

        # User Stats
        num_messages, num_words, num_media, num_urls = helper.fetch_stats(
            selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Urls Shared")
            st.title(num_urls)

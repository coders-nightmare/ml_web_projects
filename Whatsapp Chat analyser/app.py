import streamlit as st
import preprocessor as pp
import helper
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

        # finding busiest users in the group
        if selected_user == 'All':
            st.title('Most Busy Users')
            names, counts, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(names, counts, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)

        # most_common words
        most_common_df = helper.most_common_words(selected_user, df)
        st.title('Most Used Words')

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        # emoji counter
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(10),
                   labels=emoji_df[0].head(10), autopct='%0.2f')
            st.pyplot(fig)

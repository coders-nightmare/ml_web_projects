import streamlit as st
import pickle
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
import nltk


tfidf = pickle.load(open('E:\DataSets\pickle_files\sms_vectorizer.pkl', 'rb'))
model = pickle.load(open('E:\DataSets\pickle_files\sms_model.pkl', 'rb'))

st.title('Email/SMS Spam Classifier')


# preprocess funciton
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    stop_words = stopwords.words('english')
    punctuations = string.punctuation
    ps = PorterStemmer()
    for i in text:
        if i.isalnum() and i not in stop_words and i not in punctuations:
            y.append(ps.stem(i))
    return " ".join(y)


input_sms = st.text_area('Enter The Message')

if st.button("Predict"):
    # transform input text
    transformed_sms = transform_text(input_sms)

    # vectorize transfromed_sms
    vector_input = tfidf.transform([transformed_sms])

    # prdicting
    result = model.predict(vector_input)[0]

    # Result
    if result == 1:
        st.header('SPAM')
    else:
        st.header('HAM')

import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

st.set_page_config(
    page_title="Female Diabetes Prediction",
    page_icon="🧊")


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum() and i not in stopwords.words("english") and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


tfidf = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

st.title("SMS Spam Detector")

sms = st.text_input("Enter the message")

if st.button("Predict"):
    # 1. preprocess
    trans_sms = transform_text(sms)

    # 2. vectorize
    vector_input = tfidf.transform([trans_sms])

    # 3. Model predict
    result = model.predict(vector_input)[0]
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")

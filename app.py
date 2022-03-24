import streamlit as st
import streamlit.components.v1 as components
import twitter_page
import google_news

st.set_page_config(page_title="Sentiment Analyser", page_icon=":chart:", layout="wide")

c1, empty_space, c2, empty_space2 = st.columns([2.5,0.5,1.75, 0.5])

c1.markdown("# Sentiment Analyser")
option = st.sidebar.selectbox("Select analyser:",
            ('VADER',))
datasource = st.sidebar.selectbox("Select data source: ",
            ('Twitter', 'Google News'))

searchTerm = str(c1.text_area('Input',placeholder='Enter the word/sentence/hashtag to analyse.'))

if(datasource=='Twitter'):
    noOfTerms = int(c1.select_slider("Input number of terms. (Note: >100 may take time)", options=['10', '30', '50', '100', '200', '500'], value='30'))
else:
    st.markdown("Note: For Google News, only 10 recent news articles is supported.")

if(option=='VADER' and datasource=='Twitter' and noOfTerms and searchTerm):
    twitter_page.show_trends(container=c2)
    twitter_page.twitter_gui(noOfTerms, st, c1, option, searchTerm)
if(option=='VADER' and datasource=='Google News' and searchTerm):
    google_news.news_gui(st, c1, searchTerm)

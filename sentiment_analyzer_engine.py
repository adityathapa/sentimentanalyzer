import matplotlib
import tweepy, re
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import nltk
import streamlit as st
import tkinter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
matplotlib.use('TkAgg')

# twitter authentication
consumerKey = '*'
consumerSecret = '*'
accessToken = '*'
accessTokenSecret = '*'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

st.markdown("# Sentiment Analyser")

searchTerm = st.text_area('Input','Enter the word/sentence/hashtag to analyse.')
if searchTerm:
    noOfTerms = int(st.number_input('Input nubmer'))
print(searchTerm)
print(noOfTerms)
if noOfTerms:
    tweets = []
    tweetText = []
    #searching the tweets
    tweets = tweepy.Cursor(api.search, q=searchTerm+" -filter:retweets", lang = "en").items(noOfTerms)

    tweet_list = [tweet.text for tweet in tweets]
    tweet_df = pd.DataFrame(tweet_list)
    tweet_df

    def clean_data(text):
        return ' '.join(re.sub("(@[a-zA-Z0-9]+)|([^0-9A-Za-z])|(https://[\w.]+/[\w]+)", " ", text).split())

    tweet_df['cleaned_data'] = tweet_df[0].apply(clean_data)
    tweet_df

    def rem_numbers(text):
        list_new = []
        for word in text:
            if word.isalpha() or word==" ":
                list_new.append(word)
        return ''.join(list_new)

    tweet_df['cleaned_data'] = tweet_df['cleaned_data'].apply(rem_numbers)
    tweet_df

    def lower_char(text):
        list_new = word_tokenize(text)
        lower_text = [x.lower() for x in list_new]
        return ' '.join(lower_text)

    tweet_df['cleaned_data'] = tweet_df['cleaned_data'].apply(lower_char)
    tweet_df

    lemmatizer = WordNetLemmatizer()
    def lemmatise(text):
        text_tokens = word_tokenize(text)
        text_lemm = [lemmatizer.lemmatize(word) for word in text_tokens]
        return ' '.join(text_lemm)

    tweet_df['cleaned_data'] = tweet_df['cleaned_data'].apply(lemmatise)
    tweet_df

    tweet_df['cleaned_data'].values

    def remove_stopword(text):
        text_tokens = word_tokenize(text)
        tokens = [word for word in text_tokens if not word in set(stopwords.words('english'))]
        tokens_text = ' '.join(tokens)
        return tokens_text

    tweet_df['cleaned_data'] = tweet_df['cleaned_data'].apply(remove_stopword)
    tweet_df

    #Calculating sentiment polarity
    def get_polarity(text):
        textblob = TextBlob(str(text))
        pol = textblob.sentiment.polarity
        if(pol==0):
            return "Neutral"
        elif(pol>0 and pol<=0.3):
            return "Weakly Positive"
        elif(pol>0.3 and pol<=0.6):
            return "Positive"
        elif(pol>0.6 and pol<=1):
            return "Strongly Positive"
        elif(pol>-0.3 and pol<=0):
            return "Weakly Negative"
        elif(pol>-0.6 and pol<=0.3):
            return "Negative"
        elif(pol>1 and pol<=0.6):
            return "Strongly Negative"
        
    tweet_df['polarity'] = tweet_df['cleaned_data'].apply(get_polarity)
    tweet_df

    neutral = 0
    wpositive = 0
    spositive = 0
    positive = 0
    negative = 0
    snegative = 0
    wnegative = 0
    polarity = 0

    for i in range(0,noOfTerms):
        textblob = TextBlob(str(tweet_df['cleaned_data'][i]))
        polarity += textblob.sentiment.polarity
        pol = textblob.sentiment.polarity
        if(pol==0):
            neutral += 1
        elif(pol>0 and pol<=0.3):
            wpositive += 1
        elif(pol>0.3 and pol<=0.6):
            positive += 1
        elif(pol>0.6 and pol<=1):
            spositive += 1
        elif(pol>-0.3 and pol<=0):
            wnegative += 1
        elif(pol>-0.6 and pol<=0.3):
            negative += 1
        elif(pol>1 and pol<=0.6):
            snegative += 1

    #average reaction
    polarity = polarity / noOfTerms
    polarity

    def percentage(part, whole):
        temp = 100 * float(part)/float(whole)
        return format(temp, '.2f')

    #percentage of people reactions
    neutral = percentage(neutral, noOfTerms)
    wpositive = percentage(wpositive, noOfTerms)
    spositive = percentage(spositive, noOfTerms)
    positive = percentage(positive, noOfTerms)
    negative = percentage(negative, noOfTerms)
    snegative = percentage(snegative, noOfTerms)
    wnegative = percentage(wnegative, noOfTerms)

    st.header("How people are reacting on [" + searchTerm + "] by analyzing " + str(noOfTerms) + " tweets.")
    print()
    st.subheader("General Report: ")

    if(polarity==0):
            st.markdown("***Neutral***")
    elif(polarity>0 and polarity<=0.3):
            st.markdown("***Weakly Positive***")
    elif(polarity>0.3 and polarity<=0.6):
            st.markdown("***Positive***")
    elif(polarity>0.6 and polarity<=1):
            st.markdown("***Strongly Positive***")
    elif(polarity>-0.3 and polarity<=0):
            st.markdown("***Weakly Negative***")
    elif(polarity>-0.6 and polarity<=0.3):
            st.markdown("***Negative***")
    elif(polarity>1 and polarity<=0.6):
            st.markdown("***Strongly Negative***")


    st.subheader("Detailed Report: ")
    st.markdown("**"+ str(positive) + "**% people thought it was positive")
    st.markdown("**"+ str(wpositive) + "**% people thought it was weakly positive")
    st.markdown("**"+ str(spositive) + "**% people thought it was strongly positive")
    st.markdown("**"+ str(negative) + "**% people thought it was negative")
    st.markdown("**"+ str(wnegative) + "**% people thought it was weak negative")
    st.markdown("**"+ str(snegative) + "**% people thought it was strongly negative")
    st.markdown("**"+ str(neutral) + "**% people thought it was neutral")

    st.subheader("Pie Chart:")

    sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
            'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
            'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
            'Strongly Negative [' + str(snegative) + '%]']

    fig1, ax1 = plt.subplots()
    fig1.subplots_adjust(0.3, 0, 1, 1)
    
    theme = plt.get_cmap('bwr')
    ax1.set_prop_cycle("color", [theme(1. * i / len(sizes))
                                for i in range(len(sizes))])
    
    _, _ = ax1.pie(sizes, startangle=90, radius=1800)
    
    ax1.axis('image')
    plt.legend(labels=labels, loc=3,  bbox_to_anchor=(-0.1, 0.3),
        bbox_transform=fig1.transFigure)
    plt.tight_layout()
    st.pyplot(plt)

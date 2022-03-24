from logging import exception
import tweepy, re
import pandas as pd
import nltk
from emoji import UNICODE_EMOJI_ENGLISH
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import numpy as np
import pandas as pd
import re
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

#calling SentimentIntensityAnalyser() object
analyser = SentimentIntensityAnalyzer()

# twitter authentication
consumerKey = '7qWxOSZyRP0BxgV4nBoLY7vRQ'
consumerSecret = 'zWeSmr5583y8bYsL4ndSz1u1gUaaY7TXVURJECRGjhsRWK1RGJ'
accessToken = '973813387858673665-jWYUfTDNcGZ8Yy81c1rjcv8afCT4rrf'
accessTokenSecret = 'epLaVzAEG5Tn7RjIzN1IYljnC0VNUppJkLkzARnUZ7n90'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_api():
    return api

def scraper(searchTerm, noOfTerms):
    tweets = []
    #searching the tweets
    try:
        tweets = tweepy.Cursor(api.search_tweets, q=str(searchTerm)+" -filter:retweets", lang = "en").items(noOfTerms)
    except exception as e:
        print(e)
    print(tweets)
    return tweets

def tweet_analysis(tweets, noOfTerms, mode):  
    tweet_df = pd.DataFrame(tweets)
        
    def clean_data(text):
        text = re.sub(r'@[A-Za-z0-9]+', '', text) #remove @mention
        text = re.sub(r'#', '', text)   #remove hashtag
        text = re.sub(r'RT[\s]+', '', text)  #remove RT
        text = re.sub(r'https?:\/\/\S+', '', text) #remove hyperlink
        
        return text

    tweet_df['cleaned_data'] = tweet_df[0].apply(clean_data)

    def isEmoji(s):
        return s in UNICODE_EMOJI_ENGLISH

    def rem_numbers(text):
        list_new = []
        for word in text:
            if not word.isnumeric():
                if word.isalpha() or isEmoji(word) or word == ' ': 
                    list_new.append(word)
        return ''.join(list_new)

    tweet_df['cleaned_data'] = tweet_df['cleaned_data'].apply(rem_numbers)

    #Calculating sentiment polarity

    if(mode is 'VADER'):
        def get_polarity(text):
            pol = analyser.polarity_scores(str(text))
            return pol['compound']
            
        tweet_df['polarity'] = tweet_df['cleaned_data'].apply(get_polarity)

        neutral = 0
        positive = 0
        negative = 0
        polarity = 0

        for i in range(0,noOfTerms):
            polarity += tweet_df['polarity'][i]
            compound = tweet_df['polarity'][i]

            if(compound>-0.05 and compound <0.05):
                neutral += 1
            elif(compound>=0.05):
                positive += 1
            elif(compound<=-0.05):
                negative += 1

        #average reaction
        polarity = polarity / noOfTerms

        def percentage(part, whole):
            temp = 100 * float(part)/float(whole)
            return format(temp, '.2f')

        #percentage of people reactions
        neutral = percentage(neutral, noOfTerms)
        positive = percentage(positive, noOfTerms)
        negative = percentage(negative, noOfTerms)

        final_results = {
            "polarity": polarity,
            "neutral": neutral,
            "positive": positive,
            "negative": negative
        }

        return final_results
            


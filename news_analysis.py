from newspaper import Article
from newspaper import Config
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
config = Config()

def news_analysis(news_list):
    df = news_list
    try:
        list =[] #creating an empty list 
        for i in df.index:
            dict = {} #creating an empty dictionary to append an article in every single iteration
            article = Article(df['link'][i],config=config) #providing the link
            try:
                article.download() #downloading the article 
                article.parse() #parsing the article
                article.nlp() #performing natural language processing (nlp)
            except:
                pass 
            dict['Summary']=article.summary
            print(dict)
            list.append(dict)
        check_empty = not any(list)
        # print(check_empty)
        if check_empty == False:
            news_df=pd.DataFrame(list) #creating dataframe

    except Exception as e:
        #exception handling
        print("exception occurred:" + str(e))
        print('Looks like, there is some error in retrieving the data, Please try again or try with a different search term.' )
    
    def percentage(part,whole):
        return 100 * float(part)/float(whole)

    #Assigning Initial Values
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    #Iterating over the tweets in the dataframe
    for news in news_df['Summary']:
        analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
        neg = analyzer['neg']
        neu = analyzer['neu']
        pos = analyzer['pos']
        polarity += analyzer['compound']

        if neg > pos:
            negative += 1 #increasing the count by 1
        elif pos > neg:
            positive += 1 #increasing the count by 1
        elif pos == neg:
            neutral += 1 #increasing the count by 1

    polarity = polarity/len(news_df)

    positive = percentage(positive, len(news_df)) #percentage is the function defined above
    negative = percentage(negative, len(news_df))
    neutral = percentage(neutral, len(news_df))

    final_results = {
            "polarity": polarity,
            "neutral": neutral,
            "positive": positive,
            "negative": negative
        }

    return final_results
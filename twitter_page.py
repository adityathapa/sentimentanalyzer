import re
import pandas as pd
import twitter_analysis as twan
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from langdetect import detect
import hydralit_components as hc

def get_woeid(place, api):
    '''Get woeid by location'''
    try:
        trends = api.available_trends()
        for val in trends:
            if (val['name'].lower() == place.lower()):
                return(val['woeid']) 
        print('Location Not Found')
    except Exception as e:
        print('Exception:',e)
        return(0)
 
def show_trends(container,api=twan.get_api(), count=20):
    container.markdown("## <font color='#FFB52E'>#Latest Trends</font>", unsafe_allow_html=True)
    loc_id = get_woeid('New Zealand', api)
    
    '''Get Trending Tweets by Location'''
    import iso639
    try:
        trends = api.get_place_trends(loc_id)
        df = pd.DataFrame([trending['name'],  trending['tweet_volume'], iso639.to_name(detect(trending['name']))] for trending in trends[0]['trends'])
        df.columns = ['Trends','Volume','Language']
        #df = df.sort_values('Volume', ascending = False)
        final_trends = (df[:count])
    except Exception as e:
        print("An exception occurred",e)   

    for i in range(1,len(final_trends)):
        if(str(final_trends.loc[i,'Volume'])!='nan'):
            trend = str(final_trends.loc[i,'Trends'])
            volume = (str(int(final_trends.loc[i,'Volume'])))
            container.markdown("""<h5 style="text-align:left;">"""+trend+"""<span style="float:right;color:#FFB52E">"""+volume+" tweets", unsafe_allow_html=True)

def twitter_gui(noOfTerms, st, c1, mode, searchTerm):
    if noOfTerms:
        tweets = twan.scraper(searchTerm, noOfTerms)

        c1.markdown("## Some recent tweets about the topic.")
        c1.markdown("  ")

        def show_tweets(x):
            container = st.container()
            with container:
                col1, col2, col3 = st.columns(([1,1,2]))
                container.markdown("""<hr style='border-top: 2px solid #FFB52E; width:50%; border-radius: 3px;'></hr>""", unsafe_allow_html=True)
                with col1:
                    col1.image(x.user.profile_image_url)
                    col1.caption("@"+x.user.screen_name)
                with col2:
                    col2.write(x.text)


        tweet_list = []
        hashtag_list = []
        no = 10

        

        for x in tweets:
            tweet_list.append(x.text)
            if no!= 0:
                show_tweets(x)
                st.write("\n")
            else:
                continue
            no-=1
        show_tweets_is_done = 1
        
        scores = twan.tweet_analysis(tweet_list, noOfTerms, mode)

        polarity = scores["polarity"]
        neutral = scores["neutral"]
        positive = scores["positive"]
        negative = scores["negative"]
        
        if(show_tweets_is_done):
            theme_bad = {'bgcolor': '#FFF0F0','title_color': 'red','content_color': 'red','icon_color': 'red', 'icon': 'fa fa-times-circle'}

            cc = st.columns(5)
            with cc[0]:
            # can just use 'good', 'bad', 'neutral' sentiment to auto color the card
                hc.info_card(title='Positive', content=str(positive)+'% people think the term is positive.', sentiment='good',bar_value=positive)

            with cc[1]:
                hc.info_card(title='Negative', content=str(negative)+'% people think the term is negative.',bar_value=negative,theme_override=theme_bad)

            with cc[2]:
                hc.info_card(title='Neutral', content=str(neutral)+'% people think the term is neutral.', sentiment='neutral',bar_value=neutral)

            st.subheader("General Report: ")

            if(polarity>-0.05 and polarity <0.05):
                    st.markdown("***Neutral***")
            elif(polarity>=0.05):
                    st.markdown("***Positive***")
            elif(polarity<=-0.05):
                    st.markdown("***Negative***")

            st.subheader("Detailed Report: ")
            st.markdown("**"+ str(positive) + "**% people thought it was positive")
            st.markdown("**"+ str(negative) + "**% people thought it was negative")
            st.markdown("**"+ str(neutral) + "**% people thought it was neutral")

            st.subheader("Pie Chart:")

            sizes = [positive, neutral, negative]
            labels = ['Positive [' + str(positive) + '%]','Neutral [' + str(neutral) + '%]',
                    'Negative [' + str(negative) + '%]']

            fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
            fig.update_layout(
                    autosize=False,
                    width=800,
                    height=800,)
            st.plotly_chart(fig, use_container_width=False, sharing="streamlit")

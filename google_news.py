import pandas as pd
import datetime as dt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import news_analysis as nwan
import hydralit_components as hc
nltk.download('vader_lexicon')
import plotly.graph_objects as go

now = dt.date.today()
now = now.strftime('%m-%d-%Y')
yesterday = dt.date.today() - dt.timedelta(days = 1)
yesterday = yesterday.strftime('%m-%d-%Y')

nltk.download('punkt')
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10




def news_gui(st, c1, searchTerm):
        googlenews = GoogleNews(start=yesterday,end=now)
        googlenews.search(searchTerm)
        result = googlenews.result()

        c1.markdown("## Some recent news headlines about the topic.")
        c1.markdown("  ")

        def show_news(x):
            container = st.container()
            with container:
                col1, space, col2, col3 = st.columns(([2.5,0.5,2,2]))
                container.markdown("""<hr style='border-top: 2px solid #FFB52E; width:50%; border-radius: 3px;'></hr>""", unsafe_allow_html=True)
                with col1:
                    col1.markdown(df['desc'][x])
                    col1.markdown("""<a href="""+df['link'][x]+""">Link to the article..</a>""", unsafe_allow_html=True)
                with col2:
                    col2.markdown("""<h5 style='font-style: italic;'>"""+df['media'][x]+"""</h5>""", unsafe_allow_html=True)
                    col2.caption(df['date'][x])
        
        df = pd.DataFrame(result)
        no = 10

        for x in df.index:
            if no!= 0:
                show_news(x)
                st.write("\n")
            else:
                continue
            no-=1
        show_tweets_is_done = 1
        
        scores = nwan.news_analysis(df)
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
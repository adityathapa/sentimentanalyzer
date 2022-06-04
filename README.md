# Sentiment Analyzer
This repo contains files for Sentiment Analyser, based on Streamlit and VADER.

# Usage
1. During the startup of the app, user is prompted to enter a hashtag/word, any data that is to be analyzed.
2. Number of posts to be scanned are also inputted by the user.
3. The app uses Tweepy API for fetching and scraping the data from Twitter and newspaper and GoogleNews packages for fetching news from GoogleNews.
4. After all posts are retrieved, redundant and unnecessary data are removed and the data is cleaned thoroughly using regex.
5. Now, it will use VADER to generate polarity and will display the results in a detailed and visual manner using Plotly.

# Screenshots
### Input box
![image](https://user-images.githubusercontent.com/74758072/172019518-ace94162-0d06-4a8c-9f9e-a3a346e2b8a6.png)
### Recent tweets on the topic
![image](https://user-images.githubusercontent.com/74758072/172019480-2932526a-b6ee-4936-8de9-5d7e408c9f85.png)
### Polarity cards
![image](https://user-images.githubusercontent.com/74758072/172019486-51714695-332e-42c9-9ec3-4df9eae5e91b.png)
### Pie chart for visualization
![image](https://user-images.githubusercontent.com/74758072/172019494-647fedfc-0a97-4aa2-acd6-75a89e4f5359.png)


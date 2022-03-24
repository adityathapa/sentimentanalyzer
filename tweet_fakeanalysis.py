from json import load
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import string
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import nltk

def fake_score(tweet_list):
    print(tweet_list)
    load_model = joblib.load(filename='final_model.sav')
    prediction = load_model.predict(tweet_list)
    
    return prediction

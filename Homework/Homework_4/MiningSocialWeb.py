# Commented out IPython magic to ensure Python compatibility.
# !pip install twitter
import twitter
import string
import pandas as pd
import dateutil.parser as dparser
import numpy as np
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn.feature_extraction.text import TfidfVectorizer
#!pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
import gensim
from gensim import corpora
# !pip install wordcloud
from wordcloud import WordCloud

CONSUMER_API_KEY = # Enter Twitter Consumer API key here
CONSUMER_API_SECRET = # Enter Twitter Consumer API Secret here
OAUTH_TOKEN = # Enter OAuth Token here
OAUTH_TOKEN_SECRET = # Enter OAuth Token Secret here

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_API_KEY, CONSUMER_API_SECRET)

twitter_api = twitter.Twitter(auth=auth)

print(twitter_api)

from datetime import datetime,timedelta

start_date = "2020-04-10"
stop_date = "2020-04-19"

start = datetime.strptime(start_date, "%Y-%m-%d")
stop = datetime.strptime(stop_date, "%Y-%m-%d")

dt_count=0
jb_count=0
donald_trump_tweets=[]
joe_biden_tweets=[]

while start <= stop:
  print(start)
  start = start + timedelta(days=1)
  search_result_donaldTrump = twitter_api.search.tweets(q='donald trump', lang='en', exclude='retweets',count=1000, until=start)
  search_result_joebiden = twitter_api.search.tweets(q='joe biden', lang='en', exclude='retweets',count=1000, until=start)
  for tweets in search_result_donaldTrump['statuses']:
    dt_count+=1
    text = tweets['text'].lower()
    text = text.translate(str.maketrans('','', string.punctuation))
    text = text.strip()
    date = dparser.parse(tweets['created_at'])
    x = date.date()
    dt_date = x.strftime("%Y")+'-'+x.strftime("%m")+'-'+x.strftime("%d")
    dt_recs = [dt_date,tweets['text'],text]
    donald_trump_tweets.append(dt_recs)
  print('donald trump',dt_count)

  for tweets in search_result_joebiden['statuses']:
    jb_count+=1
    text = tweets['text'].lower()
    text = text.translate(str.maketrans('','', string.punctuation))
    text = text.strip()
    date = dparser.parse(tweets['created_at'])
    x = date.date()
    jb_date = x.strftime("%Y")+'-'+x.strftime("%m")+'-'+x.strftime("%d")
    jb_recs = [jb_date,tweets['text'],text]
    joe_biden_tweets.append(jb_recs)
  print('joe biden',jb_count)

donald_trump = pd.DataFrame(donald_trump_tweets,columns=['Date','Original_Tweet','Processed_Tweet'])
joe_biden = pd.DataFrame(joe_biden_tweets,columns=['Date','Original_Tweet','Processed_Tweet'])

donald_trump.head(5)

joe_biden.head(5)

plt.figure(figsize=(10,5))
chart = sns.countplot(donald_trump['Date'])
chart.set_xticklabels(chart.get_xticklabels(), rotation=45)

plt.figure(figsize=(10,5))
chart = sns.countplot(joe_biden['Date'])
chart.set_xticklabels(chart.get_xticklabels(), rotation=45)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

dt_all_tweet_words=[]
jb_all_tweet_words=[]
dt_tweet_words=[]
jb_tweet_words=[]

def sentiment_analyzer_scores(sentence):
  score = analyser.polarity_scores(sentence)
  return score

donald_trump['Filtered_Tweet']=''
joe_biden['Filtered_Tweet']=''

for index1,dt_tw in donald_trump.iterrows():
  tweet1 = ''.join(i for i in dt_tw['Processed_Tweet'] if not i.isdigit())
  word_tokens1 = wordpunct_tokenize(tweet1)
  filtered_sentence1 = [w for w in word_tokens1 if not w in stop_words]

  lemmatized1 = [lemmatizer.lemmatize(f) for f in filtered_sentence1]
  dt_all_tweet_words.append(lemmatized1)
  dt_tweet_words.extend(lemmatized1)
  donald_trump.loc[index1,'Filtered_Tweet']=' '.join(lemmatized1)
  donald_trump.loc[index1,'Negative_Score']=sentiment_analyzer_scores(dt_tw['Processed_Tweet'])['neg']
  donald_trump.loc[index1,'Positive_Score']=sentiment_analyzer_scores(dt_tw['Processed_Tweet'])['pos']
  donald_trump.loc[index1,'Neutral_Score']=sentiment_analyzer_scores(dt_tw['Processed_Tweet'])['neu']

for index2,jb_tw in joe_biden.iterrows():
  tweet2 = ''.join(i for i in jb_tw['Processed_Tweet'] if not i.isdigit())
  word_tokens2 = wordpunct_tokenize(tweet2)
  filtered_sentence2 = [w for w in word_tokens2 if not w in stop_words]
  lemmatized2 = [lemmatizer.lemmatize(f) for f in filtered_sentence2]
  jb_all_tweet_words.append(lemmatized2)
  jb_tweet_words.extend(lemmatized2)
  joe_biden.loc[index2,'Filtered_Tweet']=' '.join(lemmatized2)
  joe_biden.loc[index2,'Negative_Score']=sentiment_analyzer_scores(jb_tw['Processed_Tweet'])['neg']
  joe_biden.loc[index2,'Positive_Score']=sentiment_analyzer_scores(jb_tw['Processed_Tweet'])['pos']
  joe_biden.loc[index2,'Neutral_Score']=sentiment_analyzer_scores(jb_tw['Processed_Tweet'])['neu']

dt_dictionary = corpora.Dictionary(dt_all_tweet_words)
jb_dictionary = corpora.Dictionary(jb_all_tweet_words)

dt_doc_term_matrix = [dt_dictionary.doc2bow(doc) for doc in dt_all_tweet_words]
jb_doc_term_matrix = [jb_dictionary.doc2bow(doc) for doc in jb_all_tweet_words]

Lda = gensim.models.ldamodel.LdaModel

dt_damodel = Lda(dt_doc_term_matrix, id2word = dt_dictionary, passes=50)
print(dt_damodel.print_topics(num_words=5))

jb_damodel = Lda(jb_doc_term_matrix, id2word = jb_dictionary, passes=50)
print(jb_damodel.print_topics(num_topics=10, num_words=5))

print(dt_damodel.print_topics(num_words=5))

print(jb_damodel.print_topics(num_words=5))


unique_string=' '.join(dt_tweet_words)
wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig("your_file_name"+".png", bbox_inches='tight')
plt.show()
plt.close()

unique_string=' '.join(jb_tweet_words)
wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig("your_file_name"+".png", bbox_inches='tight')
plt.show()
plt.close()

dt_neg = np.sum(donald_trump['Negative_Score'])
dt_pos = np.sum(donald_trump['Positive_Score'])
dt_neu = np.sum(donald_trump['Neutral_Score'])

print('Donald Trump Negative Tweets score:',dt_neg)
print('Donald Trump Positive Tweets score:',dt_pos)
print('Donald Trump Neutral Tweets score:',dt_neu)

jb_neg = np.sum(joe_biden['Negative_Score'])
jb_pos = np.sum(joe_biden['Positive_Score'])
jb_neu = np.sum(joe_biden['Neutral_Score'])

print('Joe Biden Negative Tweets score:',jb_neg)
print('Joe Biden Positive Tweets score:',jb_pos)
print('Joe Biden Neutral Tweets score:',jb_neu)


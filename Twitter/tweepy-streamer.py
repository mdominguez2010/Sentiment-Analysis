from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import credentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

# # # # TWITTER AUTHENTICATOR # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    '''
    Class for streaming and processing live tweets
    '''
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API

        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hashtag_list)

# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    '''
    Basic listener class that just prints received tweets to stdout
    '''
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            # print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Return False on data method in case rate limit is reached
            return False
        print(status)

class TweetAnalyzer():
    '''
    Functionality for analyzing and categorizing content from tweets
    '''
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['n_likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['n_retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

if __name__=="__main__":

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="SamHarrisOrg", count=1000)

    # print(dir(tweets[0])) # prints methods we can ask of the 'tweets' api call
    # print(tweets[0].id) # prints id of tweet
    # print(tweets[0].retweet_count)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    # print(df.head(10))

    # Get average length over all tweets
    # print(np.mean(df['len']))
    # Get number of likes for most liked tweet
    # print(np.max(df['n_likes']))
    # Get number of retweets for most retweeted tweet
    # print(np.max(df['n_retweets']))

    # Time Series
    # time_likes = pd.Series(data=df['n_likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16,8), color='b')
    # plt.show()

    # time_retweets = pd.Series(data=df['n_retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16,8), color='b')
    # plt.show()

    time_likes = pd.Series(data=df['n_likes'].values, index=df['date'])
    time_likes.plot(figsize=(16,8), label="Likes", legend=True, color='orange')

    time_retweets = pd.Series(data=df['n_retweets'].values, index=df['date'])
    time_retweets.plot(figsize=(16,8), label='Retweets', legend=True, color='b')
    plt.show()


    # hashtag_list = ['joe biden', 'ben shapiro', 'sam harris']
    # fetched_tweets_filename = "tweets.json"

    # twitter_client = TwitterClient(twitter_user='nebula0087') # omit @ sign
    # print(twitter_client.get_user_timeline_tweets(1))

    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)



from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials

class TwitterStreamer():
    '''
    Class for streaming and processing live tweets
    '''
    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API

        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        stream.filter(track=hashtag_list)

class StdOutListener(StreamListener):
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
        print(status)


if __name__=="__main__":

    hashtag_list = ['joe biden', 'ben shapiro', 'sam harris']
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)



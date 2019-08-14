

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#Variables that contains the user credentials to access Twitter API

access_token = "1156438291593322496-nBUHachqwSAMXnP5A3A27N2Maoa2ka"
access_token_secret = "jtzVOm6hvgnPNmBmSTmSKfT2ORV1fLOHQKBdfQVCbWnGR"
consumer_key = "d3NOxDKVg8xSIhLRhCoTcWTbX"
consumer_secret = "CPXtDivffT4dJnJfCbRDVEuoHwMLn7xLfgLxRWqdZCWvYbazkt"



#This is a basic listener that just prints received tweets to stdout.


class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'

    stream.filter(track=['python', 'javascript', 'ruby'])
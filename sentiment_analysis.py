import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):

    # creating constructor of the class
    def __init__(self):
        # inputting keys and tokens from Twitter Dev Console
        consumer_key = 'OvuprmCOW4o5ag82cDZ7kio6C'
        consumer_secret = 'YjBpkxQvUca7HX5atBxptaWy7dIZDJRBgobLBshvctHhCrzF9A'
        access_token = '1493772580251004929-qYA5PwSkdyT8sxmr8yRTfhmmbhYLol'
        access_token_secret = '8qkXjorbTY9bBaGidSbKZjFfyQ3y4Hnh9eVPeG0C63C7W'

        # getting authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    # clean tweet text by removing links and special characters
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w+:\/\/\S+)", " ", tweet).split())

    # classifying sentiments of passed tweets
    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))

        # setting sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    # creating function to fetch tweets and perform sentiment analysis
    def get_tweets(self, query, count=10):

        tweets = []

        try:
            # fetching tweets
            fetched_tweets = self.api.search_tweets(q=query, count=count)

            # performing sentiment analysis
            for tweet in fetched_tweets:
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def main():
    api = TwitterClient()

    tweets = api.get_tweets(query='ben and bella', count=200)

    # positive tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("\nPositive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # printing first 5 positive tweets
    print("\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # negative tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("\n\nNegative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # printing first 5 negative tweets
    print("\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    # neutral tweets
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    print("\n\nNeutral tweets percentage: {} % ".format(100 * len(neutweets) / len(tweets)))
    # printing first 5 neutral tweets
    print("\nNeutral tweets:")
    for tweet in neutweets[:10]:
        print(tweet['text'])


# calling main function
if __name__ == "__main__":
    main()

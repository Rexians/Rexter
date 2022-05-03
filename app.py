import tweepy
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger()

consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)


class MCOC(tweepy.StreamingClient):
    def on_connect(self):
        logger.info(" Bot Started")

    def on_tweet(self, tweet: tweepy.Tweet):
        id = tweet.id
        status = api.get_status(id)
        if tweet.in_reply_to_user_id is None:
            if tweet.referenced_tweets is None:
                api.retweet(id)
                api.create_favorite(id)
                logger.info(f" Retweeted {id}")
                logger.info(f" Liked {id}")

    def on_request_error(self, status_code):
        logger.critical(f" Encountered error: {status_code}")


stream = MCOC(bearer_token)
stream.add_rules(
    [
        tweepy.StreamRule("@MarvelChampions"),
        tweepy.StreamRule("#MCoC"),
        tweepy.StreamRule("@McocBot"),
        tweepy.StreamRule("#ContestofChampions"),
        tweepy.StreamRule("#ContestOfChampions"),
        tweepy.StreamRule("#contestofchampions"),
    ]
)
stream.filter(tweet_fields=["referenced_tweets"], expansions="referenced_tweets.id")

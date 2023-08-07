import tweepy
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import calendar
import math
import random

load_dotenv()

# ---- API VARIABLES ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger()

consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

api = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)


# ---- GENERAL VARIABLES ----

HOURS = 24
MINUTES = 60
RETWEET_LIMIT = 1500

monthly_variables = {
    "current_month" : datetime.now().month,
    "days_in_a_month" : calendar.monthrange(datetime.now().year, datetime.now().month)[1],
}
monthly_variables["retweets_per_day"] = math.floor(RETWEET_LIMIT / monthly_variables["days_in_a_month"])
monthly_variables["time_interval"] = math.floor(HOURS * MINUTES / monthly_variables["retweets_per_day"])

daily_variables = {
    "current_day" : datetime.now().day,
    "total_retweets" : 0,
    "tweets" : set(),
    "current_time_interval_id" : 0,
    "previous_time_interval" : datetime.now().minute,
}

next_interval = datetime.now().minute + monthly_variables["time_interval"]
daily_variables["next_time_interval"] = next_interval if next_interval <= 59 else next_interval - 60

def monthly_reset():
    monthly_variables["current_month"] = datetime.now().month
    monthly_variables["days_in_a_month"] = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
    monthly_variables["retweets_per_day"] = math.floor(RETWEET_LIMIT / days_in_a_month)
    monthly_variables["time_interval"] = math.floor(HOURS * MINUTES / retweets_per_day)

def daily_reset():

    if (daily_variables["total_retweets"] < monthly_variables["retweets_per_day"]):
        retweet_until_limit_reached()

    daily_variables["current_day"] = datetime.now().day
    daily_variables["total_retweets"] = 0
    daily_variables["tweets"] = set()
    daily_variables["current_time_interval_id"] = 0
    daily_variables["previous_time_interval"] = datetime.now().minute
    next_interval = datetime.now().minute + monthly_variables["time_interval"]
    daily_variables["next_time_interval"] = next_interval if next_interval <= 59 else next_interval - 60

def on_day_start():
    for i in range(retweets_per_day):
        tweets[i] = set()

def check_day_change():
    if daily_variables["current_day"] != datetime.now().day:
        daily_reset()
        daily_variables["current_day"] = datetime.now().day

def check_month_change():
    if monthly_variables["current_month"] != datetime.now().month:
        monthly_reset()
        current_month = datetime.now().month

def update_time():
    while True:
        check_month_change()
        check_day_change()
        if (datetime.now().minute >= daily_variables["next_time_interval"]):
                retweet(daily_variables["current_time_interval_id"])
                daily_variables["previous_time_interval"] = datetime.now().minute
                next_interval = datetime.now().minute + monthly_variables["time_interval"]
                daily_variables["next_time_interval"] = next_interval if next_interval <= 59 else next_interval - 60
                daily_variables["current_time_interval_id"] += 1

def retweet(time_interval):

    if (daily_variables["total_retweets"] <= monthly_variables["retweets_per_day"]):
        random_id = random.choice(daily_variables["tweets"][time_interval])
        daily_variables["tweets"][time_interval].remove(random_id)
        api.retweet(random_id)
        api.create_favorite(random_id)
        daily_variables["total_retweets"] += 1
        logger.info(f" Retweeted & Liked {random_id}")
    else:
        logger.info(f" Reached daily retweet limit")

def retweet_until_limit_reached():

    busiest_intervals = []
    for interval, tweet_set in daily_variables["tweets"]:
        busiest_intervals.append((len(tweet_set), interval))

    busiest_intervals.sort(reverse=True)

    count = 0
    failsafe = 1000
    while count != (monthly_variables["retweets_per_day"] - daily_variables["total_retweets"]):
        failsafe -= 1

        if failsafe < 0:
            logger.error("Fail safe reached. Check code")
            return

        if not busiest_intervals:
            return

        interval = busiest_intervals[0][1]

        if len(daily_variables["tweets"][interval]) == 0:
            busiest_intervals.pop(0)
            continue

        retweet(interval)
        count += 1

class MCOC(tweepy.StreamingClient):
    def on_connect(self):
        logger.info(" Bot Started")
        update_time()

    def on_tweet(self, tweet: tweepy.Tweet):
        id = tweet.id
        if tweet.in_reply_to_user_id is None:
            if tweet.referenced_tweets is None:
                try:
                    daily_variables["tweets"].add(id)
                except:
                    logger.error(f" Could't perform action on {id}")

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
stream.filter(
    tweet_fields=["referenced_tweets"],
    expansions="referenced_tweets.id",
)

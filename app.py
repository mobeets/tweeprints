import os
import time
import tweepy
from sheets import add_rows

try:
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except:
    pass

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)

USER_NAME = 'tweeprint'
HASHTAG = '#tweeprint'
RUN_EVERY_N_SECONDS = 60*60*1 # e.g. 60*5 = tweets every five minutes

def get_last_tweet_id():
    tweet = api.user_timeline(screen_name=USER_NAME, count=1)
    if len(tweet) == 0:
        return None
    else:
        return tweet[0].id

def get_query():
    return HASHTAG + ' -filter:retweets'

def fetch_mentions(last_id, max_tweets=200):
    query = get_query()
    matches = []
    for status in tweepy.Cursor(api.search, q=query,
        count=max_tweets, # tweet_mode='extended',
        since_id=last_id, result_type='recent').items(max_tweets):
        print(status.text)
        if not hasattr(status, 'retweeted_status'):
            print('Found status {}'.format(status.id))
            matches.append(status)
    return matches

def get_tweeprints(tweets):
    """
    tweets contains statuses mentioning '#tweeprint'
        each tweet may be the first in the thread,
        or a reply to the first in the thread;
        in the latter case, we need to get that first thread
    """
    matches = []
    for tweet in tweets:
        if tweet.in_reply_to_status_id_str:
            prev_tweet = api.get_status(tweet.in_reply_to_status_id)
            matches.append(prev_tweet)
            print('Adding previous status {}'.format(prev_tweet.id))
        else:
            matches.append(tweet)
            print('Adding status {}'.format(tweet.id))
    return matches

def retweet_tweeprints(tweets):
    outputs = []
    for tweet in tweets:
        if tweet.in_reply_to_status_id_str:
            print('Ignoring {} because it is not the first in the thread'.format(tweet.id))
            continue
        if tweet.user.screen_name == USER_NAME:
            print('Ignoring my own tweet')
            continue
        urls = [url for url in tweet.entities['urls'] if 'twitter' not in url['display_url']]
        # need to filter out by display_url to make sure we don't include links to other tweets (i.e., RTs) as a valid url
        if len(urls) == 0:
            print('Ignoring {} because there are no urls'.format(tweet.id))
            continue
        if not tweet.retweeted:
            try:
                # tweet.retweet()
                outputs.append(tweet)
                print('Retweeting {}'.format(tweet.id))
            except tweepy.TweepError as e:
                print('Already Retweeted {}'.format(tweet.id))
    return outputs

def tweets_to_rows(tweets):
    """
    Date, ID, User, URL, Text
    """
    rows = []
    for tweet in tweets:
        url = '{}/statuses/{}'.format(tweet.source_url, tweet.id)
        row = [str(tweet.created_at), tweet.id, tweet.user.screen_name, url, tweet.text]
        rows.append(row)
    return rows

def main():
    while True:
        last_id = get_last_tweet_id()
        print('Last id = {}'.format(last_id))
        tweets = fetch_mentions(last_id)
        tweets = get_tweeprints(tweets)
        tweets = retweet_tweeprints(tweets)
        rows = tweets_to_rows(tweets)
        print(rows)
        add_rows(rows)
        time.sleep(RUN_EVERY_N_SECONDS)

if __name__ == '__main__':
    main()

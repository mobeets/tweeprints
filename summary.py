import tweepy

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

def get_all_tweets():
	all_tweets = api.user_timeline(screen_name=USER_NAME, count=20)
	ids = [x.id for x in all_tweets]
	added_one = True
	while added_one:
		added_one = False
		for tweet in api.user_timeline(screen_name='tweeprint',
				count=20, max_id=tweets[-1].id):
			if tweet.id not in ids:
				all_tweets.append(tweet)
				added_one = True
	return all_tweets

def main():
	unique_tweets = get_all_tweets()
	dts = [t.retweeted_status.created_at for t in unique_tweets if hasattr(t, 'retweeted_status')]
	pass

if __name__ == '__main__':
	main()

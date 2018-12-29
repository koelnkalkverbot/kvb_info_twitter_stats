import yaml
import tweepy 
import csv
import datetime
    
ACCOUNT_NAME = 'kvb_info'

def get_all_tweets():
	with open("api_credentials.yml", 'r') as ymlfile:
		cfg = yaml.load(ymlfile)

	auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
	auth.set_access_token(cfg['access_key'], cfg['access_secret'])
	api = tweepy.API(auth)

	alltweets = []  
	new_tweets = api.user_timeline(screen_name = ACCOUNT_NAME, count = 200, tweet_mode = 'extended')
	alltweets.extend(new_tweets)
	oldest = alltweets[-1].id - 1

	while len(new_tweets) > 0:
		new_tweets = api.user_timeline(screen_name = ACCOUNT_NAME, count = 200, tweet_mode = 'extended', max_id = oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1

	print ("Downloaded %s tweets" % (len(alltweets)))
	outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text.replace('\n', ' ').replace('\r', '')] for tweet in alltweets]

	with open('kvb_tweets_%s.csv' % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['id', 'created_at', 'text'])
		writer.writerows(outtweets)

	pass
	print ("Finished downloading tweets")


if __name__ == '__main__':
  get_all_tweets()
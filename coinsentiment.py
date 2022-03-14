import tweepy
import sys
import datetime
import yaml
import nltk
nltk.download("stopwords")
nltk.download("punkt")
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
from langdetect import detect

def setupclient(secretspath):
	""" Setup twitter client """

	with open(secretspath, "r") as secrets:
		api_secret = yaml.safe_load(secrets)
	client = tweepy.Client(api_secret["secret"])
	return client

def searchtweets(client, starttime, searchstring):
	""" search for a string and return a list of cleaned tweets """
	response = client.search_recent_tweets(
		searchstring, 
		start_time=starttime,
		max_results=100
		)
	tweets = response.data
	#cleaning:
	stopwords = nltk.corpus.stopwords.words("english")
	for tweet in tweets:
		if detect(tweet.text) != "en":
			tweets.remove(tweet)
		else:
			tokens = nltk.tokenize.word_tokenize(tweet.text)
			tokens_cleaned = [word for word in tokens if word.isalpha()]
			tokens_cleaned = [word for word in tokens_cleaned if word.lower() not in stopwords]
			tweet.text = (" ").join(tokens_cleaned)

	return tweets

def getaveragesentiment(tweets):
	
	tweetsentiment = 0
	sia = SentimentIntensityAnalyzer()
	for tweet in tweets:
		sentiment = sia.polarity_scores(tweet.text)
		tweetsentiment = tweetsentiment + sentiment['pos'] - sentiment['neg']

	tweetsentiment = tweetsentiment / len(tweets)

	return tweetsentiment

def main():
	starttime = datetime.datetime.now() - datetime.timedelta(hours = 1)
	client = setupclient("./secrets.yaml")
	clean_tweets = searchtweets(client, starttime, sys.argv[1])
	sentiment = getaveragesentiment(clean_tweets)
	print(sentiment)


if __name__ == '__main__':
	main()
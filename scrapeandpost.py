import requests
import coinsentiment
import pandas as pd
import datetime

url = "http://192.168.0.4:105/coins"

topcoins = pd.read_csv('topcoins.csv')
starttime = datetime.datetime.now() - datetime.timedelta(hours = 1)
client = coinsentiment.setupclient("./secrets.yaml")

coindict = {}

for idx, row in topcoins.iterrows():
	clean_tweets = coinsentiment.searchtweets(
		client, 
		starttime, 
		row["coinname"]
		)
	try:
		topcoins.loc[idx, "sentiment"] = coinsentiment.getaveragesentiment(clean_tweets)
	except:
		topcoins.loc[idx, "sentiment"] = 0

print(topcoins)
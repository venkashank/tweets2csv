# tweets2csv
Script to pull tweets from a search query  and save results into a csv file.

__Requires Tweepy__

    pip install Tweepy

Clone github repository with:

    git clone https://github.com/sqrt64/tweets2csv.git

## Important!

Fill out credentials.json.example with your keys from Twitter/dev. Save the file as credentials.json

Create keys from [Twitter](https://apps.twitter.com/)


## Example Usage


    python tweets2csv.py -q "cats" -n 100

## Default Options

    -o "Output File" = tweets.csv

	-n "Number of Tweets" = 10

	-rt "Include Retweets" = False

	-l "Tweet Language" = "en"


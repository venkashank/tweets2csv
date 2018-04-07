import argparse
import csv
import json
import tweepy

def read_credentials():
    """
    Fill out credentials.json.example and save as credentials.json. 
    You must create API credentials from Twitter directly before running this script.
    """
    
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    except FileNotFoundError:
        print("Credentials.json not found")
        raise
    return credentials 


def twitter_auth(credentials):
    """
    Reads the credentials.json file and stores the values and authenticates with Twitter.
    Authentication is tested by calling me method from tweepy.
    Will print username that matches the credentials.
    """

    consumer_key = credentials["consumer_key"]
    consumer_secret = credentials["consumer_secret"]
    access_token = credentials["access_token"]
    access_token_secret = credentials["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    t = tweepy.API(auth)

    try:
        user_name = t.me()._json
        print(f"Authenticated as {user_name['name']}")
    except Exception:
        print("You are not authenticated by Twitter. Check your key/tokens")
    return t


def search_query(retweets):
    """
    Builds the search query by checking if we want to include retweets.
    """
    if retweets  == False:
        search_query = "-filter:retweets"
    else:
        search_query = ""
    return search_query


def twitter_search(query, lang, items):
    """
    Searches Twitter for the search query in the language provided (en default) 
    Returns a Tweepy Cursor object
    """
    return tweepy.Cursor(t.search, q=query, lang=lang).items(items)
    

def csv_write(tweet, filename):
    """
    Writes the tweet information into a csv
    """
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(tweet)


def tweet_parse(tweet):
    """
    Parses the tweet for relevent information.
    Returns a list that contains all the information
    """
    tweet_date = str(tweet.created_at)
    tweet_id = tweet.id_str
    tweet_text = tweet.text
    # Remove new lines and pipes from the tweets
    tweet_text = tweet_text.replace('|', ' ')
    tweet_text = tweet_text.replace('\n', ' ')
    hashtags = []
    for i in tweet.entities['hashtags']:
            hashtags.append(i['text'])
    favorited = tweet.favorited
    favorite_count = tweet.favorite_count
    retweeted = tweet.retweeted
    retweet_count = tweet.retweet_count
    tweeted_from = tweet.source


    parsed_tweet = [
        tweet_date,
        tweet_id,
        tweet_text,
        hashtags,
        favorited,
        favorite_count,
        retweeted,
        retweet_count,
        tweeted_from
    ]
    return parsed_tweet


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                        description="Select Options",
                        prefix_chars='-')

    parser.add_argument(
                        '-q', '--query',
                        help='Your Twitter Search Query',
                        action='store',
                        dest='query',
                        required=True)

    parser.add_argument(
                        '-o', '--output_file',
                        help='Output File Name (.csv)',
                        action='store',
                        dest='output_file',
                        default='tweets.csv',
                        required=False)

    parser.add_argument(
                        '-n', '--number',
                        help='Number of Tweets (Default = 10)',
                        required=True,
                        default=10,
                        action='store',
                        dest='number_of_tweets',
                        type=int)

    parser.add_argument(
                        '-rt', '--retweets',
                        help='Include ReTweets? Default = False',
                        action='store',
                        dest='retweets',
                        default=False)

    parser.add_argument(
                        '-l', '--language',
                        help='Language to search. Default = "en"',
                        action='store',
                        dest='tweet_language',
                        default="en")

    args = parser.parse_args()
    
    t =  twitter_auth(read_credentials())
    search_query = search_query(args.retweets)

    search = twitter_search(search_query, args.tweet_language, args.number_of_tweets)
    for tweet in search:
            csv_write(tweet_parse(tweet), args.output_file)
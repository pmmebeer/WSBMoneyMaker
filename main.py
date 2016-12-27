import praw
import config
import pandas # Adding plotting in future
import matplotlib #Adding plotting in future
from textblob import *
from tickerdict import tickerdict

def main():
    # Authentication and creating reddit instance
    reddit = praw.Reddit(
        user_agent = config.user_agent,
        client_id = config.client_id,
        client_secret = config.client_secret,
        username = config.username,
        password = config.password
    )
    subreddit = reddit.subreddit('wallstreetbets') # defining subreddit as /r/wallstreetbets
    for submission in subreddit.stream.submissions(): # creating subreddit stream for posts
        print (submission.title)
        process_submission(submission)
    for comment in subreddit.stream.comments(): # creating subreddit stream for comments
        print (comment.body)
        process_comment(comment)

def process_submission(submission):
    title = TextBlob(submission.title) # Creating TextBlob for title
    title_lower = title.lower() # Normalizing title for short/long initial check
    submission_tokens = title.words
    for token in submission_tokens: # Loop to evaluate sentiment and return Buy/Sell/None
        if token in tickerdict.keys():
            print ("Found Ticker: " + token + "| " + tickerdict[token])
            if "short" in title_lower:
                return "Sell"
            elif "long" in title_lower:
                return "Buy"
            else:
                title_sentiment = title.sentiment # Returns NamedTuple in format (Sentiment(polarity = x, subjectivity = y)
                if title_sentiment.polarity > 0 and title_sentiment.subjectivity > 0.3:
                    return "Buy"
                elif title_sentiment.polarity < 0 and title_sentiment.subjectivity > 0.3:
                    return "Sell"
                else:
                    return "Sentiment Uncertain"
        else:
            return "No Ticker Found"

def process_comment(comment):
    comment = TextBlob(comment.body) # Creating TextBlob for comment
    comment_lower = comment.lower() # Normalizing comment for short/long initial check
    comment_tokens = comment.words
    for token in comment_tokens: # Loop to evaluate sentiment and return Buy/Sell/None
        if token in tickerdict.keys():
            print ("Found Ticker: " + token + "| " + tickerdict[token])
            if "short" in comment_lower:
                return "Sell"
            elif "long" in comment_lower:
                return "Buy"
            else:
                comment_sentiment = comment.sentiment # Returns NamedTuple in format (Sentiment(polarity = x, subjectivity = y)
                if comment_sentiment.polarity > 0 and comment_sentiment.subjectivity > 0.3:
                    return "Buy"
                elif comment_sentiment.polarity < 0 and comment_sentiment.subjectivity > 0.3:
                    return "Sell"
                else:
                    return "Sentiment Uncertain"
        else:
            return "No Ticker Found"

if __name__ == '__main__':
    main()


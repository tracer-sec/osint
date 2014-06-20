# osint.py

import sys
import json
import data
import twitter
import reddit
import whois

if __name__ == '__main__':
    config_file = open('config.json', 'r')
    config = json.load(config_file)
    config_file.close()
    
    target = sys.argv[1]
    data = data.Storage(target)

    twitter = twitter.TwitterClient(config['twitter'])
    #reddit = reddit.RedditClient(config['reddit'])
    
    # Twitter profile
    twitter_profile = twitter.get_profile(target)
    print(data.add_profile('twitter', 'profile', target, twitter_profile))
    
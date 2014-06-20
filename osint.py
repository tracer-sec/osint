# osint.py

import sys
import datetime
import json
import sqlite3
import twitter
import reddit
import whois

def create_db(connection):
    c = connection.cursor()
    c.execute('CREATE TABLE dump (provider text, query_type text, data text)')
    connection.commit()

if __name__ == '__main__':
    config_file = open('config.json', 'r')
    config = json.load(config_file)
    config_file.close()
    
    target = sys.argv[1]

    twitter = twitter.TwitterClient(config['twitter'])
    #reddit = reddit.RedditClient(config['reddit'])

    d = datetime.datetime.utcnow().isoformat('-').replace(':', '')
    d = d[:d.find('.')]  # microseconds? Er. Thanks. I'll pass
    db_filename = '{0}-{1}.db'.format(target, d)
    open(db_filename, 'a').close()
    connection = sqlite3.connect(db_filename)
    create_db(connection)

    c = connection.cursor()
    
    # Twitter profile
    twitter_profile = twitter.get_profile(target)
    c.execute('INSERT INTO dump (provider, query_type, data) VALUES (?, ?, ?)', ['twitter', 'profile', json.dumps(twitter_profile)])
    connection.commit();
    
    connection.close()
    
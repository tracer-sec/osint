# osint.py

import sys
import json
import threading
import data
import Queue
import twitter
import reddit
import whois

visited = []

def get_job_key(job):
    return '{0}~{1}~{2}'.format(job['provider'], job['task'], job['target'])

def process(job_queue, clients, data):
    while not job_queue.empty():
        job = job_queue.get()
        try:
            job_key = get_job_key(job)
            if job_key not in visited:
                visited.append(job_key)
                print(job)
                result = clients[job['provider']].get_profile(job['target'])
                data_queue.put({ 'provider': job['provider'], 'target': job['target'], 'data': result })
                print('Fetching connections')
                connections = clients[job['provider']].get_connections(job['target'])
                connections = []
                for connection in connections:
                    if job_key not in visited:
                        job_queue.put(connection)
        finally:
            job_queue.task_done()
        
    print('Stopping thread {0}'.format(threading.current_thread().name))
        
        
def process_data(data_queue):
    d = data.Storage(target)
    while(True):
        result = data_queue.get()
        print('d - {0}'.format(result))
        d.add_profile(result['provider'], 'profile', result['target'], result['data'])
        data_queue.task_done()
        

if __name__ == '__main__':
    config_file = open('config.json', 'r')
    config = json.load(config_file)
    config_file.close()
    
    target = sys.argv[1]

    twitter = twitter.TwitterClient(config['twitter'])
    #reddit = reddit.RedditClient(config['reddit'])
    
    clients = { 'twitter': twitter }
    
    job_queue = Queue.Queue()
    job_queue.put({ 'provider': 'twitter', 'task': 'profile', 'target': target })
    data_queue = Queue.Queue()
    
    # 1 data thread
    t = threading.Thread(name='data', target=process_data, args=[data_queue])
    t.daemon = True
    t.start()
    
    # 4 worker threads
    for i in range(4):
        t = threading.Thread(name=str(i), target=process, args=[job_queue, clients, data_queue])
        t.daemon = True
        t.start()
        
    job_queue.join()
    data_queue.join()
    
    print('Done.')
    
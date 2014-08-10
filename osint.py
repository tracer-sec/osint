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
node_limit = 5
    
def get_job_key(job):
    return '{0}~{1}~{2}'.format(job['provider'], job['task'], job['target'])

def process(job_queue, clients, data):
    while not job_queue.empty():
        job = job_queue.get()
        try:
            job_key = get_job_key(job)
            if job_key not in visited:
                visited.append(job_key)
                print_s(job)
                result = clients[job['provider']].get_profile(job['target'])
                data_queue.put({ 'provider': job['provider'], 'target': job['target'], 'data': result })

                connections = clients[job['provider']].get_connections(job['target'])
                for connection in connections:
                    connection_key = get_job_key(connection)
                    if connection_key not in visited:
                        job_queue.put(connection)
        finally:
            job_queue.task_done()
            
        if len(visited) >= node_limit:
            break
        
    # Empty queue so it returns control to calling thread
    while not job_queue.empty():
        job_queue.get()
        job_queue.task_done()
    
    print_s('Stopping thread')
        
        
def process_data(data_queue):
    d = data.Storage(target)
    while(True):
        result = data_queue.get()
        print_s('d - {0}'.format(result))
        friendly_name = result['target']
        if result['provider'] == 'twitter':
            friendly_name = result['data']['screen_name']
        d.add_profile(result['provider'], 'profile', friendly_name, result['data'])
        data_queue.task_done()
        
        
write_lock = threading.Lock()
        
def print_s(s):
    thread_id = threading.current_thread().name
    write_lock.acquire()
    print('[{0}] {1}'.format(thread_id, s))
    write_lock.release()
    
    
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
    
    print_s('Done.')
    
# osint.py

import sys
import json
import threading
import time
import data
import Queue
import plugins
import model

visited = []
node_limit = 8
working_count = 0
    
def get_job_key(job):
    return '{0}~{1}'.format(job['provider'], job['target'])

def process(job_queue, data):
    while not job_queue.empty() or working_count > 0:
        try:
            inc_working_count()
            job = job_queue.get(True, 5)
            job_key = get_job_key(job)
            if job_key not in visited:
                append_visited(job_key)
                #print_s(job)
                node = plugins.fetch(job['provider']).get_profile(job['target'])
                #print(node)
                data_queue.put({ 'node': node, 'parent_node': job['parent_node'], 'connection_type': job['connection_type'] })

                connections = plugins.fetch(job['provider']).get_connections(job['target'])
                for connection in connections:
                    connection_key = get_job_key(connection)
                    if connection_key not in visited:
                        connection['parent_node'] = node
                        job_queue.put(connection)
        except Queue.Empty:
            pass # swallow it - TODO: doesn't work
        finally:
            if job is not None:
                job_queue.task_done()
            job = None
            dec_working_count()
            
        if len(visited) >= node_limit:
            break
        
        time.sleep(2)
        
    # Empty queue so it returns control to calling thread
    while not job_queue.empty():
        job_queue.get()
        job_queue.task_done()
    
    print_s('Stopping thread')
    
    
def process_data(data_queue, target_name):
    d = data.Storage(target_name)
    while(True):
        try:
            result = data_queue.get()
            #print_s('d - {0}'.format(result))
            node = d.add_node(result['node'])
            if result['parent_node'] is not None:
                connection = model.Connection(result['parent_node'].id, node.id, result['connection_type'], 'concrete', '')
                d.add_connection(connection)
        finally:
            data_queue.task_done()
        
        
write_lock = threading.Lock()
working_count_lock = threading.Lock()
visited_lock = threading.Lock()

def inc_working_count():
    global working_count
    working_count_lock.acquire()
    working_count = working_count + 1
    working_count_lock.release()
        
def dec_working_count():
    global working_count
    working_count_lock.acquire()
    working_count = working_count - 1
    working_count_lock.release()

def print_s(s):
    thread_id = threading.current_thread().name
    write_lock.acquire()
    print('[{0}] {1}'.format(thread_id, s))
    write_lock.release()
    
def append_visited(key):
    global visited
    visited_lock.acquire()
    visited.append(key)
    visited_lock.release()
    
    
if __name__ == '__main__':
    config_file = open('config.json', 'r')
    config = json.load(config_file)
    config_file.close()
    
    target = sys.argv[1]
    
    plugins.load_all(config)
    
    job_queue = Queue.Queue()
    job_queue.put({ 'provider': 'twitter', 'target': target, 'parent_node': None, 'connection_type': None })
    data_queue = Queue.Queue()
    
    # 1 data thread
    t = threading.Thread(name='data', target=process_data, args=[data_queue, target])
    t.daemon = True
    t.start()
    
    # Guess associated profiles?
    
    # 4 worker threads
    for i in range(4):
        t = threading.Thread(name=str(i), target=process, args=[job_queue, data_queue])
        t.daemon = True
        t.start()
        
    job_queue.join()
    data_queue.join()
    
    print_s('Done.')
    
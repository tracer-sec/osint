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
working_count = 0
request_limit = 8       # each action could result in a tonne of nodes, so 
                        # bear in mind this won't limit the number of nodes 
                        # predictably. This more to prevent spamming APIs
    
def get_node_key(node):
    return '{0}~{1}'.format(node.node_type, node.name)

def process(job_queue, data):
    while not job_queue.empty() or working_count > 0:
        try:
            inc_working_count()
            node = job_queue.get(True, 5)
            node_key = get_node_key(node)
            if node_key not in visited:
                append_visited(node_key)
                #print_s(node)
                actions = plugins.fetch_actions(node.node_type)
                #print_s(actions)
                for action in actions:
                    new_nodes = action['func'](node)
                    #print_s(new_nodes)
                    for child in new_nodes:
                        # TODO:
                        # check to see if they're in the DB already
                        # add a connection if so
                        # else add a node and connection, and put them on the job queue
                        # TODO
                        data_queue.put({ 'node': child, 'parent_node': node, 'connection_type': action['name'] })
                        child_key = get_node_key(child)
                        if child_key not in visited:
                            job_queue.put(child)

        except Queue.Empty:
            pass # swallow it - TODO: doesn't work
        except Exception as e:
            print_s(e)
            break
        finally:
            if node is not None:
                # re-save the original node in case any of our actions updated it
                data_queue.put({ 'node': node, 'parent_node': None, 'connection_type': None })
                job_queue.task_done()
            node = None
            dec_working_count()
            
        if len(visited) >= request_limit:
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
        except Exception as e:
            print_s(e)
            break
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
    
    plugins.load_all(config)
    
    node_type = sys.argv[1]
    target = sys.argv[2]
    start_node = model.Node(node_type, target)
    
    job_queue = Queue.Queue()
    job_queue.put(start_node)
    data_queue = Queue.Queue()
    data_queue.put({ 'node': start_node, 'parent_node': None, 'connection_type': None })
    
    # 1 data thread
    t = threading.Thread(name='data', target=process_data, args=[data_queue, target])
    t.daemon = True
    t.start()
    
    # 4 worker threads
    for i in range(4):
        t = threading.Thread(name=str(i), target=process, args=[job_queue, data_queue])
        t.daemon = True
        t.start()
        # Just so our start times are staggered
        time.sleep(0.5)
        
    job_queue.join()
    data_queue.join()
    
    print_s('Done.')
    
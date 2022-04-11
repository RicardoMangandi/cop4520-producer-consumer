############## Redis Imports Start Here ###########################
import queue
from redis import Redis
from rq import Queue, Worker
from rq.registry import StartedJobRegistry

################# Redis Imports End Here ########################

############### Misc. Imports ####################################

import sys
from datetime import datetime
import time
############### Misc. Imports ####################################


########### From task_def folder #################################

from task_def import do_task_sleep

from task_def import do_video_split
from task_def import do_csv_parse
from task_def import do_webscrape

########### From producer_logic folder ###########################

from producer_logic import video_editing_logic


##################################################################

#CONFIG

# list of csv files to parse
csv_files = ['../../csv_files/ADP_data.csv', '../../csv_files/AAL_data.csv', '../../csv_files/ABC_data.csv']
searchFor = '2013'

# list of urls to try for webscraping
url_list = ['http://nvie.com', 'https://en.wikipedia.org/wiki/Main_Page']

#######################################################################################################
now = datetime.now()

current_time = now.strftime("%H:%M:%S")

q_1 = Queue(name="queue_one", connection=Redis(),default_timeout=-1) #Nick Queue CSV reading queue 

q_2 = Queue(name="queue_two", connection=Redis(), default_timeout=-1) # Ricardo Queue Video Editing

q_3 = Queue(name="queue_three", connection=Redis(),default_timeout=-1) # Kyle Queue Webscrapping Queue

q_0 = Queue(name="queue_zero", connection=Redis(),default_timeout=-1) # task is to sleep for 5 seconds

num_of_threads_in_total = Worker.count(connection=Redis())


def selection_driver(selected_queue,num_of_threads):

    task_list = []

    if selected_queue == str(1):
        print("You have selected to parse csv files.")
        for file in csv_files:
            task = q_1.enqueue(do_csv_parse,file,searchFor)
            task_list.append(task)

        return task_list

    elif selected_queue == str(2):

        print("You have selected to split videos.")
        print("------------------------------------------------")
        list_returned = video_editing_logic.produce_video_split(num_of_threads=num_of_threads)
        for i in list_returned:
            task = q_2.enqueue(do_video_split.do_video_split,i)
            task_list.append(task)
        
        return task_list

    elif selected_queue == str(3):
        print("You have selected to web scrape.")
        for url in url_list:
            task = q_3.enqueue(do_webscrape,url)
            task_list.append(task)  
    else:
        print("You have selected to sleep for 10 seconds.")
        for i in range(0,5):
            q_0.enqueue(do_task_sleep.do_task_function)

####################################################################################







if num_of_threads_in_total <= 1:
    print("It seems that there is one thread running or less than one thread running. Goodbye.")
    sys.exit()
else:
    
    print("Welcome please select a queue to utilize.")
    
    print("0. Queue 0")
    print("1. Queue 1") 
    print("2. Queue 2")
    print("3. Queue 3")

    selected_queue_val = input()

    if selected_queue_val == str(1):
        num_of_threads_for_queue = Worker.count(connection=Redis(), queue=q_1)
        
        if num_of_threads_for_queue == 0:
            print(f"Execution time for items in queue: {q_1.name} is unknown.")
            print(f"There are no workers listening to {q_1.name}, goodbye")
            sys.exit()
    
    elif selected_queue_val == str(2):
        num_of_threads_for_queue = Worker.count(connection=Redis(), queue=q_2)

        if num_of_threads_for_queue == 0:
            print(f"Execution time for items in queue: {q_2.name} is unknown.")
            print(f"There are no workers listening to {q_2.name}, goodbye")
            sys.exit()

    elif selected_queue_val == str(3):
        num_of_threads_for_queue = Worker.count(connection=Redis(), queue=q_3)

        if num_of_threads_for_queue == 0:
            print(f"Execution time for items in queue: {q_3.name} is unknown.")
            print(f"There are no workers listening to {q_3.name}, goodbye")
            sys.exit()

    else:
        num_of_threads_for_queue = Worker.count(connection=Redis(),queue=q_0)

        if num_of_threads_for_queue == 0:
            print(f"Execution time for items in queue: {q_0.name} is unknown.")
            print(f"There are no workers listening to {q_0.name}, goodbye")
            sys.exit()

    selection_driver(selected_queue_val,num_of_threads_for_queue)
    print("--------------------------------------------------")
    print("Collecting workers who are working please wait... ")
    time.sleep(3)

    if selected_queue_val == str(1):
        # = StartedJobRegistry(q_1.name,connection=Redis())
        list_of_worker_working_on_q_n = q_1.started_job_registry.get_job_ids()
        queue_name = q_1.name
    
    elif selected_queue_val == str(2):
        #registry = StartedJobRegistry(q_2.name,connection=Redis())
        list_of_worker_working_on_q_n = q_2.started_job_registry.get_job_ids()
        queue_name = q_2.name
    
    elif selected_queue_val == str(3):
        #registry = StartedJobRegistry(q_3.name,connection=Redis())
        list_of_worker_working_on_q_n = q_3.started_job_registry.get_job_ids()
        queue_name = q_3.name

    else:
        list_of_worker_working_on_q_n = q_0.started_job_registry.get_job_ids()
        queue_name = q_0.name               
    
    start_time = datetime.now()

    print("Please wait while the tasks are being exected... ")
    

    while len(list_of_worker_working_on_q_n) != 0:
            list_of_worker_working_on_q_n = StartedJobRegistry(name=str(queue_name),connection=Redis())


    end_time = datetime.now()

    final_time = end_time - start_time

    print("--------------------------------------------------")
    print("Execution time for items in queue:",queue_name,"was:",final_time)







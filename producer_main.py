############## Redis Imports Start Here ###########################
from redis import Redis
from rq import Queue, Worker
from rq.registry import StartedJobRegistry
import pandas as pd
################# Redis Imports End Here ########################

############### Misc. Imports ####################################

import sys
from datetime import datetime
import time
############### Misc. Imports ####################################


########### From task_def folder #################################

from task_def import do_task_sleep

from task_def import video_editing_logic
from task_def import do_csv_parse
from task_def import do_webscrape
from task_def import do_video_split

######################### From webscrappingfolder #########################################

from webscraping import producer_one
from webscraping import producer_two
from webscraping import producer_three

##################################################################




#CONFIG

# list of csv files to parse
csv_files = ['./csv_files/ADP_data.csv', './csv_files/AAL_data.csv', './csv_files/ABC_data.csv']
searchFor = '2014'

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
            task = q_1.enqueue(do_csv_parse.csv_count,file,searchFor)
            task_list.append(task)

        return task_list

    elif selected_queue == str(2):

        print("You have selected to split videos.")
        print("------------------------------------------------")
        list_returned = video_editing_logic.produce_video_split(num_of_threads=num_of_threads)

        if list_returned == None:
            return None
        
        else:

            for i in list_returned:
                task = q_2.enqueue(do_video_split.do_video_split,i)
                task_list.append(task)
        
        #return task_list

    elif selected_queue == str(3):
        print("You have selected to web scrape.")
        #for url in url_list:
            #task = q_3.enqueue(do_webscrape.count_words_at_url,url)
        task_1 = q_1.enqueue(producer_one.task_one)
        task_2 = q_2.enqueue(producer_two.task_two)
        task_3 = q_3.enqueue(producer_three.task_three)
        task_list.append(task_1)
        task_list.append(task_2)
        task_list.append(task_3)

        return task_list

    else:
        print("You have selected to sleep for 10 seconds.")
        for i in range(0,5):
            q_0.enqueue(do_task_sleep.do_task_function)

####################################################################################







if num_of_threads_in_total <= 0:
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

    task_results_list = selection_driver(selected_queue_val,num_of_threads_for_queue)
    print("--------------------------------------------------")
    print("Collecting workers who are working please wait... ")
    time.sleep(1)

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


    if queue_name == "queue_three":
        data_frame = []
        for i in task_results_list:
            print(i)
            data_frame.append(i.result)
        result = pd.concat(data_frame)

    end_time = datetime.now()

    final_time = end_time - start_time

    print("--------------------------------------------------")
    print("Execution time for items in queue:",queue_name,"was:",final_time)







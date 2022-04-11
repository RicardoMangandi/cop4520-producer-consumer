##############Redis Imports Start Here###########################

from redis import Redis
from rq import Queue, Worker
from rq.registry import StartedJobRegistry

#################Redis Imports End Here########################

############### Misc. Imports ####################################

import sys
from datetime import datetime

############### Misc. Imports ####################################


########### From task_def folder #################################

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

        return task_list
        
    else:
        print("Invalid queue")
####################################################################################



now = datetime.now()

current_time = now.strftime("%H:%M:%S")

q_1 = Queue(name="queue_one", connection=Redis(),default_timeout=-1) #Nick Queue CSV reading queue 

q_2 = Queue(name="queue_two", connection=Redis(), default_timeout=-1) # Ricardo Queue Video Editing

q_3 = Queue(name="queue_three", connection=Redis(),default_timeout=-1) # Kyle Queue Webscrapping Queue

num_of_threads = Worker.count(connection=Redis())



if num_of_threads <= 1:
    print("It seems that there is one thread running or less than one thread running. Goodbye.")
    sys.exit()
else:
    print("Welcome please select a queue to utilize.")
    
    print("1. Queue 1") 
    print("2. Queue 2")
    print("3. Queue 3")

    selected_queue_val = input()
    task_list = selection_driver(selected_queue_val,num_of_threads)

    if selected_queue_val == str(1):
        print(selected_queue_val)
        name_of_queue = "queue_one"
    elif selected_queue_val == str(2):
        print(selected_queue_val)
        name_of_queue = "queue_two"
    elif selected_queue_val == str(3):
        print(selected_queue_val)
        name_of_queue = "queue_three"
    
    
    start = datetime.now()
    start_time = start.strftime("%H:%M:%S")

    print("name of queue: ",name_of_queue)

    #initialize current_jobs_executing
    current_jobs_executing = StartedJobRegistry(name=str(name_of_queue),connection=Redis()).get_job_ids()
    print(len(current_jobs_executing))
    
    while len(current_jobs_executing) != 0:

        current_jobs_executing = StartedJobRegistry(name=str(name_of_queue),connection=Redis()).get_job_ids()

        #print(str(len(current_jobs_executing))+" running workers")


    end = datetime.now()

    final = end - start

    print("Time taken " +str(final))







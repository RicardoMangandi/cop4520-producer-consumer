from redis import Redis
from rq import Queue, Worker
import csv
import time
from csv_task import csv_count
startTime = time.time()
# Goal: to search for the number of instances of some string in the csv




# Config
csv_files = ['../../csv_files/ADP_data.csv', '../../csv_files/AAL_data.csv', '../../csv_files/ABC_data.csv']
searchFor = '2013'
#output_file = open('output.txt', 'a')

# Init queue and workers
redis = Redis()
q = Queue(name = "queue_1", connection=redis)

#for i in range(len(csv_files)):
    #print("Starting worker")
    
    #w = Worker([q],connection=redis)
    #w.work()







jobList = []
count = 0
def report_success(job,connection,result,*args,**kwargs):
    print('RESULT FROM JOB  ', job.job_id, ': ',  result)
    print(result)
    count+= result

for file in csv_files:
    job = q.enqueue(csv_count,file)
    jobList.append(job)

"""
with open() as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            #print(f"Enqueing job with row {row} and searchFor {searchFor}")
            msg = [row,searchFor]
            job = q.enqueue(parse_task,msg)
            jobList.append(job)
            line_count += 1
    print(f'Processed {line_count} lines.')
"""

queued_job_ids = q.job_ids
#print(queued_job_ids)

time.sleep(3)

for job_id in queued_job_ids:
    job = q.fetch_job(job_id)
    print(job.result)


endTime = time.time()
totalTime = endTime-startTime
print("Execeution time " , totalTime , " sec")

q.empty()
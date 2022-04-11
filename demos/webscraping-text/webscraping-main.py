from redis import Redis
from rq import Queue, Worker, Connection
from tasks import count_words_at_url
import time
import sys




q = Queue(connection=Redis())


job = q.enqueue(count_words_at_url, 'http://nvie.com')

time.sleep(3)
print("RESULT: ")
print(job.result)
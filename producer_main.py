from redis import Redis
from rq import Queue
from task_def import do_task_1


q_1 = Queue(name="queue_one", connection=Redis())

q_2 = Queue(name="queue_two", connection=Redis())


#one enqueue into queue_one
q_1.enqueue(do_task_1.do_task_function,10)

#one enqueue into queue_two
#q_2.enqueue(do_task_2.do_task_function,10)
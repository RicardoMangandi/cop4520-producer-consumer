import os
import sys

print("Enter the number of consumer threads, we are currently limited to 10: ")
thread_number = input()

if int(thread_number) > 10:
    print("Invalid entry")
    sys.exit()

print("Select the queue to consume from: ")

print("0. queue_zero")
print("1. queue_one")
print("2. queue_two")
print("3. queue_three")

task_number = input()

listen_on_queue_name = ""

if int(task_number) > 3:
    print("Invalid entry, goodbye")
    sys.exit
    

else:


    if int(task_number) == 1:
        listen_on_queue_name = "queue_one"

    elif int(task_number) == 2:
        listen_on_queue_name = "queue_two"

    elif int(task_number) == 3:
        listen_on_queue_name = "queue_three"
    
    else:
        listen_on_queue_name = "queue_zero"

    command = "python3 create_thread.py " + listen_on_queue_name

    for i in range(int(thread_number) - 1):
        command = command + f"& python3 create_thread.py {listen_on_queue_name}"


    os.system(command)

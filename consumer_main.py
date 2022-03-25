import os

print("Enter the number of consumer threads, we are currently limited to 10: ")
thread_number = input()


print("Select the queue to consume from: ")

print("1. ")
print("2. ")
print("3. ")



task_number = input()


listen_on_queue_name = ""

if int(thread_number) > 10 and task_number > 3:
    print("Invalid entry, goodbye")

else:

    if int(task_number) == 1:
        listen_on_queue_name = "queue_one"

    elif int(task_number) == 2:
        listen_on_queue_name = "queue_two"

    else:
        listen_on_queue_name = "queue_three"


    command = "python3 create_thread.py "+ listen_on_queue_name

    for i in range(int(thread_number) - 1):
        command = command + f"& python3 create_thread.py {listen_on_queue_name}"


os.system(command)
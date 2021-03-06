# cop4520-producer-consumer


## The Producer and Consumer Problem

The producer and consumer problem is an extremely popular programming paradigm. It is used for mult-process synchronization between more than one processes. There can be one producer and one consumer or multiple producers and multiple consumers. The data structure commanly used to solve this problem is a blocking queue. The producer enqueues items inside the queue and the consumer dequeues items from the queue.

Our project goal is to show the practical application of blocking data structures in long running tasks. We are creating a Python application that will have a blocking queue represented by Redis, producers which are represented by the user, and consumer which are represented by Redis workers. Redis is an in-memory data structure store. Redis supports different kinds of abstract data structures such as lists, sets, stacks, and queues. Our main interest is being able to parallelize tasks with a queue and multiple workers. The tasks that are queued will be long tasks such as web-scrapping, video editing, and reading fron a csv.


![Screen Shot 2022-03-25 at 10 50 40 AM](https://user-images.githubusercontent.com/62866287/160144542-b5bd8c61-6034-44eb-8e1d-3e6518f036ef.png)



## Get Started

```bash 
git clone https://github.com/RicardoMangandi/cop4520-producer-consumer.git
```

Install FFMPEG for your operating system: https://www.ffmpeg.org/download.html

Create a Python virtual environment and activate it. Once activated use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries used in the application.
```bash
pip install -r requirements.txt
```


### Redis Installation Guide:
Next we will need to install redis on your local machine to be able to run our program and build the in-memory queue. Please follow the installtion guidelines dependent on your OS.

* [Redis Download Guideline](https://redis.io/docs/getting-started/)


Once redis is installed run the command to start up the redis data structure store locally based on your local machine and requirements.
You should be able to run the following command:

```bash
redis-cli
```

The command above runs the Redis Command Line Interface. To exit, enter ```exit``` 


### Redis Dashboard

The Redis Dashboard is UI served on Flask that displays all the queues inside Redis and all the "worker" or "threads" listening to that queue.

![Screen Shot 2022-03-25 at 2 41 55 AM](https://user-images.githubusercontent.com/62866287/160068352-58b91352-f92b-4b62-b7b4-8dc9af7cddd6.png)


In the image above we can see that there is a queue names "queue_one" and there are three working threads listening to "queue_one". This example does not do anything interesting, they just sleep for a period of time. However, there are three threads accomplishing this work in parallel and once they are done they go on and continue to the next task in the queue. The play button means they are doing work and the pause button means they have no work to do. 


Run the following command to display the Redis Dashboard UI: 

```bash
rq-dashboard
```

Then open up the web-browser and go to localhost:9181


### Consumer

To run the consumers and generate "working threads" we need to run the following python script  ```consumer_main.py```

The application will ask the user how many threads they will like to spin up. We are limiting the user to a maximum of 10 threads.

The application will then ask the user on what queue they would like to listen to. If the user specifies a queue that does not exist nor has items inside it the workers will remain idle and not work. Please run this script first.



### Producer

To run the producer and enqueue items to a specific queue we need to run the following python script ```producer_main.py```

The application will ask the user on what queue they would like to listen to. Ensure that we are picking the queue that has active 
workers listening on that queue or else the queued items will remain in queue regardless of how many consuming threads we have. 


### Consumer

To run the consumers and generate "working threads" we need to run the following python script  ```consumer_main.py```

The application will ask the user how many threads they will like to spin up. We are limiting the user to a maximum of 10 threads.

The application will then ask the user on what queue they would like to listen to. If the user specifies a queue that does not exist nor has items inside it the workers will remain idle and not work.


### task_def

The task_def folder is where we will write the code logic for each enqueue that occurs.

#### To run the video editing which is queue two be sure to fix path inside video_editing_logic.py: 

This is line 7 on video_editing_logic inside task_def folder.

```Python
file_location = "/Users/ricardomangandi/Downloads/scene-2.mov"
```





### Conclusion for getting started simplified:

```ensure FFMPEG is installed```

```run command to start redis based on OS```

```activate python virtual environment```

```pip install -r requirements.txt```

```bash
rq-dashboard
```

```open up localhost:9181```

```bash
python3 consumer_main.py
```

```bash
python3 producer_main.py
```







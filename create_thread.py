import os
import sys

name_of_queue = sys.argv[1]

print(sys.argv[1])

build_command = "rq worker "+str(name_of_queue)

os.system(build_command)
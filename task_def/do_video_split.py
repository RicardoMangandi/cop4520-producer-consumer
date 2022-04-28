import os
from datetime import datetime



def do_video_split(string_command):
    start = datetime.now()
    start_time = start.strftime("%H:%M:%S")
    os.system(string_command)
    end = datetime.now()

    final = end - start
    return 
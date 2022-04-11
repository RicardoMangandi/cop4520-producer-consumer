import cv2

def produce_video_split(num_of_threads):
    #file_location = "/Users/ricardomangandi/Desktop/python/cv/Watford-vs-Liverpool-0-5-WISELOADED-HIGHLIGHTS.mp4"
    file_location = "/Users/ricardomangandi/Downloads/scene-2.mov"

    cap = cv2.VideoCapture(file_location)

    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count / fps)


    print("fps = " + str(fps))
    print("number of frames = " + str(frame_count))
    print("duration (S) = " + str(duration))
    minutes = int(duration / 60)
    seconds = int(duration % 60)
    print("duration (M:S) = " + str(int(minutes)) + ":" + str(int(seconds)))
    increment_every = int(duration / num_of_threads)

    counter = 1
    build_command = []
    start_int = 0
    while counter <= num_of_threads:

        if counter == num_of_threads:
            end = duration
        else:
            end = increment_every + start_int

        command = f"ffmpeg -y -i {file_location} -ss {start_int} -to {end} video{counter}.mp4"

        build_command.append(command)

        start_int = increment_every + start_int

        counter += 1

    return build_command
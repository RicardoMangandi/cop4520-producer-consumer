
import requests
import csv
import time


searchFor = '2013'

#Task-given a whole row, return count
def parse_task(msg):
    count = 0
    #output_file = open('output.txt', 'a')
    #for s in row:
    #    count += s.count(searchFor)

    #output = 'Result of job ' + str(count)
    #output_file.write(output)

    return msg[1]

#print(parse_task(['abcd','asdf'],"asdf"))

def csv_count(filename):
    startTime = time.time()
    count = 0
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                for s in row:
                    count += s.count(searchFor)

                line_count += 1
                
        print(f'Processed {line_count} lines.')
        print("Found " , count , " occurences of " , searchFor)

    endTime = time.time()
    totalTime = endTime-startTime
    print("Execeution time " , totalTime , " sec")
    return count

def count_words_at_url(url):
    """Just an example function that's called async."""
    #resp = requests.get(url)
    #return len(resp.text.split())
    return 4
import time
import csv

searchFor = '2013'

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
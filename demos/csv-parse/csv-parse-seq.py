import csv
import time

startTime = time.time()

# Config
file = '../../csv_files/TeamData.csv'
searchFor = '87'

count = 0
with open(file) as csv_file:
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
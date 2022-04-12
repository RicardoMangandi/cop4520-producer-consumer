from producer_one import *
from producer_two import *
from producer_three import *
import pandas as pd
import time

start_time = time.time()

df1 = task_one()
df2 = task_two()
df3 = task_three()

dataframes = [df1, df2, df3]
result = pd.concat(dataframes)
print("-- %s seconds --" % (time.time() - start_time))

result.to_csv("Data.csv")
import datetime
import time
# 用户发布的时间
time1 = datetime.datetime(2016, 5, 24, 17, 35, 10, 553391)
# 现在的时间
time2 = datetime.datetime.now()
time3 = time2-time1
# print(time3,type(time3))
print(time.gmtime())
# print(time3.days)
# print(time3.seconds)
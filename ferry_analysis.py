import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as delta
from matplotlib import pyplot as plt

regos= pd.read_csv("rego_table.csv")
ferrys = pd.read_csv("ferrys.csv")
ferrys.scheduledstart = ferrys.scheduledstart.apply(lambda x: dt.strptime(x, '%Y-%m-%d %H:%M:%S.000' ))

og_maints = pd.read_csv("maints.csv")
keyWords = ['Ferry', 'FERRY','ferry','owed','OWED','POS ',"Pos ",'pos ']#,' TO ',' to ']
maints=og_maints[og_maints.change_attributes_block_ids.str.contains("|".join(keyWords), na=False)]
maints.scheduledstart = maints.scheduledstart.apply(lambda x: dt.strptime(x, '%Y-%m-%d %H:%M:%S.000' ))
maints.source = maints.source.apply(lambda text: text.split('~!~')[1])

time_arr_f = ferrys["scheduledstart"]
today_f=min(ferrys["scheduledstart"])

time_arr_m = maints["scheduledstart"]
today_m=min(maints["scheduledstart"])

today=min(today_m,today_f)

ferrys_log=[]
maints_log=[]
dates=[]
months=4.5
step=1
#'ChgTgtAsrObjSchdBase','ChgAttsStrngMapplanned_base',
for day in range(0,int(30*months),step):
    next_day=today+ delta(days=step)
    intermediate = (time_arr_f<= next_day) & (time_arr_f>today)
    compatibleNodes = np.where(intermediate)[0]
    ferrys_log.append(len(compatibleNodes))
    
    intermediate = (time_arr_m<= next_day) & (time_arr_m>today)
    compatibleNodes = np.where(intermediate)[0]
    maints_log.append(len(compatibleNodes))
    
    dates.append(today)
    today=next_day

plt.figure(figsize=(30,17))
space=3
locs = np.arange(0, len(dates) * space, space)
plt.bar(locs+np.ones(len(dates))*0.5,ferrys_log, 0.35, alpha=0.8, label='Ferry flights')
plt.bar(locs-np.ones(len(dates))*0.5,maints_log, 0.35, alpha=0.8, label='Maintenance')
plt.xticks(locs-np.ones(len(dates))*space,dates,visible=True)
plt.legend()
plt.ylabel("Ferry flights")
plt.xticks(rotation=75)
plt.savefig("ferry_frequency.png", dpi=300)



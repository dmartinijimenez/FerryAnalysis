import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as delta
from matplotlib import pyplot as plt


og_maints = pd.read_csv("maints.csv")
keyWords = ['Ferry', 'FERRY','ferry','owed','OWED','POS ',"Pos ",'pos ']#,' TO ',' to ']
ferry_doc=[6100,6155]#%61-n-dayofweek
maints=og_maints[og_maints.change_attributes_block_ids.str.contains("|".join(keyWords), na=False)]
maints.scheduledstart = maints.scheduledstart.apply(lambda x: dt.strptime(x, '%Y-%m-%d %H:%M:%S.000' ))
maints.source = maints.source.apply(lambda text: text.split('~!~')[1])

 
        
time_arr = maints["scheduledstart"]
today=min(maints["scheduledstart"])
m_ferrys=[]
dates=[]
months=4.5

for day in range(0,int(30*months),5):
    next_day=today+ delta(days=1)
    intermediate = (time_arr<= next_day) & (time_arr>today)
    compatibleNodes = np.where(intermediate)[0]
    m_ferrys.append(len(compatibleNodes))
    dates.append(today)
    today=next_day
    
#space=3.0
#locs = np.arange(0, 30*months* space, space)
fm=len(maints)/len(og_maints)
print('Only',round(fm*100,2),'% are ferry flights out of all the maintenance activities published')

plt.figure()
plt.bar(dates,m_ferrys, 0.4, alpha=0.8, label='Time SP')
plt.ylabel("Ferry flights")
plt.xticks(rotation=75)
plt.savefig("ferry_frequency.png", dpi=300)

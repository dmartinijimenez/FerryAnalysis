# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:41:44 2019
@author: 628092
"""
'''
Metrics:
    Percentage distributin of publication befoer actual start
    Percentage maint for ferrys detected vs possibly in datset (non-hollistic apoproach + uncertainty due to written p0lacard)
    Distribution maint before start (days, hours, overnight, overlap)
    Duration distribution (indicates uncertainty of when ferry flightis going to occur)
    Difference in publication between ferry and maintenance (done not to alter stats?)
    analyze by roc/doc/ioc based on rego
'''
from maint_prev_flight import *
from matplotlib import pyplot as plt

print('Maintenance with ferry placard',len(maints)/len(og_maints)*100,'%')
print('The number of ferry flights anticipated by maintenance is',ferrysWithMaint)
print('Maintenance with ferry placard matched to an actual ferry flight',matchedMaints/len(maints)*100,'%')
print('The toal matched maintenance to ferry flights is',matchedMaints)
print('Ratio of maint vs ferry flight duration',np.mean(maintDurationration))
print('Average ferry publication occurs',np.mean(ferryDelta),'before scheduled start')
print('Average ferry publication anticipated by maint occurs',np.mean(ferryDeltaWithMaint),'before scheduled start')

time_arr_f = ferrys["scheduledstart"]
today_f=min(ferrys["scheduledstart"])

time_arr_m = maints["scheduledstart"]
today_m=min(maints["scheduledstart"])
today=min(today_m,today_f)

prevStep= delta(hours=0)
dtStart_log=[]
dtList=[]
dtPubl_log=[]
dt_list=[1,2,5,10,15]+list(range(24,30*24,24))+[150000]
for dt in dt_list:
    timeStep= delta(hours=dt)
    intermediate = (np.array(dtBeforeFlight)< timeStep)*(np.array(dtBeforeFlight)>= prevStep)
    compatibleNodes = np.where(intermediate)[0]
    dtStart_log.append(len(compatibleNodes)/len(dtBeforeFlight)*100)
    intermediate = (np.array(dtBetweenPublication)< timeStep)*(np.array(dtBetweenPublication)>= prevStep)
    compatibleNodes = np.where(intermediate)[0]
    dtPubl_log.append(len(compatibleNodes)/len(dtBetweenPublication)*100)
    dtList.append(prevStep)
    prevStep=timeStep

plt.figure(figsize=(30,17))
space=3
locs = np.arange(0, len(dtList) * space, space)
plt.bar(locs+np.ones(len(dtList))*0.5,dtStart_log, 0.35, alpha=0.8, label='Start difference')
plt.bar(locs-np.ones(len(dtList))*0.5,dtPubl_log, 0.35, alpha=0.8, label='Publication difference')

plt.xticks(locs,dtList,visible=True)
plt.legend()
plt.ylabel("Events percenatge [%]")
plt.xticks(rotation=75)
plt.savefig("maintDistribution.png", dpi=300)

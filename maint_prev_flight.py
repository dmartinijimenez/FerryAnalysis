import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as delta
from matplotlib import pyplot as plt

fleet_regos= pd.read_csv("rego_table.csv")

ferrys = pd.read_csv("ferrys.csv")
ferrys.scheduledstart = ferrys.scheduledstart.apply(lambda x: dt.strptime(x, '%Y-%m-%d %H:%M:%S.000' ))
ferrys.timestamp1 = ferrys.timestamp1.apply(lambda x: dt.strptime(x, '%Y-%m-%d %H:%M:%S.000' ))
ferrys["flightNumber"] = np.nan
ferrys["rego"] = np.nan
ferrys["fleet"] = np.nan
ferrys["subfleet"] = np.nan
ferrys.flightNumber = ferrys.source.apply(lambda text: text.split('~!~')[1])
ferrys.rego = ferrys.source.apply(lambda text: text.split('~!~')[2])
#ferrys.rego=ferrys.change_source.apply(lambda text: text.split('~!~')[2])

og_maints = pd.read_csv("maints.csv")
keyWords = ['Ferry', 'FERRY','ferry','owed','OWED']#,' TO ',' to ']
maints=og_maints[og_maints.change_attributes_block_ids.str.contains("|".join(keyWords), na=False)]
maints["rego"] = np.nan
maints.scheduledstart = maints.scheduledstart.apply(lambda x: dt.strptime(x, '%Y-%m-%d %H:%M:%S.000' ))
maints.timestamp1 = maints.timestamp1.apply(lambda x: dt.strptime(x, '%Y-%m-%d %H:%M:%S.000' ))
maints.rego = maints.source.apply(lambda text: text.split('~!~')[1])
maints["departure_port"]= maints.change_targetasrobject_id.apply(lambda text: text[::-1].split('_')[3][::-1])


arrival_port=[]
fleet=[]
subfleet=[]

for index, row in maints.iterrows():
    compatible=np.where(fleet_regos.rego==row.rego)[0]
    index_port=fleet_regos.iloc[[compatible[0]]].index[0]
    fleet.append(fleet_regos.fleet[index_port])
    subfleet.append(fleet_regos.fleet_subtype[index_port])
    listvalues=row.change_attributes_block_ids.split(' ')
    found_vals=np.nan
    for word in range(len(keyWords)):
        if keyWords[word] in listvalues :
            ind=listvalues.index(keyWords[word])
            first=listvalues[ind+1]
            second=listvalues[-1].split('=0')[0]
            if len(second)==3 :
                found_vals=second
            elif len(first)==3:
                found_vals=first
            elif '=0' in first and len(first.split('=0')[0])==3:
                found_vals=first.split('=0')[0]
            elif len(listvalues[(ind+2)%len(listvalues)])==3:
                found_vals=listvalues[(ind+2)%len(listvalues)]   
    arrival_port.append(found_vals)
    
maints["arrival_port"] = arrival_port
maints["fleet"] = fleet
maints["subfleet"] = subfleet


time_arr_maints = maints["scheduledstart"]
time_arr_flights = ferrys["scheduledstart"]

maints=maints.sort_values(by=['source'])

flightsScheduled=dict()
for index,entry in ferrys.iterrows():
    fnum=entry.flightNumber
    timePub=entry.scheduledstart-entry.timestamp1
    flightsScheduled[int(fnum)]=[timePub]
    
for index, row in maints.iterrows():
    conditional=(row.rego==ferrys.rego)*(row.arrival_port==ferrys.change_targetasrobject_destination)*(row.departure_port==ferrys.change_targetasrobject_origin)
    compatible=np.where(conditional)[0]
    for ind in range(len(compatible)):
        index_port=ferrys.iloc[[compatible[ind]]].index[0]
        maintDelta=ferrys.scheduledstart[index_port]-row.scheduledstart
        maintPublishedDelta=ferrys.scheduledstart[index_port]-row.timestamp1
        ferryDelta=ferrys.scheduledstart[index_port]-ferrys.timestamp1[index_port]
        fnum=ferrys.change_targetasrobject_flightnumber[index_port]
        if maintDelta>delta(0):
            print('Left',len(compatible)-ind,row.rego)
            print(ferrys.change_targetasrobject_carrier[index_port],ferrys.change_targetasrobject_flightnumber[index_port])
            print('The schedu led time is ', ferrys.scheduledstart[index_port])
            print('The publicatiopn time are')
            print('Maint is published at ',maintDelta)
            print('Flight is published at ',ferryDelta)
            print()
            flightsScheduled[fnum].append(maintDelta)
            

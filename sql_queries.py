#Query 1
'''
Create Table "events_programs"."swaps" as (
  select * from "program_analysis"."events" 
  where "source" <> 'compress'
  and "type"='NewEventLinkChange'
  and "change_type"='ActivityAttributeChange'
 and "change_targetasrobject_type"='LegDate')

select 
"id", "timestamp", "source","event_id","event_type","event_category",
"event_author", "event_creationdate","change_id", "change_source", "change_timestamp",
"change_targetasrobject_id", "change_targetasrobject_origin", "change_targetasrobject_destination",
"change_targetasrobject_flightnumber", "change_targetasrobject_carrier",
"change_targetasrobject_start","change_targetasrobject_end", 
"change_attributes_last_aircraft_assigned", "change_attributes_eobt","change_attributes_eibt", change_attributes_type_code
'''
#Query 2

'''
from "events_programs"."swaps"
where "timestamp" > 1546300800000 
        AND change_attributes_type_code ='P'

order by timestamp
'''
#Query 3

'''
DROP TABLE `swaps`;
'''
#query 4
'''
Create Table "events_programs"."maints" as (
  select * from "program_analysis"."events" 
  where "source" <> 'compress'
  and "type"='NewEventLinkChange'
  and "change_type"='ActivityAttributeChange'
 and "change_targetasrobject_type"='Maintenance')
'''

#Query 5
'''
select 
"id", "timestamp", "source","event_id","event_type","event_category",
"event_author", "event_creationdate","change_id", "change_source", "change_timestamp",
"change_targetasrobject_id", "change_targetasrobject_origin", "change_targetasrobject_destination",
"change_targetasrobject_flightnumber", "change_targetasrobject_carrier",
"change_targetasrobject_start","change_targetasrobject_end", 
"change_attributes_last_aircraft_assigned", "change_attributes_eobt","change_attributes_eibt", change_attributes_type_code, change_attributes_block_ids

from "events_programs"."maints"
where "timestamp" > 1546300800000 

order by timestamp
'''

#Notes on Iain sesh
'''
Where column LIKE "%ferry%"
Join table
INNER JOIN 
left join
LJOIN
Union(concatenation)
Set col3=2*col2
order by 3,4 (or write name of column)
coalesce(b.timestamp,99999)
count(*)#aggregate function
window functions
'''
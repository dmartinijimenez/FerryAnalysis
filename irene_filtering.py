### Replace the last_delay_applied field with the total delay minutes
df['ChgAttsNoMaplast_delay_applied'] = (df.ChgAttsDtTmMapeobt - df.ChgTgtAsrObjstart)/60000

##Sort Delay publications
sortList = ['ChgAttsDtTmMapeobt','TmStamp']
delays = df[(np.isnan(df.ChgAttsNoMaplast_delay_applied) == False) & (df.ChgAttsNoMaplast_delay_applied != 0)]

## Inside one publication (same timestamp, different change timestamp), find the last change & use the total delay ##from there
delays['rank'] = delays.groupby(sortList)['ChgTmStamp'].transform(lambda x: x.rank(method='first',ascending=False))
OneRowPerPub = delays[delays['rank'] == 1]

"""
This script generates the Alert Level time series for Dispa-SET
Input : SDDP database
Output : Database/ .csv

@author: Alizon Huallpara UMSS
"""
import pandas as pd

df = pd.read_csv('../03_SDDP_DATABASE/04_HYDRO/volale.csv', index_col=0, header=3)
df.columns = df.columns.str.replace(' ', '')

#hm3 to fraction
hydro = pd.read_csv('../03_SDDP_DATABASE/04_HYDRO/chidrobo.csv', usecols=['...Nombre...','.VMax..','.VInic.'], header=0)

#Activate for initial volume
df_new = pd.DataFrame(hydro[".VInic."]*hydro[".VMax.."]).T
df_new.columns = hydro['...Nombre...']
df_new=df_new.rename({0:156},axis=0)
df.update(df_new)

divisors = dict(zip(hydro['...Nombre...'], hydro['.VMax..']))
alertlev = (df.iloc[:,2:].apply(lambda x: x / divisors[x.name], axis=0))

#choosing the last year
alertlev = alertlev.loc[144:195]

#create the dataframe with hourly resolution
alertlev.set_index(pd.date_range(start='2025-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='W'), inplace=True)
alertlevh = pd.DataFrame(index=pd.date_range(start='2025-12-31 23:00:00+00:00', end='2026-12-31 23:00:00+00:00', freq='H'), 
                        columns=alertlev.columns)
alertlevh.loc[alertlev.index, :] = alertlev.loc[alertlev.index, :]
alertlevh.iloc[[0,-1],:] = alertlev.iloc[[0,0],:]
alertlevh = alertlevh.astype('float64').interpolate()

alertlevh.to_csv('../04_DISPASET_DATABASE/AlertLevel/AlertLevel1.csv', header=True, index=True)
import matplotlib.pyplot as plt
alertlevh['ANG'].plot(x=alertlevh.index, y='ANG')
plt.show()
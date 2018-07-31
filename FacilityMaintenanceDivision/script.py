import plotly.plotly as py
# custom helper modules to get, clean and graph this data
import fetcher, ploter

####### get data #########
df = fetcher.create_pm2cm_dataframe('Data/archibus_maintenance_data.xlsx')
dicts = fetcher.create_pm2cm_kpi_values_dicts(df)

####### program variables ###########
years = list(dicts[0])
kpi_values = list(dicts[0].values())
dataframes = dicts[1]

###### create & store chart figure object ######
pm2cm_fig = ploter.pm2cm_barchart(years=years,values=kpi_values,dataframes=dataframes)

if __name__ == '__main__':
    print('Sucessful. Return..... fiscal year: pm to cm KPI')
    for yr,val in dicts[0].items():
        print('{}: {}'.format(yr,round(val,1)))

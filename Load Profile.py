import demandlib.bdew as bdew
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

datapath = 'EBBR.csv'

df = pd.read_csv(datapath, index_col=1)

df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M') + pd.Timedelta(minutes=10)

profile = bdew.HeatBuilding(
    df.index,
    temperature=df["tmpc"],
    shlp_type="MFH",
    building_class=1,
    wind_class=0,
    annual_heat_demand=43483,
    name="MFH",
).get_bdew_profile()

plt.figure(figsize=(8, 6))
plt.plot(df.index, profile, label='Heat Demand Profile ', linewidth=0.3)
plt.xlim(df.index.min()-pd.Timedelta(days=1), df.index.max())

plt.xlabel('Date')
plt.ylabel('Heat Demand  [kW]')
plt.title('Heat Demand Profile of a multi-family house in Brussels 2021')

#################################### FORMATTERS #######################################
plt.axvspan(datetime.datetime(2021, 6, 21), datetime.datetime(2021, 9, 21), facecolor='orange', alpha=0.15)
plt.axvspan(datetime.datetime(2020, 12, 21), datetime.datetime(2021, 3, 20), facecolor='lightblue', alpha=0.3)

proxy_summer = plt.Rectangle((0, 0), 1, 1, fc="orange", alpha=0.15, edgecolor='orange', label='Summer')
proxy_winter = plt.Rectangle((0, 0), 1, 1, fc="lightblue", alpha=0.3, edgecolor='lightblue', label='Winter')

plt.legend(handles=[proxy_summer,proxy_winter])  # Add the legend

date_format = mdates.DateFormatter('%m-%d')
plt.gca().xaxis.set_major_formatter(date_format)
locator = mdates.MonthLocator(bymonthday=1)
plt.gca().xaxis.set_major_locator(locator)

tick_labels = [item.get_text() for item in plt.gca().get_xticklabels()]

if tick_labels:
    last_label = pd.to_datetime(tick_labels[-1], format='%m-%d')
    new_last_label = (last_label - pd.Timedelta(days=1)).strftime('%m-%d')
    tick_labels[-1] = new_last_label
plt.gca().set_xticklabels(tick_labels)
#######################################################################################

plt.grid(True)
plt.savefig(r'C:\Users\dylan\Documents\VUB\Heat duration year.pdf', format='pdf')
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(df.index, profile, label='Heat Demand Profile ', linewidth=0.8)
plt.xlim(pd.Timestamp(2021,3,1,0), pd.Timestamp(2021,3,20,0))

plt.xlabel('Date')
plt.ylabel('Heat Demand  [kW]')
plt.title('Heat Demand Profile of a multi-family house in Brussels March 2021')

#################################### FORMATTERS #######################################
for date in df.index:
    if date.weekday() >= 6:  # 5 and 6 represent Saturday and Sunday
        plt.axvspan(date - pd.Timedelta(days=4), date - pd.Timedelta(days=3), facecolor='lightgrey', alpha=0.2)
proxy_weekend = plt.Rectangle((0, 0), 1, 1, fc="lightgrey", alpha=0.5, edgecolor='lightgrey', label='Weekend')
plt.legend(handles=[proxy_weekend])
date_format = mdates.DateFormatter('%m-%d')
plt.gca().xaxis.set_major_formatter(date_format)
locator = mdates.DayLocator(interval=1)
plt.gca().xaxis.set_major_locator(locator)

tick_labels = [item.get_text() for item in plt.gca().get_xticklabels()]
ticks = []
weekday_labels = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
for tick in tick_labels:
    tick = pd.to_datetime(tick, format='%m-%d').weekday()
    ticks.append(weekday_labels[tick])
plt.gca().set_xticklabels(ticks)

#######################################################################################
plt.grid(True)
plt.savefig(r'C:\Users\dylan\Documents\VUB\Heat duration month.pdf', format='pdf')
plt.show()

sorted_profile = profile.sort_values()[::-1]
x_hours = [(i-df.index[0]).total_seconds()/3600 for i in df.index]
    
plt.figure(figsize=(8, 6))
plt.plot(x_hours, sorted_profile, label='Sorted Heat Demand Profile ', linewidth=0.8)
plt.xlim(x_hours[0]-100, x_hours[-1]+100)

plt.text(50, sorted_profile.max()-0.01, f'Peak Demand: {sorted_profile.max():.2f}', fontsize = 10) 

plt.xlabel('Hours')
plt.ylabel('Heat Demand [kW]')
plt.title('Duration curve of a multi-family house in Brussels 2021')

Area = 0
max_area = 0
max_index = 0
for i in range(len(sorted_profile)):
    Area = sorted_profile[i]*x_hours[i]
    if Area > max_area:
        max_area = Area
        max_index = i
rectangle = plt.Rectangle((0, 0), x_hours[max_index], sorted_profile[max_index], edgecolor='black', facecolor='red', alpha=0.2, label='Max Area')
plt.text(800, 2.3, f'Max area: {max_area:.0f} kWh', fontsize = 10) 
plt.gca().add_patch(rectangle)
plt.scatter(x_hours[max_index], sorted_profile[max_index], color='red', label='Point', s=10)
plt.text(x_hours[max_index]/2, sorted_profile[max_index], f'{x_hours[max_index]:.0f} h', ha='center', va='bottom')
plt.text(x_hours[max_index], sorted_profile[max_index]/2, f' {sorted_profile[max_index]:.3f} kW', ha='left', va='center')


plt.savefig(r'C:\Users\dylan\Documents\VUB\Duration curve.pdf', format='pdf')
plt.show()

profile.to_csv(r'C:\Users\dylan\Documents\VUB\Heat demand profile.csv')
import demandlib.bdew as bdew
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

datapath = 'EBBR.csv'

df = pd.read_csv(datapath, index_col=1)

df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M') + pd.Timedelta(minutes=10)

profile = bdew.HeatBuilding(
    df.index,
    temperature=df["tmpc"],
    shlp_type="MFH",
    building_class=1,
    wind_class=0,
    annual_heat_demand=1000,
    name="MFH",
).get_bdew_profile()

plt.figure(figsize=(8, 6))
plt.plot(df.index, profile, label='Heat Demand Profile ', linewidth=0.3)
plt.xlim(df.index.min()-pd.Timedelta(days=1), df.index.max())

plt.xlabel('Date')
plt.ylabel('Heat Demand')
plt.title('Heat Demand Profile of a multi-family house in Brussels 2021')

#################################### FORMATTERS #######################################
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
plt.show()
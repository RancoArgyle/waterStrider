# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
# from myParser import data_collector
from water_strider_mil import get_data as mil_get
from water_strider_nsw import get_data as nsw_get
import numpy as np
import plotly.subplots as ms
import plotly.graph_objects as go
#import pandas as pd


from plotly.offline import plot

def get_nsw_data(params):
   # scrapes nsw river transaction data
   df_nsw_tbl = nsw_get(params)
   if params['mode'] == 'allocation':
      df_nsw_tbl = df_nsw_tbl[['Assigned', 'Water Source',
         'Trade Purpose', 'Volume (ML)', 'Price Paid']]
      df_nsw_tbl.columns = ['Date', 'From',
         'Trade Purpose', 'Volume (ML)', 'Price Paid']
      df_nsw_tbl=df_nsw_tbl[df_nsw_tbl['Trade Purpose']!='Related Party']
   elif params['mode'] == 'transfer':
      # print(df_nsw_tbl.columns)
      df_nsw_tbl=df_nsw_tbl[['Transferred','Water Source','Category','Share (units or ML)',"Price Paid '$ per unit'"]]
      df_nsw_tbl["Price Paid '$ per unit'"]=df_nsw_tbl["Price Paid '$ per unit'"].str.strip().str.replace(',','').astype(float)
      df_nsw_tbl.columns=['Date','Water Source','Category','Share (units or ML)',"Price Paid '$ per unit'"]
      df_nsw_tbl.sort_values(
         by='Date',
         axis=0,
         ascending=False,
         inplace=True,
         ignore_index=True
      )
   elif params['mode'] == 'share':
      df_nsw_tbl=df_nsw_tbl[['Transferred','Water Source','Category','Share','Price Paid']]
      df_nsw_tbl.columns=['Date','From','From-category','Share','Price Paid']
      df_nsw_tbl['Date']=df_nsw_tbl['Date'].apply(lambda x: datetime.strptime(x,r'%d-%b-%Y'))
      df_nsw_tbl.sort_values(
         by='Date',
         axis=0,
         ascending=False,
         inplace=True,
         ignore_index=True
      )
      df_nsw_tbl['Date']=df_nsw_tbl['Date'].dt.strftime(r'%d-%b-%Y')
   return df_nsw_tbl

# ======================= Parameter definition ======================
# scrapes Financial times news
url = r'https://www.ft.com/world'
headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}
endDate=datetime.now()
days_back=31
mode=['allocation','share','transfer'][endDate.minute//20]
startDate=(endDate-timedelta(days=days_back)).strftime(r'%d-%b-%Y').upper()
endDate=endDate.strftime(r'%d-%b-%Y').upper()
params = {'mode': 'allocation',#mode,   # can choose from allocation/share/transfer
      'row_start': 0,
      'row_end': 999,
      'startDate': startDate,
      'endDate': endDate,
      'river': 'all'}

# fname mapping
fname_mapping = {
'allocation': 'allocation trading',
'share': 'entitlement share trading',
'transfer': 'share transfer'
}

nrows_mi = 800
nrows_nsw = 800

# ======================= End parameter definition ======================

# scrapes murray irrigation water daily sales data
df_mi = mil_get('dailysales')
df_mi_tbl = df_mi[:nrows_mi]

# scrapes nsw water data
df_nsw_tbl=get_nsw_data(params)
#df_nsw_tbl_chart=generate_line_charts(df_nsw_tbl,params['mode'])
df_nsw_tbl=df_nsw_tbl[:nrows_nsw]
nsw_tbl_name=fname_mapping[params['mode']]

# scrapes FT news
# all_data=data_collector(url=url,headers=headers,total=9)

TradePurpose = ['Forward Contract', 'Other', 'Private Lease (Not 71m)',
       'Share Transfer', 'Standard Commercial']
ft1 = (df_nsw_tbl['Price Paid']>0) & (df_nsw_tbl['Trade Purpose']==TradePurpose[4])
PB_NSW = df_nsw_tbl.loc[ft1,:].copy()
PB_NSW['Value'] = PB_NSW['Volume (ML)'] * PB_NSW['Price Paid'] 

NSW_StandardCommercial = PB_NSW.groupby(['Date']).agg(
    high_price=('Price Paid', np.max),
    low_price=('Price Paid', np.min),
    high_volume=('Volume (ML)', np.max),
    low_volume=('Volume (ML)', np.min),
    sum_volume=('Volume (ML)', np.sum),
    sum_value=('Value', np.sum),
    count_trades = ('Price Paid', np.count_nonzero))


NSW_StandardCommercial['VWAP'] = NSW_StandardCommercial['sum_value']/NSW_StandardCommercial['sum_volume']
NSW_StandardCommercial['Date'] = NSW_StandardCommercial.index

NSW_StandardCommercial["previousVWAP"] = NSW_StandardCommercial["VWAP"].shift(1)

# Define color based on close and previous close
NSW_StandardCommercial["color"] = np.where(NSW_StandardCommercial["VWAP"] > NSW_StandardCommercial["previousVWAP"], "green", "red")
# Set fill to transparent if close > open and the previously defined color otherwise
NSW_StandardCommercial["fill"] = np.where(NSW_StandardCommercial["previousVWAP"] > NSW_StandardCommercial["VWAP"], "rgba(255, 0, 0, 0)", NSW_StandardCommercial["color"])


fig = ms.make_subplots(rows=3, cols=1,
row_heights=[0.60, 0.25, 0.15],
shared_xaxes=True,
vertical_spacing=0.02)

#def plot_water_price_Candlestick(df):
df = NSW_StandardCommercial
fig.add_trace(go.Candlestick(x = df.index,
low = df['low_price'],
high = df['high_price'],
close = df['VWAP'],
open = df['previousVWAP'],
increasing_line_color = 'green',
decreasing_line_color = 'red',
name="Price Paid ($/ML)"),
row=1,
col=1)

#Add Volume Chart to Row 2 of subplot
fig.add_trace(go.Bar(x=df.index,
y=df['sum_volume'],marker_color='#e7ad2c',
name="Total Volume (ML)"),

row=2,
col=1)

#Add Volume Chart to Row 2 of subplot
fig.add_trace(go.Bar(x=df.index,
y=df['count_trades'],name="Trade Count",marker_color='#1C4E5E'),

row=3,
col=1)

#Update Price Figure layout
fig.update_layout(title = 'NSW Standard Commercial ($P > 0)',

yaxis1_title = 'Price Paid ($/ML)',
yaxis2_title = 'Volume(ML)',
yaxis3_title = 'Trade Count',
xaxis3_title = 'Date',
xaxis1_rangeslider_visible = False,
xaxis2_rangeslider_visible = False,
xaxis3_rangeslider_visible = False)

fig.update_xaxes(tickangle=(360-90))

plot(fig)
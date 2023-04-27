import pandas as pd
import requests, json, sys
from io import BytesIO
import logging
from pathlib import Path
from xlrd import XLRDError

# =============================================================================
# set logging
logger=logging.getLogger('water_strider')
logger.setLevel(logging.INFO)
handler=logging.StreamHandler()
# handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]: %(message)s',datefmt=r'%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('Program starts...')
requests.urllib3.disable_warnings()


# =============================================================================
# requests headers
headers={'accept':'*/*', 
        'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7', 
        'sec-ch-ua-platform': "Windows", 
        'user-agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

# fname mapping 
fname_mapping={
    'allocation':'allocation_trading',
    'share':'entitlement_share_trading',
    'transfer':'share_transfer'
}


# =============================================================================
# define river to code mapping
def load_river_menu(fpath=r'./nsw_water_mapping.json'):
    # create river map from json if a particular river is of interest
    with open(fpath,'r') as rf:
        menu=json.load(rf)
        return menu


# =============================================================================
# define url generator function
def generate_url(mode):
    # load river menu
    if params['river'].lower() != 'all':
        menu=load_river_menu()
        which=menu[params['river'].lower()]
    else:
        which = ''
        
    # can choose from allocation/share/transfer
    
    if mode=='allocation':
        logger.info(f"Now downloading allocation trading row {params['row_start']} to row {params['row_end']} for period {params['startDate']} to {params['endDate']} for {params['river']}")
        url=f"https://waterregister.waternsw.com.au/AllocationResult?pageCommand=export&resultType=exel&fromRow={params['row_start']}&toRow={params['row_end']}&pageCommand=search&resultType=modern&startDate={params['startDate']}&endDate={params['endDate']}&src={which}&cat=&"
    elif mode=='share':
        logger.info(f"Now downloading share trading row {params['row_start']} to row {params['row_end']} for period {params['startDate']} to {params['endDate']} for {params['river']}")
        url=f"https://waterregister.waternsw.com.au/WaterShareIntraWSResult?pageCommand=export&resultType=exel&fromRow={params['row_start']}&toRow={params['row_end']}&pageCommand=search&resultType=modern&period={params['startDate']}%20to%20{params['endDate']}&cat=&"
    elif mode=='transfer':
        logger.info(f"Now downloading share transfer row {params['row_start']} to row {params['row_end']} for period {params['startDate']} to {params['endDate']} for {params['river']}")
        url=f"https://waterregister.waternsw.com.au/WaterShareTransferResult?pageCommand=export&resultType=exel&fromRow={params['row_start']}&toRow={params['row_end']}&pageCommand=search&resultType=modern&transferType=&period={params['startDate']}%20to%20{params['endDate']}&src={which}&cat=&"

    return url


# =============================================================================
# define worker function
def get_byte_data(url,headers):
    # make requests
    response=requests.get(url,headers,verify=False)
    response.raise_for_status()
    # initialize byteIO
    f=BytesIO()
    # write to byteIO
    for chunk in response.iter_content(chunk_size=1024):
        f.write(chunk)
    # reset seeker
    f.seek(0)
    return f



# =============================================================================
# def dump df function
def dump_df(df,fname):
    fname=Path(__file__).resolve().parent / (fname + '.xlsx')
    df.to_excel(fname,header=True,index=False)
    logger.info(f"Written to {fname} successfully.")


# =============================================================================
# define get_data function
def get_data(params):
     # run loops to call worker function and then append to df until XLRDError detected
    keep_running=True
    df=pd.DataFrame()
    increment=500 if params['mode']=='allocation' else 200
    header_row=0 if params['mode']=='transfer' else 1

    # save original start date
    # raw_start=params['row_start']
    # loop thru all rows til XLRDError detected
    while keep_running:
        url=generate_url(params['mode'])
        # call worker function
        data=get_byte_data(url,headers)
        try:
            # if not error, download df, append df, increment row range
            new_df=pd.read_excel(data,header=header_row)
            df=pd.concat([df, new_df],ignore_index=True,axis=0)
            logger.info(f"Row {params['row_start']} to row {params['row_end']} for period {params['startDate']} to {params['endDate']} for {params['river']} successfully appended!")
            params['row_start']=params['row_end']+1
            # record current end date
            # raw_end=params['row_end']
            params['row_end']+=increment
        except XLRDError:
            # if XLRDError, end download, return df
            logger.error(f"Row {params['row_start']} to row {params['row_end']} for period {params['startDate']} to {params['endDate']} for {params['river']} returned unreadable data, reached end of the file, download terminated...")
            fname=f"{params['river']}_{fname_mapping[params['mode']]}_{params['startDate']}_to_{params['endDate']}"
            logger.info(f"Now writing {len(df)} rows to excel...")
            return df


# =============================================================================
# define main function
def main(params):
    # run loops to call worker function and then append to df until XLRDError detected
    keep_running=True
    df=pd.DataFrame()
    increment=500 if params['mode']=='allocation' else 200
    header_row=0 if params['mode']=='transfer' else 1

    # save original start date
    # raw_start=params['row_start']
    # loop thru all rows til XLRDError detected
    while keep_running:
        url=generate_url(params['mode'])
        # call worker function
        data=get_byte_data(url,headers)
        try:
            # if not error, download df, append df, increment row range
            new_df=pd.read_excel(data,header=header_row)
            df=pd.concat([df, new_df],ignore_index=True,axis=0)
            logger.info(f"Row {params['row_start']} to row {params['row_end']} for period {params['startDate']} to {params['endDate']} for {params['river']} successfully appended!")
            params['row_start']=params['row_end']+1
            # record current end date
            # raw_end=params['row_end']
            params['row_end']+=increment
        except XLRDError:
            # if XLRDError, end download, return df
            logger.error(f"Row {params['row_start']} to row {params['row_end']} for period {params['startDate']} to {params['endDate']} for {params['river']} returned unreadable data, reached end of the file, download terminated...")
            fname=f"{params['river']}_{fname_mapping[params['mode']]}_{params['startDate']}_to_{params['endDate']}"
            logger.info(f"Now writing {len(df)} rows to excel...")
            dump_df(df,fname)
            return None



# entry point
if __name__=='__main__':
    
    # =============================== Control Panel =============================== #
    # user defined parameters, change parameter here
    params={'mode':'transfer',   # can choose from allocation/share/transfer
            'row_start':0,
            'row_end':999,
            'startDate':'15-APR-2023',
            'endDate':'24-APR-2023',
            'river':'all'}
    # df=get_data(params)
    main(params)
    # print(df)

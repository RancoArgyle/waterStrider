import requests, sys, logging
from io import BytesIO
import pandas as pd
from pathlib import Path


# ================================ set logger =================================
logger=logging.getLogger('vic_scraper')
logger.setLevel(logging.INFO)
handler=logging.StreamHandler()
formatter=logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]: %(message)s',datefmt=r'%Y-%m-%d %H:%M:%S')
# add formatter to handler
handler.setFormatter(formatter)
# add handler to logger
logger.addHandler(handler)
logger.info('Victoria water strider start crawling...')
# =============================================================================
# define worker function
def get_file_info(url):

    headers={'win32':{},
            'linux':{
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "accept":"application/json, text/javascript, */*; q=0.01",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            }}

    data={'win32':{},
        'linux':{
            "option": "com_waterregister_reports",
            "task": "report.view",
            "type": "BR04",
            "inputRegion[]": ["Northern","Southern","Western","all"],  # manully combined individual item into a list
            "inputYear[]": "2023"
        }}


    platform=sys.platform

    res=requests.post(url,headers=headers[platform],data=data[platform])
    res.raise_for_status()
    res=res.json()
    file_name=res['csv_name']
    file_path=res['csv_file']
    logger.info(f"file info retrieved. filename: {file_name}")

    return file_name, file_path


def get_csv_response(file_name):
    url=f"https://waterregister.vic.gov.au"
    headers={'win32':{},
            'linux':{
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            }}

    params={'win32':{
            "option": "com_waterregister_reports",
            "task": "download",
            "file": file_name},
        'linux':{
            "option": "com_waterregister_reports",
            "task": "download",
            "file": file_name
        }}

    platform=sys.platform
    res=requests.get(url,headers=headers[platform],params=params[platform])
    res.raise_for_status()
    logger.info(f'Response for {file_name} has been successfully retrieved')
    return res


def parse_response(response,fname='vic_alloc_trade.csv'):
    fpath=Path(__file__).parent / fname
    with open(fpath,'w') as wf:
        wf.write(response.text)
    with open(fpath) as rf:
        # truncate meta date from both end of the file
        contents=rf.readlines()[5:-9]
        with open(fpath,'w') as wf:
            # row ends with ,\n, replaced with only \n
            # otherwise an extra empty column in the end
            wf.writelines(list(map(lambda row:row.replace(',\n','\n'),contents)))
    df=pd.read_csv(fpath,header=0)
    logger.info("csv parsed by pandas successfully!")
    return df


def main():
    url=r'https://www.waterregister.vic.gov.au'
    file_name, _ =get_file_info(url=url)
    response=get_csv_response(file_name)
    df=parse_response(response)
    return df

if __name__=='__main__':
    df=main()
    print(df)
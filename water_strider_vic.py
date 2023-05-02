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

    headers={'win32':{
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "accept":"application/json, text/javascript, */*; q=0.01",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    },
            'linux':{
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "accept":"application/json, text/javascript, */*; q=0.01",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            }}

    data={
            "option": "com_waterregister_reports",
            "task": "report.view",
            "type": "BR04",
            "inputRegion[]": ["Northern","Southern","Western","all"],  # manully combined individual item into a list
            "inputYear[]": "2023"}


    platform=sys.platform

    res=requests.post(url,headers=headers[platform],data=data)
    res.raise_for_status()
    res=res.json()
    file_name=res['csv_name']
    file_path=res['csv_file']
    logger.info(f"file info retrieved. filename: {file_name}")

    return file_name, file_path


def get_csv_response(file_name):
    url=f"https://waterregister.vic.gov.au"
    headers={'win32':{
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    },
            'linux':{
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            }}

    params={
            "option": "com_waterregister_reports",
            "task": "download",
            "file": file_name}

    platform=sys.platform
    res=requests.get(url,headers=headers[platform],params=params)
    res.raise_for_status()
    logger.info(f'Response for {file_name} has been successfully retrieved')
    return res


def parse_response(response,fname='vic_alloc.csv'):
    fpath=Path(__file__).resolve().parent / fname
    with open(fpath,'w') as wf:
        for line in response.text.split('\n')[5:-9]:
            wf.write(line.replace(',\r','')+'\n')
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
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO


url="https://apps.waterconnect.sa.gov.au/wtr/Prescribed.aspx"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
}


# =============================================================================
# define worker function
def get_byte_data(url,headers,data,cookies):
    # make requests
    response=requests.post(url,headers=headers,data=data,cookies=cookies)
    response.raise_for_status()
    # initialize byteIO
    f=BytesIO()
    # write to byteIO
    for chunk in response.iter_content(chunk_size=1024):
        f.write(chunk)
    # reset seeker
    f.seek(0)
    return f

def get_sa_entitlement_trade(mode='Temporary'):
    
    if mode=='Temporary':
        viewstate_path=r'C:\Users\RancoXu\OneDrive - Argyle Capital Partners Pty Ltd\Desktop\Ranco\Python\water_data_scraper\VIEWSTATE_et_temp.txt'
        with open(viewstate_path,'r') as rf:
            viewstate=rf.read()
        # from chomre - F12 - Network - Prescribed.aspx - Payload - Form Data
        data = {
        "DefaultScriptManager1_TSM": ";;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b;;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b",
        "ctl00$ContentPlaceHolder1$ddlAllocationYear": '2023',
        "ctl00$ContentPlaceHolder1$ddlFromState": 'ALL',
        "ctl00$ContentPlaceHolder1$ddlToState": 'ALL',
        "ctl00$ContentPlaceHolder1$rgYTDSA$ctl00$ctl03$ctl02$PageSizeComboBox": '50',
        "ctl00_ContentPlaceHolder1_rgYTDSA_ctl00_ctl03_ctl02_PageSizeComboBox_ClientState": '',
        "ctl00$ContentPlaceHolder1$ddlEntitlementYear": "2023",
        "ctl00$ContentPlaceHolder1$rblEntitlement": "Temporary",
        "__EVENTTARGET": 'ctl00$ContentPlaceHolder1$rgENT$ctl00$ctl03$ctl01$exCSV',
        "__EVENTARGUMENT": '',
        "__LASTFOCUS": '',
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": "C7B91F77",
        "__EVENTVALIDATION": "bbh1R0WDcWGE51LBYj23kW662w1562hsBUCWBkEjLB6h0Y99KSWOhjxRwIuPsml6wTpGIlCitBbt/zdjqGk1DuUZrTIG8ANRwSM75shfOjuMZIOVtrV/pP4pOSiFvt3rKA2jHsfh6INzllGOHUen8yUoH4bb6GtUjoOBpfgzeU92lzuLnurrw4ejqu+fmvj3c17wV0vDFLNxCF8qo14ggXiXAbBVGko1GPnPtsU+ghYsfnpM//hfx2+u70sPQHCtmEbUP7DqlS0ipR1eiHg3K4+OOA8I96y6Eg6/+/HOTw1/nT6LINsdPUlYwht+FxUvRk1kPdo58UDBkTDDidz/UOh671lKLBUjgq63QTPQERa2LHnzij26QxD3W/Q4fn+BRymD3OcSzf952JPCy6jz81NWldFzwZTxvLjoRyfH++6fdW8bHXNRL7cTsrUyndqvcSYf09bHLlh91SCGwEBWeR4pwAp2SAVJkg+Biy7c7WGSsrFoZ5I5Y/B3IP+WDineARobYN5cZ2vfwPnqteoWgkYS3gW2G0tqUU5jNJihb01NoTOcz0paXjX04wTG0wXPnQ0TEJrjYa0ZnBisYEOuuLQdjZ8rKFfnKHBDk+63w1Oi4Fx+l/GKrCMC5AsDRugW+D05RRb3Z3a2gJRNwmVvZsmctiUqNNxcuiq2OPUQif67iLswVOL+Ep8CMCbwuNYRtzgJmXbeK12bsVTAdE3bFx1uRe9cCI01oeW08tCYknGlVvieNL81dXkioCKiXnsEpPLaGuWY02PW0anXLNCJhpiEajQmrGaZz3Ywm8wfvapqO7Md9MGwsYjJb1yqrKJUXyZ++iUjscrJf0qsccOoHgJ4eBgS+S6GTAL+kC+tMhfQiE1dZGwEknZMZ/+C4gDUkKsmEGdFMHRed/1r/2zcUj/o21KPbVXlfqgGsthBzyufltm4/eBkNMUi2j6xDNf+qDD9NalM3Ow9Qd7sCQ5ZCmYRmYPEOFeUsRE35A8sM9tuAXTkWZBowPk7N3TePA6nwdIhyP0tvFgb6KHh4NaLc6bfvI2tU05fvhK7QgiGZ4rfHzaJvHZNncyyVUHFA7FHHeq0zWXlCE1cEH8y6Y9Ta8hk1lRx/4tWvAYvl4R39TXcy9Fz65RrCMrQJ6KEg8Mog1J316Kk50tW/NrbA7xU0gV05H+vNn+yhueH51bxvOo8mZAVDpKocnmaxBxiJLoWkPO4zpe1YNh+FVFhNsln+l5x3+VGEQ8bzE3dzda5zn6zoD+RYNM87hMySySLQzTwzxigb+JMoqIcjKz4fu1xPUFiMuJpoPsxJDma0N+2Ph1SKKAh+b3o06ai07+Yy02KyZh5lL0isNL7f5hRVW8xnsfNauozxJWxlI9RD0dN3nza09gRdOqyTcDlt0Ne29JLEsxjWHP40qTfEKb3rqGhGiva/zsjBqu0it7jLdFvHb1HWAHa0ka3bm1X/dq0zZTpErd2PwEv++xIY/SIjMvlBmwZ/5U43UUII7I/K3MkoxUn07GkRjSiRmO0oxdgFyly8ZFuzxlAn8v6KaaVGJMee27v3RlcYSDqgoYAueAUT0viIgCihy+dDK+giZBXct5LcobXHCnxcUAXbN+crr26mGCh4Y0y5UOuEeln8Hb7jn3VfsMw/lxqbh7ut1dZHHczZcC7Ms+KLu9TToWYZ3ONNrHCt60t+KDQS9JCt3WY4krZxVdmX56YZO1bbymA4leV1+Mmg9Nq25C1K4PwI0OyyI9Kt1wDpGOAWOncqWyHSPkhEVgWDaYcwYRYIJqcmLqtjpnM18nE+AtmgsARdgb2C1hnex/x+zGBsxytVzwNnRSQ8GEsgSA/O1WZCzeDFO4BT9uAqPG/BSK2j91KB83mdQ=="
        }

        # from chomre - F12 - Network - Prescribed.aspx - Cookies
        cookies={'ASP.NET_SessionId':'ct52zzrs2voqfmgvmkdnrzdc', 
                '_gid':'GA1.4.1909174387.1682567412', 
                '_ga':'GA1.4.1560349057.1681796908',
                '_ga_30SQYKN4W6':'GS1.1.1682573785.7.0.1682574357.0.0.0'}
    elif mode=='Permanent':
        viewstate_path=r'C:\Users\RancoXu\OneDrive - Argyle Capital Partners Pty Ltd\Desktop\Ranco\Python\water_data_scraper\VIEWSTATE_et_perm.txt'
        with open(viewstate_path,'r') as rf:
            viewstate=rf.read()
        # from chomre - F12 - Network - Prescribed.aspx - Payload - Form Data
        data = {
        "DefaultScriptManager1_TSM": ";;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b;;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b",
        "ctl00$ContentPlaceHolder1$ddlAllocationYear": '2023',
        "ctl00$ContentPlaceHolder1$ddlFromState": 'ALL',
        "ctl00$ContentPlaceHolder1$ddlToState": 'ALL',
        "ctl00$ContentPlaceHolder1$rgYTDSA$ctl00$ctl03$ctl02$PageSizeComboBox": '50',
        "ctl00_ContentPlaceHolder1_rgYTDSA_ctl00_ctl03_ctl02_PageSizeComboBox_ClientState": '',
        "ctl00$ContentPlaceHolder1$ddlEntitlementYear": "2023",
        "ctl00$ContentPlaceHolder1$rblEntitlement": "Permanent",
        "ctl00$ContentPlaceHolder1$rgENT$ctl00$ctl03$ctl02$PageSizeComboBox": "50",
        "__EVENTTARGET": 'ctl00$ContentPlaceHolder1$rgENT$ctl00$ctl03$ctl01$exCSV',
        "__EVENTARGUMENT": '',
        "__LASTFOCUS": '',
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": "C7B91F77",
        "__EVENTVALIDATION": "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"
        }

        # from chomre - F12 - Network - Prescribed.aspx - Cookies
        cookies={'ASP.NET_SessionId':'ct52zzrs2voqfmgvmkdnrzdc', 
                '_gid':'GA1.4.1909174387.1682567412', 
                '_ga':'GA1.4.1560349057.1681796908',
                '_ga_30SQYKN4W6':'GS1.1.1682573785.7.0.1682574357.0.0.0'}
    

    data = get_byte_data(url, headers=headers, data=data,cookies=cookies)
    df=pd.read_csv(data,header=0)
    return df

if __name__=='__main__':
    print(get_sa_entitlement_trade('Temporary'))

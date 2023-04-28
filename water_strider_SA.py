import requests, sys, json
import pandas as pd
from io import BytesIO
from pathlib import Path


BASE_DIR=Path(__file__).parent

url="https://apps.waterconnect.sa.gov.au/wtr/Prescribed.aspx"

headers={
    'win32':{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
},
    'linux':{
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}
}
with open(BASE_DIR / 'SA_VIEWSTATE.json','r') as rf:
    viewstate=json.load(rf)

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
    
    if mode.lower()=='temporary':
        # from chomre - F12 - Network - Prescribed.aspx - Payload - Form Data
        data = {'win32':{
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
        "__VIEWSTATE": viewstate['VIEWSTATE_et_temp'],
        "__VIEWSTATEGENERATOR": "C7B91F77",
        "__EVENTVALIDATION": "bbh1R0WDcWGE51LBYj23kW662w1562hsBUCWBkEjLB6h0Y99KSWOhjxRwIuPsml6wTpGIlCitBbt/zdjqGk1DuUZrTIG8ANRwSM75shfOjuMZIOVtrV/pP4pOSiFvt3rKA2jHsfh6INzllGOHUen8yUoH4bb6GtUjoOBpfgzeU92lzuLnurrw4ejqu+fmvj3c17wV0vDFLNxCF8qo14ggXiXAbBVGko1GPnPtsU+ghYsfnpM//hfx2+u70sPQHCtmEbUP7DqlS0ipR1eiHg3K4+OOA8I96y6Eg6/+/HOTw1/nT6LINsdPUlYwht+FxUvRk1kPdo58UDBkTDDidz/UOh671lKLBUjgq63QTPQERa2LHnzij26QxD3W/Q4fn+BRymD3OcSzf952JPCy6jz81NWldFzwZTxvLjoRyfH++6fdW8bHXNRL7cTsrUyndqvcSYf09bHLlh91SCGwEBWeR4pwAp2SAVJkg+Biy7c7WGSsrFoZ5I5Y/B3IP+WDineARobYN5cZ2vfwPnqteoWgkYS3gW2G0tqUU5jNJihb01NoTOcz0paXjX04wTG0wXPnQ0TEJrjYa0ZnBisYEOuuLQdjZ8rKFfnKHBDk+63w1Oi4Fx+l/GKrCMC5AsDRugW+D05RRb3Z3a2gJRNwmVvZsmctiUqNNxcuiq2OPUQif67iLswVOL+Ep8CMCbwuNYRtzgJmXbeK12bsVTAdE3bFx1uRe9cCI01oeW08tCYknGlVvieNL81dXkioCKiXnsEpPLaGuWY02PW0anXLNCJhpiEajQmrGaZz3Ywm8wfvapqO7Md9MGwsYjJb1yqrKJUXyZ++iUjscrJf0qsccOoHgJ4eBgS+S6GTAL+kC+tMhfQiE1dZGwEknZMZ/+C4gDUkKsmEGdFMHRed/1r/2zcUj/o21KPbVXlfqgGsthBzyufltm4/eBkNMUi2j6xDNf+qDD9NalM3Ow9Qd7sCQ5ZCmYRmYPEOFeUsRE35A8sM9tuAXTkWZBowPk7N3TePA6nwdIhyP0tvFgb6KHh4NaLc6bfvI2tU05fvhK7QgiGZ4rfHzaJvHZNncyyVUHFA7FHHeq0zWXlCE1cEH8y6Y9Ta8hk1lRx/4tWvAYvl4R39TXcy9Fz65RrCMrQJ6KEg8Mog1J316Kk50tW/NrbA7xU0gV05H+vNn+yhueH51bxvOo8mZAVDpKocnmaxBxiJLoWkPO4zpe1YNh+FVFhNsln+l5x3+VGEQ8bzE3dzda5zn6zoD+RYNM87hMySySLQzTwzxigb+JMoqIcjKz4fu1xPUFiMuJpoPsxJDma0N+2Ph1SKKAh+b3o06ai07+Yy02KyZh5lL0isNL7f5hRVW8xnsfNauozxJWxlI9RD0dN3nza09gRdOqyTcDlt0Ne29JLEsxjWHP40qTfEKb3rqGhGiva/zsjBqu0it7jLdFvHb1HWAHa0ka3bm1X/dq0zZTpErd2PwEv++xIY/SIjMvlBmwZ/5U43UUII7I/K3MkoxUn07GkRjSiRmO0oxdgFyly8ZFuzxlAn8v6KaaVGJMee27v3RlcYSDqgoYAueAUT0viIgCihy+dDK+giZBXct5LcobXHCnxcUAXbN+crr26mGCh4Y0y5UOuEeln8Hb7jn3VfsMw/lxqbh7ut1dZHHczZcC7Ms+KLu9TToWYZ3ONNrHCt60t+KDQS9JCt3WY4krZxVdmX56YZO1bbymA4leV1+Mmg9Nq25C1K4PwI0OyyI9Kt1wDpGOAWOncqWyHSPkhEVgWDaYcwYRYIJqcmLqtjpnM18nE+AtmgsARdgb2C1hnex/x+zGBsxytVzwNnRSQ8GEsgSA/O1WZCzeDFO4BT9uAqPG/BSK2j91KB83mdQ=="
        },
        'linux':{
        'DefaultScriptManager1_TSM':";;System.Web.Extensions,+Version=4.0.0.0,+Culture=neutral,+PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI,+Version=2020.3.1021.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b;;Telerik.Web.UI,+Version=2020.3.1021.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b",
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
        "__VIEWSTATE": viewstate['VIEWSTATE_et_temp_linux'],
        "__VIEWSTATEGENERATOR": "C7B91F77",
        "__EVENTVALIDATION":"T/2/5ef0xNAYHmgsmj8lIS9fDk4H7anidGQ6Ip33VZqiOMpudNOd3rSlllaLLcjpgHc8cX6qz6r37xwSvp44cxhpIlv9BjOIgPvibv0l8V4Vf9E2u7aVuKGi5D5+Cf3WH1ET3ZgbgNWJlff6xiNX9KD/7xc9fKNoH3rdhbe8uRjrDi1zFhKqyrzqn6zTOGXaZ7Yk6G8olq4MfLkL7QO0hebXVUvLmo7K2u2vEJUndfbD1LHl5zLmSpy2q3P2vhou3AfrProuDcpMxx5DnK89JRoEIcs8AC92jPAWFonOVdbYww6DdCywMwqz9dchZurGCrpzYnnLmy8yHjS/TLMvIE0Y51dxSpVKWk608Xv0iPWtUJdYUUSBNfHODYwu1YqaIhsbWTnLRnC6lSmFSVpvyPARbGrJ+KDHXUUXLA3cvaNRd4Hvgl7XtbFqWp3XeNX0wjXjpFOa5xjK9SUcsH1Hc+s4JHN5EafzfSW2Hd+i1gXabB3563JTW+Rd1wFoyxIdi7dVvlsv0W91UJJvBY99Iir4UHMwHIjFcTQHIiN/mgB4xZMLsnKL8couGWQ+P21rgxodIzGUPfCky5VJR1vbilWI7tQqOgAhWhWx2qX+1MDBA/mMFi6qCXfEgI9zB4o6sV072V3LcF5yKwOT+wEUY37UNCkNXMBevnDyQO9ezZqKKOaNu+adCwV3C5CStUlj+9Eo0IOMFUjkYD7uZojxFS++6soAQg32uWsBMYWJ03QVc4xSwLlMijnsee9IT5Jbb74PAct068N2vWGlIq7SylWEAcZHmcY7EPeb4zJxnoOrV791RNupxuZHH9puTeiSFjWjrMBq0BIgu1/7L6P/kRWM2JJU8PyXk9uP70+Ydn3Qf8vEA4vydnJ95L96kWS+5mXYbNKuZDYGxqjumeOGQPmg7rDvNg4hUNiuSRFlLmXybV/k6kAT/0hQVxlvCo41pbk83lJA0NpAtFGx1/van5fgblZUBQQAaMk1hKQhiCMSn6ecp54M346zAe9OxC13itTnnJaZay3yKThul4DrPFURkojotgaZz683/D203plVvqC8gZWgGKk2o1DWnkZfroRgZNDy2OmfbHeDrQPJRM4gY7VtmLsxQlalDbzZkIwA8BE+/6AZpGRULWcPM4uLRDZ7HdtB+NMigqjJotpr9oaVRxcycL2d2M7swNwedZiYszIyYtY8ksW0VOggwXb1cfr2t+QssgLR7ZuIusoSOgF5jYMEmVW9cAynBwRRWDpDXKBJTcQivBI/3VnPgPH+sL4jXDBE2sY+ubRgYombyKqCSnKE0dA8BFF6GVOp4WOzhF3iFSTIga3nxx4n6gha/nnrNdGm5R4jsdLR/cb1uv1rBboLAWF4kgUheuJ2ANBm21UQqqhkPyBwfT73K+Y3xOBOvTJ26Ir2NYBOGEbMSIjvIn3JRlPC+bG4gAxBksZP755fTk/qTx8LGTZhnxbjI7Ul89Sd+uIfypMHntLENiFa2Gs38GOxKoGYuTNES7J156lyNPHUS9FzM/QCQXhRTmXB+zWJXYUwTF7BkAaczOfDgaT9kWdKHeHUV+LtJNJU/zpESZtDq842zjRV+oWjWjvbaegKOZiIQk4xQgl6aIJcdnTtx+ll6UXqc6b50wNC25ax1Vg8FDViF7ODV7hNxZVzmhPiqrVPrjO4QAQZ9wiBbDaFR0E2yVYPkOpOaB54gVJ3lvAU22MHuqujqD9ToUT2Xkj5oteJfK8BnyrYCe0f/BZr8fLcomhn2s2ReW8Y931AOCAaxwldmYseMqK3DzMU211zTCnSgRCO1PngDyJ5EtPs44PptC06hSnj1QXJ3hhCCDTCNl0ol1tqXNp/7U/DYPY/UOIpsBTFy+mulQ=="
        }
        }

        # from chomre - F12 - Network - Prescribed.aspx - Cookies
        cookies={'win32':{'ASP.NET_SessionId':'ct52zzrs2voqfmgvmkdnrzdc', 
                        '_gid':'GA1.4.1909174387.1682567412', 
                        '_ga':'GA1.4.1560349057.1681796908',
                        '_ga_30SQYKN4W6':'GS1.1.1682573785.7.0.1682574357.0.0.0'},
                'linux':{'ASP.NET_SessionId':'mwhjgdexy4kyxtusjnu0kacd', 
                        '_gid':'GA1.4.2120303896.1682637464', 
                        '_ga':'GA1.4.463289802.1682170590',
                        '_ga_30SQYKN4W6':'GS1.1.1682637463.2.1.1682637699.0.0.0'}
                }
        
    elif mode.lower()=='permanent':
        # from chomre - F12 - Network - Prescribed.aspx - Payload - Form Data
        data = {
            'win32':{
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
                    "__VIEWSTATE": viewstate['VIEWSTATE_et_perm'],
                    "__VIEWSTATEGENERATOR": "C7B91F77",
                    "__EVENTVALIDATION": "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"
        },
            'linux':{
                    "DefaultScriptManager1_TSM": ";;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:ed16cbdc:f7645509:88144a7a:24ee1bba:2003d0b8:f46195d3:33715776:1e771326:e524c98b;;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b;",
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
                    "__VIEWSTATE": viewstate['VIEWSTATE_et_perm_linux'],
                    "__VIEWSTATEGENERATOR": "C7B91F77",
                    "__EVENTVALIDATION": "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"
        }
        }
        # from chomre - F12 - Network - Prescribed.aspx - Cookies
        cookies={'win32':{
                        'ASP.NET_SessionId':'ct52zzrs2voqfmgvmkdnrzdc', 
                        '_gid':'GA1.4.1909174387.1682567412', 
                        '_ga':'GA1.4.1560349057.1681796908',
                        '_ga_30SQYKN4W6':'GS1.1.1682573785.7.0.1682574357.0.0.0'},
                'linux':{
                        'ASP.NET_SessionId':'mwhjgdexy4kyxtusjnu0kacd', 
                        '_gid':'GA1.4.2120303896.1682637464', 
                        '_ga':'GA1.1.463289802.1682170590',
                        '_ga_30SQYKN4W6':'GS1.1.1682637463.2.1.1682639666.0.0.0'}
        }

    platform=sys.platform
    data = get_byte_data(url, headers=headers[platform], data=data[platform],cookies=cookies[platform])
    df=pd.read_csv(data,header=0)
    return df


def get_sa_allocation_trade():

    # from chomre - F12 - Network - Prescribed.aspx - Payload - Form Data
    data = {'linux':{
    "DefaultScriptManager1_TSM": ";;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b;;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b",
    "ctl00$ContentPlaceHolder1$ddlAllocationYear": '2023',
    "ctl00$ContentPlaceHolder1$ddlFromState": 'ALL',
    "ctl00$ContentPlaceHolder1$ddlToState": 'ALL',
    "ctl00$ContentPlaceHolder1$rgYTDSA$ctl00$ctl03$ctl02$PageSizeComboBox": '50',
    "ctl00_ContentPlaceHolder1_rgYTDSA_ctl00_ctl03_ctl02_PageSizeComboBox_ClientState": '',
    "ctl00$ContentPlaceHolder1$ddlEntitlementYear": "2023",
    "ctl00$ContentPlaceHolder1$rblEntitlement": "Temporary",
    "__EVENTTARGET": 'ctl00$ContentPlaceHolder1$rgYTDSA$ctl00$ctl03$ctl01$exCSV',
    "__EVENTARGUMENT": '',
    "__LASTFOCUS": '',
    "__VIEWSTATE": viewstate['VIEWSTATE_at_linux'],
    "__VIEWSTATEGENERATOR": "C7B91F77",
    "__EVENTVALIDATION": "T/2/5ef0xNAYHmgsmj8lIS9fDk4H7anidGQ6Ip33VZqiOMpudNOd3rSlllaLLcjpgHc8cX6qz6r37xwSvp44cxhpIlv9BjOIgPvibv0l8V4Vf9E2u7aVuKGi5D5+Cf3WH1ET3ZgbgNWJlff6xiNX9KD/7xc9fKNoH3rdhbe8uRjrDi1zFhKqyrzqn6zTOGXaZ7Yk6G8olq4MfLkL7QO0hebXVUvLmo7K2u2vEJUndfbD1LHl5zLmSpy2q3P2vhou3AfrProuDcpMxx5DnK89JRoEIcs8AC92jPAWFonOVdbYww6DdCywMwqz9dchZurGCrpzYnnLmy8yHjS/TLMvIE0Y51dxSpVKWk608Xv0iPWtUJdYUUSBNfHODYwu1YqaIhsbWTnLRnC6lSmFSVpvyPARbGrJ+KDHXUUXLA3cvaNRd4Hvgl7XtbFqWp3XeNX0wjXjpFOa5xjK9SUcsH1Hc+s4JHN5EafzfSW2Hd+i1gXabB3563JTW+Rd1wFoyxIdi7dVvlsv0W91UJJvBY99Iir4UHMwHIjFcTQHIiN/mgB4xZMLsnKL8couGWQ+P21rgxodIzGUPfCky5VJR1vbilWI7tQqOgAhWhWx2qX+1MDBA/mMFi6qCXfEgI9zB4o6sV072V3LcF5yKwOT+wEUY37UNCkNXMBevnDyQO9ezZqKKOaNu+adCwV3C5CStUlj+9Eo0IOMFUjkYD7uZojxFS++6soAQg32uWsBMYWJ03QVc4xSwLlMijnsee9IT5Jbb74PAct068N2vWGlIq7SylWEAcZHmcY7EPeb4zJxnoOrV791RNupxuZHH9puTeiSFjWjrMBq0BIgu1/7L6P/kRWM2JJU8PyXk9uP70+Ydn3Qf8vEA4vydnJ95L96kWS+5mXYbNKuZDYGxqjumeOGQPmg7rDvNg4hUNiuSRFlLmXybV/k6kAT/0hQVxlvCo41pbk83lJA0NpAtFGx1/van5fgblZUBQQAaMk1hKQhiCMSn6ecp54M346zAe9OxC13itTnnJaZay3yKThul4DrPFURkojotgaZz683/D203plVvqC8gZWgGKk2o1DWnkZfroRgZNDy2OmfbHeDrQPJRM4gY7VtmLsxQlalDbzZkIwA8BE+/6AZpGRULWcPM4uLRDZ7HdtB+NMigqjJotpr9oaVRxcycL2d2M7swNwedZiYszIyYtY8ksW0VOggwXb1cfr2t+QssgLR7ZuIusoSOgF5jYMEmVW9cAynBwRRWDpDXKBJTcQivBI/3VnPgPH+sL4jXDBE2sY+ubRgYombyKqCSnKE0dA8BFF6GVOp4WOzhF3iFSTIga3nxx4n6gha/nnrNdGm5R4jsdLR/cb1uv1rBboLAWF4kgUheuJ2ANBm21UQqqhkPyBwfT73K+Y3xOBOvTJ26Ir2NYBOGEbMSIjvIn3JRlPC+bG4gAxBksZP755fTk/qTx8LGTZhnxbjI7Ul89Sd+uIfypMHntLENiFa2Gs38GOxKoGYuTNES7J156lyNPHUS9FzM/QCQXhRTmXB+zWJXYUwTF7BkAaczOfDgaT9kWdKHeHUV+LtJNJU/zpESZtDq842zjRV+oWjWjvbaegKOZiIQk4xQgl6aIJcdnTtx+ll6UXqc6b50wNC25ax1Vg8FDViF7ODV7hNxZVzmhPiqrVPrjO4QAQZ9wiBbDaFR0E2yVYPkOpOaB54gVJ3lvAU22MHuqujqD9ToUT2Xkj5oteJfK8BnyrYCe0f/BZr8fLcomhn2s2ReW8Y931AOCAaxwldmYseMqK3DzMU211zTCnSgRCO1PngDyJ5EtPs44PptC06hSnj1QXJ3hhCCDTCNl0ol1tqXNp/7U/DYPY/UOIpsBTFy+mulQ=="
    },
    'win32':{
    'DefaultScriptManager1_TSM':";;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:ed16cbdc:f7645509:88144a7a:24ee1bba:2003d0b8:f46195d3:33715776:1e771326:e524c98b;;Telerik.Web.UI, Version=2020.3.1021.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:58366029:c128760b:aa288e2d:258f1c72;",
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
    "__VIEWSTATE": viewstate['VIEWSTATE_at'],
    "__VIEWSTATEGENERATOR": "C7B91F77",
    "__EVENTVALIDATION":"YBmJ3Ncenxolz4JsOLANP9QozpOjwXoStzvjztOcg5GUL8n/ryen0q5uuvQgzmazVkBWURJQrISs32yPAbiZUOEUGj59D06U85ABsDSo7Hy1rCJF86OgvOzQtsguRY7dzJLzzW/31zCGPMpuekPzLdwNimSyXlvCBmy2Z+eYvqVCtzXagvwaMmYcjfqQvmbglLk+h8L3mqh8uqvQNFjzoLh+Xh3iDjvcwcEpakGvO76PEFBN4qtObJXJMQZqwfuLmrMYdm6Hu/hOgfHfiDRgwFSQZa63hgf8LXYUI74m4VZvnT/ppbNe+Vkr9rOFKjEt5+CK6p30eOPFC/2QrHDJeKTqjBv4ZLqtxjQ/ZwCEnBhGzYPFtpDx2mDqgkjeSIR+IA6c8bLGaUOFHbIeqgyYmSudiz+l4KibNenbJcpkrEzsVTCYT70rzZOWsgI1bPNFqmcGyqIcExEn08ONOxu4/aF+wxNkBQ9gmbyqvGLp48qytAUfd7JDm8Og3kd+PffEZN7EToyYWXbZ/7D28EwxTC2yf5eVwiei3+Z1b0ysweVwgeV5+Vf74L8Wg4mbDEzjjhpu22mUJzkP+174Z7jYa3t+WmtLCfyi0WvgKyo6Npn4UedhfIQGvY/40In/I1+F4uTNVPC4PKutPMSdanmmrE6HkmUlDZ1KA3ljpj+b+OwG58wNlmRNW1WqrhkMqSACLYCeiMvv9RdbKN77h4GpudFgvka5Pm3hFgZFJjbvhQ++JPS0Y8mQ5SipC+qTBR4J+SOqObRMAKA04TdGDwlatxkRMyM/ByWXlLWmCiNEwqP9KXCJQKQd8g8yJOEowTWPywKdZ2UmQFpkSPZxK/Sx+Ay7aulyejsP5au4uZ5dR5PUj/psl/VfNA3YY/NHsXd+ZTt5E57Hfk75f3KD0/lmLfbPWz7tREhEK/kHfCoKNCuId355IdGARpENnD4vsiJdI5EqebN33nLXPCciZzrYUWvl0HfDJudEZFExHsKL6f9pNAxy3Asul5SbiE3zK04d1qdcNFYF/duZyKC/fr5gDPSZG5+DlgfttY3DmvfGLa/AECozPAS8+iFrnpW3jQEap552csvOLGqk1fS8DujVkh0m70E8pMeyZ2AV75nRjqP4hXqHwf85ODPMPF+ul2nGJBQvGGk/f4nVly/JJ5p34D0AB3FwNcY+COgJ+RZFnizqqinogKEnDALU5qhUCzhR4WSrquNg8CtGT/hgmrg5175NNcLiCfKMtLcvXOaioaQGiFc+T3qnjpYGxthtXBK9hIxgi8fdchrLO43ZiHpl9RKViw4Z1b9qXwyRtW/P8n7o+Iy0JjqLWsroTxsivFjx4jnfDW9wM+Z4T0hsr/PgyV0Y/3MfqkmpmNeB1q5wnOEzj06KrVXwxwm+e+3JJZWNh5w/I6sIri7qrGJvexiEIt9GoXIBpBqkR2DZfABjRYWIS6nG7e3NmTXJDfItnvUEIcAuSG90hWMcVZQ2jmer7cACSP/FYaqPRbxJIRwPop0HNQsxdwaiuNalJArWkvVGkHRMv+EUEX4WD1XxI/SOyjDyrTgNwLHg9ANd1/S1fHwGERh91KQW28ioMxw5vFz4ml1cKqbbrdtUtJPCBF9V8DPmM8YnqrXXWYuTtwsEMu+UBvUfY4o66U9IOUabRU11OnPWmdasRXjKD1H69pV1BfukcPwpYAXrXOTMjZxojWBYCV57cWQ+956zLloZTqb2+dl7KrjYHtdWwbkya3KqgvRrLmPzBcSO6kOP59eRxCU+oI1hJHytIHNhqVGAdKGZC93MSqsXlesfn/pQ/Nvpu+QcAITkkRRnJEd+OAHvnLGxfsVpXw8wdveMXbvzBBraVWyjFoMaoGtfS2QU64MKYw=="
    }
    }

    # from chomre - F12 - Network - Prescribed.aspx - Cookies
    cookies={'win32':{'ASP.NET_SessionId':'ct52zzrs2voqfmgvmkdnrzdc', 
                    '_gid':'GA1.4.1909174387.1682567412', 
                    '_ga':'GA1.4.1560349057.1681796908',
                    '_ga_30SQYKN4W6':'GS1.1.1682573785.7.0.1682574357.0.0.0'},
            'linux':{'ASP.NET_SessionId':'mwhjgdexy4kyxtusjnu0kacd', 
                    '_gid':'GA1.4.2120303896.1682637464', 
                    '_ga':'GA1.4.463289802.1682170590',
                    '_ga_30SQYKN4W6':'GS1.1.1682637463.2.1.1682637699.0.0.0'}
            }

    platform=sys.platform
    data = get_byte_data(url, headers=headers[platform], data=data[platform],cookies=cookies[platform])
    df=pd.read_csv(data,header=0)
    return df


if __name__=='__main__':
    # choose from Temporary/Permanent
    print(get_sa_entitlement_trade('Permanent'))  

    # print(get_sa_allocation_trade())

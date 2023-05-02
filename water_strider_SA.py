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
        "DefaultScriptManager1_TSM": ";;System.Web.Extensions,+Version=4.0.0.0,+Culture=neutral,+PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI,+Version=2020.3.1021.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b;;Telerik.Web.UI,+Version=2020.3.1021.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b",
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
        "__EVENTVALIDATION": "ZmuYDEukhH+CVxZPQs8Vx2Fd1HaDfoCXXDhXB2c4dI0u/6qmOLaJ3+VDkbotd++rQiaHbmxOgI0ul61FD1N6vx8HNcT/+rZrTTLhD+b5bV+MNtdCVPkH3TmOQjw8AlKRgj5niT73JAedZ7G8TYoPNx94BiUb+A0N9BC1tzq0jmh55RB6SVNd+02q2i2+GSx+nBt/Vp7Te8qCcqftWo5Us15xbaAMvWBsUAGaWWAZyjt/Gmi1wEkAFMvTF2LJzFYEOtCfK3Hr1pPB9HaZtVyQtkh0DBYqq+vw+KS4QlvwNXAPDg6q6sCqGsnVeD3cH14Q5cB2UmFF1cvlCDWDzszCe/Aij4uLcCtU/vSY4osTHFyVSKWxQi7qydOjp2Nl1SsJf/MgBfLzoF11F2WQN3uT1570I+3XNXIXs7ikkAWOEuY+7C7pHBpnerYu4VxljtCDXCWQEV9w8ILVIT+5CAPvxCLMQo4U/VB0V869kSjDc16hzqrvUCME5r67y0Gz/lQK6POQxLxjRI/GogVcTT33iQrVXzfC/lLEAKCxH1I7Fhia4AU5sVW4FZzy7+x5RQVBKMQytqo3ykrQNNKJLzIlBnFqa5Edzb2MCLCGf/MpkkahakThRSxvsXHwZmAecD/6Ff1Vx0eT2nreMAoGEvSg+nXGJe0Dl/HQl0qyQ5EuCh72jMXmrvxqRpduDqwVwZ5/ThrpbLW//UymtpnQQm3Oau2j7dMiLSctp4Wm8vMIux0Gji9fxv97FbjZ/FrZzE3OOeRI2CamN533IUrePhPKSTTleHeOaEbb0nM5bGGAuZqykSkmEiUeNK1M7HRo3xIJ26L42CgsfNffrVG40EFVBBZvUCzqZDGG152fKquX+Fj5Ppuv9V8UCxbHIKiJeD5gfoiatnqODe1iPXFP73dRpwmE6fF/z+4mLSUuvCS+TRQpl4EYmUKbVIz6MmXpgeGOXPUrft8yUsy/u6UHUWaxVZjaI9JXyztnuQ+i/KjV0Wj49DWnnjvGMGYPNx2KIcWWsFOGWqSLmqLgO9max4qKSYwCHTjqVmbIjzfM+PS6Wc8ndFS2rJHXIdos0cLHcBh67Pwgwz+dj5x3pL2ko1yL10Y46S4bHeXgnYs9dPikRaby2j8xUzlTfyJtwhxuVF8/AGMD6IPsp25Sk2nQ/Btu1osePCbzIL6/OwBQwy5cJ41+etHihqvT1fUKpQUe34GPYmkIFluBFfEAuyA8gHDe1bITA9qePqTrDb/rW0uPZaRIFy2TY7EFca1tToRiC3YobDYH/pYEqtrVpyK2z1Jg15+gkJgTuWstClxn0fNGdIV9q7fqxzz+A4hXkQxjo3Y9ne/zHAXjhTq+EqtA2Ln2wovD2XTsIiCLlUJP1anc41Q6rgXgkIx1GiIesoLntgwsL1FocY7v+Ea9oK1mAz/RtzGKe1m6s0C2Aw84P3RcEyUsOJ2eLgNiAEa1g0ytakNd781Jhy5iB7f6Lk3Dxm7a/K8gomVHXPRFz+jKUcjBZQFcDZcBtZBuwi1BM4fp5hxA3+H4FClayIFBKA256b6Psv1Dh69ZQ2jRxLGILkluf5K0VAe5aGNCVgulEb90UthghxR7z+kbcHpVIIVSMlI5H/gPBnFOQUWtd64eSveRX5rn/DMblRFJYlWaWY1eDwK86ZQ6FxrRfENjDUQl7kGCsdUQFBEg6B1+5Nj82JbiP4aZ8zAkWI19LI26gl/+h0BAjuwPBBYoAgLWf8QC8N9jPGo2mX4p+4iiQVX5b5HkuXx4W5qLjKa2xoRJJeaWw5h000swECOSEdxIfZCWfwr4IJh7YzUVRGWLM6WFU8oRZOLmmyViHUnm5tRu9K+YbzlvGiD562m62EMR0WoRkEWP6w=="
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
        cookies={'win32':{'ASP.NET_SessionId':'lyvdxfmz3kugmuritwaogced', 
                        '_gid':'GA1.4.853561379.1682981502', 
                        '_ga':'GA1.1.1560349057.1681796908',
                        '_ga_30SQYKN4W6':'GS1.1.1682996787.11.1.1682997499.0.0.0'},
                'linux':{'ASP.NET_SessionId':'mwhjgdexy4kyxtusjnu0kacd', 
                        '_gid':'GA1.4.2120303896.1682637464', 
                        '_ga':'GA1.4.463289802.1682170590',
                        '_ga_30SQYKN4W6':'GS1.1.1682637463.2.1.1682637699.0.0.0'}
                }
        
    elif mode.lower()=='permanent':
        # from chomre - F12 - Network - Prescribed.aspx - Payload - Form Data
        data = {
            'win32':{
                    "DefaultScriptManager1_TSM": ";;System.Web.Extensions,+Version=4.0.0.0,+Culture=neutral,+PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI,+Version=2020.3.1021.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b;;Telerik.Web.UI,+Version=2020.3.1021.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:2003d0b8:c128760b:1e771326:88144a7a:aa288e2d:258f1c72:ed16cbdc:e524c98b;",
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
                        'ASP.NET_SessionId':'lyvdxfmz3kugmuritwaogced', 
                        '_gid':'GA1.4.853561379.1682981502', 
                        '_ga':'GA1.1.1560349057.1681796908',
                        '_ga_30SQYKN4W6':'GS1.1.1682996787.11.1.1682997689.0.0.0'},
                'linux':{
                        'ASP.NET_SessionId':'mwhjgdexy4kyxtusjnu0kacd', 
                        '_gid':'GA1.4.2120303896.1682637464', 
                        '_ga':'GA1.1.463289802.1682170590',
                        '_ga_30SQYKN4W6':'GS1.1.1682637463.2.1.1682639666.0.0.0'}
        }

    platform=sys.platform
    data = get_byte_data(url, headers=headers[platform], data=data[platform], cookies=cookies[platform])
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
    'DefaultScriptManager1_TSM':";;System.Web.Extensions,+Version=4.0.0.0,+Culture=neutral,+PublicKeyToken=31bf3856ad364e35:en-AU:9ddf364d-d65d-4f01-a69e-8b015049e026:ea597d4b:b25378d2;Telerik.Web.UI,+Version=2020.3.1021.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:16e4e7cd:ed16cbdc:f7645509:88144a7a:24ee1bba:2003d0b8:f46195d3:33715776:1e771326:e524c98b;;Telerik.Web.UI,+Version=2020.3.1021.45,+Culture=neutral,+PublicKeyToken=121fae78165ba3d4:en-AU:65ded1fa-0224-45b6-a6df-acf9eb472a15:58366029:c128760b:aa288e2d:258f1c72",
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
    "__VIEWSTATE": viewstate['VIEWSTATE_at'],
    "__VIEWSTATEGENERATOR": "C7B91F77",
    "__EVENTVALIDATION":"ZmuYDEukhH+CVxZPQs8Vx2Fd1HaDfoCXXDhXB2c4dI0u/6qmOLaJ3+VDkbotd++rQiaHbmxOgI0ul61FD1N6vx8HNcT/+rZrTTLhD+b5bV+MNtdCVPkH3TmOQjw8AlKRgj5niT73JAedZ7G8TYoPNx94BiUb+A0N9BC1tzq0jmh55RB6SVNd+02q2i2+GSx+nBt/Vp7Te8qCcqftWo5Us15xbaAMvWBsUAGaWWAZyjt/Gmi1wEkAFMvTF2LJzFYEOtCfK3Hr1pPB9HaZtVyQtkh0DBYqq+vw+KS4QlvwNXAPDg6q6sCqGsnVeD3cH14Q5cB2UmFF1cvlCDWDzszCe/Aij4uLcCtU/vSY4osTHFyVSKWxQi7qydOjp2Nl1SsJf/MgBfLzoF11F2WQN3uT1570I+3XNXIXs7ikkAWOEuY+7C7pHBpnerYu4VxljtCDXCWQEV9w8ILVIT+5CAPvxCLMQo4U/VB0V869kSjDc16hzqrvUCME5r67y0Gz/lQK6POQxLxjRI/GogVcTT33iQrVXzfC/lLEAKCxH1I7Fhia4AU5sVW4FZzy7+x5RQVBKMQytqo3ykrQNNKJLzIlBnFqa5Edzb2MCLCGf/MpkkahakThRSxvsXHwZmAecD/6Ff1Vx0eT2nreMAoGEvSg+nXGJe0Dl/HQl0qyQ5EuCh72jMXmrvxqRpduDqwVwZ5/ThrpbLW//UymtpnQQm3Oau2j7dMiLSctp4Wm8vMIux0Gji9fxv97FbjZ/FrZzE3OOeRI2CamN533IUrePhPKSTTleHeOaEbb0nM5bGGAuZqykSkmEiUeNK1M7HRo3xIJ26L42CgsfNffrVG40EFVBBZvUCzqZDGG152fKquX+Fj5Ppuv9V8UCxbHIKiJeD5gfoiatnqODe1iPXFP73dRpwmE6fF/z+4mLSUuvCS+TRQpl4EYmUKbVIz6MmXpgeGOXPUrft8yUsy/u6UHUWaxVZjaI9JXyztnuQ+i/KjV0Wj49DWnnjvGMGYPNx2KIcWWsFOGWqSLmqLgO9max4qKSYwCHTjqVmbIjzfM+PS6Wc8ndFS2rJHXIdos0cLHcBh67Pwgwz+dj5x3pL2ko1yL10Y46S4bHeXgnYs9dPikRaby2j8xUzlTfyJtwhxuVF8/AGMD6IPsp25Sk2nQ/Btu1osePCbzIL6/OwBQwy5cJ41+etHihqvT1fUKpQUe34GPYmkIFluBFfEAuyA8gHDe1bITA9qePqTrDb/rW0uPZaRIFy2TY7EFca1tToRiC3YobDYH/pYEqtrVpyK2z1Jg15+gkJgTuWstClxn0fNGdIV9q7fqxzz+A4hXkQxjo3Y9ne/zHAXjhTq+EqtA2Ln2wovD2XTsIiCLlUJP1anc41Q6rgXgkIx1GiIesoLntgwsL1FocY7v+Ea9oK1mAz/RtzGKe1m6s0C2Aw84P3RcEyUsOJ2eLgNiAEa1g0ytakNd781Jhy5iB7f6Lk3Dxm7a/K8gomVHXPRFz+jKUcjBZQFcDZcBtZBuwi1BM4fp5hxA3+H4FClayIFBKA256b6Psv1Dh69ZQ2jRxLGILkluf5K0VAe5aGNCVgulEb90UthghxR7z+kbcHpVIIVSMlI5H/gPBnFOQUWtd64eSveRX5rn/DMblRFJYlWaWY1eDwK86ZQ6FxrRfENjDUQl7kGCsdUQFBEg6B1+5Nj82JbiP4aZ8zAkWI19LI26gl/+h0BAjuwPBBYoAgLWf8QC8N9jPGo2mX4p+4iiQVX5b5HkuXx4W5qLjKa2xoRJJeaWw5h000swECOSEdxIfZCWfwr4IJh7YzUVRGWLM6WFU8oRZOLmmyViHUnm5tRu9K+YbzlvGiD562m62EMR0WoRkEWP6w=="
    }
    }

    # from chomre - F12 - Network - Prescribed.aspx - Cookies
    cookies={'win32':{'ASP.NET_SessionId':'lyvdxfmz3kugmuritwaogced', 
                    '_gid':'GA1.4.853561379.1682981502', 
                    '_ga':'GA1.1.1560349057.1681796908',
                    '_ga_30SQYKN4W6':'GS1.1.1682996787.11.1.1682996837.0.0.0'},
            'linux':{'ASP.NET_SessionId':'mwhjgdexy4kyxtusjnu0kacd', 
                    '_gid':'GA1.4.2120303896.1682637464', 
                    '_ga':'GA1.4.463289802.1682170590',
                    '_ga_30SQYKN4W6':'GS1.1.1682637463.2.1.1682637699.0.0.0'}
            }

    platform=sys.platform
    data = get_byte_data(url, headers=headers[platform], data=data[platform],cookies=cookies[platform])
    df=pd.read_csv(data,header=0)
    return df


def main():
    # choose from temporary/permanent
    if sys.argv[1] == 'et':
        if len(sys.argv)<3:
            raise IndexError("No trade type detected, please choose temporary/permanent")
        elif sys.argv[2].lower() == 'temporary':
            df=get_sa_entitlement_trade('temporary')
        elif sys.argv[2].lower() == 'permanent':
            df=get_sa_entitlement_trade('permanent')
        else:
            raise ValueError("Parameter passed after et is not recognised")
    elif sys.argv[1] == 'at':
        df=get_sa_allocation_trade()

    return df


if __name__=='__main__':
    df=main()
    print(df.head(10))

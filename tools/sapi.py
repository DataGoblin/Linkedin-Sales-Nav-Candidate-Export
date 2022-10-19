import re
import requests
from cleantext import clean
import urllib.parse
import math
from time import sleep
import pandas as pd
import time



class SalesNavScrape:

    def __init__(self, url, li_at, li_a, jsessionid, file_name):

        self.url = url
        self.li_at = li_at
        self.li_a = li_a
        self.jsessionid = jsessionid
        self.file_name = file_name

        self.cookies = {"li_at": f"{self.li_at}",
                "JSESSIONID": f"{self.jsessionid}"
                }

        self.headers = {
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
          'accept': '*/*',
          'cookie': f'JSESSIONID="{self.jsessionid}"; li_at={self.li_at}; li_a={self.li_a}',
          'csrf-token': self.jsessionid,
          'referer': self.url,
          'accept-encoding': 'gzip',
          'accept-language': 'en-US,en;q=0.9',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'x-li-lang': 'en_US',
          'x-restli-protocol-version': '2.0.0',

        }


    def craft_url(self):
        url_prefix = 'https://www.linkedin.com/sales-api/salesApiLeadSearch?q=searchQuery&query='
        url_replace = re.sub(r'&sessionId=.*','',self.url).replace('https://www.linkedin.com/sales/search/people?query=', url_prefix)

        self.url = url_replace

    
    def harvest_companies(self, companyID=''):
        
        url = f'https://www.linkedin.com/sales-api/salesApiCompanies/{companyID}?decoration=%28entityUrn%2Cname%2Caccount%28saved%2CnoteCount%2ClistCount%2CcrmStatus%29%2CpictureInfo%2CcompanyPictureDisplayImage%2Cdescription%2Cindustry%2CemployeeCount%2CemployeeDisplayCount%2CemployeeCountRange%2Clocation%2Cheadquarters%2Cwebsite%2Crevenue%2CformattedRevenue%2CemployeesSearchPageUrl%2CflagshipCompanyUrl%2Cemployees*~fs_salesProfile%28entityUrn%2CfirstName%2ClastName%2CfullName%2CpictureInfo%2CprofilePictureDisplayImage%29%29'

        get_data = requests.get(url,
                headers=self.headers,
                cookies=self.cookies).json()

        try:
            data = get_data['headquarters']

            city = data.get('city', '')
            country = data.get('country', '')

            match city, country:
                case _ if not city and not country:
                    hq = ''
                case _ if city and country:
                    hq = f'{city}, {country}'

                case _ if city and not country:
                    hq = f'{city}'

                case _ if not city and country:
                    hq =f'{country}'

        except KeyError:
            hq = ''

        company = {
            "HQ": hq,
            "Industry": get_data.get('industry', ''),
            "Website": get_data.get('website', ''),
            "Employee Count": get_data.get('employeeCount', '')
        }
        
        return company


    def harvest_candidates(self):
        candidates = []
        page_total = 0

        get_data = requests.get(self.url,
                        headers=self.headers,
                        cookies=self.cookies).json()

        # parsing candidate total. dividing by 25 and rounding down to get page total. if greater than 100 then page = 100
        try:
            page_total = math.floor(get_data['paging'].get('total') / 25)
            print(f'total candidates: {get_data["paging"].get("total")}')

            if page_total > 100:
                page_total = 100
        except KeyError:
            print('No Pages found')

        if page_total > 0:
            print(f'Page total: {page_total}')
            
            for page in range(page_total+1):
                sleep(12)

                localtime = time.localtime()
                result = time.strftime("%I:%M:%S %p", localtime)
                print(f'Scraping candidates from page: {page+1}. Time: {result}')
                start = 25*page
                url = self.url + f'&start={start}&count=25'

                get_data = requests.get(url,headers=self.headers,
                                       cookies=self.cookies).json()

                try:
                    data = get_data['elements']

                    for candidate in data:

                        # job title
                        try:
                            jobtitle = candidate['currentPositions'][0].get('title')
                        except (KeyError, IndexError, AttributeError):
                            jobtitle = ''                              
                        
                        # company name
                        try:
                            companyname = candidate['currentPositions'][0].get('companyName')
                        except (KeyError, IndexError, AttributeError):
                            companyname = ''                                       

                        # years - tenure
                        try:
                            years = candidate['currentPositions'][0].get('tenureAtCompany','').get('numYears', 0)
                            match years:
                                case _ if years == 0:
                                    years = ''
                                case _ if years == 1:
                                    years = f'{years} year'
                                case _ if years > 1:
                                    years = f'{years} years'
                        except (KeyError, IndexError, AttributeError):
                            years = ''
                        
                        #months - tenure
                        try:
                            months = candidate['currentPositions'][0].get('tenureAtCompany','').get('numMonths', 0)
                            match months:
                                case _ if months == 0:
                                    months = ''
                                case _ if months == 1:
                                    months = f'{months} month'
                                case _ if months > 1:
                                    months = f'{months} months'   
                        except (KeyError, IndexError, AttributeError):
                            months = ''

                        # craft profile url
                        try:
                            profileurl = candidate.get("entityUrn","")

                            if not profileurl == '':
                                profileurl = re.search("(?<=e:\()(.*?)(?=\,)", profileurl).group(0)
                                profileurl = f'https://www.linkedin.com/in/{profileurl}'

                        except (KeyError, IndexError, AttributeError):
                            profileurl = ''                                                       

                        # craft company linkedin url
                        try:
                            companyID = candidate['currentPositions'][0].get('companyUrn','')

                            if not companyID == '':
                                companyID = re.search("(?<=urn:li:fs_salesCompany:)(.*)", companyID).group(0)
                                companyURL = f'https://www.linkedin.com/company/{companyID}'
                            else:
                                companyURL = ''
                                companyID  = ''

                        except (KeyError, IndexError, AttributeError):
                            companyURL = ''
                            companyID  = ''

                        try:
                            if companyID:
                                data = self.harvest_companies(companyID)
                                hq = data.get('HQ', '')
                                industry = data.get('Industry', '')
                                website = data.get('Website', '')
                                employees = data.get('Employee Count', '')
                            else:
                                hq = ''
                                industry = ''
                                website = ''
                                employees = ''
                        except (KeyError, IndexError, AttributeError):
                            hq = hq if hq else ''
                            industry = industry if industry else ''
                            website = website if website else ''
                            employees = employees if employees else ''

                     
                        candidate = {
                            "Full Name": clean(candidate.get('fullName',''), no_emoji=True,  to_ascii=False, lower=False),
                            "Current Job Title": jobtitle.strip(),
                            "Current Company": companyname.strip(),
                            "Current Industry": industry.strip(),
                            "Tenure": f'{years} {months}'.strip(),
                            "Location": candidate.get('geoRegion','').strip(),
                            "RecruiterURL": profileurl.strip(),
                            "CompanyLinkedin": companyURL.strip(),
                            "CompanyURL": website.strip(),
                            "CompanyHQ": hq.strip(),
                            "Employee Count": employees
                        }

                        candidates.append(candidate)

                except KeyError:
                    print('Fail')
                    
        self.data = candidates


    def export_data(self):
        data = self.data
        df = pd.DataFrame.from_records(data)
        df.to_csv(f'export/{self.file_name}.csv', index=False)
        



def api(url, li_at, li_a, jsessionid, file_name):
    url = urllib.parse.unquote(url)
    SNS = SalesNavScrape(url, li_at, li_a, jsessionid, file_name)
    SNS.craft_url()
    SNS.harvest_candidates()
    SNS.export_data()


if __name__ == "__main__":
    api()


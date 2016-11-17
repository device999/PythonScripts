from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep
import csv
 
 
def linkedin_companies_parser(url):
    for i in range(5):
        try:
            headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            response = requests.get(url, headers=headers)
            formatted_response = response.content.replace('<!--', '').replace('-->', '')
            doc = html.fromstring(formatted_response)
            datafrom_xpath = doc.xpath('//code[@id="stream-promo-top-bar-embed-id-content"]//text()')
            if datafrom_xpath:
                try:
                    json_formatted_data = json.loads(datafrom_xpath[0])
                    company_name = json_formatted_data['companyName'] if 'companyName' in json_formatted_data.keys() else None
                    size = json_formatted_data['size'] if 'size' in json_formatted_data.keys() else None
                    industry = json_formatted_data['industry'] if 'industry' in json_formatted_data.keys() else None
                    description = json_formatted_data['description'] if 'description' in json_formatted_data.keys() else None
                    follower_count = json_formatted_data['followerCount'] if 'followerCount' in json_formatted_data.keys() else None
                    year_founded = json_formatted_data['yearFounded'] if 'yearFounded' in json_formatted_data.keys() else None
                    website = json_formatted_data['website'] if 'website' in json_formatted_data.keys() else None
                    type = json_formatted_data['companyType'] if 'companyType' in json_formatted_data.keys() else None
                    specialities = json_formatted_data['specialties'] if 'specialties' in json_formatted_data.keys() else None
 
                    if "headquarters" in json_formatted_data.keys():
                        city = json_formatted_data["headquarters"]['city'] if 'city' in json_formatted_data["headquarters"].keys() else None
                        country = json_formatted_data["headquarters"]['country'] if 'country' in json_formatted_data['headquarters'].keys() else None
                        state = json_formatted_data["headquarters"]['state'] if 'state' in json_formatted_data['headquarters'].keys() else None
                        street1 = json_formatted_data["headquarters"]['street1'] if 'street1' in json_formatted_data['headquarters'].keys() else None
                        street2 = json_formatted_data["headquarters"]['street2'] if 'street2' in json_formatted_data['headquarters'].keys() else None
                        zip = json_formatted_data["headquarters"]['zip'] if 'zip' in json_formatted_data['headquarters'].keys() else None
                        street = street1 + ', ' + street2
                    else:
                        city = None
                        country = None
                        state = None
                        street1 = None
                        street2 = None
                        street = None
                        zip = None                        
                        data = {
                                    'company_name': company_name,
                                    'size': size,
                                    'industry': industry,
                                    'description': description,
                                    'follower_count': follower_count,
                                    'founded': year_founded,
                                    'website': website,
                                    'type': type,
                                    'specialities': specialities,
                                    'city': city,
                                    'country': country,
                                    'state': state,
                                    'street': street,
                                    'zip': zip,
                                    'url': url
                                }
                    return data
                except:
                    print "cant parse page", url
 
            # Retry in case of captcha or login page redirection
            if len(response.content) < 2000 or "trk=login_reg_redirect" in url:
                if response.status_code == 404:
                    print "linkedin page not found"
                else:
                    raise ValueError('redirecting to login page or captcha found')
        except :
            print "retrying :",url
 
def readurls():
    companyurls = ['https://www.linkedin.com/company/2387','https://www.linkedin.com/company/3200','https://www.linkedin.com/company/5626','https://www.linkedin.com/company/3534','https://www.linkedin.com/company/164820','https://www.linkedin.com/company/8901','https://www.linkedin.com/company/3823740','https://www.linkedin.com/company/13634','https://www.linkedin.com/company/12113','https://www.linkedin.com/company/3341','https://www.linkedin.com/company/2026087','https://www.linkedin.com/company/259898','https://www.linkedin.com/company/98795','https://www.linkedin.com/company/37155','https://www.linkedin.com/company/46174','https://www.linkedin.com/company/375426','https://www.linkedin.com/company/13819','https://www.linkedin.com/company/267045','https://www.linkedin.com/company/163562','https://www.linkedin.com/company/30170','https://www.linkedin.com/company/12387','https://www.linkedin.com/company/131824','https://www.linkedin.com/company/27242','https://www.linkedin.com/company/6426','https://www.linkedin.com/company/53137','https://www.linkedin.com/company/81608','https://www.linkedin.com/company/2611043','https://www.linkedin.com/company/28212','https://www.linkedin.com/company/118355','https://www.linkedin.com/company/19193','https://www.linkedin.com/company/12275','https://www.linkedin.com/company/784432','https://www.linkedin.com/company/51781','https://www.linkedin.com/company/83154','https://www.linkedin.com/company/44114','https://www.linkedin.com/company/55885','https://www.linkedin.com/company/2676627','https://www.linkedin.com/company/33642','https://www.linkedin.com/company/63555','https://www.linkedin.com/company/930858','https://www.linkedin.com/company/111658','https://www.linkedin.com/company/59248','https://www.linkedin.com/company/81939','https://www.linkedin.com/company/862310','https://www.linkedin.com/company/9366464','https://www.linkedin.com/company/131825','https://www.linkedin.com/company/3042631','https://www.linkedin.com/company/74680','https://www.linkedin.com/company/153781','https://www.linkedin.com/company/2212798']
    extracted_data = []
    for url in companyurls:
        print url
        extracted_data.append(linkedin_companies_parser(url))
        sleep(5)
        f = open('data.json', 'w')
        json.dump(extracted_data, f, indent=4)
 
 
if __name__ == "__main__":
    readurls()

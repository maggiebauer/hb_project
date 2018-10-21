import json
import os
import sys
import urllib.request, urllib.parse
import io
from flask import Flask
from model import connect_to_db, db
from model import FCCompany
from model import SMLink
from model import CompanyLink
from model import IndustryType
from model import CompanyIndustry
from model import CBCompany
from model import FundingRound
from model import FundingType
from model import MarketType

################################################################################
# Functions to fetch info from Crunchbase data tables, send request to FullContact API, and store response

def fetch_all_cb_companies(company_str):
    ''' Find all possible Crunchbase companies and return a list of possible matches '''

    comp_str = '%' + company_str + '%'
    companies = CBCompany.query.filter(CBCompany.cb_company_name.like(comp_str)).limit(25).all()
    return companies


def get_domain(cb_co_object):
    ''' Returns domain from Crunchbase company url '''
    
    co_url = cb_co_object.cb_url
    if co_url[:8] == 'https://':
        domain = co_url[8:]
    elif co_url[:7] == 'http://':
        domain = co_url[7:]
    return domain


def fetch_fc_company(domain):
    ''' Call FullContact API with company domain and return JSON string '''

    # set variables needed to pass and call to API
    api_key = os.environ['FULLCONTACT_API_KEY']
    req = urllib.request.Request('https://api.fullcontact.com/v3/company.enrich')

    req.add_header('Authorization', 'Bearer {}'.format(api_key))
    data = json.dumps({"domain": domain})
    binary_data = data.encode('utf-8')
    response = urllib.request.urlopen(req,binary_data)

    # turn response into json object
    response_str = response.read().decode('utf-8')
    response_json_obj = json.loads(response_str)

    # write response to file to seed into database
    with io.open('seed_data/fc_seed_data.txt', 'a') as f:
        f.write(json.dumps(response_json_obj, ensure_ascii=False))

    return response_json_obj


################################################################################
# FullContact info loaded to database


def load_fc_industry_types(response):
    ''' Load the types of FullContact industries into database '''

    for industry in response['details']['industries']:
        ind_name = industry['name']
        if not IndustryType.query.filter(IndustryType.industry_name==ind_name).first():

            industry_type = IndustryType(industry_name=ind_name)
            db.session.add(industry_type)
    
    db.session.commit()


# need to add in cb_comapny_id and domain - and uncomment cb_company backref
def load_fc_company(response, domain, cb_company_id):
    ''' Load the company info from FullContact and then load the remaining FC tables '''

    # fc_co_name = response['organization']['name']

    # if not FCCompany.query.filter(FCCompany.fc_company_name==fc_co_name).first():
    
    fc_co_domain = domain
    if not FCCompany.query.filter(FCCompany.fc_company_domain == fc_co_domain).first():
        fc_company = FCCompany(fc_company_name=response['name'],
                            fc_company_domain=fc_co_domain,
                            fc_company_bio=response['bio'],
                            logo_image_url=response['logo'],
                            location_city=response['details']['locations'][0]['city'],
                            location_state_code=response['details']['locations'][0]['region'],
                            founded=response['founded'],
                            num_employees=response['employees'],
                            cb_company_id=cb_company_id)

        db.session.add(fc_company)
    db.session.commit()

    # now adding the rest of the info out of the and referencing the fc_company_id

    def load_company_links(response, fc_company_id):
        ''' Load the company links info from FullContact '''
        # import pdb; pdb.set_trace()
        for link in response['details']['urls']:

            # if not CompanyLink.query.filter(CompanyLink.link_url == link['value']):
            company_link = CompanyLink(fc_company_id=fc_company_id,
                            link_type=link['label'],
                            link_url=link['value'])
            db.session.add(company_link)


    def load_social_media(response, fc_company_id):
        ''' Load the social media links info from FullContact '''
        # import pdb; pdb.set_trace()

        sm_site_dict = response['details']['profiles']
        # for link_type in response['details']['profiles']:
        for link_type in sm_site_dict.keys():
            # for site in link_type.keys():


            sm_link = SMLink(fc_company_id=fc_company_id,
                        sm_name=sm_site_dict[link_type]['service'],
                        sm_site_url=sm_site_dict[link_type]['url'],
                        sm_bio=sm_site_dict[link_type].get('bio'))
            db.session.add(sm_link)


    def load_company_industries(response, fc_company_id):
        ''' Load the industries for the company from FullContact '''

        all_industry_types = IndustryType.query.all()
        industry_types_dict = {}

        for industry in all_industry_types:
            industry_types_dict[industry.industry_name] = industry.industry_id

        for co_industry in response['details']['industries']:
            company_industry = CompanyIndustry(industry_id=industry_types_dict[co_industry['name']],
                                fc_company_id=fc_company_id)
            db.session.add(company_industry)



    fc_co_ojbect = FCCompany.query.filter(FCCompany.fc_company_domain==fc_co_domain).first()

    load_company_links(response, fc_co_ojbect.fc_company_id)
    load_social_media(response, fc_co_ojbect.fc_company_id)
    load_company_industries(response, fc_co_ojbect.fc_company_id)


################################################################################
# Connect to app and call functions

app = Flask(__name__)

connect_to_db(app)


null = None
false = False

# cb_company_id=8 domain=www.h2o.ai
# fc_json_co_1 = {'name': 'H2O.ai', 'location': '2307 Leghorn Street  Mountain View California, 94043 United States', 'twitter': 'https://twitter.com/h2oai', 'linkedin': 'https://www.linkedin.com/company/0xdata', 'facebook': 'https://www.facebook.com/0xdata', 'bio': 'H2O.ai provides an open source machine learning platform that makes it easy to build smart applications.', 'logo': 'https://d2ojpxxtu63wzl.cloudfront.net/static/23061fd477ebd8dd4d25fd9dca70f08c_d4ee00704c332bcc04a2a854a0d2f2a590e17a9ee632f63873426db72eb07f3a', 'website': 'http://h2o.ai', 'founded': 2012, 'employees': 94, 'locale': None, 'category': 'Other', 'details': {'locales': [], 'categories': [{'code': 'OTHER', 'name': 'Other'}], 'industries': [{'type': 'SIC', 'name': 'Computers, Peripherals, and Software', 'code': '5045'}], 'emails': [], 'phones': [{'value': '1 (650) 227-4572', 'label': 'other'}], 'profiles': {'owler': {'service': 'owler', 'username': 'h2o-ai', 'userid': '1160105', 'url': 'https://www.owler.com/iaApp/1160105/h2o-ai-company-profile'}, 'twitter': {'service': 'twitter', 'username': 'h2oai', 'url': 'https://twitter.com/h2oai'}, 'crunchbasecompany': {'service': 'crunchbasecompany', 'username': 'h2o-2', 'url': 'http://www.crunchbase.com/organization/h2o-2', 'bio': 'H2O.ai provides an open source machine learning platform that makes it easy to build smart applications.'}, 'linkedincompany': {'service': 'linkedincompany', 'username': '0xdata', 'url': 'https://www.linkedin.com/company/0xdata'}, 'facebook': {'service': 'facebook', 'username': '0xdata', 'url': 'https://www.facebook.com/0xdata'}}, 'locations': [{'label': 'work', 'addressLine1': '2307 Leghorn Street', 'city': 'Mountain View', 'region': 'California', 'regionCode': 'CA', 'postalCode': '94043', 'country': 'United States', 'countryCode': 'US', 'formatted': '2307 Leghorn Street  Mountain View California, 94043 United States'}, {'city': 'Mountain View', 'region': 'CA', 'country': 'United States', 'formatted': '  Mountain View CA,  United States'}], 'images': [{'value': 'https://d2ojpxxtu63wzl.cloudfront.net/static/b27954afe074171f4c03f5a726f3f965_71593e54e7a6922812b3e45bba2236d1b913a97f73b4afaae8b5915d0f8b2e3d', 'label': 'other'}, {'value': 'https://d2ojpxxtu63wzl.cloudfront.net/static/7488c0040392f1549b4ef05022fd6c46_ef04f26756055019aaa7e1c63fd22e20f0d19caaf126b669adbeb0e7461eed3c', 'label': 'other'}, {'value': 'https://d2ojpxxtu63wzl.cloudfront.net/static/23061fd477ebd8dd4d25fd9dca70f08c_d4ee00704c332bcc04a2a854a0d2f2a590e17a9ee632f63873426db72eb07f3a', 'label': 'logo'}], 'urls': [{'value': 'http://h2o.ai', 'label': 'website'}, {'value': 'http://0xdata.com', 'label': 'other'}], 'keywords': [], 'keyPeople': [], 'traffic': {'countryRank': {'global': {'rank': 137058, 'name': 'Global'}}, 'localeRank': {'in': {'rank': 51096, 'name': 'India'}, 'pl': {'rank': 36029, 'name': 'Poland'}, 'us': {'rank': 86173, 'name': 'United States'}}}}, 'dataAddOns': [{'id': 'keypeople', 'name': 'Key People', 'enabled': False, 'applied': False, 'description': 'Displays information about people of interest at this company.', 'docLink': 'http://docs.fullcontact.com/api/#key-people'}], 'updated': '2018-07-09'}

# # # #cb_company_id=2 domain=www.qounter.com/
# fc_json_co_2 = {"name": ":Qounter", "location": "  Delaware City Delaware,  United States", "twitter": "https://twitter.com/Qounter", "linkedin": "https://www.linkedin.com/company/-qounter", "facebook": null, "bio": "A new way to earn and share cashback with your friends", "logo": "https://d2ojpxxtu63wzl.cloudfront.net/static/2c62014ed3b38cb6903ca6edc1d74e39_f331b2118de6f783fde8c3228d9c4d1d2101b40c73b4ddc14c83c5f8cc89c8da", "website": "https://www.qounter.com", "founded": 2014, "employees": 3, "locale": null, "category": "Other", "details": {"locales": [], "categories": [{"code": "OTHER", "name": "Other"}], "industries": [{"type": "SIC", "name": "Computer and Data Processing Services", "code": "737"}], "emails": [], "phones": [], "profiles": {"angellist": {"service": "angellist", "username": "qounter", "userid": "531321", "url": "https://angel.co/qounter", "bio": ":Qounter is set to disrupt the cashback space by enabling businesses to attract not only individuals but also their social network by offering social cashback on both online and in-store purchases. :Qounter successfully balances social influence and privacy to develop an engaging platform that is safe, easy and fun to use. :Qounter is unique due to its differentiating characteristics. The social cashback is earned passively and there is no clicking on links and spamming friends to earn cashback. This all happens in real time, online and in-store, so you can actually spend your cashback right after purchasing.", "followers": 3}, "twitter": {"service": "twitter", "username": "Qounter", "userid": "2830540400", "url": "https://twitter.com/Qounter", "bio": "A new way to earn and share cashback with your friends", "followers": 2}, "crunchbasecompany": {"service": "crunchbasecompany", "username": "-qounter", "url": "http://www.crunchbase.com/organization/-qounter", "bio": "The Social Network where you earn cashback with your friends"}, "linkedincompany": {"service": "linkedincompany", "username": "-qounter", "userid": "9323597", "url": "https://www.linkedin.com/company/-qounter", "bio": "Qounter.com is a new social cashback platform which incorporates a unique social cashback benefits program via its mobile app. We provide businesses with an innovative sales and marketing platform by powering a cashback program that rewards :Qounter users with personal and social cashback in real time. Our patent-pending technology platform tracks our users’ online and in-store purchases and credits their personal :Qounters with personal cashback in real time at the time of purchase. :Qounter users are also able to invite friends and share this cashback with them, enabling a two-way social cashback platform in which our users’ :Qounters also go up in real time based on their friends’ purchases.", "followers": 20}, "instagram": {"service": "instagram", "url": "https://instagram.com/qounterapp"}}, "locations": [{"label": "work", "city": "Delaware City", "region": "Delaware", "regionCode": "DE", "country": "United States", "countryCode": "US", "formatted": "  Delaware City Delaware,  United States"}], "images": [{"value": "https://d2ojpxxtu63wzl.cloudfront.net/static/2c62014ed3b38cb6903ca6edc1d74e39_f331b2118de6f783fde8c3228d9c4d1d2101b40c73b4ddc14c83c5f8cc89c8da", "label": "logo"}], "urls": [{"value": "https://www.qounter.com", "label": "website"}, {"value": "https://www.youtube.com/watch?v=HhJj7eQvk4s&list=UUB34sRw-eortr5c7SnSUNFA", "label": "youtube"}], "keywords": ["United States"], "keyPeople": [], "traffic": {"countryRank": {"global": {"rank": 18755142, "name": "Global"}}, "localeRank": {}}}, "dataAddOns": [{"id": "keypeople", "name": "Key People", "enabled": false, "applied": false, "description": "Displays information about people of interest at this company.", "docLink": "http://docs.fullcontact.com/api/#key-people"}], "updated": "2018-08-07"}

# # # # # call functions
# load_fc_industry_types(fc_json_co_2)
# load_fc_company(fc_json_co_2, 'www.qounter.com/', 2)

# db.session.commit()

# load_fc_industry_types(fc_json_co_1)
# load_fc_company(fc_json_co_1, 'www.h2o.ai', 8)

# db.session.commit()


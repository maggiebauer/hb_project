import json
from model import connect_to_db, db
from model import FCCompany
from model import SMLink
from model import CompanyLink
from model import IndustryType
from model import CompanyIndustry



################################################################################
# FullContact

def fetch_cb_company(company_str):
    pass

def fetch_fc_company(company_domain_str):
    pass 



def load_fc_industry_types(response):
    ''' Load the types of FullContact industries into database '''


    for industry in response['industries']:
        industry_type = IndustryType(industry_name=industry['name'])
        try:
            db.session.add(industry_type)
        except db.IntegrityError: 
            # unique name failed
            pass
    db.session.commit()



# need to add in cb_comapny_id and domain
def load fc_company(response):
    ''' Load the company info from FullContact and then load the remaining FC tables '''


    fc_company = FCCompany(fc_company_name=response['organization']['name'],
                            logo_image_url=response['logo'],
                            location_city=response['organization']['contactInfo']['addresses'][0]['locality'],
                            location_state_code=response['organization']['contactInfo']['addresses'][0]['region']['code'],
                            founded=response['organization']['founded'],
                            num_employees=response['organization']['approxEmployees'])

    try:
        db.session.add(fc_company)
    except db.IntegrityError: 
        # unique name failed
        pass
    db.session.commit()

    # now adding the rest of the info out of the and referencing the fc_company_id

    def load_company_links(response, fc_company_id):
        ''' Load the company links info from FullContact '''

        for link in response['organization']['links']:
            company_link = CompanyLink(fc_company_id=fc_company_id,
                            link_type=link['label'],
                            link_url=link['url'])
            db.session.add(company_link)


    def load_social_medias(response, fc_company_id):
        ''' Load the social media links info from FullContact '''

        for link in response['socialProfiles']:
            if link['typeName'] == 'LinkedIn':
                sm_link = SMLink(fc_company_id=fc_company_id,
                            sm_name='LinkedIn',
                            sm_site_url=link['url'],
                            sm_bio_linkedin=link['bio'])
                db.session.add(sm_link)

        
            else:
                sm_link = SMLink(fc_company_id=fc_company_id,
                            sm_name=link['typeName'],
                            sm_site_url=link['url'])
                db.session.add(sm_link)


    def load_company_industries(response, fc_company_id):
        ''' Load the industries for the company from FullContact '''

        all_industry_types = IndustryType.query.all()
        industry_types_dict = {}

        for industry in all_industry_types:
            industry_types_dict[industry.industry_name] = industry.industry_types_dict
        print(industry_types_dict)

        for co_industry in response['industries']:
            company_industry = CompanyIndustry(industry_id=industry_types_dict[co_industry['name']],
                                fc_company_id=fc_comapny_id)
            print(company_industry)
            db.session.add(company_industry)





    # call functions
    load_company_links(response, fc_company.fc_company_id)
    load_social_medias(response, fc_company.fc_company_id)
    load_company_industries(response, fc_company.fc_company_id)

    db.session.commit()




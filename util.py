import json
from flask import Flask
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
        ind_name = industry['name']
        if not IndustryType.query.filter(IndustryType.industry_name==ind_name).first():

            industry_type = IndustryType(industry_name=ind_name)
            db.session.add(industry_type)
    
    db.session.commit()



# need to add in cb_comapny_id and domain
def load_fc_company(response):
    ''' Load the company info from FullContact and then load the remaining FC tables '''

    fc_co_name = response['organization']['name']

    if not FCCompany.query.filter(FCCompany.fc_company_name==fc_co_name).first():
        fc_company = FCCompany(fc_company_name=response['organization']['name'],
                            logo_image_url=response['logo'],
                            location_city=response['organization']['contactInfo']['addresses'][0]['locality'],
                            location_state_code=response['organization']['contactInfo']['addresses'][0]['region']['code'],
                            founded=response['organization']['founded'],
                            num_employees=response['organization']['approxEmployees'])

        db.session.add(fc_company)
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
            industry_types_dict[industry.industry_name] = industry.industry_id
        print(industry_types_dict)

        for co_industry in response['industries']:
            company_industry = CompanyIndustry(industry_id=industry_types_dict[co_industry['name']],
                                fc_company_id=fc_company_id)
            print(company_industry)
            db.session.add(company_industry)

    fc_co_ojbect = FCCompany.query.filter(FCCompany.fc_company_name==fc_co_name).first()
    print(fc_co_ojbect)

    load_company_links(response, fc_co_ojbect.fc_company_id)
    load_social_medias(response, fc_co_ojbect.fc_company_id)
    load_company_industries(response, fc_co_ojbect.fc_company_id)

response = {
  "status" : 200,
  "requestId" : "9ffd07d9-2ef9-4fd6-994a-228472a5be6f",
  "category" : [ {
    "name" : "Other",
    "code" : "OTHER"
  } ],
  "logo" : "https://d2ojpxxtu63wzl.cloudfront.net/static/e9f3aeb8965684906efa7ae514988ffb_0837a93ef09a70f8b9ff73efac18176225fd0b9cb8bf84a60c5926701b4c5033",
  "website" : "https://www.fullcontact.com",
  "languageLocale" : "en",
  "industries": [ {
    "type": "SIC",
    "name": "Computer Peripheral Equipment, Nec",
    "code": "3577"
  }, {
    "type": "SIC",
    "name": "Computers, Peripherals, and Software",
    "code": "5045"
  }, {
    "type": "SIC",
    "name": "Computer Integrated Systems Design",
    "code": "7373"
  }, {
    "type": "SIC",
    "name": "Computer Peripheral Equipment, Nec",
    "code": "3577"
  }, {
    "type": "SIC",
    "name": "Computers, Peripherals, and Software",
    "code": "5045"
  }, {
    "type": "SIC",
    "name": "Computer Integrated Systems Design",
    "code": "7373"
  } ],
  "organization" : {
    "name" : "FullContact Inc.",
    "approxEmployees" : 50,
    "founded" : "2010",
    "overview" : "Solving the world's contact information problem!",
    "contactInfo" : {
      "emailAddresses" : [ {
        "value" : "support@fullcontact.com",
        "label" : "support"
      }, {
        "value" : "team@fullcontact.com",
        "label" : "sales"
      } ],
      "phoneNumbers" : [ {
        "number" : "+1 (888) 330-6943",
        "label" : "other"
      } ],
      "addresses" : [ {
        "addressLine1" : "1755 Blake Street",
        "addressLine2" : "Suite 450",
        "locality" : "Denver",
        "region" : {
          "name" : "Colorado",
          "code" : "CO"
        },
        "country" : {
          "name" : "United States",
          "code" : "US"
        },
        "postalCode" : "80202",
        "label" : "work"
      } ]
    },
    "links" : [ {
      "url" : "https://www.fullcontact.com/developer",
      "label" : "other"
    }, {
      "url" : "https://fullcontact.com/blog",
      "label" : "blog"
    }, {
      "url" : "https://www.youtube.com/watch?v=koFtyUDbYak",
      "label" : "youtube"
    }, {
      "url" : "https://www.fullcontact.com/home/feed",
      "label" : "rss"
    }, {
      "url" : "https://www.fullcontact.com/feed",
      "label" : "rss"
    }, {
      "url" : "https://www.fullcontact.com/comments/feed",
      "label" : "rss"
    } ],
    "images" : [ {
      "url" : "https://d2ojpxxtu63wzl.cloudfront.net/static/edaa53d9a080aea37ddfb85d775620a9_98a2d7beef6a5b4a53f43da4dd1a90bda21dc18f755394fdbf9b6cf3283853a0",
      "label" : "twitter"
    }, {
      "url" : "https://d2ojpxxtu63wzl.cloudfront.net/static/1bacd7306731a30d2a9f024eeb1dcff1_94d77dcdedbfe40707ac4a75ca4f4d2978bffc20b2e33a3288ea9e4d47f5af6c",
      "label" : "twitter"
    }, {
      "url" : "https://d2ojpxxtu63wzl.cloudfront.net/static/3f64db7ba9331fbd1e4cc11655e2d3d4_a2477a83cafc8a98d5533f3617f0b1db2796ad0826482e2eabdc8d3345d70c17",
      "label" : "twitter"
    }, {
      "url" : "https://d2ojpxxtu63wzl.cloudfront.net/static/ee07ac81180408fde663426d3b0afb3f_3a1154347631c037b9bd2b2f33d4cbc8511d58f5c11ad3cbbc319957d1a5149b",
      "label" : "pinterest"
    }, {
      "url" : "https://d2ojpxxtu63wzl.cloudfront.net/static/80885c5e8b570e69bdc55d29aad115cd_a1ce9fb51ea43971d861e452034056d807422a391ac8e27f76ee4a9e803698d1",
      "label" : "googleplus"
    }, {
      "url" : "https://d2ojpxxtu63wzl.cloudfront.net/static/4be5211e4b0129d1c8d41e84f257f343_3d84b3de68d6060243972af12a8ca67c4a595fd86a4419d50bf429e6d778ce2d",
      "label" : "other"
    }, {
      "url" : "https://d2ojpxxtu63wzl.cloudfront.net/static/7e9aa6402ff2975e297a01243c358619_c0b8d4a63a52f4a47106494561c0332b79f848b40fcbe92336a0a17b843f44f8",
      "label" : "other"
    } ],
    "keywords" : [ "APIs", "Boulder", "Contact Management", "Denver", "Developer APIs", "Social Media", "Techstars" ]
  },
  "socialProfiles" : [{
    "bio" : "We're solving the world's contact information problem. Get your contacts under control with @FullContactApp & check out @FullContactAPI for our APIs.",
    "followers" : 6277,
    "following" : 1758,
    "typeId" : "twitter",
    "typeName" : "Twitter",
    "url" : "https://twitter.com/FullContactInc",
    "username" : "FullContactInc",
    "id" : "142954090"
  }, {
    "bio" : "The API that turns partial contact information into full contact information. We provide data enrichment, de-duplication, normalization, and much more.",
    "followers" : 5032,
    "following" : 2444,
    "typeId" : "twitter",
    "typeName" : "Twitter",
    "url" : "https://twitter.com/FullContactAPI",
    "username" : "FullContactAPI",
    "id" : "340611236"
  }, {
    "bio" : "Keep your contact information clean, complete & current across all your address books.",
    "followers" : 3171,
    "following" : 1561,
    "typeId" : "twitter",
    "typeName" : "Twitter",
    "url" : "https://twitter.com/FullContactApp",
    "username" : "FullContactApp",
    "id" : "451688048"
  }, {
    "bio" : "FullContact's address book brings all of your contacts into one place and keeps them automatically up to date on the web, as well as on your iPhone and iPad. Add photos to your contacts. Find them on social networks like Twitter, LinkedIn and of course AngelList. It's the address book that busy professionals from any walk of life can appreciate, and best of all it's free. For developers, the suite of FullContact APIs builds powerful, complete profiles of contacts that can be included in any application.",
    "followers" : 259,
    "typeId" : "angellist",
    "typeName" : "AngelList",
    "url" : "https://angel.co/fullcontact",
    "username" : "fullcontact"
  }, {
    "bio" : "FullContact provides a suite of cloud-based contact management solutions for businesses, developers, and individuals.",
    "typeId" : "crunchbasecompany",
    "typeName" : "CrunchBase",
    "url" : "http://www.crunchbase.com/organization/fullcontact",
    "username" : "fullcontact"
  }, {
    "bio" : "FullContact is the API that keeps contact information current. We build APIs that developers can integrate into their applications using any language.",
    "followers" : 28,
    "following" : 55,
    "typeId" : "pinterest",
    "typeName" : "Pinterest",
    "url" : "http://www.pinterest.com/fullcontact/",
    "username" : "fullcontact"
  }, {
    "bio" : "All your contacts in one place and automatically up-to-date. we're solving the world's contact information problem at https://www.fullcontact.com.",
    "typeId" : "google",
    "typeName" : "GooglePlus",
    "url" : "https://plus.google.com/u/0/107620035082673219790",
    "id" : "107620035082673219790"
  }, {
    "bio" : "FullContact is solving the world's contact information problem by providing APIs to software developers to keep contact information clean, complete and current. FullContact provides identity resolution for all of the disparate pieces of contact information out there on the web. We do this by aggregating billions of contact records, all with numerous attributes, including quality, freshness and frequency. Our patent pending algorithms process all of this data and automatically produce clean, accurate full contact records. As a final step, we then check each data element to make sure that it's publicly available before providing it to our customers. FullContact is a TechStars Boulder 2011 Company.",
    "typeId" : "linkedincompany",
    "typeName" : "LinkedIn",
    "url" : "https://www.linkedin.com/company/fullcontact-inc-",
    "username" : "fullcontact-inc-",
    "id" : "2431118"
  } ],
  "traffic" : {
    "topCountryRanking" : [ {
      "rank" : 7770,
      "locale" : "us"
    }, {
      "rank" : 11728,
      "locale" : "in"
    }, {
      "rank" : 11388,
      "locale" : "gb"
    } ],
    "ranking" : [ {
      "rank" : 18640,
      "locale" : "global"
    }, {
      "rank" : 7770,
      "locale" : "us"
    } ]
  }
}

app = Flask(__name__)

connect_to_db(app)


# call functions
load_fc_industry_types(response)
load_fc_company(response)

db.session.commit()





"""Models and database functions for business finder project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

################################################################################

# Crunchbase data

class CBCompany(db.Model):
    """ Crunchbase company info """

    __tablename__ = 'cb_companies'

    cb_company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cb_company_name = db.Column(db.String(100), nullable=False)
    # cb_company_domain = db.Column(db.String(100), nullable=False)
    cb_permalink = db.Column(db.String(300), nullable=False)
    cb_url = db.Column(db.String(300))
    market_type_id = db.Column(db.Integer, db.ForeignKey('market_types.market_type_id'))
    state_code = db.Column(db.String(10))
    # fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'))

    funding_rounds = db.relationship('FundingRound', backref=db.backref('cb_company'))
    market_type = db.relationship('MarketType', backref=db.backref('cb_companies'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_str = '<CBCompany: id:{}, name:{}>'
        return repr_str.format(self.cb_company_id, self.cb_company_name)

class FundingRound(db.Model):
    """ Crunchbase funding round info """

    __tablename__ = 'funding_rounds'

    funding_round_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cb_company_id = db.Column(db.Integer, db.ForeignKey('cb_companies.cb_company_id'), nullable=False)
    funding_type_id = db.Column(db.Integer, db.ForeignKey('funding_types.funding_type_id'), nullable=False)
    market_type_id = db.Column(db.Integer, db.ForeignKey('market_types.market_type_id'))
    funded_amt = db.Column(db.String(25))
    funded_date = db.Column(db.DateTime)

    funding_type = db.relationship('FundingType')
    market_type = db.relationship('MarketType')

    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_str = '<FundingRound: id:{}, cb_company_id:{}, funding_type_id:{}, funding_amt:{}>'
        return repr_str.format(self.funding_round_id, self.cb_company_id, self.funding_type_id, self.funding_amt)


class FundingType(db.Model):
    """ Crunchbase funding round type """

    __tablename__ = 'funding_types'

    funding_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    funding_type_name = db.Column(db.String(50), nullable=False)
    funding_type_code = db.Column(db.String(50))

    def __repr__(self):
        """Provide helpful representation when printed."""    
        
        epr_str = '<FundingType: id:{}, funding_type_name:{}>'
        return repr_str.format(self.funding_type_id, self.funding_type_name)


class MarketType(db.Model):
    """ Crunchbase market types """

    __tablename__ = 'market_types'

    market_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    market_type = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""    
    
        repr_str = '<MarketType: id:{}, market_type:{}>'
        return repr_str.format(self.market_type_id, self.market_type)


################################################################################
# Full Contact Data

class FCCompany(db.Model):
    """ Full Contact company info  """

    __tablename__ = 'fc_companies'

    fc_company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fc_company_name = db.Column(db.String(100), nullable=False)
    # fc_company_domain = db.Column(db.String(100), nullable=False, unique=True) 
    logo_image_url = db.Column(db.String(300))
    location_city = db.Column(db.String(100))
    location_state_code = db.Column(db.String(20))
    founded = db.Column(db.String(25))
    num_employees = db.Column(db.String(25))
    # cb_company_id = db.Column(db.Integer, db.ForeignKey('cb_companies.cb_company_id'))


    social_media = db.relationship('SMLink', backref=db.backref('fc_company'))
    companay_links = db.relationship('CompanyLink', backref=db.backref('fc_company'))
    industries = db.relationship('CompanyIndustry', backref=db.backref('fc_companies'))
    # cb_company = db.relationship('CBCompany', backref=db.backref('fc_company'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_str = '<FCCompany: id:{}, name:{}, location:{}>'
        return repr_str.format(self.fc_company_id, self.fc_company_name, self.location_cit)


class SMLink(db.Model):
    """ Full Contact company social media sites  """

    __tablename__ = 'social_media'

    sm_link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'), nullable=False)
    sm_name = db.Column(db.String(50))
    sm_site_url = db.Column(db.String(300))
    sm_bio_linkedin = db.Column(db.String(1000))
    # only pulling bio from LinkedIn because only need one bio and two linkedin profiles unlikely


    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<SocialMediaLink: sm_type_id:{}, fc_company_id:{}, sm_site_url:{}>'
        return repr_str.format(self.sm_name, self.fc_company_id, self.sm_site_url)



class CompanyLink(db.Model):
    """ Full Contact company links  """

    __tablename__ = 'company_links'

    company_link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'), nullable=False)
    link_type = db.Column(db.String(50), nullable=False)
    link_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<CompanyLink: link_type:{}, fc_company_id:{}>'
        return repr_str.format(self.link_type, self.fc_company_id)


class IndustryType(db.Model):
    """ Full Contact industry types  """

    __tablename__ = 'industry_types'

    industry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    industry_name = db.Column(db.String(100), nullable=False, unique=True)

    # fc_companies = db.relationship('CompanyIndustry', backref=db.backref('industry_name'))

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<IndustryType: industry_id:{}, industry_name:{}>'
        return repr_str.format(self.industry_id, self.industry_name)


class CompanyIndustry(db.Model):
    """ Full Contact companies with industries  """

    __tablename__ = 'company_industries'

    company_with_industry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    industry_id = db.Column(db.Integer, db.ForeignKey('industry_types.industry_id'), nullable=False)
    fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<CompanyIndustry: industry_id:{}, fc_company_id:{}>'
        return repr_str.format(self.industry_id, self.fc_company_id)



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


################################################################################

# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///company_insights'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")


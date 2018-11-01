
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
    cb_permalink = db.Column(db.String(300), nullable=False)
    cb_url = db.Column(db.String(300))
    # market_type_id = db.Column(db.Integer, db.ForeignKey('market_types.market_type_id'))
    state_code = db.Column(db.String(10))
    city_name = db.Column(db.String(50))
    first_funding = db.Column(db.DateTime)
    total_funding = db.Column(db.BigInteger)

    funding_rounds = db.relationship('FundingRound', backref=db.backref('cb_company'))
    company_markets = db.relationship('CompanyMarket', backref=db.backref('cb_company'))

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
    # market_type_id = db.Column(db.Integer, db.ForeignKey('market_types.market_type_id'))
    funded_amt = db.Column(db.String(25))
    funded_date = db.Column(db.DateTime)

    funding_type = db.relationship('FundingType', backref=db.backref('founding_rounds'))
    # market_type = db.relationship('MarketType')

    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_str = '<FundingRound: id:{}, cb_company_id:{}, funding_type_id:{}, funding_amt:{}>'
        return repr_str.format(self.funding_round_id, self.cb_company_id, self.funding_type_id, self.funded_amt)


class FundingType(db.Model):
    """ Crunchbase funding round type """

    __tablename__ = 'funding_types'

    funding_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    funding_type_name = db.Column(db.String(50), nullable=False)
    funding_type_code = db.Column(db.String(50))

    def __repr__(self):
        """Provide helpful representation when printed."""    
        
        repr_str = '<FundingType: id:{}, funding_type_name:{}>'
        return repr_str.format(self.funding_type_id, self.funding_type_name)


class MarketType(db.Model):
    """ Crunchbase market types """

    __tablename__ = 'market_types'

    market_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    market_type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""    
    
        repr_str = '<MarketType: id:{}, market_type:{}>'
        return repr_str.format(self.market_type_id, self.market_type)

class CompanyMarket(db.Model):
    """ Crunchbase market and company pairings """

    __tablename__ = 'company_markets'

    market_company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cb_company_id = db.Column(db.Integer, db.ForeignKey('cb_companies.cb_company_id'), nullable=False)
    market_type_id = db.Column(db.Integer, db.ForeignKey('market_types.market_type_id'), nullable=False)

    market_type = db.relationship('MarketType', backref=db.backref('company_markets'))

    def __repr__(self):
        """Provide helpful representation when printed."""    
    
        repr_str = '<CompanyMarket: id:{}, company_id: {}, market_type_id:{}>'
        return repr_str.format(self.market_company_id, self.cb_company_id, self.market_type_id)    


################################################################################
# Full Contact Data

class FCCompany(db.Model):
    """ Full Contact company info  """

    __tablename__ = 'fc_companies'

    fc_company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fc_company_name = db.Column(db.String(100), nullable=False)
    fc_company_domain = db.Column(db.String(100), nullable=False, unique=True) 
    fc_company_bio = db.Column(db.String(5000))
    logo_image_url = db.Column(db.String(300))
    location_city = db.Column(db.String(100))
    location_state_code = db.Column(db.String(50))
    founded = db.Column(db.String(25))
    num_employees = db.Column(db.String(25))
    cb_company_id = db.Column(db.Integer, db.ForeignKey('cb_companies.cb_company_id'))


    social_media = db.relationship('SMLink', backref=db.backref('fc_company'))
    company_links = db.relationship('CompanyLink', backref=db.backref('fc_company'))
    industries = db.relationship('CompanyIndustry', backref=db.backref('fc_companies'))
    cb_company = db.relationship('CBCompany', backref=db.backref('fc_company'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_str = '<FCCompany: id:{}, name:{}, location:{}>'
        return repr_str.format(self.fc_company_id, self.fc_company_name, self.location_city)


class SMLink(db.Model):
    """ Full Contact company social media sites  """

    __tablename__ = 'social_media'

    sm_link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'), nullable=False)
    sm_name = db.Column(db.String(50))
    sm_site_url = db.Column(db.String(300))
    sm_bio = db.Column(db.String(1000))

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
    link_url = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<CompanyLink: link_type:{}, fc_company_id:{}>'
        return repr_str.format(self.link_type, self.fc_company_id)


class IndustryType(db.Model):
    """ Full Contact industry types  """

    __tablename__ = 'industry_types'

    industry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    industry_name = db.Column(db.String(100), nullable=False, unique=True)

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

    industry_type = db.relationship('IndustryType')

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<CompanyIndustry: industry_id:{}, fc_company_id:{}>'
        return repr_str.format(self.industry_id, self.fc_company_id)



################################################################################

# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///company_insights_2'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)    
    db.create_all()

    print("Connected to DB.")



"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

################################################################################
# Full Contact Data

# class FCCompany(db.Model):
#     """ Full Contact company info  """

#     __tablename__ = 'fc_companies'

#     fc_company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     fc_company_name = db.Column(db.String(100), nullable=False)
#     fc_company_domain = db.Column(db.String(100), nullable=False) 
#     logo_image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'))
#     location = db.Column(db.String(300))
#     founded = db.Column(db.String(25))
#     num_employees = db.Column(db.String(25))
#     bio = db.Column(db.String(500))

#     social_media = db.relationship('SocialMediaLink', backref=db.backref('fc_company'))
#     companay_links = db.relationship('CompanyLink', backref=db.backref('fc_company'))
#     people = db.relationship('Person', backref=db.backref('fc_company'))
#     industries = db.relationship('CompanyIndustry', backref=db.backref('fc_companies'))
#     images = db.relationship('Image', backref=db.backref('fc_company'))
#     cb_company = db.relationship('CBCompany', backref=db.backref('fc_company'))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         repr_str = '<FCCompany: id:{}, name:{}, location:{}>'
#         return repr_str.format(self.fc_company_id, self.fc_company_name, self.location)


# class SocialMediaLink(db.Model):
#     """ Full Contact company social media sites  """

#     __tablename__ = 'social_media'

#     sm_link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'), nullable=False)
#     sm_type_id = db.Column(db.String(10), db.ForeignKey('social_media_sites.sm_type_id'), nullable=False)
#     sm_site_url = db.Column(db.String(200), nullable=False)

#     sm_type = db.relationship('SocialMediaType', backref=db.backref('social_media_links'))
#     image = db.relationship('Image')

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         repr_str = '<SocialMediaLink: sm_type_id:{}, fc_company_id:{}, sm_site_url:{}>'
#         return repr_str.format(self.sm_type_id, self.fc_company_id, self.sm_site_url)


# class SocialMediaType(db.Model):
#     """ Full Contact social media types  """

#     __tablename__ = 'sm_types'

#     sm_type_id = db.Column(db.String(10), primary_key=True)
#     sm_name = db.Column(db.String(100), nullable=False)
#     sm_logo_image_id = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         repr_str = '<SocialMediaType: sm_type_id:{}, sm_name:{}, sm_logo_image_id:{}>'
#         return repr_str.format(self.sm_type_id, self.sm_name, self.sm_logo_image_id)


# class CompanyLink(db.Model):
#     """ Full Contact company links  """

#     __tablename__ = 'company_links'

#     company_link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'), nullable=False)
#     link_type = db.Column(db.String(50), nullable=False)
#     link_url = db.Column(db.String(300), nullable=False)

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         repr_str = '<CompanyLink: link_type:{}, fc_company_id:{}>'
#         return repr_str.format(self.link_type, self.fc_company_id)


# class Person(db.Model):
#     """ Full Contact people """

#     __tablename__ = 'people'

#     person_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'), nullable=False)
#     title = db.Column(db.String(50))
#     person_image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'))

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         repr_str = '<People: person_id{}, fc_company_id:{}, title:{}>'
#         return repr_str.format(self.person_id, self.fc_company_id, self.title)


# class IndustryType(db.Model):
#     """ Full Contact industry types  """

#     __tablename__ = 'industry_types'

#     industry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     industry_name = db.Column(db.String(50), nullable=False)

#     fc_companies = db.relationship('CompanyIndustry', backref=db.backref('industry_name'))

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         repr_str = '<IndustryType: industry_id:{}, industry_name:{}>'
#         return repr_str.format(self.industry_id, self.industry_name)


# class CompanyIndustry(db.Model):
#     """ Full Contact companies with industries  """

#     __tablename__ = 'company_industries'

#     company_with_industry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     industry_id = db.Column(db.Integer, db.ForeignKey('industry_types.industry_id'), nullable=False)
#     fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'), nullable=False)

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         repr_str = '<CompanyIndustry: industry_id:{}, fc_company_id:{}>'
#         return repr_str.format(self.industry_id, self.fc_company_id)


# class Image(db.Model):
#     """ Full Contact images  """

#     __tablename__ = 'images'

#     image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     image_type = db.Column(db.String(50), nullable=False)
#     image_url = db.Column(db.String(300), nullable=False)

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         repr_str = '<Image: image_id:{}, image_type:{}>'
#         return repr_str.format(self.image_id, self.image_type)


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
    # market_type_id = db.Column(db.Integer, db.ForeignKey('market_types.market_type_id'))
    # state_code_id = db.Column(db.Integer, db.ForeignKey('state_codes.state_code_id'))
    # fc_company_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'))

    # funding_rounds = db.relationship('FundingRound', backref=db.backref('cb_company'))
    # hq_state_code = db.relationship('StateCode', backref=db.backref('cb_companies'))
    # market_type = db.relationship('MarketType', backref=db.backref('cb_companies'))

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
    funded_amt = db.Column(db.Integer, nullable=False)
    funded_date = db.Column(db.DateTime)

    funding_type = db.relationship('FundingType')

    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_str = '<FundingRound: id:{}, cb_company_id:{}, funding_type_id:{}, funding_amt:{}>'
        return repr_str.format(self.funding_round_id, self.cb_company_id, self.funding_type_id, self.funding_amt)


class FundingType(db.Model):
    """ Crunchbase funding round type """

    __tablename__ = 'funding_types'

    funding_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    funding_type_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""    
        
        epr_str = '<FundingType: id:{}, funding_type_name:{}>'
        return repr_str.format(self.funding_type_id, self.funding_type_name)


class StateCode(db.Model):
    """ Crunchbase state codes """

    __tablename__ = 'state_codes'

    state_code_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_code = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<StateCode: id:{}, state_code:{}>'
        return repr_str.format(self.state_code_id, self.state_code)


class MarketType(db.Model):
    """ Crunchbase market types """

    __tablename__ = 'market_types'

    market_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    market_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""    
    
        repr_str = '<MarketType: id:{}, market_type:{}>'
        return repr_str.format(self.market_type_id, self.market_type)


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


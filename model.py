
"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

# don't forget the backrefs!!!


class FCCompany(db.Model):
    """ Full Contact company info  """

    __tablename__ = 'fc_companies'

    fc_company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fc_company_name = db.Column(db.String(100), nullable=False)
    logo_image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'))
    location = db.Column(db.String(300))
    founded = db.Column(db.String(25))
    num_employees = db.Column(db.String(25))
    bio = db.Column(db.String(500))

    social_media = db.relationship('SocialMediaLink', backref=db.backref('fc_company'))
    companay_links = db.relationship('CompanyLink', backref=db.backref('fc_company'))
    people = db.relationship('Person', backref=db.backref('fc_company'))
    industries = db.relationship('CompanyIndustry', backref=db.backref('fc_companies'))
    images = db.relationship('Image', backref=db.backref('fc_company'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        repr_str = '<FCCompany: id:{}, name:{}, location:{}>'
        return repr_str.format(self.fc_company_id, self.fc_company_name, self.location)


class SocialMediaLink(db.Model):
    """ Full Contact company social media sites  """

    __tablename__ = 'social_media'

    fc_company_id = db.Column(db.Integer, nullable=False, db.ForeignKey('fc_companies.fc_company_id'))
    sm_type_id = db.Column(db.String(10), nullable=False, db.ForeignKey('social_media_sites.sm_type_id'))
    sm_site_url = db.Column(db.String(200, nullable=False))

    sm_type = db.relationship('SocialMediaType', backref=db.backref('social_media_links'))
    image = db.relationship('Image')

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<SocialMediaLink: sm_type_id:{}, fc_company_id:{}, sm_site_url:{}>'
        return repr_str.format(self.sm_type_id, self.fc_company_id, self.sm_site_url)


class SocialMediaType(db.Model):
    """ Full Contact social media types  """

    __tablename__ = 'sm_types'

    sm_type_id = db.Column(db.String(10), primary_key=True)
    sm_name = db.Column(db.String(100), nullable=False)
    sm_logo_image_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<SocialMediaType: sm_type_id:{}, sm_name:{}, sm_logo_image_id:{}>'
        return repr_str.format(self.sm_type_id, self.sm_name, self.sm_logo_image_id)


class CompanyLink(db.Model):
    """ Full Contact company links  """

    __tablename__ = 'company_links'

    fc_company_id = db.Column(db.Integer, nullable=False, db.ForeignKey('fc_companies.fc_company_id'))
    link_type = db.Column(db.String(50), nullable=False)
    link_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<CompanyLink: link_type:{}, fc_company_id:{}>'
        return repr_str.format(self.link_type, self.fc_company_id)


class Person(db.Model):
    """ Full Contact people """

    __tablename__ = 'people'

    person_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fc_company_id = db.Column(db.Integer, nullable=False, db.ForeignKey('fc_companies.fc_company_id'))
    title = db.Column(db.String(50))
    person_image_id = db.Column(db.Integer, db.ForeignKey('fc_companies.fc_company_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<People: person_id{}, fc_company_id:{}, title:{}>'
        return repr_str.format(self.person_id, self.fc_company_id, self.title)


class IndustryType(db.Model):
    """ Full Contact industry types  """

    __tablename__ = 'industry_types'

    industry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    industry_name = db.Column(db.String(50), nullable=False)

    fc_companies = db.relationship('CompanyIndustry', backref=db.backref('industry_name'))

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<IndustryType: industry_id:{}, industry_name:{}>'
        return repr_str.format(self.industry_id, self.industry_name)


class CompanyIndustry(db.Model):
    """ Full Contact companies with industries  """

    __tablename__ = 'company_industries'

    industry_id = db.Column(db.Integer, nullable=False, db.ForeignKey('industry_types.industry_id'))
    fc_company_id = db.Column(db.Integer, nullable=False, db.ForeignKey('fc_companies.fc_company_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<CompanyIndustry: industry_id:{}, fc_company_id:{}>'
        return repr_str.format(self.industry_id, self.fc_company_id)


class Image(db.Model):
    """ Full Contact images  """

    __tablename__ = 'images'

    imgage_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_type = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        repr_str = '<Image: image_id:{}, image_type:{}>'
        return repr_str.format(self.image_id, self.image_type)


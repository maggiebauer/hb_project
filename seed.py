"""Utility file to seed company_insights database from FullContact and Crunchbase data in seed_data/"""

from sqlalchemy import func
# from model import FCCompany
# from model import SocialMediaLink
# from model import SocialMediaType
# from model import CompanyLink
# from model import Person
# from model import IndustryType
# from model import CompanyIndustry
# from model import Image
from model import CBCompany
# from model import FundingRound
# from model import FundingType
# from model import StateCode
# from model import MarketType

from model import connect_to_db, db
# from server import app
import datetime
import csv


def load_cb_companies():
    """Load cbcompanies from seed_data/cbcompanies into database."""

    print("CBCompanies")

    # # Delete all rows in table, so if we need to run this a second time,
    # # we won't be trying to add duplicate users
    # User.query.delete()

    # Read cbcompanies.csv file and insert data
    company_csv = open('test_companies.csv')
    company_reader = csv.reader(company_csv)
    
    for row in company_reader:        
        cb_company = CBCompany(cb_company_name=row[1], 
                    cb_url=row[2],
                    cb_permalink=row[0])

    # We need to add to the session or it won't ever be stored
    #     db.session.add(cb_company)


    # # Once we're done, we should commit our work
    # db.session.commit()

"""Utility file to seed company_insights database from FullContact API and Crunchbase data csb in seed_data/"""

from sqlalchemy import func
from model import FCCompany
from model import SMLink
from model import CompanyLink
from model import IndustryType
from model import CompanyIndustry
from model import CBCompany
from model import FundingRound
from model import FundingType
from model import MarketType

from model import connect_to_db, db
from server import app
import datetime
import csv

###########################################################################
# Crunchbase data seeding


def load_market_types():
    """Load market types from seed_data/cbfundings into database."""

    print("MarketTypes")
    MarketType.query.delete()

    # Read cbrounds.csv file and insert data
    rounds_csv = open('test_rounds.csv')
    rounds_reader = csv.reader(rounds_csv)
    
    market_type_dict = {}

    for row in rounds_reader:  
        if row[2] not in market_type_dict:
            market_type_dict[row[2]] = True
            market_type = MarketType(market_type=row[2])
            
            db.session.add(market_type)
    db.session.commit()

def load_funding_types():
    """Load funding types from seed_data/cbfundings into database."""

    print("FundingTypes")
    FundingType.query.delete()

    funding_type_dict = {}

    # Read cbrounds.csv file and insert data
    rounds_csv = open('test_rounds.csv')
    rounds_reader = csv.reader(rounds_csv)

    for row in rounds_reader:  
        if (row[8], row[9]) not in funding_type_dict:
            funding_type_dict[(row[8], row[9])] = True
            funding_type = FundingType(funding_type_name=row[8], 
                            funding_type_code=row[9])       
            db.session.add(funding_type)
    
    db.session.commit()


def load_cb_companies():
    """Load cbcompanies from seed_data/cbcompanies into database."""

    print("CBCompanies")
    CBCompany.query.delete()

    # Read cbcompanies.csv file and insert data
    companies_csv = open('test_companies.csv')
    companies_reader = csv.reader(companies_csv)
    
    for row in companies_reader:        
        cb_company = CBCompany(cb_company_name=row[1].lower(), 
                    cb_url=row[2],
                    cb_permalink=row[0], 
                    state_code=row[7])
        db.session.add(cb_company)

    db.session.commit()


def load_cb_rounds():
    """Load cbrounds from seed_data/cbrounds into database."""

    print("CBRounds")
    FundingRound.query.delete()

    # Get funding types to populate foreign key for funding_rounds table
    all_funding_types = FundingType.query.all()
    funding_type_dict = {}

    for f_type in all_funding_types:
        funding_type_dict[(f_type.funding_type_name, f_type.funding_type_code)] = f_type.funding_type_id

    # Get market types to populate foreign key for market_types table
    all_market_types = MarketType.query.all()
    market_type_dict = {}

    for m_type in all_market_types:
        market_type_dict[m_type.market_type] = m_type.market_type_id

    # Get company ids for foreign key in the funding_rounds table
    all_company_ids = CBCompany.query.all()
    company_id_dict = {}

    for company in all_company_ids:
        company_id_dict[company.cb_permalink] = company.cb_company_id


    # Read cbrounds.csv file and insert data
    rounds_csv = open('test_rounds.csv')
    rounds_reader = csv.reader(rounds_csv)
    
    for row in rounds_reader:      
        cb_round = FundingRound(funded_amt=row[11],
                    funded_date=row[10], 
                    market_type_id=market_type_dict[row[2]],
                    cb_company_id=company_id_dict[row[0]],
                    funding_type_id=funding_type_dict[(row[8], row[9])])
        db.session.add(cb_round)

    db.session.commit()



############################################################################


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_market_types()
    load_funding_types()
    load_cb_companies()
    load_cb_rounds()





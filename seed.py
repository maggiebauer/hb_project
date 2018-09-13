"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import FCCompany
from model import SocialMediaLink
from model import SocialMediaType
from model import CompanyLink
from model import Person
from model import IndustryType
from model import CompanyIndustry
from model import Image
from model import CBCompany
from model import FundingRound
from model import FundingType
from model import StateCode
from model import MarketType

from model import connect_to_db, db
from server import app
import datetime
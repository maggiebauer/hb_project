from jinja2 import StrictUndefined
from flask import (Flask, request, flash, render_template, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import joinedload
import model as m
import util as u


app = Flask(__name__)
app.secret_key = 'ABC'
app.jinja_env.undefined = StrictUndefined

################################################################################
# app routes

@app.route('/')
def index():
    ''' Homepage '''

    return render_template('index.html')

@app.route('/search.json', methods=['POST'])
def search_cb_companies():
    ''' Search and display company '''

    def row_to_dict(row):
        row_dict = {}
        for column in row.__table__.columns:
            row_dict[column.name] = str(getattr(row, column.name))
        return row_dict
    
    comp_search = request.form.get('searchCompany')
    lst_comp_dicts = []
    
    if comp_search != ' ':
        poss_comp_lst = u.fetch_all_cb_companies(comp_search)

        for comp in poss_comp_lst:
            row_dict = row_to_dict(comp)
            lst_comp_dicts.append(row_dict)
    else:
        flash('Please enter a company name')
        return redirect('/')

    return jsonify(lst_comp_dicts)


@app.route('/company-profile.json', methods=['POST'])
def display_company_profile():
    ''' Check if the selected company exists in FCCompany already. If not, calls API. 
    Returns all data on company '''

    selected_cb_comp_id = int(request.form.get('selectedCompanyId'))

    # create a company info dict to store cb & fc info into that can be jsonified
    selected_comp_info_dict = {}

    joined_cb_data = (
        m.CBCompany.query.
        options(joinedload(m.CBCompany.funding_rounds).
            joinedload(m.FundingRound.funding_type)).
        options(joinedload(m.CBCompany.market_type)).
        filter(m.CBCompany.cb_company_id == selected_cb_comp_id).
        order_by(m.FundingRound.funded_date).
        first()
        )

    funding_rounds_lst = []

    # create list of funding rounds
    for item in joined_cb_data.funding_rounds:
        funding_round_dict = {
            'round_name': item.funding_type.funding_type_name,
            'funded_amount': item.funded_amt,
            'funded_date': item.funded_date,
            'funding_type_id': item.funding_type_id
        }
        funding_rounds_lst.append(funding_round_dict)

    # sort the list of funding dicts by date
    funding_rounds_lst.sort(key=lambda x: x['funded_date'])

    # add crunchbase info to selected_comp_info_dict
    selected_comp_info_dict['crunchbase'] = [
        {'cb_comp_name': joined_cb_data.cb_company_name},
        {'comp_url': joined_cb_data.cb_url},
        {'state': joined_cb_data.state_code},
        {'city': joined_cb_data.city_name},
        {'funding_rounds': funding_rounds_lst}
        ]

    # getting the funding rounds for similar market type/funding round companies
    # figure out latest round funding type id
    funding_type_id = funding_rounds_lst[-1]['funding_type_id']
    # figure out market type id
    market_type_id = joined_cb_data.market_type_id
    # query 
    same_market_type_funding_round = (
        m.FundingRound.query.options(
        joinedload(m.FundingRound.cb_company)).
        filter(
            m.FundingRound.funding_type_id==funding_type_id,
            m.FundingRound.market_type_id==market_type_id,
            m.FundingRound.cb_company_id!=selected_cb_comp_id,
            m.FundingRound.funded_amt!='').
        all()
    )

    market_research_data = []
    for funding_round in same_market_type_funding_round:
        market_research_data.append({
            'amount': funding_round.funded_amt,
            'date': funding_round.funded_date,
            'company_name': funding_round.cb_company.cb_company_name
        })
   
    selected_comp_info_dict['funding_market_research'] = market_research_data

    # check to see if fc info already stored in db
    check_fc_comp_db = ( 
        m.FCCompany.query.
        options(joinedload(m.FCCompany.social_media)).
        options(joinedload(m.FCCompany.company_links)).
        options(joinedload(m.FCCompany.industries).
            joinedload(m.CompanyIndustry.industry_type)).
        options(joinedload(m.FCCompany.cb_company)).
        filter(m.FCCompany.cb_company_id == selected_cb_comp_id).
        first()
        )

    # function that takes in the joined fc company objects and turns into a lst of dicts
    def create_fc_comp_info_lst(comp_obj):
        
        social_media_lst = []
        company_links_lst = []
        industry_lst = []

        for item in comp_obj.social_media:
            social_media_site = [
                {'site_name': item.sm_name},
                {'site_url': item.sm_site_url},
                {'site_bio': item.sm_bio}
                ]
            social_media_lst.append(social_media_site)

        for item in comp_obj.company_links:
            company_link_item = [
                {'link_type': item.link_type},
                {'link_url': item.link_url}
            ]
            company_links_lst.append(company_link_item)

        for item in comp_obj.industries:
            company_industry_item = [
                {'industry type': item.industry_type.industry_name}
            ]
            industry_lst.append(company_industry_item)

        fc_comp_info_lst = [
        {'fc_comp_name': comp_obj.fc_company_name},
        {'comp_domain': comp_obj.fc_company_domain},
        {'company_bio': comp_obj.fc_company_bio},
        {'logo_url': comp_obj.logo_image_url},
        {'founded': comp_obj.founded},
        {'employees': comp_obj.num_employees},
        {'social_media': social_media_lst},
        {'industries': industry_lst}
        ]

        return fc_comp_info_lst

    # checks if fc company exists in db or calls api and adds fc info to selected_comp_info_dict
    if check_fc_comp_db != None:
        joined_fc_data = create_fc_comp_info_lst(check_fc_comp_db)
        selected_comp_info_dict['fullcontact'] = joined_fc_data
    else:
        comp_domain = u.get_domain(joined_cb_data)
        
        api_comp_info = u.fetch_fc_company(comp_domain)

        # add to db
        u.load_fc_industry_types(api_comp_info)
        u.load_fc_company(api_comp_info, comp_domain, joined_cb_data.cb_company_id)
        u.db.session.commit()

        get_fc_comp_obj = ( 
            m.FCCompany.query.
            options(joinedload(m.FCCompany.social_media)).
            options(joinedload(m.FCCompany.company_links)).
            options(joinedload(m.FCCompany.industries).
                joinedload(m.CompanyIndustry.industry_type)).
            options(joinedload(m.FCCompany.cb_company)).
            filter(m.FCCompany.cb_company_id == selected_cb_comp_id).
            first()
        )

        joined_fc_data = create_fc_comp_info_lst(get_fc_comp_obj)

        selected_comp_info_dict['fullcontact'] = joined_fc_data

    return jsonify(selected_comp_info_dict)






################################################################################
# run file locally with debugger

if __name__ == "__main__":
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    m.connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
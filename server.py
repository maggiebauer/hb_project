from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
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
    # return render_template('homepage.html')
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

    selected_cb_comp_id = request.form.get('selectedCompanyId')

    all_selected_comp_info = []
    check_fc_comp_db = m.FCCompany.query.filter(m.FCCompany.cb_company_id == selected_cb_comp_id).first()
    print(check_fc_comp_db)

    if check_fc_comp_db != None:
        pass
    else:
        pass
    
    return jsonify(all_selected_comp_info)






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
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

@app.route('/search.json')
def search_cb_companies():
    ''' Search and display company '''
    
    comp_search = request.args.get('searchCompany')
    print(comp_search)
    
    if comp_search != ' ':
        poss_comp_lst = u.fetch_all_cb_companies(comp_search)

        # return render_template('search_page.html', poss_comp_lst=poss_comp_lst)
        # # print(jsonify(poss_comp_lst))
        return jsonify(poss_comp_lst)
    else:
        flash('Please enter a company name')
        return redirect('/')


@app.route('/company-profile')
def display_company_profile(company_obj):

    pass






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
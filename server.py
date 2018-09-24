from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session)
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
    return render_template('homepage.html')

@app.route('/search')
def search_cb_companies():
    ''' Search and display company '''
    
    comp_search = request.args.get('company_searched')
    
    poss_comp_lst = u.fetch_all_cb_companies(comp_search)

    return render_template('search_page.html', poss_comp_lst=poss_comp_lst)






################################################################################
# run file locally with debugger

if __name__ == "__main__":
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    m.connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')


class DisplayApp extends React.Component  {
  constructor(props)  {
    super(props);

    this.state = {
      searchCompany: '',
      searchResults: [],
      showCompProfile: false,
      companyProfileData: {},
    }
  };

  findCompany = (e) =>  {
    // callback function to find company entered into search bar
    e.preventDefault();

    const searchComp = this.state.searchCompany.toLowerCase();
    $.post('/search.json', { searchCompany : searchComp }, data =>  {
      this.setState({searchResults: data});
    });
  };

  setCompaniesArray = () =>  {
    // sets the array of companyies found in database from search bar input

    $.get('/search.json', data => {
      this.setState({compPreviewArray: data.searchCompany});
    });
  };

  setCompProfileData = (data) =>  {
    this.setState({companyProfileData: data});
    this.setState({showCompProfile: true}); 
  };


  render()  {
    return (
      <div>
        {!this.state.showCompProfile && <div>
          <form onSubmit={this.findCompany.bind(this)}>
            <div className="form-inputs">
              <input type="text" 
                name="search-comp"
                placeholder="Enter company name" 
                value={this.state.searchCompany} 
                required
                onChange={e => this.setState({  searchCompany: e.target.value })} 
              /> 
              <input type="submit" className="btn btn-primary" value="search" />
            </div>
          </form>

         <div className="container">
              <DisplaySearchResults 
                companies={this.state.searchResults} 
                handleResponse={this.setCompProfileData}
              />
          </div>
        </div>}

        {this.state.showCompProfile && <div className="container">
          <DisplayCompanyProfile 
            company={this.state.companyProfileData} 
          />
        </div>}

      </div>
      );
    }
};


const CompPreview = ( props ) =>  {

  return (
   <div className="card border-secondary mb-3">
      <div className="card-header">
          <span>
              <h3 className="card-title">{props.compName}</h3>
          </span>
      </div>
      <div className="card-body">
          <h4 className="card-title">Location: {props.compLocation}</h4>
          <span>
            <button type="button" className="btn btn-outline-secondary btn-lg btn-block">
              <a target="_blank" rel="noopener noreferrer" href={props.url}>{props.url}</a>
            </button>
          </span>
          <button type="button" className="btn btn-secondary center-btn" onClick={props.handleClick.bind(props)}>Select</button>
      </div>
  </div>
  )
};



class DisplaySearchResults extends React.Component  {
  constructor(props)  {
    super(props);

    this.state = {
      selectedCompanyId: '',
      compPreviewArray: [],
      showCompResults: false,
      companies: [],
    };
  }



  handleClick = (e, compId) => {
    // debugger
    // callback function
    e.preventDefault();

    const selectCompKey = compId;
    this.setState({selectedCompanyId: selectCompKey});

    $.ajax({
      type: 'POST',
      url: '/company-profile.json', 
      data: {
        selectedCompanyId: selectCompKey
      },
      success: data => {console.log(data);this.props.handleResponse(data)}
    });
  };

    

 
  checkForResults = () =>   {
      let compPreviewArray = [...this.state.compPreviewArray];
      if ( compPreviewArray != [] ) {
        this.setState({showCompResults: true});
      }
  };


  render()  {
    let comps = null;

    this.checkForResults;
    comps = (
      <div>
        {this.props.companies.map( (company, index) =>  {
          return ( 
            <CompPreview 
              compName={company['cb_company_name']}
              compLocation={company['city_name'] + ', ' + company['state_code']}
              url={company['cb_url']} 
              key={company['cb_company_id']}
              handleClick={(e) => this.handleClick(e, company['cb_company_id'])}
            />
          );
        })}
      </div>
      )
    return comps;
  }; 
    
};

const CompProfile = ( props ) =>  {
  return (
    <div className="container">
      <div className="bs-component">
        <span>{props.companyName}</span>
      </div>
    </div>
  )
};

class DisplayCompanyProfile extends React.Component  {
  constructor(props)  {
    super(props);

  }


  render()  {
    let profilePage = null;

      let company = this.props.company;
      return (
          <div>
            <CompProfile
              companyName={company['crunchbase'][0]['cb comp name']}
            />
          </div>
      );  
  };
};

ReactDOM.render(
  (
  <React.Fragment>
    <DisplayApp />
  </React.Fragment>
  ),
    document.getElementById('search-bar'),
);

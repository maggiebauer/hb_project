

class DisplaySearchBar extends React.Component  {
  constructor(props)  {
    super(props);

    this.state = {
      searchCompany: '',
      searchResults: [],
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

    $.get('/search.json${searchCompany}', data => {
      this.setState({compPreviewArray: data.searchCompany});
    });
  };


  render()  {
    return (
      <div>
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
          <DisplaySearchResults companies={this.state.searchResults} />
        </div>
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
          <button type="button" className="btn btn-secondary center-btn" onClick={props.handleClick}>Select</button>
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
      compProfile: [],
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
      success: data => {this.setState({compProfile: data})}
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

ReactDOM.render(
  (
  <React.Fragment>
    <DisplaySearchBar />
  </React.Fragment>
  ),
    document.getElementById('search-bar'),
);

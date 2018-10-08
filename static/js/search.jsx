

class DisplaySearchBar extends React.Component  {
  constructor(props)  {
    super(props);

    this.state = {
      searchCompany: '',
      searchResults: [],
    }
  }

  findCompany = (e) =>  {
    // callback function
    e.preventDefault();

    const searchComp = this.state.searchCompany.toLowerCase()
    $.post('/search.json', { 
      searchCompany : searchComp
    }, data =>  {
      this.setState({searchResults: data});
  })}

  setCompaniesLst = () =>  {
    $.get('/search.json${searchCompany}', data =>  {
      this.setState({compPreviewLst: data.searchCompany});
      })
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
}

// openLink = (e) => {


// }

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
              <a target="_blank" rel="noopener noreferrer" href={props.url}>{props.url}</a></button>
          </span>
          <button type="button" className="btn btn-secondary center-btn" onClick={props.click}>Select</button>
      </div>
  </div>
  )
};



class DisplaySearchResults extends React.Component  {
  constructor(props)  {
    super(props);

    this.state = {
      selectedCompany: '',
      compPreviewLst: [],
      showCompResults: false,
      companies: [],
    }
  }


  selectCompany = (event, selectCompanyIndex, id) => {
    console.log('I\'m in the selectCompany function');
    const compPreviewLst = [...this.state.compPreviewLst];
    this.setState({selectedCompany: compPreviewLst[selectCompanyIndex]});
    }

 
  checkForResults = () =>   {
      const compPreviewLst = [...this.state.compPreviewLst]
      if ( compPreviewLst != [] ) {
        this.setState({showCompResults: true});
      }
    }


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
            click={(event) => this.selectCompany(event, index, key)} />
            );
          })}
      </div>
      )
    return comps;
  }; 
    
}

ReactDOM.render(
  (
  <React.Fragment>
    <DisplaySearchBar />
  </React.Fragment>
  ),
    document.getElementById('search-bar'),
);



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
      success: data => {this.props.handleResponse(data)}
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
      <div className="jumbotron">
        <span><img src={props.compLogo} alt="logo" /></span>

        <div className="card text-white bg-secondary mb-3">
    
          <h1 className="card-header">{props.compName}</h1>
  
          <div className="card-body">
            <h4 className="card-title">{props.compBio}</h4>
          
            <span className="card-text">
              <div>Industry: {props.compIndustry}</div>
              <div>Founded: {props.compFounded}</div>
              <div>Location: {props.compLocation}</div>
              <div>Website: 
                <a target="_blank" rel="noopener noreferrer" href={props.compUrl}> {props.compDomain}</a>
              </div>
              <div>Company Size: {props.compEmployees}</div>
           </span>
        
          </div>
        </div>
      </div>
    </div>
  )
};

const CompSMLinks = ( props ) =>  {
  return (
    <div className="card text-white bg-secondary mb-3">
      <div className="card-header">
        <img src={props.smLogoImg} />
      </div>
      <div className="card-body">
        <div>{props.smBio}</div>
        <div>{props.smUrl}</div>
        <button type="button" className="btn btn-primary" onClick={props.handleClick}>Go to Site</button>
      </div>
    </div>
    );
};

const smSiteLogos =  {
  'linkedincompany': 'https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo.svg',
  'twitter': 'https://upload.wikimedia.org/wikipedia/commons/5/51/Twitter_logo.svg',
  'angellist': 'https://d22wwjbips5bcw.cloudfront.net/assets/shared/AngelList-1f53479b7b3bd75d55d9dd0d396a738b1a6943a7885dcd2fa3e4f1adb048f61e.png',
  'crunchbasecompany': 'https://upload.wikimedia.org/wikipedia/commons/a/a0/CrunchBase.svg',
  'instagram': 'http://www.edigitalagency.com.au/wp-content/uploads/instagram-logo-text-black-png-300x86.png',
  'owler': 'http://www.isalesman.com/dev/wp-content/uploads/2016/04/owlerlogo_highresolution-1-300x158.png',
  'facebook': 'https://upload.wikimedia.org/wikipedia/commons/8/87/Facebook_Logo_%282015%29_light.svg',
  'glassdoor': 'https://upload.wikimedia.org/wikipedia/commons/d/d2/Glassdoor_logo.png',
};

class DisplayCompanyProfile extends React.Component  {
  constructor(props)  {
    super(props);

  };

  selectLogo = ( smName ) =>  {
    for (let key of Object.keys(smSiteLogos))  {
      if (key === smName)  {
        return smSiteLogos[key];
      }
    }
  };

  handleClick = (e, url) =>  {
    window.open(url, '_blank')
  };


  render()  {
    let profilePage = null;

    let company = this.props.company;
    let compSMLinks = [...this.props.company['fullcontact'][6]['social_media']];
    let socialMedia = null;

    socialMedia = compSMLinks.map((compSmLink, index) =>  {
      console.log(compSmLink);
      return(
        <div>
          <CompSMLinks
            key={compSmLink[1]['site url']}
            smLogoImg={this.selectLogo(compSmLink[0]['site name'])}
            smUrl={compSmLink[1]['site url']}
            smBio={compSmLink[2]['site_bio']}
            handleClick={(e) => this.handleClick(e, compSmLink[1]['site url'])}
          />
        </div>
        )
    });


    return (
      <div>
        <CompProfile
          key={company['fullcontact'][1]['comp domain']}
          compIndustry={company['fullcontact'][7]['industries'][0][0]['industry type']}
          compLogo={company['fullcontact'][3]['logo url']}
          compName={company['crunchbase'][0]['cb comp name']}
          compBio={company['fullcontact'][2]['company bio']}
          compFounded={company['fullcontact'][4]['founded']}
          compLocation={company['crunchbase'][3]['city'] + ', ' + company['crunchbase'][2]['state']}
          compDomain={company['fullcontact'][1]['comp domain']}
          compUrl={company['crunchbase'][1]['comp url']}
          compEmployees={company['fullcontact'][5]['employees']}
        />
        <div className="jumbotron">
          {socialMedia}
        </div>
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

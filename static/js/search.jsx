import _ from 'lodash';
import React from 'react';
import ReactDOM from 'react-dom';
import {Doughnut, Scatter} from 'react-chartjs-2';

function titleCase(str)  {
   let splitStr = str.toLowerCase().split(' ');
   for (let i = 0; i < splitStr.length; i++)  {
       splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
   }
   return splitStr.join(' '); 
}

class DisplayApp extends React.Component  {
  constructor(props)  {
    super(props);

    // highest level state
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
    // sets the data used to display company profile when received from the server 

    this.setState({companyProfileData: data});
    this.setState({showCompProfile: true}); 
  };

  // renders the Display App components and all child components
  render()  {
    return (
      <div>

        <div>
          <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
              <div className="container">
              <a className="navbar-brand" href="http://localhost:5000/">GigSaw</a>        
            </div>
          </nav>
        </div>

        <div>
          {!this.state.showCompProfile && <div className="container">
            <h2 className="chart-title front-page-1">You found the company. You saw their deets.</h2>
            <h2 className="chart-title front-page-2">You got the gig.</h2>
            <form onSubmit={this.findCompany.bind(this)}>
              <div className="form-inputs">
                <input type="text" 
                  name="search-comp"
                  placeholder="Search Companies" 
                  value={this.state.searchCompany} 
                  required
                  onChange={e => this.setState({  searchCompany: e.target.value })} 
                  className="search-bar"
                /> 
                <input type="submit" className="btn btn-primary" value="Search" />
              </div>
            </form>

           <div>
                <DisplaySearchResults 
                  companies={this.state.searchResults} 
                  handleResponse={this.setCompProfileData}
                />
            </div>
          </div>}

          {this.state.showCompProfile && <div className="new-background">
            <DisplayCompanyProfile 
              company={this.state.companyProfileData} 
            />
          </div>}
        </div>
      </div>
    );
    }
};


const CompPreview = ( props ) =>  {
  // displays company preview and captures selected company
  return (
   <div className="card border-secondary mb-3">
      <div className="card-header">
          <span>
              <h2 className="card-title">{props.compName}</h2>
          </span>
      </div>
      <div className="card-body">
          <h4 className="card-subtitle">Location: {props.compLocation}</h4>
          <div>
            <h5>Industries: {props.compIndustries}</h5>
          </div>
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

    // handles state for the DisplaySearchResults component
    this.state = {
      selectedCompanyId: '',
      compPreviewArray: [],
      showCompResults: false,
      companies: [],
    };
  }

  handleClick = (e, compId) => {
    // debugger
    // callback function to capture selected company and update the companyProfileData state
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

  // renders the list of possible companies to have profile displayed
  render()  {
    let comps = null;

    this.checkForResults;
    comps = (
      <div className="search-cards col-7">
        {this.props.companies.map( (company, index) =>  {
          return ( 
            <CompPreview 
              compName={titleCase(company['cb_company_name'])}
              compLocation={company['city_name'] + ', ' + company['state_code']}
              compIndustries={company['markets']}
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

// component for the general company to be displayed on profile page
const CompProfile = ( props ) =>  {
  return (
    <div className="container col-6">
      
      <span><img src={props.compLogo} alt="logo" /></span>

      <div className="card text-white bg-secondary mb-3">
        <h1 className="card-header">{props.compName}</h1>
        
        <div className="card-body">
          <h4 className="card-title">{props.compBio}</h4>    
          <span className="card-text">
            <div>Markets: {props.compMarket}</div>
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
  )
};

// component for the social media links cards to be displayed on the profile page
const CompSMLinks = ( props ) =>  {
  return (
    <div className="card text-white bg-secondary mb-3">
      <div className="card-header">
        <img src={props.smLogoImg} className="sm-logos" />
      </div>
      <div className="card-body">
        <div className="sm-bio"><h5>{props.smBio}</h5></div>
        <div>{props.smUrl}</div>
        <button type="button" className="btn btn-primary sm-buttons" onClick={props.handleClick}>Go to the Site</button>
      </div>
    </div>
    );
};

// chart for company funding
const CompFundingChart = ( props ) => {
  return(

    <div className="col-6">
      <div className="chart-title">
        <h2 className="chart-title">Total Funding: ${props.totalFunding}</h2>
      </div>
      <Doughnut 
        data={props.compData}
        width={20}
        height={20}
        options={{}}
        />
    </div>
  );
}

const MarketFundingChart = ( props ) => {
  return(
    <div>
      <Scatter 
        data={props.compMarketData}
        width={50}
        height={15}
        options={{}}
      />
    </div>
  );
}

// object of social media sites and the links to their logo images
const smSiteLogos =  {
  'linkedincompany': 'https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo.svg',
  'twitter': 'https://upload.wikimedia.org/wikipedia/commons/5/51/Twitter_logo.svg',
  'angellist': 'https://d22wwjbips5bcw.cloudfront.net/assets/shared/AngelList-1f53479b7b3bd75d55d9dd0d396a738b1a6943a7885dcd2fa3e4f1adb048f61e.png',
  'crunchbasecompany': 'https://upload.wikimedia.org/wikipedia/commons/a/a0/CrunchBase.svg',
  'instagram': 'http://www.edigitalagency.com.au/wp-content/uploads/instagram-logo-text-black-png-300x86.png',
  'owler': 'http://www.isalesman.com/dev/wp-content/uploads/2016/04/owlerlogo_highresolution-1-300x158.png',
  'facebook': 'https://upload.wikimedia.org/wikipedia/commons/8/87/Facebook_Logo_%282015%29_light.svg',
  'glassdoor': 'https://upload.wikimedia.org/wikipedia/commons/d/d2/Glassdoor_logo.png',
  'youtube': 'https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg',
  'foursquare': 'https://upload.wikimedia.org/wikipedia/commons/d/dc/Foursquare_logo.svg',
  'google': 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Google_Plus_logo.svg',
  'pinterest': 'https://upload.wikimedia.org/wikipedia/commons/3/35/Pinterest_Logo.svg',
  'klout': 'https://upload.wikimedia.org/wikipedia/commons/a/ae/Klout_logo.svg',
  'gravatar': 'https://automattic.files.wordpress.com/2005/12/gravatar.png',
};


class DisplayCompanyProfile extends React.Component  {
  constructor(props)  {
    super(props);

  };

  selectLogo = ( smName ) =>  {
    // selects logo based on social media site name

    for (let key of Object.keys(smSiteLogos))  {
      if (key === smName)  {
        return smSiteLogos[key];
      }
    }
  };

  handleClick = (e, url) =>  {
    // opens social media site url in new window when button is clicked

    window.open(url, '_blank');
  }

  // renders the full company profile page
  render()  {
    let profilePage = null;

    let company = this.props.company;
    let compSMLinks = [...this.props.company['fullcontact'][6]['social_media']];
    let socialMedia = null;

    socialMedia = compSMLinks.map((compSmLink, index) =>  {
      // console.log(compSmLink);
      return(
        <div className="col-4">
          <CompSMLinks
            key={compSmLink[1]['site_url']}
            smLogoImg={this.selectLogo(compSmLink[0]['site_name'])}
            smUrl={compSmLink[1]['site_url']}
            smBio={compSmLink[2]['site_bio']}
            handleClick={(e) => this.handleClick(e, compSmLink[1]['site_url'])}
          />
        </div>
        )
    });


    return (
      <div>
        <div className="jumbotron">
        <div className="row">
          <CompProfile 
            key={company['fullcontact'][1]['comp_domain']}
            compMarket={company['crunchbase'][6]['markets']}
            compLogo={company['fullcontact'][3]['logo_url']}
            compName={titleCase(company['crunchbase'][0]['cb_comp_name'])}
            compBio={company['fullcontact'][2]['company_bio']}
            compFounded={company['fullcontact'][4]['founded']}
            compLocation={company['crunchbase'][3]['city'] + ', ' + company['crunchbase'][2]['state']}
            compDomain={company['fullcontact'][1]['comp_domain']}
            compUrl={company['crunchbase'][1]['comp_url']}
            compEmployees={company['fullcontact'][5]['employees']}
          />
          <CompFundingChart 
            totalFunding={company['crunchbase'][5]['total_funding']}
            compData={company['comp_funding_rounds_data']}
          />
        </div>
        </div>

        <div className="jumbotron market-chart">
          <h1 className="chart-title">Market Type Funding Comparison</h1>
          <MarketFundingChart
            compMarketData={company['mrkt_funding_research']}
          />
          <h4 className="chart-axis">Months since initial funding</h4>
        </div>
        <div className="jumbotron">
          <h1 className="chart-title">Social Media Sites</h1>
          <div className="row">
            {socialMedia}
          </div>
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

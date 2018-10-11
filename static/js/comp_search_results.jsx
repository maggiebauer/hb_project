

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

  // setComps = () =>    {
  //   let comps = null;
  //   if ( compPreviewLst != [] )  {
  //     this.setState.showCompResults: true;
  //   }
  //   if ( this.state.showCompResults ) {
  //     comps = ( this.state.companies.map( (company, index) =>  {

  //     }

  //       )
  //       )
  //   }
  // }
  checkForResults = () =>   {
      const compPreviewLst = [...this.state.compPreviewLst]
      if ( compPreviewLst != [] ) {
        this.setState({showCompResults: true});
      }
    }


  render()  {
    let comps = null;

    this.checkForResults;

    if ( this.state.showCompResults )   {
      comps = (
        <div>
          {this.state.companies.map( (company, index) =>  {
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
    )}}; 
    
}

ReactDOM.render(
  (
  <React.Fragment>
    <DisplaySearchResults />
  </React.Fragment>
  ),
    document.getElementById('search-results'),
);

export default DisplaySearchResults;
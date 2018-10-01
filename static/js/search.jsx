"use strict";

function findCompany(evt)  {
  // callback function
  const getSearchedComp = () => {
    $.get('/search.json${searchCompany}', data => {
      const comp = data.searchCompany;
    })
  }
}


class DisplaySearchBar extends React.Component  {
  constructor(props)  {
    super(props);

    this.state = {
      searchCompany: '',
    }
  }

  render()  {
    return (
      <form>
        <div className="form-inputs">
        <input type="text" 
          placeholder="Enter company name" 
          value={this.state.searchCompany} 
          required
          onChange={e => this.setState({  searchCompany: e.target.value })} 
        /> 
        <input type="submit" className="btn btn-primary" value="search" onClick={findCompany}/>
        </div>
      </form>
      );
    }
}

ReactDOM.render(
  (
  <React.Fragment>
    <DisplaySearchBar />,
  </React.Fragment>
  ),
    document.getElementById('search-bar'),
);


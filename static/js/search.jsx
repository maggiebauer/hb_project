"use strict";


class DisplaySearchBar extends React.Component  {
  constructor(props)  {
    super(props);

    this.state = {
      searchCompany: '',
    }
  }

  findCompany(e)  {
    // callback function
    console.log('say hello');
    const searchComp = this.state.searchCompany.toLowerCase()
    $.get('/search.json', { 
      searchCompany : searchComp
      })
   // }
  }

  render()  {
    return (
      <form>
        <div className="form-inputs">
        <input type="text" 
          name="search-comp"
          placeholder="Enter company name" 
          value={this.state.searchCompany} 
          required
          onChange={e => this.setState({  searchCompany: e.target.value })} 
        /> 
        <input type="submit" className="btn btn-primary" value="search" onClick={this.findCompany.bind(this)}/>
        </div>
      </form>
      );
    }
}

ReactDOM.render(
  (
  <React.Fragment>
    <DisplaySearchBar />
  </React.Fragment>
  ),
    document.getElementById('search-bar'),
);


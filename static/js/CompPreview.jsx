"use strict";


const compPreview = ( props ) =>  {
    return (
     <div className="card text-white bg-secondary mb-3" style="max-width: 20rem;">
        <div className="card-header">
            <span>
                <h2 className="card-title">{props.compName}</h2>
            </span>
        </div>
        <div className="card-body">
            <h4 className="card-title">{props.compLocation}</h4>
            <p className="card-text"><a href={props.url} onClick={() => window.open(this.props.url, '_blank')}/>{props.url}</p>
            <button type="button" className="btn btn-secondary" onClick={props.click}>Select</button>
        </div>
    </div>
    )
};

export default compPreview;
import React from 'react';

import ContributionMatrix from './Contribution/ContributionMatrix.jsx';
import CommitMatrix from './Commit/CommitMatrix.jsx';
import ContainerComponent from './ContainerComponent.jsx';
import IssueContributionMatrix from './Contribution/IssueContributionMatrix.jsx';
import MergeRequestContributionMatrix from './Contribution/MergeRequestContributionMatrix.jsx';

/**
 * A component that displays the activity tables.
 */
export default class ActivityMatrix extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div>
                <ContainerComponent
                    title={"Code & Commit Contribution Comparison Matrices"}>
                    <ContributionMatrix data={this.props.data}/>
                    <hr></hr>
                    <CommitMatrix data={this.props.data}/>
                    <hr style={{marginBottom: '-0.25rem'}}></hr>
                    <small className="d-block text-left mt-3" style={{float: 'left'}}>
                        &nbsp;<span className="info-block"
                                    style={{backgroundColor: '#ea7266'}}>&nbsp;</span> Below
                        average (&lt;50%)&nbsp;
                        &nbsp;<span className="info-block"
                                    style={{backgroundColor: '#f5da85'}}>&nbsp;</span> Above
                        average ({'>'}200%)&nbsp;
                        &nbsp;<span className="info-block"
                                    style={{backgroundColor: '#69b1ff'}}>&nbsp;</span> Needs
                        attention&nbsp;
                    </small>
                    <small className="d-block text-right mt-3">
                <span>The contributions are based off the master branch. The commits are based off
                    all branches. <br/> Reverting commits may significantly skew contribution data.</span>
                    </small>
                </ContainerComponent>
                {!this.props.data.matrix.merge_requests || !this.props.data.matrix.issues || Object.keys(this.props.data.matrix.merge_requests).length == 0 || Object.keys(this.props.data.matrix.issues).length == 0 ? null :
                    <ContainerComponent
                        title={"Issues & Merge Requests Contribution Comparison Matrices"}>
                        {/*<div className="matrix bordered-box">*/}
                        {/*    {generateMatrix(data.matrix.issues)}*/}
                        {/*</div>*/}
                        <IssueContributionMatrix data={this.props.data}/>
                        <hr></hr>
                        <MergeRequestContributionMatrix data={this.props.data}/>
                        {/*<div className="matrix bordered-box">*/}
                        {/*    {generateMatrix(data.matrix.merge_requests)}*/}
                        {/*</div>*/}
                        <hr style={{marginBottom: '-0.25rem'}}></hr>
                        <small className="d-block text-left mt-3" style={{float: 'left'}}>
                            &nbsp;<span className="info-block"
                                        style={{backgroundColor: '#ea7266'}}>&nbsp;</span> Below
                            average (&lt;50%)&nbsp;
                            &nbsp;<span className="info-block"
                                        style={{backgroundColor: '#f5da85'}}>&nbsp;</span> Above
                            average ({'>'}200%)&nbsp;
                            &nbsp;<span className="info-block"
                                        style={{backgroundColor: '#69b1ff'}}>&nbsp;</span> Needs
                            attention&nbsp;
                        </small>
                        <small className="d-block text-right mt-3">
                <span>Both the issue contribution matrix and the merge requests matrix
                    only lists users <br/> that have created issues or merge requests (respectively) at some point.</span>
                            {/*The merge requests matrix only lists users that have created a merge requests at some point.</span>*/}
                        </small>
                    </ContainerComponent>}
            </div>
        );
    }
}
import React from 'react';

import ContributionMatrix from './ContributionMatrix.jsx';
import CommitMatrix from './CommitMatrix.jsx';
import ContainerComponent from './ContainerComponent.jsx';
import IssueContributionMatrix from './IssueContributionMatrix.jsx';
import MergeRequestContributionMatrix from './MergeRequestContributionMatrix.jsx';

const generateMatrix = (targetData) => {
  const dataKeys = Object.keys(targetData);

  const totalKeys = Object.keys(targetData).length;

  const head = dataKeys.map((key, index) => {
    return (
        <th key={index}
            style={{borderRight: totalKeys - 1 == index ? 'none' : ''}}>{key}</th>
    );
  });

  const sharedObject = dataKeys.map((user) => {
    return targetData[user]
  })[0];

  const bodyData = Object.keys(sharedObject).map((key, index) => {
    return (
        <tr key={index}>
          <td style={{borderLeft: 'none'}}>{key}</td>
          {dataKeys.map((user, subIndex) => {
            return (
                <td key={subIndex}
                    style={{borderRight: totalKeys - 1 == subIndex ? 'none' : ''}}>{targetData[user][key].toFixed(1)}</td>
            )
          })}
        </tr>
    );
  });

  return (
    <table>
    <colgroup>
    <col style={{width: '20%'}}/>
    </colgroup>
      <thead>
        <tr>
          <th style={{borderLeft: 'none'}}>&nbsp;</th>
          {head}
        </tr>
      </thead>
      <tbody>
        {bodyData}
      </tbody>
    </table>
  );
};

export default class ActivityMatrix extends React.Component {

  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    return (
      <div>
        <ContainerComponent title={"Code & Commit Contribution Matrices"}>
            <ContributionMatrix />
            <hr></hr>
            <CommitMatrix />
            <hr style={{marginBottom: '-0.25rem'}}></hr>
            <small className="d-block text-left mt-3" style={{float: 'left'}}>
                &nbsp;<span className="info-block" style={{backgroundColor: '#ea7266'}}>&nbsp;</span> Below average (&lt;50%)&nbsp;
                &nbsp;<span className="info-block" style={{backgroundColor: '#f5da85'}}>&nbsp;</span> Above average (>200%)&nbsp;
                &nbsp;<span className="info-block" style={{backgroundColor: '#69b1ff'}}>&nbsp;</span> Needs attention&nbsp;
            </small>
            <small className="d-block text-right mt-3">
                <span>The contributions are based off the master branch. The commits are based off
                    all branches. <br /> Reverting commits may significantly skew contribution data.</span>
            </small>
        </ContainerComponent>
        <ContainerComponent title={"Issues & Merge Requests Contribution Matrices"}>
            {/*<div className="matrix bordered-box">*/}
            {/*    {generateMatrix(data.matrix.issues)}*/}
            {/*</div>*/}
            <IssueContributionMatrix />
            <hr></hr>
            <MergeRequestContributionMatrix />
            {/*<div className="matrix bordered-box">*/}
            {/*    {generateMatrix(data.matrix.merge_requests)}*/}
            {/*</div>*/}
            <hr style={{marginBottom: '-0.25rem'}}></hr>
            <small className="d-block text-left mt-3" style={{float: 'left'}}>
                &nbsp;<span className="info-block" style={{backgroundColor: '#ea7266'}}>&nbsp;</span> Below average (&lt;50%)&nbsp;
                &nbsp;<span className="info-block" style={{backgroundColor: '#f5da85'}}>&nbsp;</span> Above average (>200%)&nbsp;
                &nbsp;<span className="info-block" style={{backgroundColor: '#69b1ff'}}>&nbsp;</span> Needs attention&nbsp;
            </small>
            <small className="d-block text-right mt-3">
                <span>Both the issue contribution matrix and the merge requests matrix
                    only lists users <br /> that have created issues or merge requests (respectively) at some point.</span>
                {/*The merge requests matrix only lists users that have created a merge requests at some point.</span>*/}
            </small>

        </ContainerComponent>
      </div>
    );
  }
}
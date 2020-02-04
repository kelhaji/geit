import React from 'react';
import { sum, std, median }  from 'mathjs';

const cutEmail = (email) => {
    return email.split('@')[0]
};

const capitalize = (s) => {
  if (typeof s !== 'string') return ''
  return s.charAt(0).toUpperCase() + s.slice(1)
};

const formattedName = (name) => {
    return capitalize(name.replace(/_/g, ' '))
};

const generateContributionMatrix = (targetData) => {
  const dataKeys = Object.keys(targetData);

    // https://stackoverflow.com/questions/21700773/javascripts-sort-method-handling-of-capital-letters
    dataKeys.sort(function (a, b) {
        return a.localeCompare(b);
    });

  const totalKeys = Object.keys(targetData).length;

  const head = dataKeys.map((key, index) => {
    return (
        <th key={index}
            style={{borderRight: totalKeys - 1 == index ? 'none' : '', width: '100px'}}>{cutEmail(key)}</th>
    );
  });

  const sharedObject = dataKeys.map((user) => {
    return targetData[user]
  })[0];

  const bodyData = Object.keys(sharedObject).map((key, index) => {
    const allDataPoints = dataKeys.map((user) => {
     return targetData[user][key];
    });

    const mean = sum(allDataPoints) / allDataPoints.length;
    const poorlyPerformingThreshold = mean - 0.5 * mean;
    const overPerformingThreshold = 2 * mean;

    const performanceColor = (value) => {
        if (key == 'large_commit_ratio') {
            if (value > 0.10) {
                return '#69b1ff';
            } else {
                return '';
            }
        }

        if (key == 'median_committed_lines' || key == 'average_committed_lines') {
            if (value >= 500) {
                return '#69b1ff';
            } else {
                return '';
            }
        }

        if (value >= overPerformingThreshold) {
            return '#f5da85';
        }

        if (value <= poorlyPerformingThreshold) {
            return '#ea7266';
        }

        return '';
    };

    return (
        <tr key={index}>
          <td style={{borderLeft: 'none'}}>{formattedName(key)}</td>
          {dataKeys.map((user, subIndex) => {
            return (
                <td key={subIndex}
                    style={{borderRight: totalKeys - 1 == subIndex ? 'none' : '',
                    backgroundColor: performanceColor(targetData[user][key])}}
                    >{key == 'total_commits' ? targetData[user][key] : targetData[user][key].toFixed(2)}</td>
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

export default class CommitMatrix extends React.Component {

  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    return (
        <div className="matrix" style={{marginTop: '10px'}}>
            {generateContributionMatrix(data.matrix.committs)}
        </div>
    );
  }
}
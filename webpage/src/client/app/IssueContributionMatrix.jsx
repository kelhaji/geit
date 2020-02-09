import React from 'react';
import Util from './Util.js';

const generateContributionMatrix = (targetData) => {
    const dataKeys = Object.keys(targetData);

    dataKeys.sort(function (a, b) {
        return a.localeCompare(b);
    });

    const totalKeys = Object.keys(targetData).length;

    const head = dataKeys.map((key, index) => {
        return (
            <th key={index}
                style={{
                    borderRight: totalKeys - 1 === index ? 'none' : '',
                    width: '100px'
                }}>
                {Util.cutEmail(key)}
            </th>
        );
    });

    const sharedObject = dataKeys.map((user) => {
        return targetData[user]
    })[0];

    const bodyData = Object.keys(sharedObject).map((key, index) => {
        const allDataPoints = dataKeys.map((user) => {
            return targetData[user][key];
        });

        const mean = Util.sum(allDataPoints) / allDataPoints.length;
        const poorlyPerformingThreshold = mean - 0.5 * mean;
        const overPerformingThreshold = 2 * mean;

        const performanceColor = (value) => {
            if (key === 'total_issues_self_assigned_only') {
                return '';
            }

            if (key === 'total_issues_without_milestones' ||
                key === 'total_issues_without_labels' ||
                key === 'total_issues_without_description' ||
                key === 'total_issues_without_assignee') {
                if (value > 0) {
                    return '#69b1ff';
                } else {
                    return '';
                }
            }

            if (key === 'median_committed_lines' || key === 'average_committed_lines') {
                if (value >= 500) {
                    return '#69b1ff';
                } else {
                    return '';
                }
            }

            if (value > overPerformingThreshold) {
                return '#f5da85';
            }

            if (value < poorlyPerformingThreshold) {
                return '#ea7266';
            }

            return '';
        };

        const keysWithFixedValues = ['average_time_in_hours_estimated_on_issues',
            'average_time_in_hours_all_assignees_spent_on_issues',
            'total_time_spent_in_hours_individually_on_all_issues',
            'average_assignees_per_issue'];

        return (
            <tr key={index}>
                <td style={{borderLeft: 'none'}}>{Util.formattedName(key)}</td>
                {dataKeys.map((user, subIndex) => {
                    return (
                        <td key={subIndex}
                            style={{
                                borderRight: totalKeys - 1 === subIndex ? 'none' : '',
                                backgroundColor: performanceColor(targetData[user][key])
                            }}
                        >
                            {keysWithFixedValues.includes(key) ?
                                targetData[user][key].toFixed(2) : targetData[user][key]}
                        </td>
                    );
                })}
            </tr>
        );
    });

    return (
        <table>
            <colgroup>
                <col style={{width: '35%'}}/>
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

export default class IssueContributionMatrix extends React.Component {

    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div className="matrix" style={{marginTop: '10px'}}>
                {generateContributionMatrix(data.matrix.issues)}
            </div>
        );
    }
}
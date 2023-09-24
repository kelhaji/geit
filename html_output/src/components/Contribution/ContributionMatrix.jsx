import React from 'react';
import Util from '../../logic/Util.js';

/**
 * Renders a contribution matrix from the Geit data.
 */
export default class ContributionMatrix extends React.Component {

    /**
     * Get the performance color for a specific cell in the matrix.
     * 
     * @param {string} key 
     * @param {string} user 
     * @param {object} allDataPoints 
     * @param {object} targetData 
     * @returns hex color code
     */
    getPerformanceColor(key, user, allDataPoints, targetData) {
        const total = Util.sum(allDataPoints);    
        const mean = total / allDataPoints.length;
        const poorlyPerformingThreshold = mean - 0.5 * mean;
        const overPerformingThreshold = 2 * mean;

        const value = targetData[user][key];

        // The color #69b1ff is red
        if (total == 0 && (key === 'code' || key === 'test' || key == 'comments')) {
            return '#69b1ff';
        }

        if (total == 0 && (key === 'user_interface' || key === 'documentation' || key == 'configuration')) {
            return '';
        }

        if ((key === 'code' || key === 'test' || key === 'comments') && value === 0) {
            return '#69b1ff';
        }

        // Based off https://everything2.com/title/comment-to-code+ratio
        if (key === 'comments') {
            const commentRatio = value / (targetData[user]['code'] + targetData[user]['test']);

            if (commentRatio < 0.09) {
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
    }

    render() {
        const matrixContribution = this.props.data.matrix.contribution_types;

        // Sort data by user name
        const dataKeys = Object.keys(matrixContribution);
        dataKeys.sort(function (a, b) {
            return a.localeCompare(b);
        });
    
        const totalKeys = Object.keys(matrixContribution).length;
    
        // Generate table header with user names
        const head = dataKeys.map((key, index) => {
            return (
                <th key={index}
                    style={{
                        borderRight: totalKeys - 1 === index ? 'none' : '',
                        width: '100px'
                    }}>
                    {Util.cutEmail(key)}</th>
            );
        });
        
        // Get shared object keys among all users
        // This is used to iterate through the data
        const sharedObject = dataKeys.map((user) => {
            return matrixContribution[user]
        })[0];

        // Iterate through shared object keys and generate a row for each
        const bodyData = Object.keys(sharedObject).map((key, index) => {
            const rowOfData = dataKeys.map((user) => {
                return matrixContribution[user][key];
            });
    
            return (
                <tr key={index}>
                    <td style={{borderLeft: 'none'}}>{Util.formattedName(key)}</td>
                    {dataKeys.map((user, subIndex) => {
                        return (
                            <td key={subIndex}
                                style={{
                                    borderRight: totalKeys - 1 === subIndex ? 'none' : '',
                                    backgroundColor: this.getPerformanceColor(key, user, rowOfData, matrixContribution)
                                }}
                            >{matrixContribution[user][key]}</td>
                        )
                    })}
                </tr>
            );
        });

        return (
            <div className="matrix">
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
            </div>
        );
    }
}
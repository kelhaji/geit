import React, { PureComponent } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';
import Util from './Util.js';


const chartData = Object.keys(data.contribution.types.contributors).map((key) => {
    let dataPoint = {
        name: Util.cutEmail(key)
    };

    Object.assign(dataPoint, data.contribution.types.contributors[key]);

    return dataPoint;
});

chartData.sort((A, B) => {
    let sumA = 0;
    let sumB = 0;

    Object.keys(A).forEach((key) => {
        if (key !== 'name') {
            sumA += A[key];
        }
    });

    Object.keys(B).forEach((key) => {
        if (key !== 'name') {
            sumB += B[key];
        }
    });

    return sumB - sumA;
});

export default class ContributionChart extends PureComponent {

    render() {
        return (
            <div style={{width: '100%', height: 400}}>
                <ResponsiveContainer>
                    <BarChart
                        data={chartData}
                        margin={{
                            top: 30, right: 50, left: 0, bottom: 20,
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="name" tick={{fontSize: 14}}/>
                        <YAxis tick={{fontSize: 14}}/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="code" name="Code" stackId="1" fill="#8884d8"/>
                        <Bar dataKey="test" name="Tests" stackId="1" fill="#00C49F"/>
                        <Bar dataKey="comments" name="Comments" stackId="1"
                             fill="#FFBB28"/>
                        <Bar dataKey="configuration" name="Configuration" stackId="1"
                             fill="#FF8042"/>
                        <Bar dataKey="user_interface" name="User interface" stackId="1"
                             fill="#0088FE"/>
                        <Bar dataKey="documentation" name="Documentation" stackId="1"
                             fill="#82ca9d"/>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        );
    }
}
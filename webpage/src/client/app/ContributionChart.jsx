import React, { PureComponent } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';

const cutEmail = (email) => {
    return email.split('@')[0]
};

const chartData = Object.keys(data.contribution.types.contributors).map((key) => {
    let dataPoint = {
        name: cutEmail(key)
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

// console.log(dataFake);

// const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];
//
// const capitalize = (s) => {
//   if (typeof s !== 'string') return ''
//   return s.charAt(0).toUpperCase() + s.slice(1)
// };


export default class ContributionChart extends PureComponent {

  render() {
    return (
                <div style={{ width: '100%', height: 400 }}>
          <ResponsiveContainer>
      <BarChart
        data={chartData}
        margin={{
          top: 30, right: 50, left: 0, bottom: 20,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" tick={{fontSize: 14}} />
        <YAxis tick={{fontSize: 14}} />
        <Tooltip />
        <Legend />
        <Bar dataKey="code" name="Code" stackId="a" fill="#8884d8" />
        <Bar dataKey="documentation" name="Documentation" stackId="a" fill="#82ca9d" />
        <Bar dataKey="user_interface" name="User interface" stackId="a" fill="#0088FE" />
        <Bar dataKey="test" name="Test" stackId="a" fill="#00C49F" />
        <Bar dataKey="comments" name="Comments" stackId="a" fill="#FFBB28" />
        <Bar dataKey="configuration" name="Configuration" stackId="a" fill="#FF8042" />
      </BarChart>
          </ResponsiveContainer>
                </div>

    );
  }
}
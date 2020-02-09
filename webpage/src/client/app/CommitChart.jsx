import React, {Component} from 'react';
import moment from 'moment';
import {
    BarChart,
    Bar,
    ReferenceLine,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from 'recharts';

let chartData = Array.from(Array(365), () => 0)

data.commits.overall.timeline.forEach((datapoint) => {
    let date = moment.unix(datapoint.committed_date);
    chartData[date.dayOfYear() - 1] += 1
});

let firstNonzeroValue = null;
let lastPoint = null;
let lastNonZeroValue = null;

chartData.forEach((datapoint, index) => {
    if (firstNonzeroValue == null) {
        if (datapoint > 0) {
            firstNonzeroValue = index
        }
    }

    if (datapoint == 0 && lastPoint > 0) {
        lastNonZeroValue = index - 1
    }

    lastPoint = datapoint
});

let finalChartData = chartData.slice(firstNonzeroValue, lastNonZeroValue + 1);

let finalData = finalChartData.map((point, index) => {
    return {
        day: 'Day ' + index.toString(),
        commits: point
    }
});


export default class CommitChart extends Component {

    render() {
        return (
            <div style={{width: '100%', height: 400}}>
                <ResponsiveContainer>
                    <BarChart
                        data={finalData}
                        margin={{
                            top: 30, right: 50, left: 0, bottom: 20,
                        }}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="day" tick={{fontSize: 14}} tickMargin={15}
                               height={50}
                               interval={Math.floor(finalData.length / 10)}/>
                        <YAxis tick={{fontSize: 14}}/>
                        <Tooltip/>
                        <ReferenceLine y={0} stroke="#000"/>
                        <Bar dataKey="commits" name="Total commits" fill="#007bff"/>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        );
    }
}
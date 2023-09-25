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
import PropTypes from "prop-types";

/**
 * Renders a commit timeline from the Geit data.
 */
export default class CommitChart extends Component {

    static propTypes = {
        data: PropTypes.object.isRequired
    };

    /**
     * Generates a timeline of commits from the Geit data and returns it in a format that can be used by the chart library.
     * 
     * @returns chart timeline starting from first commit
     */
    getTimeline() {
        // Generate array with 365 entries, each representing a day of the year
        let chartData = Array.from(Array(365), () => 0)

        // Fill relevant array locations cumulatively with the number of commits on that day
        this.props.data.commits.overall.timeline.forEach((datapoint) => {
            let date = moment.unix(datapoint.committed_date);
            chartData[date.dayOfYear() - 1] += 1
        });
        
        let firstNonzeroValue = null;
        let lastPoint = null;
        let lastNonZeroValue = null;
        
        // Find first and last non-zero value
        chartData.forEach((datapoint, index) => {
            if (firstNonzeroValue === null) {
                if (datapoint > 0) {
                    firstNonzeroValue = index
                }
            }
        
            if (datapoint === 0 && lastPoint > 0) {
                lastNonZeroValue = index - 1
            }
        
            lastPoint = datapoint
        });
        
        // Slice array to only include relevant data
        let finalChartData = chartData.slice(firstNonzeroValue, lastNonZeroValue + 1);
        
        // Minor post-processing to make the chart look nicer
        let finalData = finalChartData.map((point, index) => {
            return {
                day: 'Day ' + index.toString(),
                commits: point
            }
        });

        return finalData;
    }

    render() {
        const chartData = this.getTimeline();

        return (
            <div style={{width: '100%', height: 400}}>
                <ResponsiveContainer>
                    <BarChart
                        data={chartData}
                        margin={{
                            top: 30, right: 50, left: 0, bottom: 20,
                        }}>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="day" tick={{fontSize: 14}} tickMargin={15}
                               height={50}
                               interval={Math.max(Math.floor(chartData.length / 10), 1)}/>
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
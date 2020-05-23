import React from 'react';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ScatterChart, Scatter, ZAxis} from 'recharts';
import axios from 'axios';
import './style.sass'
import backendUrl from '../../assets/backendUrl';

export default class Statistics extends React.Component {
    state = {
        lineChartData: null,
        bubbleChartData: null,
        bubbleRange: null,
        domain: null
    }

    componentDidMount() {
        axios.get(backendUrl.tweets_per_hour).then(response => {
            if (response.status === 200) {
                this.setState({
                    lineChartData: response.data.rows
                });
            }
        }, error => {
            console.log(error);
        });
        axios.get(backendUrl.total_tweets_by_day_and_hour).then(response => {
            if (response.status === 200) {
                let bubbleChartData = [];
                let maxValue = -1;
                [0, 1, 2, 3, 4, 5, 6].forEach(index => {
                    bubbleChartData[index] = [];
                });
                response.data.forEach(dataItem => {
                    let key = dataItem['key'];
                    let value = dataItem['value'];
                    let hour;
                    if (key[1] > 12) {
                        hour = key[1] % 12 + "p";
                    } else {
                        hour = key[1] + "a";
                    }
                    bubbleChartData[key[0]].push({hour: hour, index: 1, value: value});
                    if (maxValue < value) {
                        maxValue = value;
                    }
                });
                this.setState({
                    bubbleChartData: bubbleChartData,
                    bubbleRange: [0, maxValue],
                    domain: [0, maxValue]
                });
            }
        }, error => {
            console.log(error);
        });
    }

    render() {
        return (
            <div className={"content"}>
                {this.state.lineChartData &&
                <div className={"line-chart"}>
                    <LineChart width={1000} height={700} data={this.state.lineChartData}
                               margin={{
                                   top: 5, right: 30, left: 20, bottom: 5,
                               }}>
                        <CartesianGrid strokeDasharray="5 5"/>
                        <XAxis dataKey="key"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Line type="monotone" dataKey="value" stroke="#82ca9d"/>
                    </LineChart>
                    <div className={"chart-title"}>Number Of Tweets Per Hour</div>
                </div>}
                {this.state.bubbleChartData &&
                <div className={'bubble-chart'}>
                    {this.state.bubbleChartData.map((row, index) => {
                        let days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                        let day = days[index];
                        let tick = {fontSize: 0};
                        if (day === 'Sunday') {
                            tick = {};
                        }
                        return <ScatterChart
                            key={index}
                            width={1000}
                            height={60}
                            margin={{
                                top: 15, right: 0, bottom: 0, left: 0,
                            }}>
                            <XAxis type="category" dataKey="hour" name="Hour" interval={0} tick={tick}
                                   tickLine={{transform: 'translate(0, -6)'}}/>
                            <YAxis type="number" dataKey="index" name={day} height={10} width={100} tick={{fontSize: 0}}
                                   tickLine={false} axisLine={false}
                                   label={{value: day, position: 'insideRight'}}/>
                            <ZAxis type="number" dataKey="value" name="Number Of Tweets" domain={this.state.domain}
                                   range={this.state.bubbleRange}/>
                            <Tooltip cursor={{strokeDasharray: '3 3'}} wrapperStyle={{zIndex: 100}}
                                     content={this.renderTooltip}/>
                            <Scatter data={row} fill="#41b1db"/>
                        </ScatterChart>
                    })}
                    <div className={"chart-title"}>Activity Last 5 months</div>
                </div>}
            </div>
        );
    }
}
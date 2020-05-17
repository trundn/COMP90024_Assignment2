import React from "react";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar} from "recharts";
import axios from 'axios';
import './style.sass'

export default class Statistics extends React.Component {
    state = {
        lineChartData: [],
        barChartData: [
            {
                name: 'Page A', uv: 4000, pv: 2400, amt: 2400,
            },
            {
                name: 'Page B', uv: 3000, pv: 1398, amt: 2210,
            },
            {
                name: 'Page C', uv: 2000, pv: 9800, amt: 2290,
            },
            {
                name: 'Page D', uv: 2780, pv: 3908, amt: 2000,
            },
            {
                name: 'Page E', uv: 1890, pv: 4800, amt: 2181,
            },
            {
                name: 'Page F', uv: 2390, pv: 3800, amt: 2500,
            },
            {
                name: 'Page G', uv: 3490, pv: 4300, amt: 2100,
            }
        ]
    }

    componentDidMount() {
        axios.get("http://127.0.0.1:8000/tweets/tweets-per-hour/").then(response => {
            if (response.status === 200) {
                this.setState({
                    lineChartData: response.data.rows
                });
            }
        }, error => {
            console.log(error);
        });
        axios.get("http://127.0.0.1:8000/tweets/language-statistics/").then(response => {
            if (response.status === 200) {
                console.log(response.data.rows);
                this.setState({
                    barChartData: response.data.rows
                });
            }
        }, error => {
            console.log(error);
        });
    }

    render() {
        return (
            <div>
                <div className={"float-content"}>
                    <LineChart width={980} height={600} data={this.state.lineChartData}
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
                    <div>Number Of Tweets Per Day</div>
                </div>
                <div className={"float-content"}>
                    <BarChart width={600}
                              height={600}
                              data={this.state.barChartData}
                              margin={{
                                  top: 5, right: 30, left: 20, bottom: 5,
                              }}>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="key"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="value" fill="#8884d8"/>
                    </BarChart>
                    <div>Language Statistics</div>
                </div>
            </div>
        );
    }
}
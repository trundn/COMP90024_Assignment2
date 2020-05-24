import React from 'react';
import {XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    BarChart,
    Bar,
} from 'recharts';
import axios from 'axios';
import './style.sass'
import backendUrl from '../../assets/backendUrl';

export default class Language extends React.Component {
    state = {
        barChartData: null
    }

    componentDidMount() {
        axios.get(backendUrl.language_statistics).then(response => {
            if (response.status === 200) {
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
            <div className={"content"}>
                {this.state.barChartData &&
                <div className={"bar-chart"}>
                    <BarChart width={1600}
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
                    <div className={"chart-title"}>Language Statistics</div>
                </div>}
            </div>
        );
    }
}

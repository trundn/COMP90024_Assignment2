import React, {PureComponent} from 'react';
import {
    PieChart, Pie, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend,
} from 'recharts';
import axios from 'axios';
import './style.sass'
import backendUrl from '../../assets/backendUrl';

const barChartData = [
    {
        name: 'Tweets Without Coordinates', basic: 4000, covid: 2400
    },
    {
        name: 'Tweets With Coordinates', basic: 3000, covid: 1398
    }
];

export default class Example extends PureComponent {
    state = {
        pieChartData: null,
        barChartData: null
    }

    componentDidMount() {
        axios.get(backendUrl.tweets_by_categories).then(response => {
            if (response.status === 200) {
                let pieChartData = []
                for (let i = 0; i < response.data.length; i++) {
                    let dataItem = response.data[i];
                    pieChartData.push({
                        name: dataItem.key,
                        value: dataItem.value
                    });
                }
                this.setState({
                    pieChartData: pieChartData
                });
            }
        });
        axios.get(backendUrl.tweets_with_coordinates).then(response => {
            if (response.status === 200) {
                let barChartData = []
                for (let i = 0; i < response.data.length; i++) {
                    let dataItem = response.data[i];
                    let name = dataItem['key'][0];
                    let key = dataItem['key'][1];
                    let value = dataItem['value'];
                    let updated = false;
                    for (let j = 0; j < barChartData.length; j++) {
                        if (barChartData[j]['name'] === name) {
                            barChartData[j][key] = value;
                            updated = true;
                        }
                    }
                    if (!updated) {
                        let chartDataItem = {name: name}
                        chartDataItem[key] = value;
                        barChartData.push(chartDataItem);
                    }
                }
            }
        });
    }

    render() {
        return (
            <div className={"content"}>
                <div className={"left-chart"}>
                    <PieChart width={600} height={600}>
                        <Pie dataKey="value" isAnimationActive={false} data={this.state.pieChartData} cx={300} cy={300}
                             outerRadius={200}
                             fill="#8884d8" label/>
                        <Tooltip/>
                    </PieChart>
                </div>
                <div className={"right-chart"}>
                    <BarChart
                        width={600}
                        height={600}
                        data={barChartData}>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="name"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="basic" stackId="a" fill="#8884d8"/>
                        <Bar dataKey="covid" stackId="a" fill="#82ca9d"/>
                    </BarChart>
                </div>
            </div>
        );
    }
}

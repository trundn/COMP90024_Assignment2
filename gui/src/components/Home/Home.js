import React, {PureComponent} from 'react';
import {
    PieChart, Pie, Tooltip, BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Legend,
} from 'recharts';

import './style.sass'

const barChartData = [
    {
        name: 'Tweets Without Coordinates', basic: 4000, covid: 2400
    },
    {
        name: 'Tweets With Coordinates', basic: 3000, covid: 1398
    }
];

const pieChartData = [
    {name: 'Number of tweets talking about Covid19', value: 400}, {name: 'Number of other tweets', value: 300}
];

export default class Example extends PureComponent {
    render() {
        return (
            <div className={"content"}>
                <div className={"left-chart"}>
                    <PieChart width={600} height={600}>
                        <Pie dataKey="value" isAnimationActive={false} data={pieChartData} cx={300} cy={300} outerRadius={200}
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

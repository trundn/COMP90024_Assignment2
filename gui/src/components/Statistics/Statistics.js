import React from 'react';
import {Tooltip, Pie, Cell, PieChart} from 'recharts';
import axios from 'axios';
import './style.sass'
import backendUrl from '../../assets/backendUrl';

const data = [
    {name: 'The ruling party', value: 400},
    {name: 'The opposition', value: 300}
];

const COLORS = ['#00C49F', '#FF8042'];
const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({cx, cy, midAngle, innerRadius, outerRadius, percent, index}) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
        <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
            {`${(percent * 100).toFixed(0)}%`}
        </text>
    );
};

export default class Statistics extends React.Component {
    state = {
        lineChartData: null,
        bubbleChartData: null,
        bubbleRange: null,
        pieChartForTheRulingData: null,
        pieChartForTheOppositionData: null,
        domain: null
    }

    componentDidMount() {
        axios.get(backendUrl.tweets_by_political_parties).then(response => {
            if (response.status === 200) {
                let pieChartForTheRulingData = [];
                let pieChartForTheOppositionData = [];
                response.data.forEach(dataItem => {
                    let pieChartDataItem = {};
                    if (dataItem.key[1] === true) {
                        pieChartDataItem['name'] = 'Tweets about Covid';
                    } else {
                        pieChartDataItem['name'] = 'Not about Covid';
                    }
                    pieChartDataItem['value'] = dataItem.value;

                    if (dataItem.key[0] === 'ruling') {
                        pieChartForTheRulingData.push(pieChartDataItem);
                    } else {
                        pieChartForTheOppositionData.push(pieChartDataItem);
                    }
                });
                this.setState({
                    pieChartForTheRulingData: pieChartForTheRulingData,
                    pieChartForTheOppositionData: pieChartForTheOppositionData
                });
            }
        }, error => {
            console.log(error)
        });
    }

    render() {
        return (
            <div className={"content"}>
                <div className={"pie-chart-1"}>
                    <PieChart width={400} height={400}>
                        <Pie
                            data={this.state.pieChartForTheRulingData}
                            cx={200}
                            cy={200}
                            labelLine={false}
                            label={renderCustomizedLabel}
                            outerRadius={180}
                            fill="#8884d8"
                            dataKey="value">
                            {
                                data.map((entry, index) =>
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]}/>
                                )
                            }
                        </Pie>
                        <Tooltip/>
                    </PieChart>
                    <div className={"chart-title"}>The ruling Party</div>
                </div>
                <div class={"pie-chart-2"}>
                    <PieChart width={400} height={400}>
                        <Pie
                            data={this.state.pieChartForTheOppositionData}
                            cx={200}
                            cy={200}
                            labelLine={false}
                            label={renderCustomizedLabel}
                            outerRadius={180}
                            fill="#8884d8"
                            dataKey="value">
                            {
                                data.map((entry, index) =>
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]}/>
                                )
                            }
                        </Pie>
                        <Tooltip/>
                    </PieChart>
                    <div className={"chart-title"}>The opposition</div>
                </div>
            </div>
        );
    }
}
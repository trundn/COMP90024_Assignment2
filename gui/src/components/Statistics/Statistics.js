import React from 'react';
import {Tooltip, Pie, Cell, PieChart, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend,} from 'recharts';
import axios from 'axios';
import './style.sass'
import backendUrl from '../../assets/backendUrl';

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
        pieChartForTheRulingData: null,
        pieChartForTheOppositionData: null,
        barChartForTheRulingData: null,
        barChartForTheOppositionData: null
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
        axios.get(backendUrl.tweets_by_politicians).then(response => {
            if (response.status === 200) {
                let barChartForTheRulingData = [];
                let barChartForTheOppositionData = [];
                response.data.forEach(dataItem => {
                    let character = dataItem.key[2];
                    if (character.length >= 10) {
                        character = character.split(" ")[1];
                    }
                    let covid = dataItem.key[1];
                    let party = dataItem.key[0];
                    let value = dataItem.value;

                    let existing = false;
                    barChartForTheRulingData.forEach(item => {
                        if (item['name'] === character) {
                            if (covid) {
                                item['uv'] = value;
                            } else {
                                item['pv'] = value;
                            }
                            existing = true;
                        }
                    });
                    barChartForTheOppositionData.forEach(item => {
                        if (item['name'] === character) {
                            if (covid) {
                                item['uv'] = value;
                            } else {
                                item['pv'] = value;
                            }
                            existing = true;
                        }
                    });

                    if (existing === false) {
                        let barChartDataItem = {
                            name: character
                        };

                        if (covid) {
                            barChartDataItem['uv'] = value;
                            barChartDataItem['pv'] = 15;
                        } else {
                            barChartDataItem['uv'] = 15;
                            barChartDataItem['pv'] = value;
                        }

                        if (party === 'ruling') {
                            barChartForTheRulingData.push(barChartDataItem)
                        } else {
                            barChartForTheOppositionData.push(barChartDataItem)
                        }
                    }
                });
                this.setState({
                    barChartForTheRulingData: barChartForTheRulingData,
                    barChartForTheOppositionData: barChartForTheOppositionData
                });
            }
        }, error => {
            console.log(error)
        });
    }

    render() {
        return (
            <div className={"content"}>
                {this.state.pieChartForTheOppositionData &&
                <div className={"pie-chart-1"}>
                    <div className={"chart-title"}>The ruling party</div>
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
                                this.state.pieChartForTheOppositionData.map((entry, index) =>
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]}/>
                                )
                            }
                        </Pie>
                        <Tooltip/>
                    </PieChart>
                </div>}
                {this.state.pieChartForTheOppositionData &&
                <div className={"pie-chart-2"}>
                    <div className={"chart-title"}>The opposition</div>
                    <PieChart width={400} height={400}>
                        <div className={"chart-title"}>The opposition</div>
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
                                this.state.pieChartForTheOppositionData.map((entry, index) =>
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]}/>
                                )
                            }
                        </Pie>
                        <Tooltip/>
                    </PieChart>
                </div>}
                <div className={"politicians"}>
                    <BarChart
                        width={1600}
                        height={400}
                        data={this.state.barChartForTheRulingData}
                        margin={{
                            top: 20, right: 30, left: 20, bottom: 5,
                        }}>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="name"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="pv" name="Not about Covid19" stackId="a" fill="#8884d8"/>
                        <Bar dataKey="uv" name="About Covid19" stackId="a" fill="#82ca9d"/>
                    </BarChart>
                    <div className={"chart-title"}>The ruling party</div>
                    <BarChart
                        width={1600}
                        height={400}
                        data={this.state.barChartForTheOppositionData}
                        margin={{
                            top: 20, right: 30, left: 20, bottom: 5,
                        }}>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="name"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="pv" name="Not about Covid19" stackId="a" fill="#8884d8"/>
                        <Bar dataKey="uv" name="About Covid19" stackId="a" fill="#82ca9d"/>
                    </BarChart>
                    <div className={"chart-title"}>The opposition</div>
                </div>
            </div>
        );
    }
}
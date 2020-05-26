import React, {PureComponent} from 'react';
import {
    PieChart,
    Pie,
    Tooltip,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Legend,
    Line,
    ScatterChart,
    ComposedChart,
    ZAxis,
    Scatter
} from 'recharts';
import './style.sass'
import axios from 'axios';
import backendUrl from '../../assets/backendUrl';

export default class Example extends PureComponent {
    state = {
        pieChartData: null,
        barChartData: null,
        composedChartData: null,
        bubbleChartData: null,
        bubbleRange: null,
        domain: null
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
        }, error => {
            console.log(error);
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
                this.setState({
                    barChartData: barChartData
                });
            }
        }, error => {
            console.log(error);
        });
        axios.get(backendUrl.tweets_per_hour).then(response => {
            if (response.status === 200) {
                let composedChartData = response.data.rows;
                composedChartData.forEach(dataItem => {
                    dataItem['key'] = dataItem['key'] + 'h';
                });
                this.setState({
                    composedChartData: composedChartData
                });
            }
        }, error => {
            console.log(error);
        });
        axios.get(backendUrl.total_tweets_by_day_and_hour).then(response => {
            if (response.status === 200) {
                let bubbleChartData = [];
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
                });
                this.setState({
                    bubbleChartData: bubbleChartData,
                    bubbleRange: [0, 500],
                    domain: [0, 500]
                });
            }
        }, error => {
            console.log(error);
        });
    }

    render() {
        return (
            <div className={"content"}>
                {this.state.pieChartData &&
                <div className={"left-chart"}>
                    <PieChart width={600} height={810}>
                        <Pie dataKey="value" isAnimationActive={false} data={this.state.pieChartData} cx={300} cy={300}
                             outerRadius={200}
                             fill="#8884d8" label/>
                        <Tooltip/>
                    </PieChart></div>}
                {this.state.barChartData &&
                <div className={"right-chart"}>
                    <BarChart
                        width={600}
                        height={850}
                        data={this.state.barChartData}>
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="name"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="basic" stackId="a" fill="#8884d8"/>
                        <Bar dataKey="covid" stackId="a" fill="#82ca9d"/>
                    </BarChart>
                </div>}
                {this.state.composedChartData &&
                <div className={"composed-chart"}>
                    <ComposedChart width={1000}
                                   height={700}
                                   data={this.state.composedChartData}>
                        <CartesianGrid stroke="#f5f5f5"/>
                        <XAxis dataKey="key"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="value" barSize={20} fill="#413ea0"/>
                        <Line type="monotone" dataKey="value" stroke="#ff7300"/>
                    </ComposedChart>
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

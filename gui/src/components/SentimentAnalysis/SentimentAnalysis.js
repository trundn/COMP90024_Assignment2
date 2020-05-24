import React from 'react';
import {
    Tooltip, Cell, PieChart, Pie, ComposedChart, CartesianGrid, XAxis, YAxis, Legend, Bar, Line
} from 'recharts';
import './style.sass'
import axios from 'axios';
import backendUrl from '../../assets/backendUrl';

const COLORS = ['#803C05', '#97BBE0', '#30582C'];
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

export default class SentimentAnalysis extends React.Component {
    state = {
        pieChartAboutCovidData: null,
        pieChartAboutNonCovidData: null,
        positiveComposedChartData: null,
        negativeComposedChartData: null
    }

    componentDidMount() {
        axios.get(backendUrl.feelings_about_covid.format('yes')).then(response => {
            if (response.status === 200) {
                let pieChartAboutCovidData = [];
                response.data.forEach(dataItem => {
                    pieChartAboutCovidData.push({
                        name: dataItem['key'],
                        value: dataItem['value']
                    });
                });
                this.setState({
                    pieChartAboutCovidData: pieChartAboutCovidData
                });
            }
        });
        axios.get(backendUrl.feelings_about_covid.format('no')).then(response => {
            if (response.status === 200) {
                let pieChartAboutNonCovidData = [];
                response.data.forEach(dataItem => {
                    pieChartAboutNonCovidData.push({
                        name: dataItem['key'],
                        value: dataItem['value']
                    });
                });
                this.setState({
                    pieChartAboutNonCovidData: pieChartAboutNonCovidData
                });
            }
        });
        axios.get(backendUrl.most_positive_hours).then(response => {
            let composedChartData = [];
            if (response.status === 200) {
                response.data.forEach(dataItem => {
                    composedChartData.push({
                        name: dataItem['key'] + 'h',
                        value: dataItem['value']['sum'] / dataItem['value']['count']
                    });
                });
                this.setState({
                    positiveComposedChartData: composedChartData
                });
            }
        });
        axios.get(backendUrl.most_negative_hours).then(response => {
            let composedChartData = [];
            if (response.status === 200) {
                response.data.forEach(dataItem => {
                    composedChartData.push({
                        name: dataItem['key'] + 'h',
                        value: dataItem['value']['sum'] / dataItem['value']['count']
                    });
                });
                this.setState({
                    negativeComposedChartData: composedChartData
                });
            }
        });
    }

    render() {
        return (
            <div className={"content"}>
                {this.state.pieChartAboutCovidData &&
                <div className={"pie-chart-1"}>
                    <div className={"chart-title"}>Emotions about Covid</div>
                    <PieChart width={400} height={400}>
                        <Pie
                            data={this.state.pieChartAboutCovidData}
                            cx={200}
                            cy={200}
                            labelLine={false}
                            label={renderCustomizedLabel}
                            outerRadius={180}
                            fill="#8884d8"
                            dataKey="value">
                            {
                                this.state.pieChartAboutCovidData.map((entry, index) =>
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]}/>
                                )
                            }
                        </Pie>
                        <Tooltip/>
                    </PieChart>
                </div>}
                {this.state.pieChartAboutNonCovidData &&
                <div className={"pie-chart-2"}>
                    <div className={"chart-title"}>Emotions about others</div>
                    <PieChart width={400} height={400}>
                        <div className={"chart-title"}>The opposition</div>
                        <Pie
                            data={this.state.pieChartAboutNonCovidData}
                            cx={200}
                            cy={200}
                            labelLine={false}
                            label={renderCustomizedLabel}
                            outerRadius={180}
                            fill="#8884d8"
                            dataKey="value">
                            {
                                this.state.pieChartAboutNonCovidData.map((entry, index) =>
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]}/>
                                )
                            }
                        </Pie>
                        <Tooltip/>
                    </PieChart>
                </div>}
                {this.state.positiveComposedChartData &&
                <div className={"composed-chart"}>
                    <ComposedChart width={1400}
                                   height={700}
                                   data={this.state.positiveComposedChartData}>
                        <CartesianGrid stroke="#f5f5f5"/>
                        <XAxis dataKey="name"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="value" barSize={20} fill="#413ea0"/>
                        <Line type="monotone" dataKey="value" stroke="#ff7300"/>
                    </ComposedChart>
                    <div className={"chart-title"}>When Australian people feel most positive</div>
                </div>}
                {this.state.negativeComposedChartData &&
                <div className={"composed-chart"}>
                    <ComposedChart width={1400}
                                   height={700}
                                   data={this.state.negativeComposedChartData}>
                        <CartesianGrid stroke="#f5f5f5"/>
                        <XAxis dataKey="name"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Bar dataKey="value" barSize={20} fill="#413ea0"/>
                        <Line type="monotone" dataKey="value" stroke="#ff7300"/>
                    </ComposedChart>
                    <div className={"chart-title"}>When Australian people feel most negative</div>
                </div>}
            </div>
        );
    }
}

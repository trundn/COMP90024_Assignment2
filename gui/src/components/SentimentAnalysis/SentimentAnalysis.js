import React from 'react';
import {
    Tooltip, Cell, PieChart, Pie
} from 'recharts';
import './style.sass'
import axios from 'axios';
import backendUrl from '../../assets/backendUrl';

const COLORS = ['#FF8042', '#00C49F', '#66ff66'];
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
        pieChartAboutNonCovidData: null
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
            </div>
        );
    }
}

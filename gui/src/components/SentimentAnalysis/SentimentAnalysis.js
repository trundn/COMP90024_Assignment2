import React from 'react';
import {
    ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Cell
} from 'recharts';
import {scaleOrdinal} from 'd3-scale';
import {schemeCategory10} from 'd3-scale-chromatic';
import './style.sass'
import axios from 'axios';
import backendUrl from '../../assets/backendUrl';

const colors = scaleOrdinal(schemeCategory10).range();

export default class SentimentAnalysis extends React.Component {
    state = {
        negData: [],
        neuData: [],
        posData: []
    }

    componentDidMount() {
        axios.get(backendUrl.tweets_with_emotion_values_and_pro_cnt.format(100, 0)).then(response => {
            if (response.status === 200) {
                let negData = [];
                let neuData = [];
                let posData = [];
                response.data.forEach(tweet => {
                    let statistics = tweet['value'];
                    ['neg', 'neu', 'pos'].forEach(emotionKey => {
                        ['fps_cnt', 'fpp_cnt', 'sp_cnt', 'tp_cnt'].forEach((wordType, index) => {
                            let dataItem = {
                                x: statistics[1][wordType],
                                y: statistics[0][emotionKey],
                                colorIndex: index
                            }
                            switch (emotionKey) {
                                case 'neg':
                                    negData.push(dataItem);
                                    break;
                                case 'neu':
                                    neuData.push(dataItem);
                                    break;
                                case 'pos':
                                    posData.push(dataItem);
                                    break;
                            }
                        });
                    });
                });
                this.setState({
                    negData: negData,
                    neuData: neuData,
                    posData: posData
                });
                console.log(neuData);
            }
        });
    }

    render() {
        return (
            <div className={"content"}>
                <div className={"left"}>
                    <ScatterChart
                        width={400}
                        height={400}>
                        <CartesianGrid/>
                        <XAxis type="number" dataKey="x" name="words" unit=""/>
                        <YAxis type="number" dataKey="y" name="probability" unit=""/>
                        <Tooltip cursor={{strokeDasharray: '3 3'}}/>
                        <Scatter name="A school" data={this.state.negData} fill="#8884d8">
                            {
                                this.state.posData.map((entry, index) => <Cell key={`cell-${index}`}
                                                                               fill={colors[entry.colorIndex]}/>)
                            }
                        </Scatter>
                    </ScatterChart>
                    <div>Negative Emotions</div>
                </div>
                <div className={"middle"}>
                    <ScatterChart
                        width={400}
                        height={400}>
                        <CartesianGrid/>
                        <XAxis type="number" dataKey="x" name="words" unit=""/>
                        <YAxis type="number" dataKey="y" name="probability" unit=""/>
                        <Tooltip cursor={{strokeDasharray: '3 3'}}/>
                        <Scatter name="A school" data={this.state.neuData} fill="#8884d8">
                            {
                                this.state.posData.map((entry, index) => <Cell key={`cell-${index}`}
                                                                               fill={colors[entry.colorIndex]}/>)
                            }
                        </Scatter>
                    </ScatterChart>
                    <div>Neural Emotions</div>
                </div>
                <div className={"right"}>
                    <ScatterChart
                        width={400}
                        height={400}>
                        <CartesianGrid/>
                        <XAxis type="number" dataKey="x" name="words" unit=""/>
                        <YAxis type="number" dataKey="y" name="probability" unit=""/>
                        <Tooltip cursor={{strokeDasharray: '3 3'}}/>
                        <Scatter name="A school" data={this.state.posData} fill="#8884d8">
                            {
                                this.state.posData.map((entry, index) => <Cell key={`cell-${index}`}
                                                                               fill={colors[entry.colorIndex]}/>)
                            }
                        </Scatter>
                    </ScatterChart>
                    <div>Positive Emotions</div>
                </div>
            </div>
        );
    }
}

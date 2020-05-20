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
console.log(colors);
const data = [
    {x: 100, y: 200, z: 200},
    {x: 120, y: 100, z: 260},
    {x: 170, y: 300, z: 400},
    {x: 140, y: 250, z: 280},
    {x: 150, y: 400, z: 500},
    {x: 120, y: 280, z: 200},
    {x: 130, y: 280, z: 200},
    {x: 140, y: 280, z: 200},
    {x: 150, y: 280, z: 200},
    {x: 160, y: 280, z: 200},
    {x: 170, y: 280, z: 200},
];

export default class SentimentAnalysis extends React.Component {
    static jsfiddleUrl = 'https://jsfiddle.net/alidingling/9Lfxjjty/';

    render() {
        return (
            <ScatterChart
                width={400}
                height={400}
                margin={{
                    top: 20, right: 20, bottom: 20, left: 20,
                }}
            >
                <CartesianGrid />
                <XAxis type="number" dataKey="x" name="stature" unit="cm" />
                <YAxis type="number" dataKey="y" name="weight" unit="kg" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Scatter name="A school" data={data} fill="#8884d8">
                    {
                        data.map((entry, index) => <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />)
                    }
                </Scatter>
            </ScatterChart>
        );
    }
}

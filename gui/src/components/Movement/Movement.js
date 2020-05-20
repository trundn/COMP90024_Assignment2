import React from 'react';
import {CircleMarker, Map, Polyline, TileLayer} from 'react-leaflet';
import './style.sass';
import axios from 'axios'
import backendUrl from '../../assets/backendUrl.js'

export default class Movement extends React.Component {
    state = {
        lat: -25,
        lng: 130,
        zoom: 4,
        polylines: [],
        borderPoints: []
    }

    componentDidMount() {
        axios.get(backendUrl.movement).then(response => {
            if (response.status === 200) {
                let polylines = [];
                let borderPoints = [];
                let movementData = response.data;
                movementData.forEach((movementDataItem) => {
                    if (movementDataItem.value.length >= 2) {
                        polylines.push(movementDataItem.value);
                        movementDataItem.value.forEach(borderPoint => {
                            borderPoints.push(borderPoint);
                        });
                    }
                });
                this.setState({
                    polylines: polylines,
                    borderPoints: borderPoints
                });
            }
        });
    }

    render() {
        const center = [this.state.lat, this.state.lng];
        return (
            <Map center={center} zoom={this.state.zoom}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"/>
                {this.state.polylines.map((polyline, index) => {
                    return <Polyline key={index} color="purple" positions={polyline}/>
                })};
                {this.state.borderPoints &&
                this.state.borderPoints.map((borderPoint, index) => {
                    return <CircleMarker key={index} center={borderPoint} color="purple" fillOpacity={1}
                                         fill="purple"
                                         radius={5}/>
                })}
            </Map>
        );
    }
}

import React from 'react';
import {CircleMarker, Map, Polyline, TileLayer} from 'react-leaflet';
import './style.sass';
import axios from 'axios'
import backendUrl from '../../assets/backendUrl.js'
import GridLoader from "react-spinners/GridLoader";

export default class Movement extends React.Component {
    state = {
        lat: -25,
        lng: 130,
        zoom: 4,
        polylines: [],
        borderPoints: [],
        loading: false
    }

    componentDidMount() {
        this.setState({
            loading: true
        });
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
        }).then(() => {
            this.setState({
                loading: false
            });
        });
    }

    render() {
        const center = [this.state.lat, this.state.lng];
        return (
            <div className={"relative"}>
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
                <div className={"absolute"}>
                    <GridLoader
                        size={50}
                        margin={2}
                        color={'#006600'}
                        loading={this.state.loading}/>
                </div>
                {this.state.loading && <div className={'loading-layer'}/>}
            </div>
        );
    }
}

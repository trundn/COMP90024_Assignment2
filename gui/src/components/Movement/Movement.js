import React from 'react'
import {Map, Polyline, TileLayer} from 'react-leaflet'
import axios from 'axios'
import './style.sass';
import PacmanLoader from 'react-spinners/PacmanLoader';
import config from '../../assets/config.js'

export default class Movement extends React.Component {
    state = {
        lat: -37.8136,
        lng: 144.9631,
        zoom: 7,
        polyline: null,
        loading: false
    }

    componentDidMount() {
        this.setState({
            loading: true
        });
        axios.get(config.find_route_url).then(response => {
            if (response.status === 200) {
                this.setState({
                    polyline: response.data,
                    lat: response.data[0][0],
                    lng: response.data[0][1]
                });
            }
            console.log(response.data);
        }).then(() => {
            this.setState({
                loading: false
            });
        });
    }

    render() {
        const position = [this.state.lat, this.state.lng]
        return (
            <div className={"relative"}>
                <Map center={position} zoom={this.state.zoom}>
                    <TileLayer attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                               url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>

                    {this.state.polyline && <Polyline color="black" positions={this.state.polyline}/>}
                </Map>
                <div className={"absolute"}>
                    <PacmanLoader
                        size={100}
                        margin={2}
                        color={'#006600'}
                        loading={this.state.loading}/>
                </div>
                {this.state.loading && <div className={"loading-layer"}/>}
            </div>
        )
    }
}

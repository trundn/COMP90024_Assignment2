import React from 'react';
import {Map, Marker, Popup, TileLayer} from 'react-leaflet';
import './style.sass';

export default class Movement extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            lat: 51.505,
            lng: -.09,
            zoom: 13
        };
    }

    render() {
        const position = [this.state.lat, this.state.lng];
        return (
            <Map center={position} zoom={this.state.zoom}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"/>
                <Marker position={position}>
                    <Popup>
                        A pretty CSS3 popup. <br/> Easily customizable.
                    </Popup>
                </Marker>
            </Map>
        );
    }
}

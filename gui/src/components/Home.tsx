import React from "react";
import {Map, TileLayer, Popup, Marker} from 'react-leaflet';

class Home extends React.Component<{}, { lat: number, lng: number, zoom: number }> {
    constructor(props: any) {
        super(props)
        this.state = {
            lat: 51.505,
            lng: -.09,
            zoom: 13
        };
    }

    render() {
        const position: [number, number] = [this.state.lat, this.state.lng];
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

export default Home
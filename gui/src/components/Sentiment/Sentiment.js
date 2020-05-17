import React, {Component} from 'react'
import {Map, TileLayer, GeoJSON, Tooltip} from 'react-leaflet'
import lga2018data from '../../assets/lga2018.json'


export default class Sentiment extends Component {
    state = {
        lat: -37.8136,
        lng: 144.9631,
        zoom: 10,
    }

    geoJSONStyle() {
        return {
            color: '#1f2021',
            weight: 1,
            fillOpacity: 0.5,
            fillColor: '#fff2af',
        }
    }

    onEachFeature(feature, layer) {
        console.log(feature);
        console.log(layer);
        const popupContent = `<Popup><p>${feature.properties.feature_name}</p></Popup>`
        layer.bindPopup(popupContent)
        layer.on('mouseover', () => {
            layer.setStyle({
                'fillColor': '#ff0000'
            })
        });
        layer.on('mouseout', () => {
            layer.setStyle({
                'fillColor': '#fff2af'
            })
            layer.closePopup();
        });
    }


    render() {
        const position = [this.state.lat, this.state.lng]
        return (
            <Map center={position} zoom={this.state.zoom}>
                <TileLayer
                    attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                <GeoJSON
                    data={lga2018data}
                    style={this.geoJSONStyle}
                    onEachFeature={this.onEachFeature}
                    onmouseover={this.onMouseOver}
                />
            </Map>
        )
    }
}

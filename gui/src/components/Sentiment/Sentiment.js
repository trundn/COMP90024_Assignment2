import React, {Component} from 'react'
import {Map, TileLayer, GeoJSON} from 'react-leaflet'
import statesData from '../../assets/states.json'
import axios from 'axios'

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
        layer.on('click', () => {
            axios.post('http://127.0.0.1:8000/tweets/statistics-in-polygon/', feature.geometry.coordinates).then(response => {
                if (response.status === 200) {
                    let data = response.data;
                    let popupContent = `<Popup>
                        <p>${feature.properties.feature_name}</p>
                        <p>Number Of Positive Tweets: ${data.number_of_positive_tweets}</p>
                        <p>Number Of Neural Tweets: ${data.number_of_neural_tweets}</p>
                        <p>Number Of Negative Tweets: ${data.number_of_negative_tweets}</p>
                        </Popup>`;
                    layer.bindPopup(popupContent);
                    layer.openPopup();
                }

                console.log(response);
            }, error => {
                console.log(error);
            });
        });
        layer.on('mouseover', () => {
            layer.setStyle({
                'fillColor': '#ff0000'
            })
        });
        layer.on('mouseout', () => {
            layer.setStyle({
                'fillColor': '#fff2af'
            })
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
                    data={statesData}
                    style={this.geoJSONStyle}
                    onEachFeature={this.onEachFeature}
                    onmouseover={this.onMouseOver}/>
            </Map>
        )
    }
}

import React, {Component} from 'react'
import {Map, TileLayer, GeoJSON} from 'react-leaflet'
import axios from 'axios'
import './style.sass';
import TreeMenu from 'react-simple-tree-menu';

const treeData = [
    {
        key: 'australia',
        label: 'Australia',
        nodes: [
            {
                key: 'states-and-territories',
                label: 'State and Territories',
                nodes: [],
                url: 'http://localhost:8000/tweets/polygon/2'
            },
            {
                key: 'postal-areas-2016',
                label: 'Postal Areas',
                nodes: [],
                url: 'http://localhost:8000/tweets/polygon/3'
            }
        ],
        url: 'http://localhost:8000/tweets/polygon/1'
    }
];


export default class Sentiment extends Component {
    state = {
        lat: -37.8136,
        lng: 144.9631,
        zoom: 8,
        polygonData: null
    }

    constructor(props) {
        super(props);
        this.geoJsonLayer = React.createRef();
    }

    geoJSONStyle() {
        return {
            color: '#1f2021',
            weight: 1,
            fillOpacity: 0.5,
            fillColor: '#66ff66',
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
                    let offset = 0;
                    if (data.number_of_positive_tweets - data.number_of_negative_tweets !== 0) {
                        offset = (data.number_of_positive_tweets - data.number_of_negative_tweets) / (data.number_of_positive_tweets + data.number_of_negative_tweets)
                    }
                    layer.bindPopup(popupContent)
                }
            }, error => {
                console.log(error);
            });
        });

        layer.on('mouseover', () => {
            layer.setStyle({
                'fillColor': '#fff2af',
                'fillOpacity': 0.5
            });
        });

        layer.on('mouseout', () => {
            layer.setStyle({
                'fillColor': '#66ff66',
                'fillOpacity': 0.5
            });
        });
    }

    componentDidMount() {
        axios.get("http://localhost:8000/tweets/polygon/1/").then(response => {
            if (response.status === 200) {
                let polygonData = JSON.parse(response.data.content);
                this.geoJsonLayer.current.leafletElement.clearLayers().addData(polygonData);
                this.setState({
                    polygonData: polygonData
                });
            }
        });
    }

    onMenuItemClick(event) {
        if (event.url !== null) {
            axios.get(event.url).then(response => {
                if (response.status === 200) {
                    let polygonData = JSON.parse(response.data.content);
                    this.geoJsonLayer.current.leafletElement.clearLayers().addData(polygonData);
                    this.setState({
                        polygonData: polygonData
                    });
                }
            });
        }

    }

    render() {
        const position = [this.state.lat, this.state.lng]
        return (
            <div className={"relative"}>
                <Map center={position} zoom={this.state.zoom}>
                    <TileLayer
                        attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                    <GeoJSON
                        key={"map"}
                        data={this.state.polygonData}
                        style={this.geoJSONStyle}
                        onEachFeature={this.onEachFeature}
                        onmouseover={this.onMouseOver}
                        ref={this.geoJsonLayer}/>
                </Map>
                <div className={"fixed"}>
                    <TreeMenu data={treeData} debounceTime={125} disableKeyboard={false}
                              hasSearch onClickItem={event => this.onMenuItemClick(event)}
                              resetOpenNodesOnDataUpdate={false}/>
                </div>
            </div>
        )
    }
}

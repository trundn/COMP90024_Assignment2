import React, {Component} from 'react'
import {GeoJSON, Map, TileLayer} from 'react-leaflet'
import axios from 'axios'
import './style.sass';
import TreeMenu from 'react-simple-tree-menu';
import PacmanLoader from "react-spinners/PacmanLoader";

const treeData = [
    {
        key: 'australia',
        label: 'Australia',
        nodes: [
            {
                key: 'states-and-territories',
                label: 'State and Territories',
                nodes: [],
                polygonId: 2
            },
            {
                key: 'postal-areas-2016',
                label: 'Postal Areas',
                nodes: [],
                polygonId: 3
            }
        ],
        polygonId: 1
    }
];


export default class Sentiment extends Component {
    state = {
        lat: -37.8136,
        lng: 144.9631,
        zoom: 8,
        selectedId: 1,
        polygonData: null,
        loading: false
    }

    constructor(props) {
        super(props);
        this.geoJson = React.createRef();
        this.statistics = null;
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
        let offset = 0;
        let statistics = feature.statistics;
        if (statistics.number_of_positive_tweets - statistics.number_of_negative_tweets !== 0) {
            offset = (statistics.number_of_positive_tweets - statistics.number_of_negative_tweets) / (statistics.number_of_positive_tweets + statistics.number_of_negative_tweets)
        }
        let popupContent = `<Popup>
                        <p>${feature.properties.feature_name}</p>
                        <p>Number Of Positive Tweets: ${statistics.number_of_positive_tweets}</p>
                        <p>Number Of Neural Tweets: ${statistics.number_of_neural_tweets}</p>
                        <p>Number Of Negative Tweets: ${statistics.number_of_negative_tweets}</p>
                        </Popup>`;
        layer.bindPopup(popupContent);

        layer.on('mouseover', () => {
            layer.setStyle({
                'fillColor': '#ff0000',
                'fillOpacity': 0.5
            });
        });

        layer.on('mouseout', () => {
            layer.setStyle({
                'fillColor': '#66ff66',
                'fillOpacity': 0.5 + offset * 0.5
            });
        });
    }

    componentDidMount() {
        let polygon_url = "http://localhost:8000/tweets/polygon/1/";
        let statistics_url = "http://localhost:8000/tweets/statistics-in-polygon/1";
        this.setState({
            loading: true
        });
        this.requestDataForMap(polygon_url, statistics_url);
    }

    onMenuItemClick(event) {
        if (event.polygonId !== this.state.selectedId) {
            this.setState({
                selectedId: event.polygonId
            });
            let polygon_url = `http://localhost:8000/tweets/polygon/${event.polygonId}`;
            let statistics_url = `http://localhost:8000/tweets/statistics-in-polygon/${event.polygonId}`;
            this.geoJson.current.leafletElement.clearLayers();
            this.setState({
                loading: true
            });
            this.requestDataForMap(polygon_url, statistics_url);
        }
    }

    requestDataForMap(polygon_url, statistics_url) {
        let request1 = axios.get(polygon_url);
        let request2 = axios.get(statistics_url);
        axios.all([request1, request2]).then(axios.spread((...responses) => {
            let response1 = responses[0];
            let response2 = responses[1];
            if (response1.status === 200 && response2.status === 200) {
                let polygonData = JSON.parse(response1.data.content);
                let statistics = response2.data;
                for (let i = 0; i < polygonData.features.length; i++) {
                    let feature_code = polygonData.features[i].properties.feature_code;
                    let particular_statistics = statistics.find(statistics_per_area => statistics_per_area.code === feature_code);
                    polygonData.features[i].statistics = particular_statistics.statistics;
                }
                this.geoJson.current.leafletElement.addData(polygonData);
                this.setState({
                    polygonData: polygonData,
                    loading: false
                });
            }
        }));
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
                        ref={this.geoJson}/>
                </Map>
                <div className={"fixed"}>
                    <TreeMenu data={treeData} debounceTime={125} disableKeyboard={false}
                              hasSearch onClickItem={event => this.onMenuItemClick(event)}
                              resetOpenNodesOnDataUpdate={false}/>
                </div>
                <div className={"absolute"}>
                    <PacmanLoader
                        size={100}
                        margin={2}
                        color={"#006600"}
                        loading={this.state.loading}/>
                </div>
                {this.state.loading && <div className={"loading-layer"}/>}
            </div>
        )
    }
}

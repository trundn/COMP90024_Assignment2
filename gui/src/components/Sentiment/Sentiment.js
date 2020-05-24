import React, {Component} from 'react'
import {GeoJSON, Map, TileLayer} from 'react-leaflet'
import axios from 'axios'
import './style.sass';
import TreeMenu from 'react-simple-tree-menu';
import GridLoader from 'react-spinners/GridLoader';
import backendUrl from '../../assets/backendUrl.js'
import {PieChart, Pie, Tooltip} from 'recharts';

export default class Sentiment extends Component {
    state = {
        treeData: [],
        lat: -37.8136,
        lng: 144.9631,
        zoom: 8,
        selectedId: 1,
        polygonData: null,
        pieChartData: null,
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
            weight: 1
        }
    }

    onEachFeature(feature, layer) {
        let offset = 0;
        let statistics = feature.statistics;
        let numberOfPositiveTweets = statistics.number_of_positive_tweets;
        let numberOfNegativeTweets = statistics.number_of_negative_tweets;
        if (numberOfPositiveTweets - numberOfNegativeTweets !== 0) {
            offset = (numberOfPositiveTweets - numberOfNegativeTweets) / (numberOfPositiveTweets + numberOfNegativeTweets)
        }
        let popupContent = `<Popup>
                                <h3>${feature.properties.feature_name}</h3>
                                <p>There is/are <strong>${statistics.number_of_positive_tweets}</strong> <strong>positive</strong> tweet(s)</p>
                                <p>There is/are <strong>${statistics.number_of_negative_tweets}</strong> <strong>negative</strong> tweet(s)</p>
                            </Popup>`;
        layer.bindPopup(popupContent);
        layer.on('click', () => {
            if (numberOfPositiveTweets === 0 && numberOfNegativeTweets === 0) {
                this.setState({
                    pieChartData: null
                });
            } else {
                this.setState({
                    pieChartData: [
                        {name: 'Positive', value: numberOfPositiveTweets},
                        {name: 'Negative', value: numberOfNegativeTweets}
                    ]
                });
            }

        });
        layer.on('mouseover', () => {
            layer.setStyle({
                'fillColor': '#fff2af',
                'fillOpacity': 0.5
            });
        });
        if (offset >= 0) {
            layer.setStyle({
                'fillColor': '#66ff66',
                'fillOpacity': 0.5 + offset * 0.5
            });
        } else {
            layer.setStyle({
                'fillColor': '#ff0000',
                'fillOpacity': 0.5 + offset * 0.5 * (-1)
            });
        }
        layer.on('mouseout', () => {
            if (offset >= 0) {
                layer.setStyle({
                    'fillColor': '#66ff66',
                    'fillOpacity': 0.5 + offset * 0.5
                });
            } else {
                layer.setStyle({
                    'fillColor': '#ff0000',
                    'fillOpacity': 0.5 + offset * 0.5 * (-1)
                });
            }
        });
    }

    componentDidMount() {
        axios.get(backendUrl.list_polygon).then(response => {
            if (response.status === 200) {
                let treeData = [];
                let melbourneNode = {
                    key: "Victoria",
                    label: "Victoria",
                    nodes: []
                };
                let sydneyNode = {
                    key: "New South Wales",
                    label: "New South Wales",
                    nodes: []
                };
                response.data.forEach(polygon => {
                    let treeDataItem = {
                        key: polygon.name,
                        label: polygon.name,
                        nodes: [],
                        polygonId: polygon.id
                    }
                    if (polygon.region === "Victoria") {
                        melbourneNode.nodes.push(treeDataItem);
                    } else if (polygon.region === "New South Wales") {
                        sydneyNode.nodes.push(treeDataItem);
                    } else {
                        treeData.push(treeDataItem);
                    }
                });
                treeData.push(melbourneNode);
                treeData.push(sydneyNode);

                let polygon_url = backendUrl.detail_polygon.format(treeData[0].polygonId);
                let statistics_url = backendUrl.statistics_in_polygon.format(treeData[0].polygonId);
                this.setState({
                    treeData: treeData,
                    loading: true
                });
                this.requestDataForMap(polygon_url, statistics_url);
            }
        });
    }

    onMenuItemClick(event) {
        if (event.polygonId) {
            if (event.polygonId !== this.state.selectedId) {
                this.setState({
                    selectedId: event.polygonId
                });
                let polygon_url = backendUrl.detail_polygon.format(event.polygonId);
                let statistics_url = backendUrl.statistics_in_polygon.format(event.polygonId);
                this.geoJson.current.leafletElement.clearLayers();
                this.requestDataForMap(polygon_url, statistics_url);
            }
        }
    }

    requestDataForMap(polygon_url, statistics_url) {
        this.setState({
            loading: true
        });
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
                });
            }
        })).then(() => {
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
                    <TileLayer
                        attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                    <GeoJSON key={"map"}
                             data={this.state.polygonData}
                             style={this.geoJSONStyle}
                             onEachFeature={(feature, layer) => {
                                 this.onEachFeature(feature, layer)
                             }}
                             ref={this.geoJson}/>
                </Map>
                <div className={"fixed"}>
                    <TreeMenu data={this.state.treeData} debounceTime={125} disableKeyboard={false}
                              hasSearch onClickItem={event => this.onMenuItemClick(event)}
                              resetOpenNodesOnDataUpdate={false}/>
                </div>
                <div className={"absolute"}>
                    <GridLoader
                        size={50}
                        margin={2}
                        color={'#006600'}
                        loading={this.state.loading}/>
                </div>
                {this.state.pieChartData &&
                <div className={"region-info"}>
                    <strong>Positive/Negative Ratio</strong>
                    <PieChart width={300} height={300}>
                        <Pie dataKey="value" isAnimationActive={false} data={this.state.pieChartData} cx={150} cy={150}
                             outerRadius={80} fill="#8884d8" label/>
                        <Tooltip/>
                    </PieChart>;
                </div>}
                {this.state.loading && <div className={'loading-layer'}/>}
            </div>
        )
    }
}

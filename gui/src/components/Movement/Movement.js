import React from 'react'
import {Map, Marker, Polyline, CircleMarker, Popup, TileLayer} from 'react-leaflet'
import axios from 'axios'
import './style.sass';
import PacmanLoader from 'react-spinners/PacmanLoader';
import config from '../../assets/config.js'
import TreeMenu from "react-simple-tree-menu";

export default class Movement extends React.Component {
    state = {
        zoom: 7,
        treeMenuData: [],
        polyline: null,
        startPoint: null,
        endPoint: null,
        startPointPopup: null,
        endPointPopup: null,
        borderPoints: [],
        userInfo: null,
        loading: false
    }

    componentDidMount() {
        this.setState({
            loading: true
        });
        axios.get(config.get_most_active_users).then(response => {
            if (response.status === 200) {
                let treeMenuData = [];
                let users = response.data;
                users.forEach(user => {
                    let dataItem = {
                        key: user.key[0],
                        label: user.key[1],
                        nodes: [],
                        user_key: user.key,
                        number_of_tweets: user.value
                    };
                    treeMenuData.push(dataItem);
                });
                console.log(treeMenuData);

                this.setState({
                    treeMenuData: treeMenuData
                });
            }
        }).then(() => {
            this.setState({
                loading: false
            });
        });
    }

    onMenuItemClick(event) {
        axios.get(config.find_route_url.format(JSON.stringify(event.user_key))).then(response => {
            if (response.status === 200) {
                let polyline = response.data;
                if (polyline.length > 0) {
                    this.setState({
                        polyline: polyline
                    });
                    let startPoint = polyline[0];
                    let endPoint = polyline[polyline.length - 1];
                    if (startPoint[0] === endPoint[0] && startPoint[1] === endPoint[1]) {
                        this.setState({
                            startPoint: startPoint,
                            endPoint: null,
                            startPointPopup: "Start & End Point",
                            endPointPopup: "Start & End Point"
                        });
                    } else {
                        this.setState({
                            startPoint: startPoint,
                            endPoint: endPoint,
                            startPointPopup: "Start Point",
                            endPointPopup: "End Point"
                        });
                    }
                    let borderPoints = [startPoint, endPoint];
                    for (let i = 1; i < polyline.length - 1; i++) {
                        let point = polyline[i];
                        let added = false;
                        for (let j = 0; j < borderPoints.length; j++) {
                            let borderPoint = borderPoints[j];
                            if (point[0] === borderPoint[0] && point[1] === borderPoint[1]) {
                                added = true;
                                break;
                            }
                        }
                        if (!added) {
                            borderPoints.push(point);
                        }
                    }
                    this.setState({
                        borderPoints: borderPoints
                    });
                }
            }
        });
        axios.get(config.get_user_info.format(event.user_key[0])).then(response => {
            if (response.status === 200) {
                if (response.data !== {}) {
                    this.setState({
                        userInfo: response.data.value
                    });
                }
            }
        });
    }

    render() {
        const center = [-37.8136, 144.9631];
        return (
            <div className={"relative"}>
                <Map center={this.state.startPoint ? this.state.startPoint : center} zoom={this.state.zoom}>
                    <TileLayer attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                               url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>

                    {this.state.polyline && <Polyline color="purple" positions={this.state.polyline}/>}
                    {this.state.startPoint &&
                    <Marker position={this.state.startPoint}>
                        <Popup>
                            {this.state.startPointPopup}
                        </Popup>
                    </Marker>}
                    {this.state.endPoint &&
                    <Marker position={this.state.endPoint}>
                        <Popup>
                            {this.state.endPointPopup}
                        </Popup>
                    </Marker>}
                    {this.state.borderPoints &&
                    this.state.borderPoints.map((borderPoint, index) => {
                        return <CircleMarker key={index} center={borderPoint} color="purple" fillOpacity={1}
                                             fill="purple"
                                             radius={5}/>
                    })}

                </Map>
                {this.state.userInfo && <div className={"user-info"}>
                    Name:<strong> {this.state.userInfo.name}</strong><br/>
                    Screen Name:<strong> {this.state.userInfo.screen_name}</strong><br/>
                    <p>{this.state.userInfo.description}</p>
                     {/*eslint-disable-next-line*/}
                    <img className={"user-info-image"} src={this.state.userInfo.profile_image_url}
                         alt={"profile-image"}/><br/>
                    Location: <strong>{this.state.userInfo.location}</strong>
                </div>}
                <div className={"fixed"}>
                    <TreeMenu data={this.state.treeMenuData} debounceTime={125} disableKeyboard={false}
                              hasSearch onClickItem={event => this.onMenuItemClick(event)}
                              resetOpenNodesOnDataUpdate={false}/>
                </div>
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

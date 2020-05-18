import React from 'react';
import ReactDOM from 'react-dom';
import TabPanel from './TabPanel';
import './index.css'

String.prototype.format = function () {
    let str = this;
    for (k in arguments) {
        str = str.replace("{" + k + "}", arguments[k])
    }
    return str
}

ReactDOM.render(<TabPanel/>, document.querySelector('#root'));

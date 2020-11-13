//import 'bootstrap/dist/css/bootstrap.min.css';
//import 'bootstrap/dist/js/bootstrap.bundle.min';

import 'startbootstrap-sb-admin-2/css/sb-admin-2.min.css'
import '@fortawesome/fontawesome-free/css/all.css';

import React from 'react';
import ReactDOM from 'react-dom';

import App from './App';

import WebFont from 'webfontloader';    
// import {BrowserRouter} from "react-router-dom";
import { BrowserRouter } from "react-router-dom";

require('bootstrap')

WebFont.load({
    google: {
        families: ['Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i']
    }
});

ReactDOM.render(
    <BrowserRouter>
        <App/>
    </BrowserRouter>, document.getElementById('root')
);

import React from 'react';
import {Link} from "react-router-dom";
import axios from "axios";
import { API } from "../function_utils";

export const Sidebar = () => (
    <ul className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion"
        id="accordionSidebar">

        {/* Sidebar - Brand */}
        <Link to="/dashboard" href="#"
              className="sidebar-brand d-flex align-items-center justify-content-center">
            <div className="sidebar-brand-icon">
                <i className="fas fa-cross fa-flip-vertical"></i>
            </div>
            <div className="sidebar-brand-text mx-3">
                Taint Saviour
            </div>
            <div className="sidebar-brand-icon">
                <i className="fas fa-cross fa-flip-vertical"></i>
            </div>
        </Link>

        {/* Divider */}
        <hr className="sidebar-divider my-0"/>

        {/* Nav Item */}
        <li className="nav-item">
            <Link href="#" className="nav-link" to="/dashboard">
                <i className="fas fa-fw fa-tachometer-alt"></i>
                <span>Dashboard</span>
            </Link>
        </li>

        {/* Divider */}
        <hr className="sidebar-divider"/>

        {/* Sidebar Heading */}
        <div className="sidebar-heading">Dataset</div>

        {/* Nav Item */}
        <li className="nav-item">
            <Link href="#" className="nav-link" to="/apks">
                <i className="fab fa-android"></i>
                <span>Apks</span>
            </Link>
        </li>

        {/* Divider */}
        <hr className="sidebar-divider"/>

        {/* Sidebar Heading */}
        <div className="sidebar-heading">Other</div>

        {/* Nav Item */}
        <li className="nav-item">
            <a href="https://github.com/ClaudioRizzo/TaintSaviour"
               className="nav-link">
                <i className="fab fa-github"></i>
                <span>Github</span>
            </a>
        </li>

        {/* Nav Item */}
        <li className="nav-item">
            <Link href="#" to="/about" className="nav-link">
                <i className="fas fa-heart"></i>
                <span>About</span>
            </Link>
        </li>

        {/* Divider */}
        <hr className="sidebar-divider"/>
        
        {/* Sidebar Heading */}
        <div className="sidebar-heading">Debugging</div>

        <li className="nav-item">
            <div style={{ cursor: "pointer" }}
                className="nav-link"
                onClick={() => {
                    axios.post(API + '/workers/push-job', {
                        'apk_id': "test",
                        'timeout': 60,
                        'signature': "<uk.ac.rhul.clod.samplejniapp.MainActivity: int testMe(int,int)>",
                        'isa': "x86_64"
                    }, { withCredentials: true })
                        .then((response) => {
                            if (response.data.success) {
                               alert("Test job correctly pushed")
                            } else {
                                console.log('error in pushing a job')
                            }
                        })
                        .catch((err) => console.log(err))
                }
                }>Fuzz Test</div>
        </li>
        <li className="nav-item">
            <div style={{ cursor: "pointer" }}
                className="nav-link"
                onClick={() => {
                    axios.get(API + '/token', { withCredentials: true })
                        .then((response) => {
                            prompt("Copy with Ctrl+c", response.data.token);
                        })
                        .catch((err) => console.log(err))
                }}>
                Get Auth Token
        </div>
        </li>
        {/* Divider */}
        <hr className="sidebar-divider"/>

    </ul>
);

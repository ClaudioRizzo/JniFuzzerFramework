import React, { Component } from "react";
import axios from "axios";
import { API } from "../function_utils";

export default class TopbarUserInfo extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: window.localStorage.getItem('username')
        };
    }

    handleClickLogout(evt) {
        axios.get(API+'/logout',
            { withCredentials: true })
            .then((response) => {
                console.log(response);
                window.localStorage.clear();
                window.location.replace('/');
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    render() {
        return (
            <li className="nav-item dropdown no-arrow">
                <a className="nav-link dropdown-toggle" href="#"
                    id="userDropdown" role="button" name="userDropdown"
                    data-toggle="dropdown"
                    aria-haspopup="true" aria-expanded="false">
                    <span
                        className="mr-2 d-none d-lg-inline text-gray-600 small">{this.state.username}</span>
                </a>
                {/* Dropdown - User Information */}
                <div
                    className="dropdown-menu dropdown-menu-right shadow animated--grow-in"
                    aria-labelledby="userDropdown">
                    <a className="dropdown-item" href="#">
                        <i className="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                        Profile
                    </a>
                    <a className="dropdown-item" href="#">
                        <i className="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"></i>
                        Settings
                    </a>
                    <a className="dropdown-item" href="#">
                        <i className="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>
                        Activity Log
                    </a>
                    <div className="dropdown-divider"></div>
                    <a className="dropdown-item" href="#"
                        onClick={evt => this.handleClickLogout(evt)}
                        data-toggle="modal" data-target="#logoutModal">
                        <i className="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                        Logout
                    </a>
                </div>
            </li>
        );
    }
}

import React, {Component} from "react";
import TopbarUserInfo from "./TopbarUserInfo";
import { SearchBar } from "./SearchBar";
import { TopBarTagFilters } from "./TopBarTagFilters";
import { JobNotification } from "./TopbarJobNotification";

export class Topbar extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <nav
                className="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">

                {/* Sidebar Toggle (Topbar) */}
                <button id="sidebarToggleTop"
                        className="btn btn-link d-md-none rounded-circle mr-3">
                    <i className="fa fa-bars"> </i>
                </button>

                {/* Topbar Search */}
                <SearchBar/>
                

                {/* <!-- Topbar Navbar --> */}
                <ul className="navbar-nav ml-auto">
                    
                    <JobNotification></JobNotification>
                    <TopBarTagFilters/>
                    <div className="topbar-divider d-none d-sm-block"></div>
                    
                    {/* Nav Item - User Information */}
                    <TopbarUserInfo/>

                </ul>

            </nav>
        );
    }
}

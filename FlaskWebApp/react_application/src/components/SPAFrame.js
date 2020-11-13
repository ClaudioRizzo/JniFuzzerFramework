import React from 'react';
import {Sidebar} from './Sidebar';
import {Redirect, Route, Switch} from "react-router-dom";
import {Apks} from "./Apks";
import {NotFound} from "./NotFound";
import {Topbar} from "./Topbar";
import {Dashboard} from "./Dashboard";
import {ApkResult} from "./ApkResult";
import {About} from "./About";
import {Test} from "./Test"
import {Jobs} from "./Jobs"
import { Login } from './Login';

export const SPAFrame = () =>
    (window.localStorage.getItem('username') === null)
        ? <Redirect to="/login"/>
        : (
            <div id="wrapper">
                <Sidebar/>
                {/* Content Wrapper */}
                <div id="content-wrapper" className="d-flex flex-column">

                    {/* Main Content */}
                    <div id="content">
                        <Topbar/>

                        {/*<Routes/>*/}
                        <Switch>
                            <Route path="/" exact component={Dashboard}/>
                            <Route path="/about" exact component={About}/>
                            <Route path="/dashboard" component={Dashboard}/>
                            <Route path="/apks" exact component={Apks}/>
                            <Route path="/testing" exact component={Test}/>
                            <Route path="/jobs" exact component={Jobs}/>
                            <Route path="/apks/:id" component={ApkResult}/>
                            <Route component={NotFound}/>
                        </Switch>
                    </div>
                </div>
            </div>
        );

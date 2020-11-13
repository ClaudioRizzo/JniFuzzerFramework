import React, { Component } from "react";
import axios from "axios";
import { ApkTags } from "./ApkTags";
import { Link, Route, Switch } from "react-router-dom";
import { ApkFlows } from "./ApkFlows";
import { ApkLibs } from "./ApkLibs";
import { ApkNotes } from "./ApkNotes";
import { FlowViz } from "./FlowViz";
import { API } from "../function_utils";
import {ApkSummary} from "./ApkSummary"

export class ApkResult extends Component {
    constructor(props) {
        super(props);
        this.state = {
            id: props.match.params.id,
            apk: {
                flows: [],
                libraries: [],
                notes: []
            }
        };

        this.onNotesUpdate = this.onNotesUpdate.bind(this);
    }

    componentDidMount() {
        axios.get(API + '/apks/' + this.state.id, { withCredentials: true })
            .then((response) => {
                this.setState({ apk: response.data })
            })
            .catch(function (error) {
                console.log(error);
            });
    }


    RenderApkFlows = () => {
        return <ApkFlows flows={this.state.apk.flows} parentId={this.state.id} />
    };

    RenderApkLibs = () => {
        return <ApkLibs libraries={this.state.apk.libraries}
            parentId={this.state.id} />
    };

    RenderApkNotes = () => {
        return <ApkNotes onUpdate={this.onNotesUpdate} notes={this.state.apk.notes} parentId={this.state.id} />
    };

    RenderFlowViz = (match) => {
        return <FlowViz flows={this.state.apk.flows} match={match} />
    };

    RenderApkSummary = () => {
        return <ApkSummary apk_id={this.props.match.params.id}/>
    }

    onNotesUpdate(notes) {
        console.log("a note has been added/removed: " + notes);
        var tmp_state = this.state;
        tmp_state.apk.notes = notes;
        this.setState(tmp_state);
    }

    render() {
        let lengthOrZero = function (p) {
            return (undefined === p) ? 0 : p.length
        };

        let n_flows = lengthOrZero(this.state.apk.flows);
        let n_libs = lengthOrZero(this.state.apk.libraries);
        let n_notes = lengthOrZero(this.state.apk.notes);

        return (

            <div className="container-fluid">
                <div
                    className="d-sm-flex align-items-center justify-content-between mb-4">
                    <h1 className="h3 mb-0 text-gray-800" title={this.state.id}>
                        {this.state.apk.app_name}
                    </h1>
                    <ApkTags apkId={this.state.id} />
                    <a href={API + '/apks/' + this.state.id + '/download'}
                        className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                        <i className="fas fa-download fa-sm text-white-50"> </i> Download
                        APK
                    </a>
                </div>

                <div className="row">

                    <div className="col-xl-3 col-md-6 mb-4">
                        <Link to={"/apks/" + this.state.id + "/summary"}>
                            <div className="card border-left-primary shadow h-100 py-2">
                                <div className="card-body">
                                    <div
                                        className="row no-gutters align-items-center">
                                        <div className="col mr-2">
                                            <div
                                                className="text-xs font-weight-bold text-danger text-uppercase mb-1">Summary
                                            </div>
                                            <div
                                                className="h5 mb-0 font-weight-bold text-gray-800">{this.state.apk.app_name}
                                            </div>
                                        </div>
                                        <div className="col-auto">
                                            <i className="fab fa-android fa-2x text-gray-300"> </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>

                    <div className="col-xl-3 col-md-6 mb-4">
                        <Link to={"/apks/" + this.state.id + "/flows"}>

                            <div
                                className="card border-left-primary shadow h-100 py-2">
                                <div className="card-body">
                                    <div
                                        className="row no-gutters align-items-center">
                                        <div className="col mr-2">
                                            <div
                                                className="text-xs font-weight-bold text-primary text-uppercase mb-1">Flows
                                            </div>
                                            <div
                                                className="h5 mb-0 font-weight-bold text-gray-800">{n_flows}
                                            </div>
                                        </div>
                                        <div className="col-auto">
                                            <i className="fas fa-tint fa-2x text-gray-300"> </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>

                    <div className="col-xl-3 col-md-6 mb-4">
                        <Link to={"/apks/" + this.state.id + "/libraries"}>
                            <div
                                className="card border-left-success shadow h-100 py-2">
                                <div className="card-body">
                                    <div
                                        className="row no-gutters align-items-center">
                                        <div className="col mr-2">
                                            <div
                                                className="text-xs font-weight-bold text-success text-uppercase mb-1">Libraries
                                            </div>
                                            <div
                                                className="h5 mb-0 font-weight-bold text-gray-800">{n_libs}
                                            </div>
                                        </div>
                                        <div className="col-auto">
                                            <i className="fas fa-book fa-2x text-gray-300"> </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>

                    <div className="col-xl-3 col-md-6 mb-4">
                        <Link href="#" to={"/apks/" + this.state.id + "/notes"}>

                            <div
                                className="card border-left-danger shadow h-100 py-2">
                                <div className="card-body">
                                    <div
                                        className="row no-gutters align-items-center">
                                        <div className="col mr-2">
                                            <div
                                                className="text-xs font-weight-bold text-danger text-uppercase mb-1">Notes
                                            </div>
                                            <div
                                                className="h5 mb-0 font-weight-bold text-gray-800">{n_notes}
                                            </div>
                                        </div>
                                        <div className="col-auto">
                                            <i className="fas fa-sticky-note fa-2x text-gray-300"> </i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>
                </div>
                
                {/*<Routes/>*/}
                <Switch>
                    <Route path="/apks/:id/flows" exact
                        component={this.RenderApkFlows} />
                    <Route path="/apks/:id/libraries"
                        component={this.RenderApkLibs} />
                    <Route path="/apks/:id/notes" component={this.RenderApkNotes} />
                    <Route path="/apks/:id/summary" component={this.RenderApkSummary} />
                </Switch>
            </div>
        );
    }

}

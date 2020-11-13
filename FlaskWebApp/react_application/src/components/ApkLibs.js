import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API, filterByTag } from "../function_utils";

export class ApkLibs extends Component {
    constructor(props) {
        super(props);

        this.state = {
            libraries: props.libraries,
            parentId: props.parentId
        };

    }

    
    render() {
        if (this.state.libraries === undefined) {
            return (<div>Libraries!</div>);
        }

        var libraries_component = this.state.libraries.map(
            (lib, i) => <ApkLibrary name={lib.name}
                symbols={lib.symbols}
                apks={lib.apks}
                fail={lib.fail} 
                isa={lib.isa}
                key={i}/>
        )

        return (
            <span>

                <h1 className="h4 mb-0 text-gray-800">
                    Libraries
                </h1>
                <br />
                {libraries_component}
            </span>
        );
    }
}

/**
 * This component represent an APK library in this project.
 * As such, it will have the following props:
 * 
 * (string) name
 * (list) symbols
 * (list) apks
 * (bool) fail
 */
class ApkLibrary extends Component {
    constructor(props) {
        super(props);
        this.state = {
            all_apk: this.props.apks,
            apks: this.props.apks,
            showApks: false,
            loaded: false
        }
        this.localStorageUpdated = this.localStorageUpdated.bind(this);
    }

    
    componentDidMount() {
        
        axios.post(API + '/apks', { apks: this.props.apks },
            { withCredentials: true })
            .then((response) => {
                var showApks = this.state.showApks
                this.setState({
                    all_apks: response.data,
                    apks: filterByTag(response.data), 
                    showApks: showApks,
                    loaded: true,
                }, () => window.addEventListener('tag-filter', this.localStorageUpdated))
            })
            .catch(function (error) {
                console.log(error);
            });

    }


    componentWillUnmount() {
        window.removeEventListener('tag-filter', this.localStorageUpdated);
    }

    localStorageUpdated() {
        this.setState({
            all_apks: this.state.all_apks,
            apks: filterByTag(this.state.all_apks), 
            showApks: this.state.showApks,
            loaded: true,});
    }

    getCheckmark() {
        let lib = this.props
        let fa = (lib.fail) ? "fas fa-times-circle" : "fas fa-check-circle";
        let col = (lib.fail) ? "#e74a3b" : "#1cc88a";
        let title = (lib.fail) ? "Failed" : "Succeeded";

        return (
            <i className={fa + " fa-sm"} style={{ color: col }}
                title={title}> </i>
        );
    }

    renderSymbol(sym, i) {
        return (
            <span key={i}><span
                className="lst-inline">{sym.name}</span>, </span>
        )
    }

    renderSymbols(symbols) {
        if (symbols.length === 0) {
            return (<span className="text-gray-500">None</span>);
        }
        return (symbols.map((x, i) => this.renderSymbol(x, i)));
    }

    renderApk(apk, key) {
        let thisOne = (apk === this.state.parentId) ? "(This one)" : "";
        return (
            <li key={key} className="texttt"><Link
             to={`/apks/${apk}`}>{apk}</Link> {thisOne}
            </li>)
    }

    toggleShowMore() {
        this.setState({
            all_apks: this.state.all_apks,
            apks: this.state.apks,
            showApks: !this.state.showApks,
            loaded: this.state.loaded,
        });
    }

    renderShowMore() {
        let text = (this.state.showApks) ? "Hide apks" : "Show more apks (" + this.props.apks.length + ")";
        return (
            <div onClick={() => this.toggleShowMore()} 
            style={{cursor: 'pointer'}}>{text}</div>
        );
    }

    renderApks() {
        let end = (this.state.showApks) ? this.props.length : 5;
        return (
            <span>
                <ul>
                    {this.state.apks.slice(0, end).map((apk, i) => this.renderApk(apk._id, i))}
                </ul>
                {(this.state.apks.length > 5) ? this.renderShowMore() : ""}
            </span>
        )
    }

    // TODO (clod): show a round loading into the card while it is loading
    render() {
        if(!this.state.loaded){
            return <div></div>
        }
        return (
            <div id={this.props.name} className="row">
                <div className="col-lg-12">

                    <div className="card shadow mb-4">
                        <div className="card-header py-3">
                            <h6 className="m-0 font-weight-bold text-primary">{this.props.name+" ("+this.props.isa+")"} {this.getCheckmark()}</h6>
                        </div>
                        <div className="card-body">

                            <div className="subcard-body">
                                <h1 className="h5 mb-0 text-gray-800">
                                    Symbols
                                </h1>

                                <div>
                                    {/*{el.symbols.map((x, i) => this.renderSymbol(x, i))}*/}
                                    {this.renderSymbols(this.props.symbols)}
                                </div>
                            </div>

                            <div>
                                <h1 className="h5 mb-0 text-gray-800">
                                    All APKs
                                </h1>

                                <div>
                                    {this.renderApks()}
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

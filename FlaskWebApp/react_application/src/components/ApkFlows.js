import React, { Component } from "react";
import { Link } from "react-router-dom";
import { FuzzDialog } from "./FuzzDialog"



export class ApkFlows extends Component {
    constructor(props) {
        super(props);
        this.state = {
            flows: props.flows,
            parentId: props.parentId
        };

    }

    drawNode(node, i) {
        return (
            node.called_signature !== "" && node.is_native_node ?
                <tr key={i}>
                    <td className="texttt text-black bg-warning">
                        {node.stmt}
                        <FuzzDialog className="text-black bg-white"
                            apk_id={this.state.parentId}
                            sink={node.called_signature}
                            index={i}></FuzzDialog>
                    </td>
                </tr>
                :
                <tr key={i}>
                    <td className="texttt">
                        {node.stmt}
                    </td>
                </tr>
        );
    }

    drawSources(source, i) {
        return (
            <tr key={i}>
                <td className="texttt">{source}</td>
            </tr>
        );
    }

    createRow(el, i) {
        if (el.path === undefined || el.source === undefined) {
            // we are supporting old Database here... legacy....
            return (
                <div className="row" key={i}>
                    <div className="col-lg-12">

                        <div className="card shadow mb-4">
                            <div
                                className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 className="m-0 font-weight-bold text-primary">#{i} Sink {el.sink.length > 90 ? el.sink.slice(0, 90) + '...' : el.sink}</h6>
                                <div className="row">
                                    <div className="col">
                                        <Link
                                            to={"/apks/" + this.state.parentId + "/flows/" + i}
                                            href="#"
                                            className="d-none d-sm-inline-block btn btn-sm btn-primary">
                                            Graph
                                        </Link>
                                    </div>
                                    <div className="col">
                                        <FuzzDialog apk_id={this.state.parentId} sink={el.sink} index={i}></FuzzDialog>
                                    </div>
                                </div>
                            </div>
                            <div className="card-body">
                                <div className="table-responsive">
                                    <table className="table table-bordered"
                                        id="dataTable"
                                        width="100%" cellSpacing="0">
                                        <thead>
                                            <tr>
                                                <th>Sources</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {el.sources.map((x, j) => this.drawSources(x, j))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>);
        } else {
            return (
                <div className="row" key={i}>
                    <div className="col-lg-12">

                        <div className="card shadow mb-4">
                            <div
                                className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 className="m-0 font-weight-bold text-primary">
                                    #{i} Source {el.source.length > 90 ? el.source.slice(0, 90) + '...' : el.source} -> Sink {el.sink.length > 90 ? el.sink.slice(0, 90) + '...' : el.sink}
                                </h6>
                            </div>
                            <div className="card-body">
                                <div className="table-responsive">
                                    <table className="table table-bordered"
                                        id="dataTable"
                                        width="100%" cellSpacing="0">
                                        <thead>
                                            <tr>
                                                <th>Source to Sink</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {el.path.map((x, j) => this.drawNode(x, j))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    }

    render() {
        if (this.state.flows === undefined) {
            return (<div>Flows!</div>);
        }
        return (
            <span>

                <h1 className="h4 mb-0 text-gray-800">
                    Flows
        </h1>
                <br />
                {this.state.flows.map((x, i) => this.createRow(x, i))}
            </span>
        );
    }
}


import React from "react";
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { Link } from "react-router-dom";

import 'react-bootstrap-table/dist/react-bootstrap-table-all.min.css'

/**
 * The component is meant to show a list of apks along with the number of flows and libraries and notes.
 * 
 * Props:
 *      entries: list of elements with the following property:
 *                  - apk_id
 *                  - n_flows
 *                  - n_libraries
 *                  - n_notes
 */
export class ApksTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = { apks: [], entries: this.props.entries, showDialog: false }
        this.options = {
            paginationSize: 5,
            
        };

        this.apkIdFormat = this.apkIdFormat.bind(this);
    }

    componentWillReceiveProps(nextProps) {
        var newState = this.state;
        newState.entries = nextProps.entries;
        this.setState(newState);
    }

    apkIdFormat(cell){
        return <Link className="texttt" to={"/apks/"+cell+"/summary"}>{cell}</Link>
    }

    render() {
        return (

            <div className="container-fluid">
                <BootstrapTable
                    search={true}
                    data={this.state.entries}
                    pagination
                    options={this.options}
                >
                    <TableHeaderColumn  dataField='_id' isKey={true} dataFormat={this.apkIdFormat}>Apks</TableHeaderColumn>
                    <TableHeaderColumn  dataField='n_flows' filter={{type: 'NumberFilter'}}>#Flows</TableHeaderColumn>
                    <TableHeaderColumn  dataField='n_libs' filter={{type: 'NumberFilter'}}>#Libs</TableHeaderColumn>
                    <TableHeaderColumn  dataField='n_notes'>#Notes</TableHeaderColumn>
                </BootstrapTable>

            </div>
        );
    }
}
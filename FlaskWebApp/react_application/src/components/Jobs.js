import React, { Component } from "react";
import axios from "axios";
import { API } from "../function_utils";
import 'react-bootstrap-table/dist/react-bootstrap-table-all.min.css'
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { Link } from "react-router-dom";


export class Jobs extends React.Component {
    constructor(props) {
        super(props);
        this.state = { compltedJobs: [] }
        this.formatID.bind();
        this.apkIdFormat.bind();
    }

    compareJobByRequestUtcEpoch(job1, job2) {
        if (job1.utc_epoch_request < job2.utc_epoch_request) {
            return 1;
        } else if (job1.utc_epoch_request > job2.utc_epoch_request) {
            return -1;
        } else {
            return 0;
        }
    }

    componentDidMount() {
        axios.get(API + '/workers/completed-jobs',
            { withCredentials: true })
            .then((response) => {
                //console.log(response.data);
                this.setState({ compltedJobs: response.data.jobs.sort(this.compareJobByRequestUtcEpoch) });
            });
    }

    formatID(reportId) {
        return <div>
            <span>{reportId}</span>
            <a href={API + '/worker/jobs/' + reportId + '/download'}
            className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
            Download
            </a>
        </div>;
    }

    apkIdFormat(cell) {
        return <Link className="texttt" to={"/apks/" + cell + "/summary"}>{cell}</Link>
    }

    formatDryRun(dry_run) {
        return dry_run === "Failed" ?
            <span className="glyphicon glyphicon-remove-sign">Failed</span>
            :
            <span className="glyphicon glyphicon-ok">Success</span>
    }

    render() {

        var tableData = this.state.compltedJobs.map((job, index) => {
            var date = new Date(0);
            date.setUTCSeconds(job.utc_epoch_request)
            return {
                "_id": job._id,
                "date": date.toDateString(),
                "apk_id": job.data.apk_id,
                "dry_run": job.dry_run ? "Failed" : "Success",
                "signature": job.data.signature
            }
        })

        return (

            <div className="container-fluid">
                <BootstrapTable
                    search={true}
                    data={tableData}
                    pagination
                //options={this.options}
                >
                    <TableHeaderColumn dataField='_id' isKey={true} dataFormat={this.formatID}>Job ID</TableHeaderColumn>
                    <TableHeaderColumn dataField='apk_id' dataFormat={this.apkIdFormat}>APK ID</TableHeaderColumn>
                    <TableHeaderColumn dataField='date'>Date</TableHeaderColumn>
                    <TableHeaderColumn dataField='signature' filter={{ type: 'TextFilter', delay: 1000 }}>Signature</TableHeaderColumn>
                    <TableHeaderColumn dataField='dry_run' dataFormat={this.formatDryRun}
                        filter={{ type: 'SelectFilter', options: { "Success": "Success", "Failed": "Failed" } }}>Dry Run</TableHeaderColumn>

                </BootstrapTable>

            </div>
        );
    }
}
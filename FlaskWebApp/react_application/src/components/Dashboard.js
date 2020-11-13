import React from "react";
import "../css/taint-saviour.css";
import ProgressBar from 'react-bootstrap/ProgressBar'
import axios from "axios";
import { API } from "../function_utils";

export class Dashboard extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {



        var dashboard =
            <div className="container-fluid">


                <div className="d-sm-flex align-items-center justify-content-between mb-4">
                    <h1 className="h3 mb-0 text-gray-800">Dashboard</h1>
                    <a href="#" className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i className="fas fa-download fa-sm text-white-50"></i> Generate Report</a>
                </div>

                <JobsProgressCard></JobsProgressCard>


            </div>

        return dashboard;

    }
}

class JobsProgressCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = { jobs: [] }
    }

    componentDidMount() {
        axios.get(API + '/workers/active-jobs',
            { withCredentials: true })
            .then((response) => {
                this.setState({ jobs: response.data })
                /*
                this.interval = setInterval(() => {
                    axios.get(API + '/workers/active-jobs', { withCredentials: true }).then((response) => {
                        let newJobs= response.data;
                        let newState = this.state;
                        newState.jobs = newJobs;
                        this.setState(newState);
                    })
                }, 10000)
                */

            })
            .catch(function (error) {
                console.log(error);
            });
    }

    render() {

        return (
            <div className="card shadow mb-4">
                <div className="card-header py-3">
                    <h6 className="m-0 font-weight-bold text-primary">Jobs Progress</h6>
                </div>
                <div className="card-body">
                    {this.state.jobs.map(job => {
                        var date = new Date(0)
                        date.setUTCSeconds(job.utc_epoch_request)
                        return <JobProgressBar key={job._id}
                            job_id={job._id}
                            progress={job.progress}
                            job_start={date.toDateString()} 
                            status={job.status}/>
                    })}
                </div>
            </div>
        );
    }

}

/**
 * Props:
 *      progres: progress of the current job
 *      job_id: id of the job to render
 *      job_start: when this job was started
 */
class JobProgressBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = { job_start: this.props.job_start, job_id: this.props.job_id, progress: this.props.progress, failed: (this.props.status === 'completed-failed')}
    }

    componentDidMount() {
        this.interval = setInterval(() => {
            axios.get(API + '/workers/job-progress/' + this.state.job_id, { withCredentials: true }).then((response) => {
                let newProgress = response.data.progress;
                let failed = response.data.status === 'completed-failed'
                let newState = this.state;
                newState.progress = newProgress;
                newState.failed = failed
                this.setState(newState);
            })
        }, 10000)
    }

    render() {
        let prog = parseFloat(this.state.progress).toFixed(0)
        if(this.state.failed){
            return(
                <div>
                    <h4 className="small font-weight-bold">Job {this.state.job_id} started on {this.state.job_start}
                        <span className="float-right">{"100%"}</span>
                    </h4>
                    <div className="mb-4">
                    <ProgressBar variant={"danger"} now={100} label={"100%"} animated={false} srOnly/>
                    </div>
                </div>
            )
        } else {
            return (
                <div>
                    <h4 className="small font-weight-bold">Job {this.state.job_id} started on {this.state.job_start}
                        <span className="float-right">{`${prog}%`}</span>
                    </h4>
                    <div className="mb-4">
                    <ProgressBar variant={this.state.progress === 100 ? "success" : ""} now={this.state.progress} label={`${prog}%`} animated={this.state.progress !== 100} srOnly/>
                    </div>
                </div>
            )
        }
    }


}

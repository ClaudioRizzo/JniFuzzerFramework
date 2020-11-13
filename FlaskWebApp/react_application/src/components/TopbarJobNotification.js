import React, { Component } from "react";
import axios from "axios";
import { API } from "../function_utils";

export class JobNotification extends React.Component {
    constructor(props) {
        super(props);
        this.state = {compltedJobs: []}
        this.onJobSeen = this.onJobSeen.bind(this);
        
    }

    hasjob(jobList, job) {
        // This method inside a callback doesn't work for some reason
        jobList.forEach(currJob => {
            if(currJob._id === job._id){
                return true
            }
        });
        return false;
    }

    compareJobByRequestUtcEpoch(job1, job2){
        if(job1.utc_epoch_request < job2.utc_epoch_request) {
            return 1;
        } else if(job1.utc_epoch_request > job2.utc_epoch_request) {
            return -1;
        } else {
            return 0;
        }
    }

    jobArrayUnion(x, y) {
        var obj = {};
        for (var i = x.length - 1; i >= 0; --i)
            obj[x[i]._id] = x[i];
        for (var i = y.length - 1; i >= 0; --i)
            obj[y[i]._id] = y[i];
        var res = []
        for (var k in obj) {
            if (obj.hasOwnProperty(k))  // <-- optional
                res.push(obj[k]);
        }
        return res;
    }

    getUnseenJobs(){
        var unseenJobs = [];
        this.state.compltedJobs.forEach(job => {
            if(!job.seen) {
                unseenJobs.push(job);
            }
        })
        return unseenJobs;
    }

    howManyUnseen(){
        return this.getUnseenJobs().length
    }

    componentDidMount() {
        axios.get(API+'/workers/completed-jobs',
            { withCredentials: true })
            .then((response) => {
                //console.log(response.data);
                this.setState({compltedJobs: response.data.jobs.sort(this.compareJobByRequestUtcEpoch)})
                
                this.interval = setInterval(() => {
                    axios.get(API+'/workers/unseen-jobs', { withCredentials: true }).then((response) => {
                        let polledJobs = response.data.jobs;
                        let newState = this.state;
                        
                        newState.compltedJobs = this.jobArrayUnion(newState.compltedJobs, polledJobs);
                        
                        newState.compltedJobs.sort(this.compareJobByRequestUtcEpoch)
                        this.setState(newState);   
                    })
                }, 10000)
            })
            
            .catch(function (error) {
                console.log(error);
            });
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    onJobSeen(job_id, seen) {
        axios.post(API+'/workers/completed-jobs/',
            {job_id: job_id, seen: seen},
            { withCredentials: true })
            .then((response) => {
                var newState = this.state;
                newState.compltedJobs = response.data.jobs;
                newState.compltedJobs.sort(this.compareJobByRequestUtcEpoch)
                this.setState(newState);
            })
            .catch(err=>console.log(err))
    }

    render(){
        return(
        <li className="nav-item dropdown no-arrow mx-1">
        <a className="nav-link dropdown-toggle" href="#" id="alertsDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i className="fas fa-bell fa-fw"></i>
          
          <span className="badge badge-danger badge-counter">
            {this.howManyUnseen() > 0 ? this.howManyUnseen() : ""}
          </span>
        </a>
        
        <div className="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="alertsDropdown">
          <h6 className="dropdown-header">
            Job Alers
          </h6>
          {this.state.compltedJobs.map((job, index)=>{
              return <JobAlert apk_id={job.data.apk_id} onSeen={this.onJobSeen} epoch={job.utc_epoch_request} seen={job.seen} job_id={job._id} key={job._id}/>
          })}
          <a className="dropdown-item text-center small text-gray-500" href="#">Show All Alerts</a>
        </div>
      </li>);
    }
}

class JobAlert extends React.Component{
    constructor(props){
        super(props);
        this.state = {seen: props.seen}
        this.onEntryClicked = this.onEntryClicked.bind(this)
    }

    onEntryClicked(job_id, seen){
        // we update the parent component
        this.props.onSeen(job_id, seen);

        // we update the entry
        var newState = this.state
        newState.seen = seen;
        this.setState(newState);
    }

    onDownloadReport(job_id, seen){
        // we simply mark the job as seen if it was unseen
        if(!this.state.seen){
            this.onEntryClicked(job_id, seen);
        }
    }

    render() {
        var date = new Date(0);
        date.setUTCSeconds(this.props.epoch)
        var generate_report = 
            <a onClick={() => this.onDownloadReport(this.props.job_id, !this.state.seen)} 
               href={API + '/worker/jobs/' + this.props.job_id + '/download'} className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                <i className="fas fa-download fa-sm text-white-50"></i> 
                Download Report
            </a>

        var entry = this.state.seen ?
            <div className="dropdown-item d-flex align-items-center">
                <div className="mr-3">
                    <div style={{cursor: 'pointer'}} onClick={() => this.onEntryClicked(this.props.job_id, !this.state.seen)} 
                         className="icon-circle bg-primary">
                        <i className="fas fa-file-alt text-white"></i>
                    </div>    
                </div> 
                <div >
                    <div className="small text-gray-500">{date.toLocaleString()}</div>
                    <span>
                        apk: {this.props.apk_id.slice(0,20)}... 
                    </span>
                    <p>job: {this.props.job_id}</p>
                    {generate_report}
                </div>
            </div> 
            :
            <div className="dropdown-item d-flex align-items-center">
                <div className="mr-3">
                    <div style={{cursor: 'pointer'}} onClick={() => this.onEntryClicked(this.props.job_id, !this.state.seen)} 
                         className="icon-circle bg-primary">
                        <i className="fas fa-file-alt text-black"></i>
                    </div>    
                </div>
                <div >
                    <div className="small text-gray-500">{date.toLocaleString()}</div>
                    <span className="font-weight-bold">
                    apk: {this.props.apk_id.slice(0,20)}...
                    </span>
                    <p>job: {this.props.job_id}</p>
                    {generate_report}
                    
                </div>
            </div>

        return entry;
        
    }
}
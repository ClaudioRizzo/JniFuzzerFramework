import React from "react";
import axios from "axios";
import { API } from "../function_utils";

export class FuzzDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = { apk_id: props.apk_id, sink: props.sink, timeout: 0, isa: 'armeabi-v7a'}
        this.onFuzzRequest = this.onFuzzRequest.bind(this);
        this.onTimeoutUpdated = this.onTimeoutUpdated.bind(this);
        this.onIsaRadioChange = this.onIsaRadioChange.bind(this);
    
    }   

    onTimeoutUpdated(timeout){
        var stateTmp = this.state;
        stateTmp.timeout = timeout;
        this.setState(stateTmp);
    }

    onIsaRadioChange(isa) {
        var stateTmp = this.state;
        stateTmp.isa = isa;
        this.setState(stateTmp);
        
    }

    onFuzzRequest(apk_id, timeout, sink_id, isa) {
        axios.post(API + '/workers/push-job', {
            'apk_id': apk_id,
            'timeout': timeout,
            'signature': sink_id,
            'isa': isa
        }, { withCredentials: true })
            .then((response) => {
                if (response.data.success) {
                    this.closeButton.click()
                } else {
                    console.log('booo')
                }
            })
            .catch((err) => console.log(err))
    }

    render() {
        return (
            <div>
                <button type="button" className="btn btn-primary btn-sm" data-toggle="modal" data-target={"#modal-" + this.props.index}>
                    Fuzz 
                </button>

                <div className="modal fade" id={"modal-" + this.props.index} tabIndex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                    <div className="modal-dialog modal-dialog-centered" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title" id="exampleModalLongTitle">{this.state.apk_id.slice(0, 10)}...</h5>
                                <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div className="modal-body">
                            <FuzzForm onIsaRadioChange={this.onIsaRadioChange} onRadioChange={this.onTimeoutUpdated}> </FuzzForm>
                            </div>
                            <div className="modal-footer">
                                <button ref={button => this.closeButton = button} type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
                                <button type="button" className="btn btn-primary" 
                                        onClick={()=>this.onFuzzRequest(this.state.apk_id, 
                                            this.state.timeout, this.state.sink, this.state.isa)
                                        }>Submit
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>);
    }
}

class FuzzForm extends React.Component {
    // supported timeouts [0.5h, 1h, 3h, 6h, 12h, 24h, 48h]
    constructor(props) {
        super(props);
        this.state = {timeouts: [0.5, 1, 3, 6, 12, 24, 48], isa: ['armeabi', 'armeabi-v7a', 'x86', 'x86_64']}
    }

    createRadio(index, value) {
        return(
        <div key={index} className="form-check">
            <input onClick={(event) => {
                var toHours = event.target.value;
                var toSeconds = event.target.value * 60 * 60;
                this.props.onRadioChange(toSeconds);
            }} 
                   className="form-check-input" 
                   type="radio" 
                   name="timeout-radios" 
                   id={"timeout-"+index} value={value} />
            <label className="form-check-label" htmlFor={"timeout-"+index}>
                {value} hours
            </label>
        </div>);
    }

    createIsaRadio(index, value){
        return(
        <div key={index} className="form-check">
            <input onClick={(event) => {
                var isa = event.target.value;
                
                this.props.onIsaRadioChange(isa);
            }} 
                   className="form-check-input" 
                   type="radio" 
                   name="isa-radios" 
                   id={"isa-"+index} value={value}/>
            <label className="form-check-label" htmlFor={"isa-"+index}>
                {value}
            </label>
        </div>);
    }

    render() {
        return(
            <div>
                <h4>Select Timeout</h4>
                {this.state.timeouts.map((timeout, index) => {
                    return this.createRadio(index, timeout)
                })}
                <h4>Select ISA</h4>
                {this.state.isa.map((isa, index) => {
                    return this.createIsaRadio(index, isa)
                })}
            </div>
        )
    }

}
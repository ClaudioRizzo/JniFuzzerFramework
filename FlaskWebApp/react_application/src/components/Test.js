import React from "react";
import axios from "axios";
import { API } from '../function_utils'
export class Test extends React.Component {
    constructor(props) {
        super(props);
        this.state = { signatures: [] };
        this.testSignature.bind();
    }

    componentDidMount() {
        axios.get(API + '/signatures/test',
            { withCredentials: true }).then((response) => {
                console.log(response);
                this.setState({ signatures: response.data });
            });
    }

    testSignature(signature, timeout) {
        if (!this.state.signatures.includes(signature)) {
            console.log("invalid signature " + signature);
            return;
        }

        axios.post(API + '/workers/push-job', {
            'apk_id': "test",
            'timeout': timeout,
            'signature': signature,
            'isa': "x86_64"
        }, { withCredentials: true })
            .then((response) => {
                if (response.data.success) {
                    alert("Test job correctly pushed")
                } else {
                    console.log('error in pushing a job')
                }
            })
            .catch((err) => console.log(err))
    }

    render() {
        return (this.state.signatures.map((signature, index) => {
            return (<div>
                <h5>{signature}</h5>
                <div class="btn-group btn-group-toggle" data-toggle="buttons">
                    <label class="btn btn-secondary">
                        <button type="button" onClick={() => this.testSignature(signature, 60)}/> 60sec
                    </label>
                    <label class="btn btn-secondary">
                        <button type="button" onClick={() => this.testSignature(signature, 1800)}/> 30mins
                    </label>
                    <label class="btn btn-secondary">
                        <button type="button" onClick={() => this.testSignature(signature, 3600)}/> 1hour
                    </label>
                </div>
            </div>);
        }));
    }
}
import React from "react";
import axios from "axios";
import { API } from "../function_utils";

export class ApkSummary extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            apk: {}
        }
    }

    componentDidMount() {
        axios.get(API + '/apks/' + this.props.apk_id, { withCredentials: true })
            .then((response) => {
                
                this.setState({ apk: response.data })
                console.log("here: "+this.state.apk.app_name)
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    render() {
        return (<div>This has to be currently implemented... :)</div>)
    }
}
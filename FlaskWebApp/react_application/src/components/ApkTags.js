import React, { Component } from "react";
import axios from "axios";
import { API } from "../function_utils";


export class ApkTags extends Component {
    constructor(props) {
        super(props);
        this.state = { 'tags': [] }
    }

    componentDidMount() {
        axios.get(API + '/apks/' + this.props.apkId + '/tags', { withCredentials: true })
            .then((response) => {
                this.setState({ 'tags': response.data });
            }).then((response) => {

            });
    }


    render() {
        let apkId = this.props.apkId;
        return (
            <div id="tags-container">
                <div className="row">
                    {this.state.tags.map(function (tag, index) {
                        return (
                            <ApkTag key={index}
                                apkId={apkId}
                                tagId={tag.tag_id}
                                active={tag.active}
                                color={tag.color} />
                        )
                    })}
                </div>
            </div>);
    }
}


class ApkTag extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            active: this.props.active
        };
    }


    updateTag(value) {
        let action = (this.state.active) ? 'unset' : 'set';

        let url = (
            API + '/apks/' + this.props.apkId +
            '/tags/' + this.props.tagId + '/' + action);

        axios.post(url, {}, { withCredentials: true });
    }

    onTagUpdated(event) {
        this.setState({ active: !this.state.active });
        this.updateTag(!this.state.active);
    }

    render() {
        let style = { borderColor: this.props.color };
        if (this.state.active) {
            style.backgroundColor = this.props.color
        }
        return (
            <div className="tag-spacer">
                <div
                    onClick={(e) => this.onTagUpdated(e)}
                    className="circle-small inline"
                    style={style}>
                </div>
            </div>

        );
    }
}



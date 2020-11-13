import React, { Component } from "react";
import axios from "axios";
import { API, isColorInFilter, removeTagFilter, addTagFilter } from "../function_utils";

export class TopBarTagFilters extends Component {
    constructor(props) {
        super(props);
        this.state = { 'tags': [] }
    }

    componentDidMount() {
        axios.get(API + '/tags', { withCredentials: true })
            .then((response) => {
                console.log(response.data);
                let tags = [];
                for (var i = 0; i < response.data.length; i++) {
                    let tag = response.data[i];
                    
                    tag.active = isColorInFilter(tag.color);
                    
                    tags.push(tag);
                }

                this.setState({ 'tags': tags });
            }).then((response) => {
            });
    }

    render() { 
        return (
            
            <li className="nav-item dropdown no-arrow mx-1">

                <div className="nav-link dropdown-toggle" 
                    id="filterDropdown" role="button"
                    data-toggle="dropdown"
                    aria-haspopup="true" aria-expanded="false"
                    style={{cursor: "pointer"}}>
                    Filters
                </div>

                <div className="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in"
                    aria-labelledby="messagesDropdown">
                    <h6 className="dropdown-header">
                        Available Tag Filters
                    </h6>

                    {/* here we place the TagFilters */}
                    {this.state.tags.map(function (tag, index) {
                        return (
                            <TagFilter key={index}
                                active={tag.active}
                                color={tag.color} />
                        )
                    })}

                </div>
            </li>
                
            )
    }

}

class TagFilter extends Component {
    constructor(props) {
        super(props);
        this.state = { 'active': this.props.active }
        this.event = new Event('tag-filter')
    }

    updateTag() {

        if (this.state.active) {
            // unset
            removeTagFilter(this.props.color);
        } else {
            // set
            addTagFilter(this.props.color);
        }
        
        window.dispatchEvent(this.event);

    }

    onTagUpdated(event) {
        this.setState({ active: !this.state.active });
        this.updateTag(!this.state.active);
    }

    render() {
        let circle_style = { borderColor: this.props.color, cursor: "pointer"};
        
        if (this.state.active) {
            
            circle_style.backgroundColor = this.props.color;
        }

        let tag_filter =      
            <div style={{cursor: "pointer"}}className="dropdown-item d-flex align-items-center" onClick={(e) => this.onTagUpdated(e)}>
                <div className="dropdown-list-image mr-3">
                    <div className="circle-small" style={circle_style} />
                </div>
                <div className="font-weight-bold">
                    <div className="text-truncate">
                        This filter is currently 
                        {this.state.active ?
                            <strong> avtivate!</strong> :
                            <strong> not activated</strong>}
                    </div>
                </div>
            </div>

        return (
            tag_filter
        );
    }
}
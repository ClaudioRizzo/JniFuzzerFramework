import React, {Component} from "react";
import axios from "axios";
import {API} from "../function_utils";
import PropTypes from 'prop-types';

export class ApkNotes extends Component {
    constructor(props) {
        super(props);

        this.state = {
            notes: props.notes,
            parentId: props.parentId
        };
    }

    addNote(title, text) {
        axios.post(API + '/apks/' + this.state.parentId + '/notes/add', {
            title: title,
            text: text
        }, {withCredentials: true})
            .then((response) => {
                let notes = this.state.notes;
                notes.push(response.data);
                this.setState({notes: notes});
                this.props.onUpdate(notes)
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    drawNewNoteCard() {
        return (
            <div id="new-note-card" className="row">
                <div className="col-lg-12">

                    <div className="card shadow mb-4">
                        <div className="card-header py-3">
                            <h6 className="m-0 font-weight-bold text-primary">New
                                Note</h6>
                        </div>
                        <div className="card-body">
                            <div className="input-group mb-3">
                                <input id="nn-title" type="text"
                                       className="form-control"
                                       placeholder="Title"/>
                            </div>
                            <div className="input-group mb-3">
                                <textarea id="nn-text" className="form-control"
                                          placeholder="Tell your story..."/>
                            </div>
                            <a href='#new-note-card'
                               onClick={() => this.addNote(
                                   document.getElementById("nn-title").value,
                                   document.getElementById("nn-text").value)}
                               className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                                Add Note
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    deleteNote(noteId) {
        axios.post(API + '/notes/' + noteId + '/delete', {}, {withCredentials: true})
            .then((response) => {
                let notes = this.state.notes.filter(function (o) {
                    return o._id !== noteId;
                });
                this.setState({notes: notes});
                this.props.onUpdate(notes)
            })
            .catch(function (error) {
                console.log(error);
            });
        
    }

    drawNoteCard(el, i) {
        return (
            <div className="row" key={i}>
                <div className="col-lg-12">

                    <div className="card shadow mb-4">
                        <div
                            className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                            <h6 className="m-0 font-weight-bold text-primary">{el.title}</h6>
                            <div className="d-flex flex-row">
                                <div className="text-gray-400">
                                    {el.time}&nbsp;&nbsp;&nbsp;&nbsp;
                                </div>
                                <div>
                                    <a href="#" title="Delete"
                                       onClick={() => this.deleteNote(el._id)}><i
                                        className="text-gray-400 far fa-trash-alt"> </i></a>
                                </div>
                            </div>
                        </div>
                        <div className="card-body">
                            {el.text}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    render() {
        if (this.state.notes === undefined) {
            return (<div>Notes!</div>);
        }
        return (
            <span>

            <h1 className="h4 mb-0 text-gray-800">
            Notes
            </h1>
            <br/>
                {this.drawNewNoteCard()}
                <hr/>
                <br/>
                {this.state.notes.map((x, i) => this.drawNoteCard(x, i))}
    </span>
        );
    }
}

ApkNotes.propTypes = {
    onUpdate: PropTypes.func.isRequired,
    notes: PropTypes.array.isRequired,
    parentId: PropTypes.string.isRequired,
};

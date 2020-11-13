import React, {Component} from "react";
import axios from "axios";
import PropTypes from 'prop-types';
import { API } from "../function_utils";



export class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: ''
        };
    }

    updateUsername(evt) {
        this.setState({username: evt.target.value})
    }

    updatePassword(evt) {
        this.setState({password: evt.target.value})
    }

    handleClick(evt) {
        axios.post(API+'/login', {
            username: this.state.username,
            password: this.state.password
        }, {withCredentials: true})
            .then((response) => {
                console.log(response);
                if(response.data.success){
                    window.localStorage.setItem('username', this.state.username);
                    window.location.replace('/');
                } else {
                    //console.log("Invalid login")
                    this.props.onLoginError();
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    render() {
        return (
            <form className="user">
                <div className="form-group">
                    <input type="text"
                           className="form-control form-control-user"
                           id="exampleInputEmail"
                           value={this.state.username}
                           onChange={evt => this.updateUsername(evt)}
                           placeholder="Username"/>
                </div>
                <div className="form-group">
                    <input type="password"
                           className="form-control form-control-user"
                           id="exampleInputPassword"
                           value={this.state.password}
                           onChange={evt => this.updatePassword(evt)}
                           placeholder="Password"
                           onKeyPress={evt => {
                               if (evt.key === 'Enter') {
                                   this.handleClick(evt)
                               }
                           }}/>
                </div>

                <a href="#" onClick={evt => this.handleClick(evt)}
                   className="btn btn-primary btn-user btn-block">
                    Login
                </a>

            </form>);
    }
}

LoginForm.propTypes = {
    onLoginError: PropTypes.func.isRequired,
};

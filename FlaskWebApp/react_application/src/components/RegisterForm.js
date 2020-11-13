import React, {Component} from "react";
import axios from "axios";
import { API } from "../function_utils";

export class RegisterForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            repeatPassword: ''
        };
    }

    updateUsername(evt) {
        this.setState({username: evt.target.value})
    }

    updatePassword(evt) {
        this.setState({password: evt.target.value})
    }

    updateRepeatPassword(evt) {
        this.setState({repeatPassword: evt.target.value})
    }

    handleClick(evt) {
        if (this.state.password === this.state.repeatPassword) {
            axios.post(API + '/register', {
                username: this.state.username,
                password: this.state.password
            }, {withCredentials: true})
                .then((response) => {
                    console.log(response);
                    if (response.data.success === true) {
                        window.location.replace('/');
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        } else {
            console.log("Error: passwords must match!");
        }
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
                <div className="form-group row">
                    <div className="col-sm-6 mb-3 mb-sm-0">
                        <input type="password"
                               className="form-control form-control-user"
                               id="exampleInputPassword"
                               value={this.state.password}
                               onChange={evt => this.updatePassword(evt)}
                               placeholder="Password"/>
                    </div>
                    <div className="col-sm-6">
                        <input type="password"
                               className="form-control form-control-user"
                               id="exampleRepeatPassword"
                               value={this.state.repeatPassword}
                               onChange={evt => this.updateRepeatPassword(evt)}
                               placeholder="Repeat Password"
                               onKeyPress={evt => {
                                   if (evt.key === 'Enter') {
                                       this.handleClick(evt)
                                   }
                               }}/>
                    </div>
                </div>
                <a href="#" onClick={evt => this.handleClick(evt)}
                   className="btn btn-primary btn-user btn-block">
                    Register Account
                </a>

            </form>);
    }
}

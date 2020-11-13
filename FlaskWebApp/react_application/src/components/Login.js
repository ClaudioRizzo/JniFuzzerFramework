import React, {Component} from "react";
import { Link } from "react-router-dom";
import { LoginForm } from "./LoginForm";

document.body.classList.add('bg-gradient-primary');

export class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {'error': false};
        this.onLoginError = this.onLoginError.bind(this);
        this.onErrorDismiss = this.onErrorDismiss.bind(this);
    }

    onLoginError() {
        this.setState({'error': true});
    }

    onErrorDismiss() {
        this.setState({'error': false});
    }

    render() {

        var login_form = (
            <div className="row justify-content-center">

                <div className="col-xl-10 col-lg-12 col-md-9">

                    <div className="card o-hidden border-0 shadow-lg my-5">
                        <div className="card-body p-0">
                            {/* Nested Row within Card Body */}
                            <div className="row">
                                <div
                                    className="col-lg-6 d-none d-lg-block bg-login-image"></div>
                                <div className="col-lg-6">
                                    <div className="p-5">
                                        <div className="text-center">
                                            <h1 className="h4 text-gray-900 mb-4">Welcome
                                            Back!</h1>
                                        </div>
                                        <LoginForm onLoginError={this.onLoginError}/>
                                        <hr />
                                        <div className="text-center">
                                            <Link className="small" to="/register">
                                                Register if you do not have an
                                                account!
                                        </Link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );

        var error_wrapper = (
            <div className="alert alert-danger alert-dismissible fade show" role="alert">
                <p align="center">
                <strong>Holy guacamole!</strong> You should check your login again or <a href="/register">register</a> a new account!
                </p>
                <button type="button" className="close" onClick={this.onErrorDismiss} aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        );

        if (this.state.error){  
            return (<div className="container">{login_form}{error_wrapper}</div>);
        } else {
            return (<div className="container">{login_form}</div>);
        }
        
    }
}

import React from "react";
import {Link} from "react-router-dom";
import {RegisterForm} from "./RegisterForm";

document.body.classList.add('bg-gradient-primary');

export const Register = () => (

    <div className="container">

        <div className="card o-hidden border-0 shadow-lg my-5">
            <div className="card-body p-0">
                {/* Nested Row within Card Body */}
                <div className="row">
                    <div
                        className="col-lg-5 d-none d-lg-block bg-register-image"> </div>
                    <div className="col-lg-7">
                        <div className="p-5">
                            <div className="text-center">
                                <h1 className="h4 text-gray-900 mb-4">Create an
                                    Account!</h1>
                            </div>
                            <RegisterForm/>
                            <hr/>
                            <div className="text-center">
                                <Link className="small" to="/login">
                                    Already have an account? Login!
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
);

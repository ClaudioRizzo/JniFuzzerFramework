import React from "react";
import {Link} from "react-router-dom";

// document.body.classList.remove('bg-gradient-primary');
// document.body.classList.add('bg-gradient-secondary');

export const NotFound = () => (

    <div id="wrapper">

        {/* Content Wrapper */}
        <div id="content-wrapper" className="d-flex flex-column">

            {/* Main Content */}
            <div id="content">

                {/* Begin Page Content */}
                <div className="container-fluid">

                    {/* 404 Error Text */}
                    <div className="text-center">
                        <div className="error mx-auto" data-text="404">404</div>
                        <p className="lead text-gray-800 mb-5">Page Not
                            Found</p>
                        <p className="text-gray-500 mb-0">It looks like you
                            found a glitch in the matrix...</p>
                        <Link to="/">&larr; Back to Dashboard</Link>
                    </div>

                </div>
                {/* /.container-fluid */}

            </div>
            {/* End of Main Content */}


        </div>
        {/* End of Content Wrapper */}

    </div>
);




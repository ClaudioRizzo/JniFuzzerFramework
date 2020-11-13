import React, {Component} from 'react';
// import './App.css';
import {Route, Switch} from "react-router-dom";
import {Login} from "./components/Login";
import {Register} from "./components/Register";
import {SPAFrame} from "./components/SPAFrame";


// import './css/sb-admin-2.min.css';

class App extends Component {
    render() {
        return (
            <Switch>
                <Route path="/login" exact component={Login}/>
                <Route path="/register" exact component={Register}/>
                <Route path="/" component={SPAFrame}/>
            </Switch>
        )
    }
}

export default App;

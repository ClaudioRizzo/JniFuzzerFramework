import React from "react";
import "../css/taint-saviour.css";
import { ApkList } from "./ApkList";
import axios from "axios";
import { filterByTag, API } from '../function_utils'
import { ApksTable } from "./ApkTable";

export class Apks extends React.Component {
    constructor(props) {
        super(props);
        this.state = { apks: [] }
        this.localStorageUpdated = this.localStorageUpdated.bind(this);
    }

    localStorageUpdated() {

        this.setState({ apks: this.state.apks });
    }

    componentWillUnmount() {
        window.removeEventListener('tag-filter', this.localStorageUpdated);
    }

    componentDidMount() {
        window.addEventListener('tag-filter', this.localStorageUpdated)
        axios.get(API + '/apks/summaries', { withCredentials: true })
            .then((response) => {
                console.log(response);
                this.setState({ apks: response.data })

            })
            .catch(function (error) {
                console.log(error);
            })
    }


    render() {
        let apk_list = filterByTag(this.state.apks);
        // apk_list = apk_list.map(apk => {apk._id = apk._id.slice(0, 2); return apk})
        return <ApksTable entries={apk_list}></ApksTable>
    }
}


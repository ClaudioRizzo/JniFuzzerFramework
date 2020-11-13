import React from "react";
import axios from "axios";
import "../css/search-bar.css";
import { API } from "../function_utils";


export class SearchBar extends React.Component {

    constructor(props) {
        super(props);
        this.state = {query: '', ids: [], selected: '', focus: -1};
        this.inputChange = this.inputChange.bind(this);
        this.onSelectedApk = this.onSelectedApk.bind(this);
        this.onFocusChange = this.onFocusChange.bind(this);
        this.onMouseOverList = this.onMouseOverList.bind(this);
    }

    getApkIds() {
        axios.get(API + '/apks/search/' + this.state.query,
            { withCredentials: true })
            .then((response) => {
                var sel = ""
                if (response.data.length > 0) {
                    sel = response.data[0];
                }
                this.setState({ ids: response.data, selected: sel, query: '' });
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    inputChange(event) {
        // we do the search
        this.setState({
            query: this.search.value
          }, () => {
              if(this.state.query && this.state.query.length > 2){
                //if (this.state.query.length % 2 === 0) {
                    this.getApkIds();
                //}
              } else {
                // we do not show results, so we reset everything
                this.setState({query: '', ids: [], selected: '', focus: -1});
              }
          });
       
    }

    onSelectedApk(apk_id) {
        // Basically called when the user clicks on the apk he/she wants to go to
        /*
        var tmp = this.state;
        tmp.selected = apk_id;

        tmp.focus = -1;
        this.search.value = apk_id

        this.setState(tmp);
        */
       this.submitSearch(apk_id);
    }

    submitSearch(apk_id) {
        console.log("submitting: "+apk_id);
        var path = "/apks/"+apk_id+"/summary";
        window.location.assign(path); 
    }

    onFocusChange(evnt){
        // this is called when a user goes up and down in the
        // results

        if(this.state.ids.length <= 0) {
            // there is no result to browse
            return;
        }
        var tmp = this.state;;
        if (evnt.keyCode === 40) {
            // down
            if(this.state.focus > this.state.ids.length-1){
                return;
            }

            
            tmp.focus += 1;
            tmp.selected = this.state.ids[this.state.focus];
            this.setState(tmp);
        } else if (evnt.keyCode === 38) {
            // up
            if(this.state.focus < 0) {
                return;
            }
            
            tmp.focus -= 1;
            tmp.selected = this.state.ids[this.state.focus];
            this.setState(tmp);
        } else if (evnt.keyCode === 13) {
            // enter
            evnt.preventDefault();
            if(this.state.focus > -1 && this.state.focus < this.state.ids.length-1) {
                this.submitSearch(this.state.ids[this.state.focus]);
            }
        }
    }

    onMouseOverList(index, selected_apk) {
        var tmp = this.state;
        tmp.focus = index;
        tmp.selected = selected_apk;
        this.setState(tmp);
    }

    render() {
        console.log("selected: "+this.state.selected)
        var search_bar =
        
            <div
                className="navbar-form d-sm-inline-block navbar-search"
                onSubmit={evt => {evt.preventDefault()}}
                autoComplete="off">
                
                    <input type="text"
                        id="search-bar-input"
                        onChange={this.inputChange}
                        onKeyDown={this.onFocusChange}
                        className="form-control bg-light border-0"
                        placeholder="Search for..."
                        aria-label="Search"
                        aria-describedby="basic-addon2"
                        ref={input => this.search = input}>
                    </input>
                    
                
                <Suggestions hide={this.state.selected === ""} focus={this.state.focus} results={this.state.ids} onSelectedApk={this.onSelectedApk} onMouseOverList={this.onMouseOverList}/>
                
                <div/>
            </div>

        return search_bar;
    }
}

class Suggestions extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            results: this.props.results,
            focus: props.focus,
            hide: props.hide,
        };
    }

    createSuggestions(){
        // TODO: (clod) we may add badges to the list to show how many flows that apks has
        var suggestions = this.state.results.map((res, index) => {
            return (
                index === this.state.focus ? 
                    <li className="list-group-item active" key={index} onClick={() => { this.props.onSelectedApk(res);}}>
                        <strong>{res.substring(0, 1)}</strong>
                        {res.substring(1, res.length-30)}...
                        <input type="hidden" value={res} />
                    </li> :
                    
                    <li onMouseOver={(evnt) => this.props.onMouseOverList(index, res)} className="list-group-item" key={index} onClick={() => { this.props.onSelectedApk(res);}}>
                        <strong>{res.substring(0, 1)}</strong>
                        {res.substring(1, res.length-30)}...
                        <input type="hidden" value={res} />
                    </li>
            )
        });

        var suggestions_div =
            <ul id="searchResults" className="list-group list-group-flush">
                {suggestions}
            </ul>
        
        
        return this.state.hide ? <div/> : suggestions_div;
    }


    componentWillReceiveProps(nextProps){
        if (!this._array_equals(nextProps.results, this.props.results) ||
            nextProps.focus !== this.props.focus) {

            this.setState({ results: nextProps.results, focus: nextProps.focus, hide: nextProps.hide});
        }
    }

    _array_equals(_arr1, _arr2){
        if (!Array.isArray(_arr1) || ! Array.isArray(_arr2) || _arr1.length !== _arr2.length)
            return false;
        var arr1 = _arr1.concat().sort();
        var arr2 = _arr2.concat().sort();

        for (var i = 0; i < arr1.length; i++) {

            if (arr1[i] !== arr2[i])
                return false;

        }

        return true;
    }

    render() {
        return this.createSuggestions();
    }
}
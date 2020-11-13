import React, {Component} from "react";
import axios from "axios";
import "../datatables/dataTables.bootstrap4.min.css";
import {Link} from "react-router-dom";


export class ApkList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            apk_list: this.props.apk_list.slice(0, 1),
            
        };
    }
    
    recursive = () => {
        
        setTimeout(() => {
          let hasMore = this.state.apk_list.length + 1 < this.props.apk_list.length;
          this.setState( (prev, props) => ({
            apk_list: props.apk_list.slice(0, prev.apk_list.length + 50)
          }));
          if (hasMore) this.recursive();
        }, 0);
      }

    componentDidMount() {
        // this.recursive();    
    }

    createRow(el) {
        return (
            <tr key={el._id}>
                <td className="texttt">
                    <Link to={`/apks/${el._id}`}>{el._id}</Link></td>
                <td>{el.n_flows}</td>
                <td>{el.n_libs}</td>
                <td>{el.n_notes}</td>
            </tr>
        );
    }

    componentWillReceiveProps(nextProps){
        // this.setState({apk_list: nextProps.apk_list})
        this.recursive();
    }

    render() {
        return (

            <div>
                <div className="card-header py-3">
                    <h6 className="m-0 font-weight-bold text-primary">
                        APKs With One or More Flows
                    </h6>
                </div>
                <div className="card-body">
                    <div className="table-responsive">
                        <table className="table table-bordered" id="dataTable"
                               width="100%" cellSpacing="0">
                            <thead>
                            <tr>
                                <th>SHA256</th>
                                <th>Flows</th>
                                <th>Libraries</th>
                                <th>Notes</th>
                            </tr>
                            </thead>
                            <tfoot>
                            <tr>
                                <th>SHA256</th>
                                <th>Flows</th>
                                <th>Libraries</th>
                                <th>Notes</th>
                            </tr>
                            </tfoot>
                            <tbody>
                            {this.state.apk_list.map(
                                x => this.createRow(x))
                            }
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        );
    }
}

import React, {Component} from "react";
import Graph from "vis-react";

export class FlowViz extends Component {
    constructor(props) {
        super(props);
        this.state = {
            flow: props.flow
        };
    }

    drawFlow() {
        let sink = this.state.flow['sink'];
        let sources = [this.state.flow['source']];

        //  Nodes
        let nodes = [];
        for (let i = 0; i < sources.length; i++) {
            nodes.push({id: i, label: sources[i]});
        }
        nodes.push({id: sources.length, label: sink});

        //  Edges
        let edges = [];
        for (let i = 0; i < sources.length; i++) {
            edges.push({from: i, to: sources.length, arrows: 'to'})
        }

        // provide the data in the vis format
        let graph = {
            nodes: nodes,
            edges: edges
        };
        let options = {
            interaction: {
                zoomView: false
            },
            layout: {
                hierarchical: true
            }
        };
        return [graph, options];
    }

    drawFlowFromPath() {

    }

    render() {
        let [graph, options] = this.drawFlow();
        return (
            <div style={{height: "600px"}}>
                <Graph graph={graph} options={options}/>
            </div>
        );
    }

}

<template>
  <v-network-graph :zoom-level="0.5" :nodes="nodes" :edges="edges" :configs="configs" id="graph" />
</template>

<script>
import * as vNG from "v-network-graph"
import {
  ForceLayout
} from "v-network-graph/lib/force-layout"

import axios from 'axios'
export default {
  data() {
    return {
      nodes: {
        1: { name: "Node 1" },
        2: { name: "Node 2" },
        3: { name: "Node 3" },
        4: { name: "Node 4" },
      }
      ,
      edges: {
        1: { source: "1", target: "2" },
        2: { source: "2", target: "3" },
        3: { source: "3", target: "4" },
      },
      configs: vNG.defineConfigs({
        view: {
          scalingObjects: true,
          layoutHandler: new ForceLayout({
            positionFixedByDrag: false,
            positionFixedByClickWithAltKey: true,
            createSimulation: (d3, nodes, edges) => {
              // d3-force parameters
              const forceLink = d3.forceLink(edges).id(d => d.id)
              return d3
                .forceSimulation(nodes)
                .force("edge", forceLink.distance(40).strength(0.5))
                .force("charge", d3.forceManyBody().strength(-800))
                .force("center", d3.forceCenter().strength(0.05))
                .alphaMin(0.001)

              // * The following are the default parameters for the simulation.
              // const forceLink = d3.forceLink<ForceNodeDatum, ForceEdgeDatum>(edges).id(d => d.id)
              // return d3
              //   .forceSimulation(nodes)
              //   .force("edge", forceLink.distance(100))
              //   .force("charge", d3.forceManyBody())
              //   .force("collide", d3.forceCollide(50).strength(0.5))
              //   .force("center", d3.forceCenter().strength(0.05))
              //   .alphaMin(0.001)
            }
          })
        },
        node: {
          // radius: node => node.size,
          normal: {
            type: "circle",
            radius: node => node.size, // Use the value of each node object
            color: node => node.color,
          },

        }
      })
    }
  },
  mounted() {
    axios
      .get('/graph')
      .then(response => { this.nodes = response.data.nodes; this.edges = response.data.edges });
  }
}


// export default {
//   data() {
//     return {
//       nodeCount: 10,
//       nodes: {},
//       edges: {},
//     }
//   },
//   
// }

</script>
<style>
#graph {
  width: 800px;
  height: 600px;
  border: 1px solid #000;
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

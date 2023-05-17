<template>
  <div class="tooltip-wrapper">
    <v-network-graph :zoom-level="0.5" :nodes="nodes" :edges="edges" :configs="configs" :layouts="layouts"
      :event-handlers="eventHandlers" id="graph" ref="graph" />
    <!-- Tooltip -->
    <div ref="tooltip" class="tooltip" :style="{ top: tooltipPos.y, left: tooltipPos.x, opacity: tooltipOpacity }">
      <VacCard :raw_text="nodes[targetNodeId]" :desc="nodes[targetNodeId].small_text" />
      <!-- <div>{{ nodes[targetNodeId] }}</div> -->
      <!-- </VacCard> -->
    </div>
  </div>
</template>

<script>
import * as vNG from "v-network-graph"
import {
  ForceLayout
} from "v-network-graph/lib/force-layout"

import axios from 'axios'
import VacCard from './../components/vacancies_card.vue'
import { watch } from "vue"

export default {
  data() {
    return {
      nodes: {
        0: { name: "user", small_text: "" },
      }
      ,
      edges: {
      },
      configs: vNG.defineConfigs({
        view: {
          scalingObjects: true,
          minZoomLevel: 1,
          layoutHandler: new ForceLayout({
            positionFixedByDrag: false,
            positionFixedByClickWithAltKey: true,
            createSimulation: (d3, nodes, edges) => {
              // d3-force parameters
              const forceLink = d3.forceLink(edges).id(d => d.id)
              return d3
                .forceSimulation(nodes)
                .force("edge", forceLink.distance(20).strength(0.5))
                .force("charge", d3.forceManyBody().strength(-800))
                .force("center", d3.forceCenter().strength(0.05))
                .alphaMin(0.001)
            }
          })
        },
        node: {
          normal: {
            type: "circle",
            radius: node => node.size, // Use the value of each node object
            color: node => node.color,
          },

        },
        edge: {
          normal: {
            width: 0,
          },
          hover: {
            width: 0,
          }
        },
      }),
      eventHandlers: {
        "node:pointerover": ({ node }) => {
          if (this.nodes[node.toString()].small_text == "") {
            console.log("Hello")
            axios({
              method: 'post',
              responseType: 'json',
              url: '/summorize',
              data: {
                text: this.nodes[node.toString()].text,
              },
            })
              // axios
              //   .post('/summorize', {
              //     text: this.nodes[node.toString()].text,
              //   })
              .then(response => { this.nodes[node.toString()].small_text = response.data.text });
          };
          this.targetNodeId = node
          this.tooltipOpacity = 1 // show
          this.tooltipPos.x = this.layouts.nodes[this.targetNodeId.toString()].x
          this.tooltipPos.y = this.layouts.nodes[this.targetNodeId.toString()].y

          const domPoint = this.$refs.graph.translateFromSvgToDomCoordinates(this.tooltipPos)
          this.tooltipPos.x = (domPoint.x + 50).toString() + "px"
          this.tooltipPos.y = (domPoint.y - 200).toString() + "px"
          console.log(this.tooltipPos)
        },
        "node:pointerout": _ => {
          this.tooltipOpacity = 0 // hide
        },
      },
      layouts: {},
      tooltipPos: { x: "0px", y: "0px" },
      tooltipOpacity: 0,
      targetNodeId: 0,
    }
  },
  mounted() {
    axios
      .get('/graph')
      .then(response => { this.nodes = response.data.nodes; this.edges = response.data.edges; this.layouts = response.data.layouts });
  },
  components: {
    VacCard,
  },
}

</script>
<style>
#graph {
  width: 1000px;
  height: 800px;
  border: 1px solid #000;
}

.tooltip-wrapper {
  position: relative;
}

.tooltip {
  top: 0;
  left: 0;
  opacity: 0;
  position: absolute;
  min-width: 80px;
  min-height: 36px;
  padding: 10px;
  text-align: center;
  font-size: 12px;
  background-color: #9c07ff;
  border: 2px solid #ffb950;
  box-shadow: 2px 2px 2px #aaa;
  transition: opacity 0.2s linear;
  pointer-events: none;
}
</style>

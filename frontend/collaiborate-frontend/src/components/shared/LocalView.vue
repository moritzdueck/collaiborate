<template>

  <div class="description"><span>Changes between <img src="/pin_red.svg" alt="pin"
                                                      style="width: 20px; display: inline-block; vertical-align: middle"/> <span
      style="color: var(--red)">{{ layers[lastLayer] }}</span> and {{ layers[currentLayer] }}</span></div>

  <div class="menu" id="local-view-menu">

    <div class="local-view-layer-option"><span class="layer-pin"/> <span>Choose representation</span></div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(0)"
                                               :class="(lastLayer === 0)? 'active-pin' : ''"><img
        id="local-view-layer-pin" src="/pin_red.svg" alt="pin"/></span>
      <Button :outlined="currentLayer!==0" severity="secondary" @click="updateLayer(0)">Input</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(1)"
                                               :class="(lastLayer === 1)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==1" severity="secondary" @click="updateLayer(1)">(0): Conv2d</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(2)"
                                               :class="(lastLayer === 2)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==2" severity="secondary" @click="updateLayer(2)">(1): ReLU</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(3)"
                                               :class="(lastLayer === 3)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==3" severity="secondary" @click="updateLayer(3)">(2): MaxPool2d</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(4)"
                                               :class="(lastLayer === 4)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==4" severity="secondary" @click="updateLayer(4)">(3): Conv2d</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(5)"
                                               :class="(lastLayer === 5)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==5" severity="secondary" @click="updateLayer(5)">(4): ReLU</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(6)"
                                               :class="(lastLayer === 6)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==6" severity="secondary" @click="updateLayer(6)">(5): MaxPool2d</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(7)"
                                               :class="(lastLayer === 7)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==7" severity="secondary" @click="updateLayer(7)">(6): Conv2d</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(8)"
                                               :class="(lastLayer === 8)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==8" severity="secondary" @click="updateLayer(8)">(7): ReLU</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(9)"
                                               :class="(lastLayer === 9)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                  alt="pin"/></span>
      <Button :outlined="currentLayer!==9" severity="secondary" @click="updateLayer(9)">(8): MaxPool2d</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(10)"
                                               :class="(lastLayer === 10)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                   alt="pin"/></span>
      <Button :outlined="currentLayer!==10" severity="secondary" @click="updateLayer(10)">(9): Flatten</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(11)"
                                               :class="(lastLayer === 11)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                   alt="pin"/></span>
      <Button :outlined="currentLayer!==11" severity="secondary" @click="updateLayer(11)">(10): Linear</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(12)"
                                               :class="(lastLayer === 12)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                   alt="pin"/></span>
      <Button :outlined="currentLayer!==12" severity="secondary" @click="updateLayer(12)">(11): ReLU</Button>
    </div>
    <div class="local-view-layer-option"><span class="layer-pin" @click="updateLastLayer(13)"
                                               :class="(lastLayer === 13)? 'active-pin' : ''"><img src="/pin_red.svg"
                                                                                                   alt="pin"/></span>
      <Button :outlined="currentLayer!==13" severity="secondary" @click="updateLayer(13)">(12): Linear</Button>
    </div>

    <div class="menu-legend">
      <img src="/pin_red.svg" alt="pin" style="width: 30px"/>
      <span>initial layer</span>
    </div>

  </div>


  <div class="bottom-menu">
    <Button outlined severity="secondary" @click="emit('updateIndex', undefined)" id="leave-local-view-button">Leave
      View
    </Button>
  </div>


  <div ref="resizeRef" class="container">
    <svg ref="svgRef"/>
  </div>

</template>

<script setup>
import Button from 'primevue/button';
import {onMounted, ref, shallowRef, watch} from "vue";
import * as d3 from "d3";
import useResizeObserver from "../../use/resizeObserver.js";
import {getNeighborhoodForSample} from "../../utils/utils.ts";
import introJs from "intro.js";
import {localViewIntroJsConfig} from "../demo/introJsConfig";

const {resizeRef, resizeState} = useResizeObserver();
const svgRef = ref(null);
const neighborsRef = shallowRef()
const neighborsRefBefore = shallowRef()
const neighborsData = shallowRef([])
const labels = shallowRef([])
const lastLayer = ref(0)
const counts = ref(undefined)
const currentLayer = ref(13)
const brushFilter = ref(() => true)
const firstUpdate = ref(true)

const props = defineProps(['index', 'allImages', 'lines'])
const emit = defineEmits(['updateIndex'])

const classes = ['airplane', 'apple', 'bee', 'car', 'dragon', 'mosquito', 'moustache', 'mouth', 'pear', 'piano', 'pineapple', 'smiley face', 'train', 'umbrella', 'wine bottle']

const layers = [
  "Input",
  "(0): Conv2d",
  "(1): ReLU",
  "(2): MaxPool2d",
  "(3): Conv2d",
  "(4): ReLU",
  "(5): MaxPool2d",
  "(6): Conv2d",
  "(7): ReLU",
  "(8): MaxPool2d",
  "(9): Flatten",
  "(10): Linear",
  "(11): ReLU",
  "(12): Linear"
]


const apiUrl = import.meta.env.VITE_APIURL

function updateLayer(layer) {
  currentLayer.value = layer
  neighborsRef.value = neighborsData.value[currentLayer.value];
  // neighborsRefBefore.value = neighborsData.value[lastLayer.value];
}

function updateLastLayer(layer) {
  lastLayer.value = layer
  // neighborsRef.value = neighborsData.value[currentLayer.value];
  neighborsRefBefore.value = neighborsData.value[lastLayer.value];
}

let angleLookup = {}
let radiiBefore = {}


function setupCircleView() {
  const margin = {top: 10, right: 10, bottom: 10, left: 10}
  let neighbors = []
  let neighborsBefore = []

  const {width, height} = resizeState.dimensions;
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  const svgContainer = d3.select(svgRef.value)
      .attr("viewBox", [0, 0, width, height])
      .property("value", [])
      .attr("width", width)
      .attr("height", height)

  svgContainer.selectAll("g").remove()

  const background = svgContainer
      .append("g")
      .style("width", innerWidth)
      .style("height", innerHeight)
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  const svg = svgContainer
      .append("g")
      .style("width", innerWidth)
      .style("height", innerHeight)
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  const r = Math.min(innerWidth, innerHeight) * 0.25

  svg.selectAll('circle')
      .data([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
      .enter()
      .append('circle')
      .attr('cx', width / 2)
      .attr('cy', height / 2)
      .attr("r", d => d)
      // .attr("fill", d => circleColors(d))
      .attr("fill", "none")
      .attr("stroke", "#eee")

  svg.selectAll("#center")
      .data([apiUrl + "sketch/pngcolor/" + props.index])
      .enter()
      .append('image')
      .attr('xlink:href', (d) => d)
      .attr('width', 30)
      .attr('height', 30)
      .attr('x', width / 2 - 15)
      .attr('y', height / 2 - 15)

  const update = () => {
    if (!props.allImages)
      return

    neighbors = Object.fromEntries(Object.entries(neighborsRef.value).sort((a, b) => a[1] - b[1]).slice(0, 1000))
    neighborsBefore = Object.fromEntries(Object.entries(neighborsRefBefore.value).sort((a, b) => a[1] - b[1]).slice(0, 1000))

    // __________ LABELS _____________
    const countsTmp = [
      {label: 'airplane', count: 0, index: 0},
      {label: 'apple', count: 0, index: 1},
      {label: 'bee', count: 0, index: 2},
      {label: 'car', count: 0, index: 3},
      {label: 'dragon', count: 0, index: 4},
      {label: 'mosquito', count: 0, index: 5},
      {label: 'moustache', count: 0, index: 6},
      {label: 'mouth', count: 0, index: 7},
      {label: 'pear', count: 0, index: 8},
      {label: 'piano', count: 0, index: 9},
      {label: 'pineapple', count: 0, index: 10},
      {label: 'smiley face', count: 0, index: 11},
      {label: 'train', count: 0, index: 12},
      {label: 'umbrella', count: 0, index: 13},
      {label: 'wine bottle', count: 0, index: 14},
    ]
    Object.keys(neighbors).map(idx => labels.value[idx]).forEach(i => countsTmp[i].count++)
    counts.value = countsTmp

    const cumSum = [0]
    let i = 1
    for (const count of counts.value.map(i => i.count)) {
      cumSum[i] = cumSum[i - 1] + count
      i++
    }

    for (const n of Object.entries(neighbors)) {
      angleLookup[n[0]] = ((Math.random() * counts.value[labels.value[n[0]]] + cumSum[labels.value[n[0]]]) / cumSum[cumSum.length - 1]) * 2 * Math.PI - (Math.PI / 2)
    }

    // Calculate angles
    const pie = countsTmp.map(item => {
      return {
        ...item,
        startAngle: cumSum[item.index] / cumSum[cumSum.length - 1] * 2 * Math.PI,
        endAngle: cumSum[(item.index + 1)] / cumSum[cumSum.length - 1] * 2 * Math.PI,
      }
    })

    for (const n of Object.entries(neighbors)) {
      const arc = pie.find(arc => arc.index === labels.value[n[0]])
      if (arc.endAngle - arc.startAngle < (Math.PI / 180 * 8)) {
        // if we have less than 8 degrees, we do not leave space
        angleLookup[n[0]] = Math.random() * (arc.endAngle - arc.startAngle) + arc.startAngle - (Math.PI / 2)
      } else {
        angleLookup[n[0]] = Math.random() * ((arc.endAngle - arc.startAngle) - 6 * (Math.PI / 180)) + arc.startAngle + 3 * (Math.PI / 180) - (Math.PI / 2)
      }
    }

    for (const n of Object.entries(neighborsBefore)) {
      const arc = pie.find(arc => arc.index === labels.value[n[0]])
      if (arc.endAngle - arc.startAngle < (Math.PI / 180 * 5)) {
        // if we have less than 8 degrees, we do not leave space
        angleLookup[n[0]] = Math.random() * (arc.endAngle - arc.startAngle) + arc.startAngle - (Math.PI / 2)
      } else {
        angleLookup[n[0]] = Math.random() * ((arc.endAngle - arc.startAngle) - 6 * (Math.PI / 180)) + arc.startAngle + 3 * (Math.PI / 180) - (Math.PI / 2)
      }
    }

    // __________ Pie chart class distribution _____________

    const colorSector = props.lines.items.find(item => item.idx === props.index).y;

    background.selectAll('.pie').remove()
    background.selectAll('whatever')
        .data(pie)
        .enter()
        .append('path')
        .attr("class", "pie")
        .attr('d', d3.arc()
            .innerRadius(30)
            .outerRadius(r * 1.5)
        )
        .attr('fill', (d, i) => (colorSector !== undefined && i === colorSector) ? '#dcdcdc' : 'none')
        .attr("stroke", "#ccc")
        .attr("transform", "translate(" + (width / 2) + "," + (height / 2) + ")")
        .style("stroke-width", "2px")
        .style("opacity", 0.3)


    // __________ LINES TO SHOW MOVEMENT _____________

    const scaleR = d3.scaleLinear([Math.min(...Object.values(neighbors)), Math.max(...Object.values(neighbors))], [0.5, 1.5]).clamp(false)
    const scaleOld = d3.scaleLinear([Math.min(...Object.values(neighborsBefore)), Math.max(...Object.values(neighborsBefore))], [0.5, 1.5]).clamp(false)


    const enterLines = []
    const updateLines = []
    const exitLines = []

    for (const x of Object.entries(neighbors)) {
      if (Object.keys(neighborsBefore).includes(x[0])) {
        updateLines.push(x[0])
      } else {
        enterLines.push(x[0])
      }
    }
    for (const x of Object.entries(neighborsBefore)) {
      if (!Object.keys(neighbors).includes(x[0])) {
        exitLines.push(x[0])
      }
    }


    background.selectAll('line')
        .remove()

    const all = new Set([...enterLines, ...updateLines, ...exitLines])

    background.selectAll("line.move")
        .data(all, d => d)
        .enter()
        .append('line')
        .style("stroke-width", 5)
        .attr("x1", d => scaleOld(neighborsRefBefore.value[d]) * r * Math.cos(angleLookup[d]) + width / 2)
        .attr("y1", d => scaleOld(neighborsRefBefore.value[d]) * r * Math.sin(angleLookup[d]) + height / 2)
        .attr("x2", d => scaleR(neighborsRef.value[d]) * r * Math.cos(angleLookup[d]) + width / 2)
        .attr("y2", d => scaleR(neighborsRef.value[d]) * r * Math.sin(angleLookup[d]) + height / 2)
        .style("stroke", d => scaleOld(neighborsRefBefore.value[d]) > scaleR(neighborsRef.value[d]) ? "var(--blue)" : "var(--orange)")
        .style("opacity", 0.2)
        .attr("class", "move")

    // __________ SKETCHES _____________

    const radii = {}
    svg.selectAll('image.n')
        .data(Object.entries(neighbors).sort((a, b) => a[1] - b[1]).slice(0, 1000), item => item[0])
        .join(
            enter => enter
                .append('image')
                .attr('xlink:href', (d) => 'data:image/png;base64, ' + props.allImages[d[0]])
                .attr('x', (d) => ((scaleOld(neighborsRefBefore.value[d[0]]) * r) * Math.cos(angleLookup[d[0]])) + width / 2 - 10)
                .attr('y', (d) => ((scaleOld(neighborsRefBefore.value[d[0]]) * r) * Math.sin(angleLookup[d[0]])) + height / 2 - 10)
                .attr('width', 20)
                .attr('height', 20)
                .attr('opacity', 0)
                .each(d => radii[d[0]] = (scaleR(d[1]) * r))
                .attr('class', 'n closer')
                // .transition()
                // .ease(d3.easeLinear)
                // .duration(3000)
                .attr('x', (d) => (scaleR(d[1]) * r * Math.cos(angleLookup[d[0]])) + width / 2 - 10)
                .attr('y', (d) => (scaleR(d[1]) * r * Math.sin(angleLookup[d[0]])) + height / 2 - 10)
                .attr('opacity', (d) => brushFilter.value(d[0]) ? 1 : 0.1)
                .selection(),
            update => update
                .attr('x', (d) => (radiiBefore[d[0]] * Math.cos(angleLookup[d[0]])) + width / 2 - 10)
                .attr('y', (d) => (radiiBefore[d[0]] * Math.sin(angleLookup[d[0]])) + height / 2 - 10)
                // .transition()
                // .ease(d3.easeLinear)
                // .duration(3000)
                .attr('x', (d) => (scaleR(d[1]) * r * Math.cos(angleLookup[d[0]])) + width / 2 - 10)
                .attr('y', (d) => (scaleR(d[1]) * r * Math.sin(angleLookup[d[0]])) + height / 2 - 10)
                .each(d => radii[d[0]] = (scaleR(d[1]) * r))
                .attr('class', d => scaleOld(neighborsBefore[d]) > scaleR(neighbors[d]) ? "closer n" : "away n")
                .selection(),
            exit => exit
                .attr('x', (d) => (radiiBefore[d[0]] * Math.cos(angleLookup[d[0]])) + width / 2 - 10)
                .attr('y', (d) => (radiiBefore[d[0]] * Math.sin(angleLookup[d[0]])) + height / 2 - 10)
                // .transition()
                // .ease(d3.easeLinear)
                // .duration(3000)
                .attr('x', (d) => (scaleR(neighborsRef.value[d[0]]) * r * Math.cos(angleLookup[d[0]])) + width / 2 - 10)
                .attr('y', (d) => (scaleR(neighborsRef.value[d[0]]) * r * Math.sin(angleLookup[d[0]])) + height / 2 - 10)
                .attr('opacity', 0)
                .remove()
        );
    radiiBefore = radii;

    // __________ histogram _____________

    const rescalingFactors = [...all].map(x => ({
      icon: x,
      factor: scaleOld(neighborsRefBefore.value[x]) - scaleR(neighborsRef.value[x])
    }))

    rescalingFactors.sort((x, y) => x.factor - y.factor)

    const scaleX = d3.scaleLinear([0, rescalingFactors.length], [150, width - 150]).clamp(false)
    background.selectAll("line.other")
        .data(rescalingFactors, d => d.icon)
        .enter()
        .append('line')
        .style("stroke-width", 1)
        .attr("x1", (d, i) => scaleX(i))
        .attr("y1", d => (innerHeight - 60) + d.factor * 30)
        .attr("x2", (d, i) => scaleX(i))
        .attr("y2", () => (innerHeight - 60))
        .style("stroke", d => d.factor > 0 ? "var(--blue)" : "var(--orange)")
        .style("opacity", 0.5)
        .attr("class", "other")

    const brush = d3.brushX()
        .extent([[150, innerHeight - 90], [width - 150, innerHeight - 30]])
        .on("brush", brushed)
        .on("end", brushended);

    svg.selectAll("g.brush").remove()

    const defaultSelection = [150, width - 150]
    const gb = svg.append("g")
        .attr("class", "brush")
        .attr("id", 'local-view-subset-brush')
        .call(brush)
        .call(brush.move, defaultSelection);

    function brushed({selection}) {

    }

    function brushended({selection}) {
      if (selection) {
        const selected = rescalingFactors.filter((d, i) => (scaleX(i) > selection[0]) && (scaleX(i) < selection[1])).map(i => i.icon)

        function f(sketch) {
          return selected.includes(sketch)
        }

        background.selectAll("line.move").style("stroke", d => {
          if (!f(d)) {
            return "var(--gray)"
          }
          return scaleOld(neighborsRefBefore.value[d]) > scaleR(neighborsRef.value[d]) ? "var(--blue)" : "var(--orange)"
        })

        svg.selectAll('image.n').attr('opacity', (d) => f(d[0]) ? 1 : 0.1)

      }
      if (!selection) {
        gb.call(brush.move, defaultSelection);
      }
    }

  }

  update();
  watch(neighborsRef, update)
  watch(neighborsRefBefore, update)
}

function setupDiffView() {
  const margin = {top: 10, right: 10, bottom: 10, left: 10}
  const {width, height} = resizeState2.dimensions;
  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  const svgContainer = d3.select(svgRef2.value)
      .attr("viewBox", [0, 0, width, height])
      .property("value", [])
      .attr("width", width)
      .attr("height", height)

  svgContainer.selectAll("g").remove()

  const svg = svgContainer
      .append("g")
      .style("width", innerWidth)
      .style("height", innerHeight)
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.append("line")
      .attr("x1", width / 2 + 10)
      .attr("y1", 100)
      .attr("x2", width / 2 + 10)
      .attr("y2", height - 100)
      .style("stroke", "#444")

  const update = () => {
    let neighbors = Object.fromEntries(Object.entries(neighborsRef.value).sort((a, b) => a[1] - b[1]).slice(0, 1000))
    let neighborsBefore = Object.fromEntries(Object.entries(neighborsRefBefore.value).sort((a, b) => a[1] - b[1]).slice(0, 1000))

    const scale = d3.scaleLinear([Math.min(...Object.values(neighbors)), Math.max(...Object.values(neighbors))], [0, 1]).clamp(false)
    const scaleBefore = d3.scaleLinear([Math.min(...Object.values(neighborsBefore)), Math.max(...Object.values(neighborsBefore))], [0, 1]).clamp(false)

    neighbors = Object.fromEntries(Object.entries(neighborsRef.value).filter(x => x[0] % 10 > 7))
    neighborsBefore = Object.fromEntries(Object.entries(neighborsRefBefore.value).filter(x => x[0] % 10 > 7))


    const overlapNew = []
    const overlapOld = []
    const diff = []

    for (const x of Object.entries(neighbors).sort((a, b) => a[1] - b[1])) {
      if (Object.keys(neighborsBefore).includes(x[0])) {
        overlapNew.push(x[0])
      }
    }

    let i = 0
    for (const x of Object.entries(neighborsBefore).sort((a, b) => a[1] - b[1])) {
      if (Object.keys(neighbors).includes(x[0])) {
        overlapOld.push(x[0])
        let j = overlapNew.indexOf(x[0])
        diff.push([x[0], scaleBefore(neighborsBefore[x[0]]) - scale(neighbors[x[0]])])
        i++
      }
    }

    const yScale = d3.scaleLinear([0, overlapNew.length], [105, height - 105])
    const max = Math.max(...Object.values(diff).map(x => Math.abs(x[1])))
    const xScale = d3.scaleLinear([-max, max], [width * 0.1, width * 0.9])

    svg.selectAll('image').remove()

    diff.sort((a, b) => neighbors[a[0]] - neighbors[b[0]])

    svg.selectAll('image')
        .data(diff, item => item[0])
        .enter()
        .append('image')
        .attr('xlink:href', (d) => apiUrl + "sketch/pngcolor/" + d[0])
        .attr('x', (d) => xScale(d[1]))
        .attr('y', (d, i) => yScale(i) - 10)
        .attr('width', 20)
        .attr('height', 20)
  }

  update()
  watch(neighborsRef, update)
  watch(neighborsRefBefore, update)
}

onMounted(() => {

  const render = () => {
    getNeighborhoodForSample(props.index)
        .then(result => result.json())
        .then(json => {
          labels.value = json.labels
          neighborsData.value = json.layers;
          neighborsRef.value = json.layers[13]
          neighborsRefBefore.value = json.layers[0]

          setupCircleView();
          // watch(resizeRef2, setupCircleView)
          // setupDiffView();
          // watch(resizeRef2, setupDiffView)
          if (firstUpdate.value) {
            setTimeout(() => {
              introJs().setOptions(localViewIntroJsConfig).start();
            }, 500)
            firstUpdate.value = false
          }
        })
  }

  watch(() => props.index, render)
  watch(() => props.allImages, render)

  if (props.index) {
    render()
  }

})
</script>

<style>
rect.selection {
  fill: var(--blue-transparent);
}
</style>

<style scoped>
.container {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.container > svg {
  width: 100%;
  height: 100%;
}

.menu {
  position: absolute;
  display: flex;
  flex-direction: column;
}

.bottom-menu {
  position: absolute;
  display: flex;
  flex-direction: column;
  bottom: 20px;
}

.diff-container {
  position: absolute;
  left: 70%;
  width: 30%;
  height: 100%;
  top: 0;
  background: linear-gradient(90deg, rgba(255, 0, 0, 0.2), rgba(0, 255, 0, 0.2));
}

.diff-container > .description {
  position: absolute;
  margin-top: 20px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.label-counts {
  position: absolute;
  bottom: 70px;
  left: 10px;
}

.label-counts > span {
  display: flex;
}

.layer-pin {
  width: 30px;
  height: 30px;
  display: inline-block;
  border-radius: 30px;
  cursor: pointer;
}

.layer-pin > img {
  width: 30px;
  opacity: 0;
}

.layer-pin:hover > img {
  opacity: 1;
}

.layer-pin.active-pin > img {
  opacity: 1;
}


.local-view-layer-option {
  display: flex;
  align-items: center;
}

.local-view-layer-option > button {
  width: 100%;
}

.menu-legend {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 40px;
  gap: 10px;
}

.description {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 30px;
  position: absolute;
  width: 100%;
}

</style>
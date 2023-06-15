<template>
  <div ref="resizeRef" class="container">
    <svg ref="svgRef"/>
  </div>
</template>

<script setup>
import {onMounted, ref, shallowRef, watch} from "vue";
import * as d3 from "d3";
import useResizeObserver from "../../use/resizeObserver.js";

const {resizeRef, resizeState} = useResizeObserver();
const svgRef = ref(null);
const neighborsRef = shallowRef()
const neighborsRefBefore = shallowRef()
const neighborsData = shallowRef([])
const labels = shallowRef([])
const counts = ref(undefined)

const props = defineProps(['allImages', 'index', 'numSamples', 'imgSize', 'color', 'referenceLayer', 'comparisonLayer'])
const emit = defineEmits(['index'])

const classes = ['airplane', 'apple', 'bee', 'car', 'dragon', 'mosquito', 'moustache', 'mouth', 'pear', 'piano', 'pineapple', 'smiley face', 'train', 'umbrella', 'wine bottle']

watch(() => props.referenceLayer, (layer) => {
  neighborsRefBefore.value = neighborsRef.value
  neighborsRef.value = neighborsData.value[layer];
})

// watch(() => props.comparisonLayer, (layer) => {
//   neighborsRefBefore.value = neighborsData.value[layer];
// })

const apiUrl = import.meta.env.VITE_APIURL
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

  const r = Math.min(innerWidth, innerHeight) * 0.3

  svg.selectAll('circle')
      .data([1.5, 1, 0.5])
      .enter()
      .append('circle')
      .attr('cx', width / 2)
      .attr('cy', height / 2)
      .attr("r", d => d * r)
      .attr("fill", "none")
      .attr("stroke", props.color)
      .attr("stroke-width", "3px")

  svg.selectAll("#center")
      .data(['data:image/png;base64, ' + props.allImages[props.index]])
      .enter()
      .append('image')
      .attr('xlink:href', (d) => d)
      .attr('width', 30)
      .attr('height', 30)
      .attr('x', width / 2 - 15)
      .attr('y', height / 2 - 15)

  const update = (selection) => {
    if (!props.allImages) {
      return;
    }

    neighbors = Object.fromEntries(Object.entries(neighborsRef.value).sort((a, b) => a[1] - b[1]).slice(0, props.numSamples || 1000))
    neighborsBefore = Object.fromEntries(Object.entries(neighborsRefBefore.value).sort((a, b) => a[1] - b[1]).slice(0, props.numSamples || 1000))

    // __________ LINES TO SHOW MOVEMENT _____________

    const scaleR = d3.scaleLinear([Math.min(...Object.values(neighbors)), Math.max(...Object.values(neighbors))], [0.5, 1.5]).clamp(false)
    const scaleOld = d3.scaleLinear([Math.min(...Object.values(neighborsBefore)), Math.max(...Object.values(neighborsBefore))], [0.5, 1.5]).clamp(false)

    const imgSize = props.imgSize

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
        .style("stroke", d => scaleOld(neighborsRefBefore.value[d]) > scaleR(neighborsRef.value[d]) ? "green" : "red")
        .style("opacity", 0.1)
        .attr("class", "move")

    // __________ SKETCHES _____________

    const radii = {}
    svg.selectAll('image.n')
        .data(Object.entries(neighbors).sort((a, b) => a[1] - b[1]).slice(0, 1000), item => item[0])
        .join(
            enter => enter
                .append('image')
                .attr('xlink:href', (d) => 'data:image/png;base64, ' + props.allImages[d[0]])
                .attr('x', (d) => ((scaleOld(neighborsRefBefore.value[d[0]]) * r) * Math.cos(angleLookup[d[0]])) + width / 2 - (imgSize / 2))
                .attr('y', (d) => ((scaleOld(neighborsRefBefore.value[d[0]]) * r) * Math.sin(angleLookup[d[0]])) + height / 2 - (imgSize / 2))
                .attr('width', imgSize)
                .attr('height', imgSize)
                .attr('opacity', 0)
                .each(d => radii[d[0]] = (scaleR(d[1]) * r))
                .attr('class', 'n closer')
                // .transition()
                // .ease(d3.easeLinear)
                // .duration(100)
                .attr('x', (d) => (scaleR(d[1]) * r * Math.cos(angleLookup[d[0]])) + width / 2 - (imgSize / 2))
                .attr('y', (d) => (scaleR(d[1]) * r * Math.sin(angleLookup[d[0]])) + height / 2 - (imgSize / 2))
                .attr('opacity', 1)
                .selection(),
            update => update
                .attr('x', (d) => (radiiBefore[d[0]] * Math.cos(angleLookup[d[0]])) + width / 2 - (imgSize / 2))
                .attr('y', (d) => (radiiBefore[d[0]] * Math.sin(angleLookup[d[0]])) + height / 2 - (imgSize / 2))
                // .transition()
                // .ease(d3.easeLinear)
                // .duration(100)
                .attr('x', (d) => (scaleR(d[1]) * r * Math.cos(angleLookup[d[0]])) + width / 2 - (imgSize / 2))
                .attr('y', (d) => (scaleR(d[1]) * r * Math.sin(angleLookup[d[0]])) + height / 2 - (imgSize / 2))
                .each(d => radii[d[0]] = (scaleR(d[1]) * r))
                .attr('class', d => scaleOld(neighborsBefore[d]) > scaleR(neighbors[d]) ? "closer n" : "away n")
                .selection(),
            exit => exit
                .attr('x', (d) => (radiiBefore[d[0]] * Math.cos(angleLookup[d[0]])) + width / 2 - (imgSize / 2))
                .attr('y', (d) => (radiiBefore[d[0]] * Math.sin(angleLookup[d[0]])) + height / 2 - (imgSize / 2))
                // .transition()
                // .ease(d3.easeLinear)
                // .duration(100)
                .attr('x', (d) => (scaleR(neighborsRef.value[d[0]]) * r * Math.cos(angleLookup[d[0]])) + width / 2 - (imgSize / 2))
                .attr('y', (d) => (scaleR(neighborsRef.value[d[0]]) * r * Math.sin(angleLookup[d[0]])) + height / 2 - (imgSize / 2))
                .attr('opacity', 0)
                .remove()
        );
    radiiBefore = radii;

  }

  update();
  watch(neighborsRef, update)
  // watch(neighborsRefBefore, update)
  watch(() => props.numSamples, update)
}


onMounted(() => {

  fetch(apiUrl + "neighborhood/" + props.index)
      .then(result => result.json())
      .then(json => {
        labels.value = json.labels
        neighborsData.value = json.layers;
        neighborsRef.value = json.layers[props.referenceLayer]
        neighborsRefBefore.value = json.layers[props.comparisonLayer]
        watch(resizeRef, setupCircleView)
        watch(() => props.allImages, setupCircleView)

        for (const n of Object.keys(labels.value)) {
          if (!angleLookup[n]) {
            angleLookup[n] = Math.random() * 2 * Math.PI
          }
        }

        setupCircleView()

      })

})
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
}

.container > svg {
  width: 100%;
  height: 100%;
  overflow: unset;
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

</style>
<template>
  <div ref="resizeRef" class="lines-container">
    <svg ref="svgRef"/>
  </div>
</template>

<script setup>

import {onMounted, ref, watch} from "vue";
import * as d3 from "d3";
import useResizeObserver from "../../use/resizeObserver.js";
import {layers} from "../../utils/utils"

const {resizeRef, resizeState} = useResizeObserver();
const props = defineProps(['data', 'selection', 'scatterData', 'enableBrush', 'animateLineDraw'])
const emit = defineEmits(['selection'])
const svgRef = ref(null);

onMounted(() => {

  const margin = {top: 50, right: 50, bottom: 50, left: 50}


  const update = () => {
    if (props.data?.length === 0 || !props.data) {
      return
    }

    let filterF = () => true

    const selection = props.selection
    if (selection.length > 0) {
      filterF = (item) => selection.includes(item.idx)
    }

    const {width, height} = resizeState.dimensions;
    const innerWidth = width - margin.left - margin.right
    const innerHeight = height - margin.top - margin.bottom

    const svgContainer = d3.select(svgRef.value)
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

    const dimensions = props.data.layers
    const xScale = d3.scaleLinear()
        .domain([0, 100])
        .range([innerWidth, 50])

    const yScale = d3.scalePoint()
        .range([1, innerHeight - 1])
        .domain(dimensions);

    function path(d) {
      return d3.line()(dimensions.map(function (p, i) {
        return [xScale(d.layers[i]), yScale(p)];
      }));
    }

    const color = d3.scaleSequential().domain([-20, 60])
        .interpolator(d3.interpolateViridis);

    let filteredData = props.data.items
        .filter(filterF)

    if (props.scatterData) {
      const dataIdxShownInScatter = props.scatterData.map(item => item.id)
      filteredData = filteredData.filter(item => dataIdxShownInScatter.includes(item.idx))
    }

    const brush = d3.brush()
        .on("start brush end", brushed)
        .on('end', ({selection}) => brushEnd(selection, filteredData, dimensions, xScale, yScale))

    function brushEnd(selection, filteredData, dimensions, xScale, yScale) {
      const indices = filteredData.filter(item => dimensions
          .map((p, i) => [xScale(item.layers[i]), yScale(p)])
          .some(item => selection[0][0] < item[0] && selection[1][0] > item[0] && selection[0][1] < item[1] && selection[1][1] > item[1])
      ).map(item => item.idx)

      if (props.scatterData) {
        const items = props.scatterData.filter(item => indices.includes(item.id))
        emit("selection", items)
      }

    }

    function brushed(e) {
    }

    let items = props.data.items

    console.log(props.data.items)
    if (props.scatterData) {
      items = props.data.items.filter(item => props.scatterData.some(i => i.id === item.idx))
    }

    const svgPath = svg.selectAll("path")
        .data(items)
        .enter()
        .append("path")
        .sort((a,b) => (selection?.includes(a.idx)? 1 : 0) - (selection?.includes(b.idx)? 1 : 0))
        .attr("class", function (d) {
          return "line " + d.y
        }) // 2 class for each line: 'line' and the group name
        .attr("d", path)
        .style("fill", "none")
        .style("stroke", function (d) {
          if(!selection || selection.length === 0 || selection.includes(d.idx)){
            return (color(d.layers[d.layers.length-1]))
          }
          return "rgba(212,212,212,0.34)"
        })
        .style("stroke-width", function (d) {
          if(selection.includes(d.idx) && selection.length < 100){
            return 1
          }
          return 0.1
          // filteredData.length > 100 ? 0.1 : 1
        })
        .style("opacity", 1)

    let lengths = []

    if(props.animateLineDraw){
      svgPath
          .each(function (d, i) {
            lengths[i] = d3.select(this).node().getTotalLength();
          })
          .attr("stroke-dasharray", (d, i) => lengths[i] + " " + lengths[i])
          .attr("stroke-dashoffset", (d, i) => lengths[i])
          .transition()
          .ease(d3.easeLinear)
          .attr("stroke-dashoffset", 0)
          .delay(function (d, i) {
            return i;
          })
          .duration(2000)
    }

    svg.selectAll("myAxis")
        // For each dimension of the dataset I add a 'g' element:
        .data(dimensions).enter()
        .append("g")
        .attr("class", "axis")
        // I translate this element to its right position on the x axis
        .attr("transform", function (d) {
          return "translate(0," + yScale(d) + ")";
        })
        // And I build the axis with the call function
        .each(function (d) {
          d3.select(this).call(d3.axisTop().ticks(10).scale(xScale));
        })
        // Add axis title
        .append("text")
        .style("text-anchor", "end")
        .attr("x", 30)
        .attr("y", 0)
        .text(function (d, i) {
          return layers[i].label
        })
        .style("fill", "black")

    const brushArea = svgContainer
        .append("g")
        .style("width", innerWidth)
        .style("height", innerHeight)
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    if (props.enableBrush) {
      brushArea.call(brush);
    }

  }

  watch(props, update)
  watch( () => props.scatterData?.length, update)
  update()

})

</script>

<style scoped>
.lines-container {
  width: 100%;
  height: 100%;
}
</style>
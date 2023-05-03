<template>
  <div ref="resizeRef" class="lines-container">
    <svg ref="svgRef"/>
  </div>
</template>

<script setup>

import {onMounted, ref, watch} from "vue";
import * as d3 from "d3";
import useResizeObserver from "../use/resizeObserver.js";

const {resizeRef, resizeState} = useResizeObserver();
const props = defineProps(['data', 'selection', 'scatterData'])
const emit = defineEmits(['selection'])
const svgRef = ref(null);

onMounted(() => {

  const margin = {top: 50, right: 50, bottom: 50, left: 50}

  //watchEffect(() => {

  watch(props, async (newQuestion, oldQuestion) => {

    if (props.data.length === 0) {
      return
    }

    console.log(props.selection)

    let filterF = () => true

    const dataIdxShownInScatter = props.scatterData.map(item => item.id)
    const selection = props.selection.map(item => item.id)
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


    const yScales = {}
    const dimensions = props.data.layers
    for (const dim of dimensions) {
      yScales[dim] = d3.scaleLinear()
          .domain([0, 100])
          .range([innerHeight, 0])
    }

    const x = d3.scalePoint()
        .range([1, innerWidth-1])
        .domain(dimensions);

    function path(d) {
      return d3.line()(dimensions.map(function (p, i) {
        // console.log(yScales)
        // console.log(p)
        // console.log(i)
        // console.log(d)
        return [x(p), yScales[p](d.layers[i])];
      }));
    }

    const color = d3.scaleSequential().domain([1, 100])
        .interpolator(d3.interpolateViridis);

    const filteredData = props.data.items
        .filter(item => dataIdxShownInScatter.includes(item.idx))
        .filter(filterF)


    const brush = d3.brush()
        .on("start brush end", brushed)
        .on('end', ({selection}) => brushEnd(selection, filteredData, dimensions, x, yScales))

    function brushEnd(selection, filteredData, dimensions, x, yScales) {
      console.log(selection)
      const indices = filteredData.filter(item => dimensions
          .map((p, i) => [x(p), yScales[p](item.layers[i])])
          .some(item => selection[0][0] < item[0] && selection[1][0] > item[0] && selection[0][1] < item[1] && selection[1][1] > item[1])
      ).map(item => item.idx)

      const items = props.scatterData.filter(item => indices.includes(item.id))
      console.log(items)
      emit("selection", items)

    }

    function brushed(e) {
    }

    svg.selectAll("path")
        .data(filteredData)
        .enter()
        .append("path")
        .attr("class", function (d) {
          return "line " + d.y
        }) // 2 class for each line: 'line' and the group name
        .attr("d", path)
        .style("fill", "none")
        .style("stroke", function (d) {
          return (color(d.layers[0]))
        })
        .style("stroke-width", filteredData.length > 100 ? 0.1 : 1)
        .style("opacity", 1)
    //.on("mouseover", highlight)
    //.on("mouseleave", doNotHighlight )


    svg.selectAll("myAxis")
        // For each dimension of the dataset I add a 'g' element:
        .data(dimensions).enter()
        .append("g")
        .attr("class", "axis")
        // I translate this element to its right position on the x axis
        .attr("transform", function (d) {
          return "translate(" + x(d) + ")";
        })
        // And I build the axis with the call function
        .each(function (d) {
          d3.select(this).call(d3.axisLeft().ticks(10).scale(yScales[d]));
        })
        // Add axis title
        .append("text")
        .style("text-anchor", "middle")
        .attr("y", -9)
        .text(function (d) {
          return d;
        })
        .style("fill", "black")

    const brushArea = svgContainer
        .append("g")
        .style("width", innerWidth)
        .style("height", innerHeight)
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    brushArea.call(brush);

  })


})

</script>

<style scoped>
.lines-container {
  width: 100%;
  height: 45vh;
}
</style>
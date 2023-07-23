<template>
  <div ref="resizeRef" class="container">
    <svg ref="svgRef"/>
  </div>
</template>

<script setup>

import useResizeObserver from "../../../use/resizeObserver.js";
import {onMounted, ref, watch} from "vue";
import * as d3 from "d3";
import {layers} from "../../../utils/utils.ts";

const {resizeRef, resizeState} = useResizeObserver();
const props = defineProps(['lines', 'highlightedSample', 'allImages'])
const svgRef = ref(null);

onMounted(() => {

  const draw = () => {

    if (!props.lines)
      return

    const margin = {top: 50, right: 50, bottom: 50, left: 50}

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

    const dimensions = props.lines.layers

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

    const filteredData = props.lines.items
        .filter((item) => props.highlightedSample.includes(item.idx))

    const redrawPath = (delay) => {
      const filteredData = props.lines.items
          .filter((item) => props.highlightedSample.includes(item.idx))

      svg.selectAll("path.line").remove()
      svg.selectAll("path.hover").remove()

      let color = () => "black"
      if(filteredData.length > 1){
       color = d3.scaleSequential().domain([-20, 60])
            .interpolator(d3.interpolateViridis);
      }


      const o = svg.selectAll("path.hover")
          .data(filteredData)
          .enter()
          .append("path")
          .attr("d", path)
          .attr('class', 'hover')
          .style("fill", "none")
          .style("stroke", d => color(d.layers[d.layers.length-1]))
          .style("stroke-width", "30px")
          .style("opacity", 0)
          .on('mouseover', function(e,d){
            svg.selectAll('.parallelLineImg').style('opacity', 0)
            svg.selectAll('.parallelLineLine').style("stroke", d => '#ccc')
            svg.selectAll('#line_'+d.idx).style("stroke", d => color(d.layers[d.layers.length-1]))
            svg.select('#img_'+d.idx).style('opacity', 1)
          })
          .on('mouseout', d => {
            svg.selectAll('.parallelLineImg').style('opacity', 1)
            svg.selectAll('.parallelLineLine').style("stroke", d => color(d.layers[d.layers.length-1]))
          })

      const svgPath = svg.selectAll("path.line")
          .data(filteredData)
          .enter()
          .append("path")
          .attr("class", function (d) {
            return "parallelLineLine line line " + d.y
          }) // 2 class for each line: 'line' and the group name
          .attr("d", path)
          .style("fill", "none")
          .style("stroke", d => color(d.layers[d.layers.length-1]))
          .style("stroke-width", "10px")
          .style("opacity", 0.5)
          .on('mouseover', function(e,d){
            svg.selectAll('.parallelLineImg').style('opacity', 0)
            svg.selectAll('.parallelLineLine').style("stroke", d => '#ccc')
            svg.selectAll('#line_'+d.idx).style("stroke", d => color(d.layers[d.layers.length-1]))
            svg.select('#img_'+d.idx).style('opacity', 1)
          })
          .on('mouseout', d => {
            svg.selectAll('.parallelLineImg').style('opacity', 1)
            svg.selectAll('.parallelLineLine').style("stroke", d => color(d.layers[d.layers.length-1]))
          })


      let lengths = []

      svgPath
          .each(function (d, i) {
            lengths[i] = d3.select(this).node().getTotalLength();
          })
          .attr("stroke-dasharray", (d, i) => lengths[i] + " " + lengths[i])
          .attr("stroke-dashoffset", (d, i) => lengths[i])
          .transition()
          .ease(d3.easeLinear)
          .attr("stroke-dashoffset", 0)
          .attr('id', d => 'line_'+d.idx)
          .delay(function (d, i) {
            return delay + 100 * i;
          })
          .duration(2000)

      svg.selectAll("circle.dot")
          .remove()

      for(const l of filteredData){
        svg.selectAll("g.axis")
            .data(l.layers)
            .append("circle")
            .attr("class", "dot")
            .attr("cx", d => xScale(d))
            .attr("r", 2)
            .style("fill", "black")
      }

      svg.selectAll('image').remove()
      svg.selectAll('image')
          .data(filteredData)
          .enter()
          .append('image')
          .attr('xlink:href', (d) => 'data:image/png;base64, ' + props.allImages[d.idx])
          .attr('width', 50)
          .attr('height', 50)
          .attr('class', 'parallelLineImg')
          .attr('id', d => "img_"+d.idx)
          .attr('x', (d) => xScale(d.layers[13]) -25)
          .attr('y', (d) => innerHeight)
          .style('opacity', 1)

    }

    watch(() => props.highlightedSample, () => redrawPath(0))
    redrawPath(1000)


    const axis = svg.selectAll("myAxis")
        .data(dimensions).enter()
        .append("g")
        .attr("class", "axis")
        .attr("transform", function (d) {
          return "translate(0," + innerHeight / 2 + ")";
        })



    // And I build the axis with the call function
    axis.each(function (d, i) {
      d3.select(this).call(d3.axisTop().ticks(10).scale(xScale))
          .append("text")
          .style("text-anchor", "end")
          .attr("x", 30)
          .attr("y", 0)
          .text(function (d) {
            return layers[i].label
          })
          .style("fill", "black")
    })

    axis
        .transition()
        .ease(d3.easeCubicOut)
        .duration(1000)
        .attr("transform", function (d) {
          return "translate(0," + yScale(d) + ")";
        })

    for(const l of filteredData){
      axis.data(l.layers)
          .join()
          .append("circle")
          .attr("class", "dot")
          .attr("cx", d => xScale(d))
          .attr("r", 3)
          .style("fill", "black")
    }




  }

  watch(() => props.lines, draw)
  draw()

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
}


</style>
<template>
  <div ref="resizeRef" class="scatter-container">
    <svg ref="svgRef"/>
    <div style="position: absolute; bottom: 0; right: 0">
      Hold <span class="key">⇧ Shift</span>  to select samples
    </div>
  </div>

</template>

<script setup>
import * as d3 from "d3";
import {onMounted, ref, watch} from "vue";
import useResizeObserver from "../../use/resizeObserver.js";
import {axisBottom, axisLeft, axisRight, axisTop, extent, max, min, scaleLinear} from "d3";

const {resizeRef, resizeState} = useResizeObserver();
const props = defineProps(['data', 'colorStrategy', 'selection'])
const emit = defineEmits(['selection', 'viewport'])
const svgRef = ref(null);

onMounted(() => {
  const margin = {top: 0, right: 0, bottom: 0, left: 0}
  const myColor = d3.scaleOrdinal()
      .domain([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
      .range(['rgb(47,170,255)', 'rgb(181,205,241)', 'rgb(255,165,83)', 'rgb(255,220,185)',
        'rgb(255,45,46)', 'rgb(44, 160, 44)', 'rgb(152, 223, 138)', 'rgb(255,152,152)',
        'rgb(148, 103, 189)', 'rgb(197, 176, 213)', 'rgb(198,134,126)', 'rgb(186,136,128)',
        'rgb(227, 119, 194)', 'rgb(255,97,156)', 'rgb(62,255,168)', 'rgb(245,255,250)',
        'rgb(188, 189, 34)', 'rgb(219, 219, 141)', 'rgb(23, 190, 207)', 'rgb(158, 218, 229)']);

  const update = () => {

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

    const xExtent = d3.extent(props.data, d => d.x)
    const xRange = xExtent[1] - xExtent[0]

    const yExtent = d3.extent(props.data, d => d.y)
    const yRange = yExtent[1] - yExtent[0]

    const xScale = scaleLinear()
        .domain([xExtent[0] - (xRange * .1), xExtent[1] + (xRange * .1)])
        .range([0, innerWidth]);
    // const xAxis = axisTop(xScale)
    // svg.append("g")
    //     .call(xAxis);

    const yScale = scaleLinear()
        .domain([yExtent[0] - (yRange * .1), yExtent[1] + (yRange * .1)])
        .range([innerHeight, 0]);
    // const yAxis = axisLeft(yScale)
    // svg.append("g")
    //     .call(yAxis);


    const brush = d3.brush()
        .filter(e => !!e.shiftKey)
        .keyModifiers(false)
        .on("start brush end", brushed)
        .on('end', brushEnd)

    const dot = svg.append("g")
        .attr("fill", "none")
        .attr("stroke-width", 0.3)
        .selectAll("circle")
        .data(props.data)
        .attr("stroke", d => d ? (d.c === d.c_hat ? 'rgb(59, 130, 246)' : 'rgb(235, 64, 52)') : 'rgb(59, 130, 246)')
        .join("circle")
        .attr("transform", d => `translate(${xScale(d.x)},${yScale(d.y)})`)
        .attr("r", 1);

    const dotMirror = svg.append("g")
        .attr("fill", "none")
        .attr("stroke-width", 0.3)
        .selectAll("circle")
        .data(props.data)
        .attr("stroke", d => d ? (d.c === d.c_hat ? 'rgb(59, 130, 246)' : 'rgb(235, 64, 52)') : 'rgb(59, 130, 246)')
        .join("circle")
        .attr("transform", d => `translate(${xScale(d.x)},${yScale(d.y)})`)
        .attr("r", 1);

    svg.call(brush);

    let zx = xScale
    let zy = yScale
    const gGrid = svg.append("g");
    let r = 1

    let zoomed = ({transform}) => {
      svg.call(brush.move, null);
      zx = transform.rescaleX(xScale).interpolate(d3.interpolateRound);
      zy = transform.rescaleY(yScale).interpolate(d3.interpolateRound);

      //emit("viewport", [zx.domain()[0], zx.domain()[1], zy.domain()[0], zy.domain()[1]])

      r = transform.k
      dot.attr("transform", transform)
          .attr("stroke-width", 0.3 * r)
          .attr("r", 1 * r)
          .attr("transform", d => `translate(${zx(d.x)},${zy(d.y)})`)

      dotMirror.attr("transform", transform)
          .attr("stroke-width", 0.3 * r)
          .attr("r", 1 * r)
          .attr("transform", d => `translate(${zx(d.x)},${zy(d.y)})`)

      gGrid.call(grid, zx, zy);
    }

    const zoom = d3.zoom()
        .scaleExtent([0.5, 32])
        .filter(e => !e.shiftKey)
        .on("zoom", zoomed);

    svg.call(zoom).call(zoom.transform, d3.zoomIdentity);


    function grid(g, x, y) {
      g.attr("stroke", "currentColor")
          .attr("stroke-opacity", 0.1)
          .call(g => g
              .selectAll(".x")
              .data(x.ticks(12))
              .join(
                  enter => enter.append("line").attr("class", "x").attr("y2", height),
                  update => update,
                  exit => exit.remove()
              )
              .attr("x1", d => 0.5 + x(d))
              .attr("x2", d => 0.5 + x(d)))
          .call(g => g
              .selectAll(".y")
              .data(y.ticks(12 * (innerHeight / innerWidth)))
              .join(
                  enter => enter.append("line").attr("class", "y").attr("x2", width),
                  update => update,
                  exit => exit.remove()
              )
              .attr("y1", d => 0.5 + y(d))
              .attr("y2", d => 0.5 + y(d)))
    }


    function brushed({selection}) {
      let value = [];
      if (selection) {
        const [[x0, y0], [x1, y1]] = selection;
        value = dot
            .style("stroke", "gray")
            .filter(d => x0 <= zx(d.x) && zx(d.x) < x1 && y0 <= zy(d.y) && zy(d.y) < y1)
            .style("stroke", getColor)
            .data();

        dotMirror
            .style("stroke", "none")
            .filter(d => x0 <= zx(d.x) && zx(d.x) < x1 && y0 <= zy(d.y) && zy(d.y) < y1)
            .style("stroke", getColor)
            .data();

      } else {
        if (props.selection.length > 0) {
          const selectedIds = props.selection.map(item => item.id)
          dot.style("stroke", "gray")
              .attr("r",  r)
              .filter(d => selectedIds.includes(d.id))
              .style("stroke", getColor)
              .attr("r",  2 * r)
              .style("stroke-width",  r)

          dotMirror.style("stroke", "none")
              .attr("r",  r)
              .filter(d => selectedIds.includes(d.id))
              .style("stroke", getColor)
              .attr("r",  2 * r)
              .style("stroke-width",  r)
        } else {
          dot.style("stroke", getColor)
          dotMirror.style("stroke", getColor)
        }
      }
      svg.property("value", value).dispatch("input");

    }

    function brushEnd(e) {
      if (!e.sourceEvent)
        return

      let value = [];
      if (e.selection) {
        const [[x0, y0], [x1, y1]] = e.selection;
        value = dot.filter(d => x0 <= zx(d.x) && zx(d.x) < x1 && y0 <= zy(d.y) && zy(d.y) < y1).data();
      }

      emit("selection", value)
    }

    function getColor(d) {
      if (!d)
        return 'rgb(59, 130, 246)'

      if (props.colorStrategy === 'true/false') {
        return (d.c === d.c_hat) ? 'rgb(59, 130, 246)' : 'rgb(235, 64, 52)'
      } else if (props.colorStrategy === 'by_prediction') {
        return myColor(d.c_hat)
      }
      return myColor(d.c)
    }

  }

  watch(() => props.data, update)
  watch(() => resizeRef, update)
  watch(() => props.selection, update)


})

</script>

<style scoped>
.scatter-container {
  width: 100%;
  height: 45vh;
  background-color: white;
  box-sizing: border-box;
  border: 2px solid var(--gray);
  position: relative;
  color: white;
}

.scatter-container > svg {
  width: 100%;
  height: 100%;
  background-color: #2c2c2c
}

</style>
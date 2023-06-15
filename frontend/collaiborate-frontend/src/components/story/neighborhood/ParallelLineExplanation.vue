<template>
  <div ref="resizeRef" class="container">
    <svg ref="svgRef"/>
  </div>
</template>

<script setup>
import {onMounted, ref, shallowRef, watch} from "vue";
import * as d3 from "d3";
import useResizeObserver from "../../../use/resizeObserver.js";
import {getNeighborhoodForSample} from "../../../utils/utils.ts";

const {resizeRef, resizeState} = useResizeObserver();
const svgRef = ref(null);
const neighborsData = shallowRef([])
const labels = shallowRef([])
const counts = ref(undefined)
const summaryCount = ref(undefined)

const props = defineProps(['allImages', 'index', 'numSamples', 'imgSize', 'color1', 'layer1', 'color2', 'layer2', 'step'])
const emit = defineEmits(['index', 'overlapCount'])

const classes = ['airplane', 'apple', 'bee', 'car', 'dragon', 'mosquito', 'moustache', 'mouth', 'pear', 'piano', 'pineapple', 'smiley face', 'train', 'umbrella', 'wine bottle']

const apiUrl = import.meta.env.VITE_APIURL
let angleLookup = {}
let radiiBefore = {}

const timeouts = []


function setupCircleView() {

  console.log("setup")

  const margin = {top: 50, right: 50, bottom: 50, left: 50}
  const {width, height} = resizeState.dimensions;

  if (height === 0)
    return

  const innerWidth = width - margin.left - margin.right
  const innerHeight = height - margin.top - margin.bottom

  const svgContainer = d3.select(svgRef.value)
      .attr("viewBox", [0, 0, width, height])
      .property("value", [])
      .attr("width", width)
      .attr("height", height)

  svgContainer.selectAll("g").remove()

  const background1 = svgContainer
      .append("g")
      .style("width", innerWidth)
      .style("height", innerHeight / 2)
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  const background2 = svgContainer
      .append("g")
      .style("width", innerWidth)
      .style("height", innerHeight / 2)
      .attr("transform", "translate(" + margin.left + "," + (margin.top + innerHeight / 2) + ")");

  const svg1 = svgContainer
      .append("g")
      .style("width", innerWidth)
      .style("height", innerHeight / 2)
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  const svg2 = svgContainer
      .append("g")
      .style("width", innerWidth)
      .style("height", innerHeight / 2)
      .attr("transform", "translate(" + margin.left + "," + (margin.top + innerHeight / 2) + ")");

  const r = Math.min(innerWidth, innerHeight / 2) * 0.25

  const update = (height, svg, background, neighbors, color) => {
    summaryCount.value = undefined

    if (!props.allImages) {
      return;
    }


    svgContainer.selectAll("line.connect").interrupt()
    background.selectAll('.pie').interrupt()
    background.selectAll('circle').interrupt()
    background.selectAll('circle').remove()
    svgContainer.selectAll(".axis").remove()

    svgContainer.selectAll('line.connect')
        .style('opacity', 1)
        .transition()
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .style("stroke-opacity", 0)
        .remove()

    const setup = (height, svg) => {
      background.selectAll('circle')
          .data([1.5, 1, 0.5])
          .enter()
          .append('circle')
          .attr('cx', width / 2)
          .attr('cy', height / 2)
          .attr("r", d => d * r)
          .attr("fill", "none")
          .attr("stroke", color)
          .attr("stroke-width", "3px")
          .style("stroke-opacity", 0)
          .transition(1000)
          .ease(d3.easeCubicIn)
          .style("stroke-opacity", 1)

      background.selectAll("#center")
          .data(['data:image/png;base64, ' + props.allImages[props.index]])
          .enter()
          .append('image')
          .attr("class", "center-img")
          .attr('xlink:href', (d) => d)
          .attr('width', 30)
          .attr('height', 30)
          .attr('x', width / 2 - 15)
          .attr('y', height / 2 - 15)
          .style("opacity", 0)
          .transition(1000)
          .ease(d3.easeCubicIn)
          .style("opacity", 1)
    }


    setup(height, svg);


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
      angleLookup[n[0]] = Math.random() * (arc.endAngle - arc.startAngle) * 0.8 + arc.startAngle + (arc.endAngle - arc.startAngle) * 0.1 - (Math.PI / 2)
    }

    // __________ Pie chart class distribution _____________

    background.selectAll('.pie').remove()
    background.selectAll('whatever')
        .data(pie)
        .enter()
        .append('path')
        .attr("class", "pie")
        .attr('d', d3.arc()
            .innerRadius(r * 0.5)
            .outerRadius(r * 1.5)
        )
        .attr('fill', "none")
        .attr("stroke", props.color)
        .attr("transform", "translate(" + (width / 2) + "," + (height / 2) + ")")
        .style("stroke-width", "3px")
        .style("opacity", 0)
        .transition(1000)
        .ease(d3.easeCubicIn)
        .style("opacity", 1)


    // __________ SKETCHES _____________

    const scaleR = d3.scaleLinear([Math.min(...Object.values(neighbors)), Math.max(...Object.values(neighbors))], [0.5, 1.5]).clamp(false)

    const imgSize = props.imgSize


    const radii = {}
    svg.selectAll('image.n')
        .data(Object.entries(neighbors).sort((a, b) => a[1] - b[1]).slice(0, 1000), item => item[0])
        .join(
            enter => enter
                .append('image')
                .attr('xlink:href', (d) => 'data:image/png;base64, ' + props.allImages[d[0]])
                .attr('width', imgSize)
                .attr('height', imgSize)
                .each(d => radii[d[0]] = (scaleR(d[1]) * r))
                .attr('class', 'n closer')
                .attr('x', (d) => (scaleR(d[1]) * r * Math.cos(angleLookup[d[0]])) + width / 2 - (imgSize / 2))
                .attr('y', (d) => (scaleR(d[1]) * r * Math.sin(angleLookup[d[0]])) + height / 2 - (imgSize / 2))
                .attr("i", d => d[0])
                .style('opacity', 1)
                .selection(),
            update => update
                .transition()
                .ease(d3.easeExpIn)
                .duration(1200)
                .attr('x', (d) => (scaleR(d[1]) * r * Math.cos(angleLookup[d[0]])) + width / 2 - (imgSize / 2))
                .attr('y', (d) => (scaleR(d[1]) * r * Math.sin(angleLookup[d[0]])) + height / 2 - (imgSize / 2))
                .each(d => radii[d[0]] = (scaleR(d[1]) * r))
                .selection(),
            exit => exit.remove()
        )


    radiiBefore = radii;

    const all = {}
    svgContainer.selectAll("image.n")
        .each(function () {
          const i = d3.select(this).attr("i")
          all[i] = (all[i] || 0) + 1
        })

    const count = Object.values(all).filter(x => x === 2).length
    summaryCount.value = count
    emit("overlapCount", count)

    if (props.step > 1) {
      setStep(props.step)
    }

  }

  function realign(svg, background, height) {
    svgContainer.selectAll(".axis").remove()


    console.log("realign")

    background.selectAll('.pie')
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style("opacity", 0)
        .style("stroke-opacity", 0)

    background.selectAll('circle')
        .style('opacity', 1)
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .remove()

    background.selectAll('.center-img')
        .style('opacity', 1)
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .remove()

    svg.selectAll("image.n")
        .order(x => x.i)
        .transition("connectAnimation")
        .ease(d3.easeExpIn)
        .duration(1200)
        .attr("x", (d, i) => i * innerWidth / props.numSamples)
        .attr("y", height)
        .style("opacity", 1)

    svgContainer.selectAll('line.connect')
        .style('opacity', 1)
        .transition("connectAnimation")
        .ease(d3.easeLinear)
        .duration(1000)
        .style('opacity', 0)
        .style("stroke-opacity", 0)
        .remove()
  }

  function connect() {

    svgContainer.selectAll(".axis").remove()
    d3.selectAll().interrupt("shrink")

    const sketches = {}
    svgContainer.selectAll("image.n")
        .each(function () {
          const i = d3.select(this).attr("i")
          sketches[i] = [...(sketches[i] || []), [
            Number.parseInt(d3.select(this).attr("x")),
            Number.parseInt(d3.select(this).attr("y"))]]
        })

    svg1.selectAll("image.n")
        .transition("connectAnimation")
        .ease(d3.easeExpIn)
        .duration(1000)
        .style("opacity", 1)

    svg2.selectAll("image.n")
        .transition("connectAnimation")
        .ease(d3.easeExpIn)
        .duration(1000)
        .style("opacity", 1)


    svgContainer.selectAll("line.connect")
        .data(Object.entries(sketches).filter(x => x[1].length > 1))
        .enter()
        .append('line')
        .attr("class", "connect")
        .style("stroke-width", 5)
        .attr("x1", d => d[1][0][0] + margin.left + props.imgSize / 2)
        .attr("y1", d => d[1][0][1] + margin.top + props.imgSize / 2)
        .attr("x2", d => d[1][0][0] + margin.left + props.imgSize / 2)
        .attr("y2", d => d[1][0][1] + margin.top + props.imgSize / 2)
        .style("opacity", 0.3)
        .transition("connectAnimation")
        .delay(function (d, i) {
          return 10 * i;
        })
        .duration(1000)
        .attr("x2", d => d[1][1][0] + margin.left + props.imgSize / 2)
        .attr("y2", d => d[1][1][1] + innerHeight / 2 + margin.top + props.imgSize / 2)
        .style("stroke", props.color2)
        .style("opacity", 0.3)

  }

  function shrinkAndAddAxis() {

    d3.selectAll().interrupt("connectAnimation")

    // svgContainer.selectAll("line.connect").interrupt()
    // background1.selectAll('.pie').interrupt()
    // background1.selectAll('circle').interrupt()
    // svgContainer.selectAll("image").interrupt()
    // background2.selectAll('.pie').interrupt()
    // background2.selectAll('circle').interrupt()
    // svgContainer.selectAll("image.n").interrupt()

    console.log("shrink")

    background1.selectAll('.pie')
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style("opacity", 0)
        .style("stroke-opacity", 0)

    background1.selectAll('circle')
        .style('opacity', 1)
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .remove()

    background1.selectAll('.center-img')
        .style('opacity', 1)
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .remove()

    background2.selectAll('.pie')
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style("opacity", 0)
        .style("stroke-opacity", 0)

    background2.selectAll('circle')
        .style('opacity', 1)
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .remove()

    background2.selectAll('.center-img')
        .style('opacity', 1)
        .transition("connectAnimation")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .remove()

    svgContainer.selectAll("line.connect")
        .transition("shrink")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .style('stroke-opacity', 0)

    svg1.selectAll("image.n")
        .transition("shrink")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .style('stroke-opacity', 0)

    svg2.selectAll("image.n")
        .transition("shrink")
        .ease(d3.easeCubicOut)
        .duration(1000)
        .style('opacity', 0)
        .style('stroke-opacity', 0)


    let scale = d3.scaleLinear()
        .domain([0, props.numSamples])
        .range([innerWidth, 0]);

    svgContainer.selectAll("line.connect")
        .transition("shrink")
        .delay(function (d, i) {
          return 10 * i;
        })
        .duration(1000)
        .attr("x1", margin.left + scale(summaryCount.value))
        .attr("y1", height / 2)
        .attr("x2", margin.left + scale(summaryCount.value))
        .attr("y2", height / 2)
        .style("stroke", props.color2)


    svgContainer.selectAll(".axis").remove()
    const axisSelection = svgContainer.selectAll("myAxis")
        // For each dimension of the dataset I add a 'g' element:
        .data([
          "Convolution"
        ]).enter()
        .append("g")
        .attr("class", "axis")
        // I translate this element to its right position on the x axis
        .attr("transform", function (d) {
          return "translate(" + margin.left + "," + height / 2 + ")";
        })
        // And I build the axis with the call function
        .each(function (d) {
          d3.select(this).call(d3.axisTop().ticks(10).scale(scale));
        })

    axisSelection
        // Add axis title
        .append("circle")
        .attr("cx", scale(summaryCount.value))
        .attr("r", 5)
        .style("fill", props.color2)
    axisSelection
        .append("text")
        .text(summaryCount.value)
        .attr("x", scale(summaryCount.value))
        .attr("y", -30)
        .style("text-anchor", "middle")
        .style("fill", "black")
  }

  const setStep = (step) => {
    if (step === 1) {
      timeouts.forEach(t => clearTimeout(t));

      update(height / 2, svg1, background1, getNeighbors(props.layer1), props.color1);
      update(height / 2, svg2, background2, getNeighbors(props.layer2), props.color2);
    } else if (step === 2) {
      timeouts.forEach(t => clearTimeout(t));

      realign(svg1, background1, height / 2 - 80)
      realign(svg2, background2, 80)
      timeouts.push(setTimeout(connect, 1500));
    } else if (step === 3) {
      timeouts.forEach(t => clearTimeout(t));
      shrinkAndAddAxis()
    }
  }

  watch(() => props.step, setStep)

  update(height / 2, svg1, background1, getNeighbors(props.layer1), props.color1);
  update(height / 2, svg2, background2, getNeighbors(props.layer2), props.color2);

  watch(() => props.numSamples, () => {
    update(height / 2, svg1, background1, getNeighbors(props.layer1), props.color1);
    update(height / 2, svg2, background2, getNeighbors(props.layer2), props.color2);
    // setStep(props.step)
  })
}


function getNeighbors(layer) {
  return Object.fromEntries(Object.entries(neighborsData.value[layer]).sort((a, b) => a[1] - b[1]).slice(0, props.numSamples || 1000))
}

onMounted(() => {

  getNeighborhoodForSample(props.index)
      .then(result => result.json())
      .then(json => {
        labels.value = json.labels
        neighborsData.value = json.layers;
        watch(resizeRef, setupCircleView)
        watch(() => props.allImages, setupCircleView)

        setupCircleView()
      })

  watch(() => props.layer1, () => {
    setupCircleView()
  })

  watch(() => props.layer2, () => {
    setupCircleView()
  })

  watch(() => props.index, () => {
    getNeighborhoodForSample(props.index)
        .then(result => result.json())
        .then(json => {
          labels.value = json.labels
          neighborsData.value = json.layers;
          setupCircleView()
        })
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
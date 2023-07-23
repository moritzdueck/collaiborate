<template>
  <div style="display: flex; flex-direction: column; height: 100vh; width: 100%; overflow: hidden;">
    <div class="projection-container__menu">

      <span/>
      <span>Projection</span>
      <span>Visualization type</span>
      <span>Color points by</span>
      <span>Restrict Labels</span>
      <span>Restrict Predictions</span>
      <span></span>

      <div
          style="padding-left: 50px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: -15px">
        <span class="jump-section" @click="$emit('story')">
          Back to the story
          <img class="left" src="/arrow_left.svg">
        </span>
      </div>

      <Dropdown v-model="projection" editable :options="projectionOptions"
                placeholder="Select a Projection" id="projection-dropdown"/>

      <Dropdown v-model="analysisType" editable :options="analysisTypeOptions" v-on:change="updateSelectionDisplay"
                placeholder="Select a Visualization" id="analysis-type-dropdown"/>

      <Dropdown v-model="colorStrategy" editable :options="colorStrategyOptions" id="color-strategy-dropdown"
                placeholder="Color Strategy">
      </Dropdown>

      <MultiSelect v-model="selectedTrueClasses" :options="trueClassOptions" id="label-dropdown"
                   option-label="label" option-value="value"
                   placeholder="Select Classes">
        <template #value="slotProps">
          <div v-if="slotProps.value" class="multi-select-options-grid">
              <span v-for="v of slotProps.value" class="selected-color-option">
                  <span style="width: 30px; height:30px; display: inline-block"
                        :style="'background-color:' + myColor(trueClassOptions[v].label)"></span>
              {{ trueClassOptions[v].label }}
              </span>

          </div>
          <span v-else>{{ slotProps.placeholder }}</span>
        </template>
        <template #option="slotProps">
          <div class="flex align-items-center">
            <div>{{ slotProps.option.label }}</div>
          </div>
        </template>
      </MultiSelect>
      <MultiSelect v-model="selectedPredictedClasses" :options="predictedClassOptions" option-label="label"
                   id="prediction-dropdown"
                   option-value="value"
                   placeholder="Select Classes">
        <template #value="slotProps">
          <div v-if="slotProps.value" class="multi-select-options-grid">
              <span v-for="v of slotProps.value" class="selected-color-option">
                  <span style="width: 30px; height:30px; display: inline-block"
                        :style="'background-color:' + myColor(predictedClassOptions[v].label)"></span>
              {{ predictedClassOptions[v].label }}
              </span>

          </div>
          <span v-else>{{ slotProps.placeholder }}</span>
        </template>
        <template #option="slotProps">
          <div class="flex align-items-center">
              <span style="width: 30px; height:30px; display: block"
                    :style="'background-color:' + myColor(slotProps.option.label)"></span>
            <div>{{ slotProps.option.label }}</div>
          </div>
        </template>
      </MultiSelect>
      <span class="reset-button" v-if="selection.length > 0" @click="handleSelection([])" id="reset-button">Reset</span>
    </div>

    <div class="explorer-container">
      <div class="projection-container">
        <div style="flex-grow: 1; width: 100%; height: 100%;" id="parallel-lines-component">
          <ParallelLines :data="linesData" :selection="selection.map((s:any) => s.id)" :scatterData="data"
                         v-on:selection="handleSelection" :enable-brush="true"/>
        </div>
      </div>
      <div class="projection-sample-container">

        <Scatterplot :data="data" :color-strategy="colorStrategy" v-on:selection="handleSelection"
                     :selection="selection" id="scatter-plot-component"
                     v-on:viewport="handleViewport"></Scatterplot>

        <!--   Class mode   -->

        <div class="samples-container" v-if="mode === 'class'" id="samples-component">
          <div v-for="(sketch, i) of sketches" class="sample" :id="'sample_'+i"
               @click="selection.length && emit('index', selection[i]?.id )">
            <!--            <a style="cursor: pointer">{{ selection.length > 0 ? selection[i]?.id : "" }}</a>-->
            <span>{{ sketch[0].label }}</span>
            <span v-if="sketch[0].label === sketch[0].prediction"/>
            <span v-if="sketch[0].label !== sketch[0].prediction"
                  class="samples__wrong-prediction">predicted: {{ sketch[0].prediction }}</span>
            <img class="samples__image" :src="sketch[1]"/>
          </div>
        </div>

      </div>

    </div>
  </div>


</template>

<script setup lang="ts">

import Scatterplot from "./Scatterplot.vue";
import {computed, onMounted, ref, shallowRef, watch} from "vue";
import * as d3 from "d3";
import introJs from "intro.js";
import "intro.js/introjs.css";
import ParallelLines from "../shared/ParallelLines.vue";
import {introJsConfig} from "./introJsConfig";

console.log(import.meta.env.MODE)
console.log(import.meta.env.VITE_APIURL)
const apiUrl = import.meta.env.VITE_APIURL

const emit = defineEmits(['index', 'story'])

const data = shallowRef([])
const linesData = shallowRef([])
const sketches = shallowRef([] as any)
const selection = shallowRef([] as any)

const mode = ref('class' as 'class' | 'no_class')
const analysisType = ref('sketch only' as 'sketch only' | 'predicted probabilities' | 'vanilla gradients' | 'grad cam' | 'occlusion' | 'knn');
const analysisTypeOptions = ref(['sketch only', 'predicted probabilities', 'vanilla gradients', 'grad cam', 'occlusion', 'knn'])
const projection = ref('input images' as 'input images' | 'last conv layer' | 'output')
const projectionOptions = ref(['input images', 'last conv layer', 'output'])
const firstUpdate = ref(true)

const trueClassOptions = ref([
  {label: 'airplane', value: 0},
  {label: 'apple', value: 1},
  {label: 'bee', value: 2},
  {label: 'car', value: 3},
  {label: 'dragon', value: 4},
  {label: 'mosquito', value: 5},
  {label: 'moustache', value: 6},
  {label: 'mouth', value: 7},
  {label: 'pear', value: 8},
  {label: 'piano', value: 9},
  {label: 'pineapple', value: 10},
  {label: 'smiley face', value: 11},
  {label: 'train', value: 12},
  {label: 'umbrella', value: 13},
  {label: 'wine bottle', value: 14},
])
const selectedTrueClasses = ref([])

const predictedClassOptions = ref([
  {label: 'airplane', value: 0},
  {label: 'apple', value: 1},
  {label: 'bee', value: 2},
  {label: 'car', value: 3},
  {label: 'dragon', value: 4},
  {label: 'mosquito', value: 5},
  {label: 'moustache', value: 6},
  {label: 'mouth', value: 7},
  {label: 'pear', value: 8},
  {label: 'piano', value: 9},
  {label: 'pineapple', value: 10},
  {label: 'smiley face', value: 11},
  {label: 'train', value: 12},
  {label: 'umbrella', value: 13},
  {label: 'wine bottle', value: 14},
])
const selectedPredictedClasses = ref([])

const myColor = d3.scaleOrdinal()
    .domain(['airplane', 'apple', 'bee', 'car', 'dragon', 'mosquito', 'moustache', 'mouth', 'pear', 'piano', 'pineapple', 'smiley face', 'train', 'umbrella', 'wine bottle'])
    .range(['rgb(47,170,255)', 'rgb(181,205,241)', 'rgb(255,165,83)', 'rgb(255,220,185)',
      'rgb(255,45,46)', 'rgb(44, 160, 44)', 'rgb(152, 223, 138)', 'rgb(255,152,152)',
      'rgb(148, 103, 189)', 'rgb(197, 176, 213)', 'rgb(198,134,126)', 'rgb(186,136,128)',
      'rgb(227, 119, 194)', 'rgb(255,97,156)', 'rgb(62,255,168)', 'rgb(245,255,250)',
      'rgb(188, 189, 34)', 'rgb(219, 219, 141)', 'rgb(23, 190, 207)', 'rgb(158, 218, 229)']);


const colorStrategy = ref('by_class' as 'by_class' | 'by_prediction' | 'true/false')
const colorStrategyOptions = ref(['by_class', 'by_prediction', 'true/false'])


onMounted(() => {
  const projectionPath = {
    'input images': 'umap',
    'last conv layer': 'umap-cl',
    'output': 'umap-logits'
  }[projection.value]

  fetch(apiUrl + projectionPath + "/10000")
      .then(res => res.json())
      .then(d => {
        data.value = d
        handleSelection(d.filter((item: any) => [110635, 101647, 272791, 271551, 185767, 146028, 115656].includes(item.id)));
      })

  fetch(apiUrl + 'lines')
      .then(res => res.json())
      .then(d => {
        linesData.value = d
      })
})

const reloadData = (viewport: number[]) => {

  const projectionPath = {
    'input images': 'umap',
    'last conv layer': 'umap-cl',
    'output': 'umap-logits'
  }[projection.value]
  const viewportPath = (viewport.length == 4)
      ? ('/' + viewport[0].toPrecision(8)
          + '/' + viewport[1].toPrecision(8)
          + '/' + viewport[2].toPrecision(8)
          + '/' + viewport[3].toPrecision(8))
      : ''

  if (selectedTrueClasses.value.length > 0 || selectedPredictedClasses.value.length > 0) {

    const filterString = 't' + selectedTrueClasses.value.join("-") + 'p' + selectedPredictedClasses.value.join("-")

    fetch(apiUrl + projectionPath + "_filtered/" + filterString + "/10000" + viewportPath)
        .then(res => res.json())
        .then(d => {
          data.value = d
        })
  } else {
    fetch(apiUrl + projectionPath + "/10000" + viewportPath)
        .then(res => res.json())
        .then(d => {
          data.value = d
        })
  }
}

watch([selectedTrueClasses, selectedPredictedClasses, projection], () => reloadData([]))

const handleSelection = (s: any) => {
  selection.value = s
  updateSelectionDisplay()
}

let timeout = 0
const handleViewport = (viewport: any) => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    reloadData(viewport);
  }, 1000)
}

const updateSelectionDisplay = () => {

  let path = ''

  switch (analysisType.value) {
    case "sketch only":
      path = "png"
      break;
    case "predicted probabilities":
      path = "probs"
      break;
    case "vanilla gradients":
      path = "vg"
      break;
    case "grad cam":
      path = "gradcam"
      break;
    case "occlusion":
      path = "occlusion"
      break;
    case "knn":
      path = "lclknn/2000"
  }

  if (selection.value.length === 0) {
    sketches.value = []
  }

  Promise.all(selection.value.slice(0, 32).flatMap((item: any) => [
    fetch(apiUrl + "sketch/" + item.id).then(res => res.json()),
    fetch(apiUrl + "sketch/" + path + "/" + item.id).then(res => res.blob())
  ])).then((values: any) => {
    const meta = values.filter((x: any) => x.label)
    const images = values.filter((x: any) => !x.label).map((blob: any) => URL.createObjectURL(blob))
    sketches.value = meta.map(function (e: any, i: number) {
      return [e, images[i]];
    });

    if (firstUpdate.value) {
      setTimeout(() => {
        introJs().setOptions(introJsConfig).start();
      }, 500)
      firstUpdate.value = false
    }
  })

}

</script>

<style scoped>

.explorer-container {
  display: grid;
  grid-template-columns: 350px 1fr;
  height: calc(100vh - 60px);
  width: 100%;
  align-content: stretch;
}

.projection-container {
  width: 100%;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.projection-container__menu {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 100px;
  padding-top: 15px;
  padding-bottom: 10px;
  background-color: var(--gray);
}

.projection-sample-container {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.samples-container {
  width: 100%;
  flex-grow: 1;
  box-sizing: border-box;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  background-color: #f9f9f9;
  padding: 5px;
  align-content: start;
  overflow: auto;
  border: 2px solid var(--gray);
}

.sample {
  width: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: white;
  border-radius: 2px;
  padding: 10px;
  margin: 4px;
}

.sample:hover {
  width: 128px;
  margin: 0;
  border: 5px solid var(--blue);
  cursor: pointer;
}

.sample > span {
  height: 20px;
  font-size: small;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.samples__image {
  width: 100%;
  display: block;
}

.samples__wrong-prediction {
  color: rgb(235, 64, 52);
}

.legend__class {
  padding: 10px;
}

.legend__class > p {
  margin: 5px;
}

.samples__fill-prediction {
  width: 100%;
  background-color: black;
}

.samples__fill_wrong-prediction {
  width: 100%;
  background-color: rgb(235, 64, 52);
}

.selected-color-option {
  font-size: 8px;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  margin: 0 1px;
}

.multi-select-options-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  overflow: auto;
  max-height: 70px;
}

.reset-button {
  display: inline-flex;
  width: 100px;
  height: 40px;
  justify-content: center;
  align-items: center;
  border: 3px solid var(--red);
  border-radius: 15px;
  cursor: pointer;
}

.reset-button:hover {
  background-color: var(--red-transparent);
}

</style>
<template>
  <div class="all">

    <div class="network">

        <div @mouseover="hoverLayer = 0" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-input ' + (active===0? 'active' : '')" @click="setLayer(0)">
          <img v-if="showPin" src="/pin_red.svg" alt="pin" class="layer-pin"/>
          <img style="margin: 0 -10px; width: 80px" :src="(hoverLayer === 0 || active === 0)? '/layers/input_active.svg' : '/layers/input.svg'" alt="input"/>
          <span>Input</span>
        </div>
        <div @mouseover="hoverLayer = 1" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-convolution ' + (active===1? 'active' : '')" @click="setLayer(1)">
          <img style="margin: 0 -10px; width: 80px" :src="(hoverLayer === 1 || active === 1)? '/layers/conv1_active.svg' : '/layers/conv1.svg'" alt="input"/>
          <span>Conv</span>
        </div>
        <div @mouseover="hoverLayer = 2" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-relu ' + (active===2? 'active' : '')" @click="setLayer(2)">
          <img style="margin: 0 -10px; width: 80px" :src="(hoverLayer === 2 || active === 2)? '/layers/conv1_active.svg' : '/layers/conv1.svg'" alt="input"/>
          <span>ReLU</span>
        </div>
        <div @mouseover="hoverLayer = 3" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-max-pooling ' + (active===3? 'active' : '')" @click="setLayer(3)">
          <img style="margin: 0 -20px; width: 80px" :src="(hoverLayer === 3 || active === 3)? '/layers/maxpool1_active.svg' : '/layers/maxpool1.svg'" alt="input"/>
          <span>MaxPool</span>
        </div>
        <div @mouseover="hoverLayer = 4" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-convolution ' + (active===4? 'active' : '')" @click="setLayer(4)">
          <img style="margin: 0 -20px; width: 80px" :src="(hoverLayer === 4 || active === 4)? '/layers/conv2_active.svg' : '/layers/conv2.svg'" alt="input"/>
          <span>Conv</span>
        </div>
        <div @mouseover="hoverLayer = 5" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-relu ' + (active===5? 'active' : '')" @click="setLayer(5)">
          <img style="margin: 0 -20px; width: 80px" :src="(hoverLayer === 5 || active === 5)? '/layers/conv2_active.svg' : '/layers/conv2.svg'" alt="input"/>
          <span>ReLU</span>
        </div>
        <div @mouseover="hoverLayer = 6" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-max-pooling ' + (active===6? 'active' : '')" @click="setLayer(6)">
          <img style="margin: 0 -20px; width: 80px" :src="(hoverLayer === 6 || active === 6)? '/layers/maxpool2_active.svg' : '/layers/maxpool2.svg'" alt="input"/>
          <span>MaxPool</span>
        </div>
        <div @mouseover="hoverLayer = 7" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-convolution ' + (active===7? 'active' : '')" @click="setLayer(7)">
          <img style="margin: 0 -20px; width: 80px" :src="(hoverLayer === 7 || active === 7)? '/layers/conv3_active.svg' : '/layers/conv3.svg'" alt="input"/>
          <span>Conv</span>
        </div>
        <div @mouseover="hoverLayer = 8" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-relu ' + (active===8? 'active' : '')" @click="setLayer(8)">
          <img style="margin: 0 -20px; width: 80px" :src="(hoverLayer === 8 || active === 8)? '/layers/conv3_active.svg' : '/layers/conv3.svg'" alt="input"/>
          <span>ReLU</span>
        </div>
        <div @mouseover="hoverLayer = 9" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-max-pooling ' + (active===9? 'active' : '')" @click="setLayer(9)">
          <img style="margin: 0 -20px; width: 80px" :src="(hoverLayer === 9 || active === 9)? '/layers/maxpool3_active.svg' : '/layers/maxpool3.svg'" alt="input"/>
          <span>MaxPool</span>
        </div>
        <div @mouseover="hoverLayer = 10" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-flatten ' + (active===10? 'active' : '')" @click="setLayer(10)">
          <img style="margin: 0 -25px; width: 80px" :src="(hoverLayer === 10 || active === 10)? '/layers/flatten_active.svg' : '/layers/flatten.svg'" alt="input"/>
          <span>Flatten</span>
        </div>
        <div @mouseover="hoverLayer = 11" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-linear ' + (active===11? 'active' : '')" @click="setLayer(11)">
          <img style="margin: 0 -25px; width: 80px" :src="(hoverLayer === 11 || active === 11)? '/layers/linear1_active.svg' : '/layers/linear1.svg'" alt="input"/>
          <span>Linear</span>
        </div>
        <div @mouseover="hoverLayer = 12" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-relu ' + (active===12? 'active' : '')" @click="setLayer(12)">
          <img style="margin: 0 -25px; width: 80px" :src="(hoverLayer === 12 || active === 12)? '/layers/linear1_active.svg' : '/layers/linear1.svg'" alt="input"/>
          <span>ReLU</span>
        </div>
        <div @mouseover="hoverLayer = 13" @mouseout="hoverLayer = undefined" :class="'shape-layer shape-linear ' + (active===13? 'active' : '')" @click="setLayer(13)">
          <img style="margin: 0 -25px; width: 80px" :src="(hoverLayer === 13 || active === 13)? '/layers/linear2_active.svg' : '/layers/linear2.svg'" alt="input"/>
          <span>Linear</span>
        </div>

    </div>
  </div>

</template>

<script setup>

import {onMounted, ref, watch} from "vue";

const active = ref(0)
const emit = defineEmits(['selectedLayer'])
const props = defineProps(['initialLayer', 'controlled', 'locked', 'showPin'])
const hoverLayer = ref(undefined)

const setLayer = (layer) => {
  if (props.locked)
    return

  active.value = layer
  emit("selectedLayer", layer)
}

onMounted(() => {
  setLayer(props.initialLayer)

  if (props.controlled) {
    watch(() => props.initialLayer, l => active.value = l);
  }
})

</script>
<style scoped>

.all {
  --network-background: var(--gray);
  display: flex;
}

.outer-group {
  width: 100%;
}

.network {
  width: 100%;
  border-radius: 10px;
  padding: 1px;
  flex-grow: 1;
  display: flex;
  flex-direction: row;
}

.layer-group {
  gap: 3px;
}

.shape-layer {
  display: flex;
  flex-direction: column;
  cursor: pointer;
  position: relative;
}

.shape-layer > span {
  writing-mode: vertical-lr;
  user-select: none;
  font-size: small;
  font-weight: bold;
}

.shape-layer > img {
  pointer-events: none;
  user-select: none;
}

.shape-layer.active > span {
  color: var(--red);
}

.layer-pin {
  width: 40px;
  display: inline-block;
  transform: rotate(70deg);
  writing-mode: vertical-lr;
  position: absolute;
}

</style>
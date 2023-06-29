<template>
  <div class="all">

    <div class="network">

        <div :class="'shape-layer shape-input '">
          <img style="margin: 0 -10px; width: 80px" :src="showInput? '/layers/input_yellow.svg' : '/layers/input_passive.svg'" alt="input"/>
          <span>Input</span>
        </div>
        <div :class="'shape-layer shape-convolution '">
          <img style="margin: 0 -10px; width: 80px" :src="showConv? '/layers/conv1_purple.svg' : '/layers/conv1_passive.svg'" alt="input"/>
          <span>Conv</span>
        </div>
        <div :class="'shape-layer shape-relu '">
          <img style="margin: 0 -10px; width: 80px" src="/layers/conv1_passive.svg" alt="input"/>
          <span>ReLU</span>
        </div>
        <div :class="'shape-layer shape-max-pooling '">
          <img style="margin: 0 -20px; width: 80px" src="/layers/maxpool1_passive.svg" alt="input"/>
          <span>MaxPool</span>
        </div>
        <div :class="'shape-layer shape-convolution '">
          <img style="margin: 0 -20px; width: 80px" src="/layers/conv2_passive.svg" alt="input"/>
          <span>Conv</span>
        </div>
        <div :class="'shape-layer shape-relu '">
          <img style="margin: 0 -20px; width: 80px" src="/layers/conv2_passive.svg" alt="input"/>
          <span>ReLU</span>
        </div>
        <div :class="'shape-layer shape-max-pooling '">
          <img style="margin: 0 -20px; width: 80px" src="/layers/maxpool2_passive.svg" alt="input"/>
          <span>MaxPool</span>
        </div>
        <div :class="'shape-layer shape-convolution '">
          <img style="margin: 0 -20px; width: 80px" src="/layers/conv3_passive.svg" alt="input"/>
          <span>Conv</span>
        </div>
        <div :class="'shape-layer shape-relu '">
          <img style="margin: 0 -20px; width: 80px" src="/layers/conv3_passive.svg" alt="input"/>
          <span>ReLU</span>
        </div>
        <div :class="'shape-layer shape-max-pooling '">
          <img style="margin: 0 -20px; width: 80px" src="/layers/maxpool3_passive.svg" alt="input"/>
          <span>MaxPool</span>
        </div>
        <div :class="'shape-layer shape-flatten '">
          <img style="margin: 0 -25px; width: 80px" src="/layers/flatten_passive.svg" alt="input"/>
          <span>Flatten</span>
        </div>
        <div :class="'shape-layer shape-linear '">
          <img style="margin: 0 -25px; width: 80px" src="/layers/linear1_passive.svg" alt="input"/>
          <span>Linear</span>
        </div>
        <div :class="'shape-layer shape-relu '">
          <img style="margin: 0 -25px; width: 80px" src="/layers/linear1_passive.svg" alt="input"/>
          <span>ReLU</span>
        </div>
        <div :class="'shape-layer shape-linear '">
          <img style="margin: 0 -25px; width: 80px" src="/layers/linear2_passive.svg" alt="input"/>
          <span>Linear</span>
        </div>

    </div>
  </div>

</template>

<script setup>

import {onMounted, ref, watch} from "vue";

const active = ref(0)
const props = defineProps(['showInput', 'showConv'])

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
  cursor: not-allowed;
}

.shape-layer > span {
  writing-mode: vertical-lr;
  user-select: none;
  font-size: small;
  font-weight: bold;
  color: #6a6a6a;
}

.shape-layer > img {
  pointer-events: none;
  user-select: none;
}

.shape-layer.active > span {
  color: var(--red);
}

</style>